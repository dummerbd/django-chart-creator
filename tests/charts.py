from chart_creator import charts


@charts.register('custom_chart_name')
class ExampleChart(charts.ChartBase):
    """
    Example line chart.
    """
    template_name = 'example_line_chart.json'

    class Options(charts.ChartOptions):
        pass
