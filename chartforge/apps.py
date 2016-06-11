from importlib import import_module
from django.apps import AppConfig

from chartforge.settings import ChartForgeSettings


class ChartForgeConfig(AppConfig):
    """
    Hook into the ready() hook to load all the modules in the CHART_APPS
    setting.
    """
    name = 'chartforge'
    verbose_name = 'Chart Forge'

    def __init__(self, app_name, app_module):
        self.settings = {}
        super().__init__(app_name, app_module)
    
    def ready(self):
        """
        Initialize the settings and import all of the charts modules in the
        chart_apps setting.

        Each entry in chart_apps should be a dot path to an app that has a
        charts module, or dot path to a module containing charts::

            CHARTFORGE = {
                'chart_apps': {
                    # path to app, project.my_app.charts will also be loaded
                    'project.my_app',

                    # path directly to a module
                    'project.my_app.other_charts'
                }
            }

        """
        self.settings = ChartForgeSettings()

        for entry in self.settings.chart_apps:
            # import entry, which should evaluate all the @chartforge() charts
            import_module(entry)
            try:
                # Common convention is to use a 'charts' module
                import_module('%s.charts' % entry)
            except ImportError:
                pass
