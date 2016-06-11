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


def _get_chart_import(app_name, chart_name):
    """
    Look up a chart for an app. Raises KeyError when no match found.

    :param app_name: The app name
    :param chart_name: The chart class or function (or name='' kwarg) name
    :return: The matching key
    """
    key = '%s.%s' % (app_name, chart_name)
    if key not in charts_registry.charts.keys():
        key = '%s.charts.%s' % (app_name, chart_name)
        if key not in charts_registry.charts.keys():
            raise KeyError('No chart named %s.%s' % (app_name, chart_name))
    return key


def get_chart_classes():
    """
    Get a list of all installed charts.

    :return: list(chartforge.charts.ChartBase)
    """
    return [entry.chart_class for entry in charts_registry.charts.values()]


def get_chart_class(app_name, chart_name):
    """
    Get the chart class for a given name and app.

    :param app_name: Something like 'myproject.myapp'
    :param chart_name: Chart, like 'MyChart'
    :return: chartforge.charts.ChartBase
    """
    key = _get_chart_import(app_name, chart_name)
    return charts_registry.charts[key].chart_class


def is_chart_class(app_name, chart_name):
    """
    Check if a chart class name exists.

    :param app_name:
    :param chart_name:
    :return: bool
    """
    try:
        _get_chart_import(app_name, chart_name)
        return True
    except KeyError:
        return False
