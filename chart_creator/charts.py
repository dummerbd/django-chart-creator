from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from .chart_options import ChartOptions


class ChartMeta(type):
    """
    Metaclass for Charts, automatically registers each subclass of ChartBase.
    """
    do_not_register = [
        'ChartBase'
    ]

    @staticmethod
    def __new__(mcs, name, bases, attrs):
        """
        Called for each defined subclass of ChartBase
        """
        if name not in mcs.do_not_register:
            pass

        return type(name, bases, attrs)


class ChartBase(metaclass=ChartMeta):
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
