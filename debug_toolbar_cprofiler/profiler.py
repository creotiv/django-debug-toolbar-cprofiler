from __future__ import absolute_import, division, unicode_literals

from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from debug_toolbar.panels import Panel
from debug_toolbar import settings as dt_settings

try:
    import cProfile as profile
except ImportError:
    import profile
import pstats

# Occasionally the disable method on the profiler is listed before
# the actual view functions. This function call should be ignored as
# it leads to an error within the tests.
INVALID_PROFILER_FUNC = '_lsprof.Profiler'


def contains_profiler(func_tuple):
    """Helper function that checks to see if the tuple contains
    the INVALID_PROFILE_FUNC in any string value of the tuple."""
    has_profiler = False
    for value in func_tuple:
        if isinstance(value, six.string_types):
            has_profiler |= INVALID_PROFILER_FUNC in value
    return has_profiler

class DjangoDebugToolbarStats(pstats.Stats):
    __root = None

    def get_root_func(self):
        if self.__root is None:
            for func, (cc, nc, tt, ct, callers) in self.stats.items():
                if len(callers) == 0 and not contains_profiler(func):
                    self.__root = func
                    break
        return self.__root

class CProfilerPanel(Panel):
    """
    Panel that displays profiling information.
    """
    title = _("Profiling")

    template = 'debug_toolbar_cprofiler/panels/cprofiler.html'

    def process_view(self, request, callback, callback_args, callback_kwargs):
        self.profiler = profile.Profile()
        args = (request,) + callback_args
        try:
            return self.profiler.runcall(callback, *args, **callback_kwargs)
        except:
            return

    def process_response(self, request, response):
        if not hasattr(self, 'profiler'):
            return None

        self.profiler.create_stats()
        stats = DjangoDebugToolbarStats(self.profiler)
        stats.sort_stats('time')
        func_list = {}
        for func, (cc, nc, tt, ct, callers) in stats.stats.iteritems():
            func_list[func] = {
                'filename':func[0] if func[0] != '~' else '',
                'line':func[1] if func[1] != 0 else '',
                'function':func[2],
                'count': nc,
                'cumtime':ct,
                'tottime':tt,
                'tottime_per_call':tt/nc,
                'cumtime_per_call':ct/nc
            }              
        res = [func_list.get(k) for k in stats.fcn_list]
        self.record_stats({'func_list': res})

