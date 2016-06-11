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

        For every subclass of Chart, the ChartMeta class will call the
        register() method on this singleton instance. This will make those
        chart classes available in the admin.
        """
        self.settings = ChartForgeSettings()

        for charts in self.settings.installed_charts:
            # This is enough to get the ChartMeta to register all the
            # charts in this module.
            import_module(charts)
