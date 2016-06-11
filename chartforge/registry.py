from collections import OrderedDict


class ChartRegistry:
    """
    Singleton instance used to keep track of all available chart types and
    templates.
    """
    class _Entry:
        def __init__(self, app_name, chart_name, chart_class):
            self.app_name = app_name
            self.chart_name = chart_name
            self.chart_class = chart_class

    def __init__(self):
        self.charts = OrderedDict()

    def register(self, app_name, chart_name, chart_class):
        """
        Register a chart. This is called by the ChartMeta class for every
        subclass of ChartBase.

        :param app_name: The django app name
        :param chart_name: The name of the chart class
        :param chart_class: The actual chart class
        """
        from chartforge.charts import ChartBase

        key = '%s.%s' % (app_name, chart_name)
        if key in self.charts:
            raise ValueError('Duplicate chart registered: %s' % key)

        assert issubclass(chart_class, ChartBase), 'Must be a subclass of ChartBase'

        self.charts[key] = self._Entry(app_name, chart_name, chart_class)


charts_registry = ChartRegistry()


def get_chart_class(app_name, chart_name):
    """
    Get the chart class for a given name and app.

    :param app_name: Something like 'myproject.myapp'
    :param chart_name: Chart, like 'MyChart'
    :return: chartforge.charts.ChartBase
    """

    # Prefer full paths, either ('project.app', 'charts.MyChart')
    # Or ('project.app.charts', 'MyChart') will work.
    key = '%s.%s' % (app_name, chart_name)
    try:
        return charts_registry.charts[key].chart_class
    except KeyError:
        # Common convention is to place the charts in a module called charts
        key = '%s.charts.%s' % (app_name, chart_name)
        return charts_registry.charts[key].chart_class
