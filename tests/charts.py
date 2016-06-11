from chartforge import charts


@charts.chartforge()
class ExampleChart:
    """
    Example line chart.
    """
    template_name = 'example_line_chart.json'

    def get_data(self):
        return {'bvah': 1}


@charts.chartforge('CustomChartName', template_name='example_line_chart.json')
def my_chart(chart):
    print('my_chart(%s)' % chart)
    return {'data': 123}
