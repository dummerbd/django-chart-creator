from django.template.loader import render_to_string
from django.core.exceptions import ValidationError


registered_charts = []


def register(chart_name=None):
    """
    Class decorator for registering a chart.
    :param chart_name: A custom name, otherwise the class name is used
    :return: func
    """
    def wrapper(cls):
        name = cls.__name__ if wrapper._name is None else wrapper._name
        registered_charts.append((name, cls))
        return cls

    wrapper._name = chart_name
    return wrapper


class ChartOptions:
    """
    Similar to a Django Form class. Defines input fields that can be set by the
    user in the chart admin.

    ```
    options = ChartOptions({'key': 123})
    if options.is_valid():
        do_stuff(options.data)
    else:
        oh_no(options.errors)
    ```
    """
    def __init__(self, data):
        self._data = data
        self._cleaned_data = {}
        self._validated = False
        self.errors = None

    @property
    def data(self):
        """
        Get access to the
        :return:
        """
        if self.is_valid():
            return self._cleaned_data
        return None

    def validate(self):
        """
        Run validation against all the fields.
        :return:
        """
        self._validated = True

    def is_valid(self):
        """
        Test if the provided inputs are valid.
        :return: boolean
        """
        if not self._validated:
            self.validate()

        return self.errors is None


class ChartBase:
    """
    Abstract base class for charts.
    """
    Options = None
    template_name = None

    def get_template_name(self):
        """
        Get the template name for the chart config.
        :return: str
        """
        if self.template_name is None:
            raise ValueError('Must set the template_name attribute')
        return self.template_name

    def get_chart_options(self, data):
        """
        Get the ChartOptions instance with the given data.
        :return: ChartOptions
        """
        if not isinstance(self.Options, ChartOptions):
            raise NotImplementedError('Must define an Options class that subclasses ChartOptions')

        return self.Options(data)

    def get_context(self, **kwargs):
        """
        Accept the result of the ChartOptions as kwargs and return a template
        context for rendering the options_template.
        :param kwargs: Result from the ChartOptions
        :return: dict
        """
        return kwargs

    def get_editing_context(self, **kwargs):
        """
        Similar to get_context() but used when the chart is in editing mode.
        By default this simple calls get_context().
        :param kwargs: Result from the ChartOptions
        :return: dict
        """
        return self.get_context(**kwargs)

    def render(self, data, editing=False):
        """
        Render the input values and get a complete chart options string.
        :param data: The input option values
        :param editing:
        :return: str
        """
        options = self.get_chart_options(data)
        if options.is_valid():
            context = (self.get_editing_context(**options.data)
                       if editing else self.get_context(**options.data))
            template = self.get_template_name()
            return render_to_string(template, context)

        raise ValidationError(options.errors)
