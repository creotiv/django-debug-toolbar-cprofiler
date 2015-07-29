==============================
Django Debug Toolbar CProfiler
==============================

The Django Debug Toolbar CProfiler is profiler panel for Django Debug Toolbar.

Here's a screenshot of the panel in action:

.. image:: https://raw.github.com/creotiv/django-debug-toolbar-cprofiler/master/example.png
   :width: 1214
   :height: 743
   
**How to use**

Add to the installed apps:
    
    INSTALLED_APPS += ('debug_toolbar','debug_toolbar_cprofiler')

Add to the debug toolbar panels:

   DEBUG_TOOLBAR_PANELS = [
       'debug_toolbar.panels.versions.VersionsPanel',
       'debug_toolbar.panels.timer.TimerPanel',
       'debug_toolbar.panels.settings.SettingsPanel',
       'debug_toolbar.panels.headers.HeadersPanel',
       'debug_toolbar.panels.request.RequestPanel',
       'debug_toolbar.panels.sql.SQLPanel',
       'debug_toolbar.panels.staticfiles.StaticFilesPanel',
       'debug_toolbar.panels.templates.TemplatesPanel',
       'debug_toolbar.panels.cache.CachePanel',
       'debug_toolbar_cprofiler.profiler.CProfilerPanel', # here it is
       'debug_toolbar.panels.signals.SignalsPanel',
       'debug_toolbar.panels.logging.LoggingPanel',
       'debug_toolbar.panels.redirects.RedirectsPanel',
   ]



