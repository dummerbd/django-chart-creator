import json
from collections import OrderedDict
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured

from chartforge.registry import charts_registry


class ChartBase:
    """
    Abstract base class for charts. Subclasses are made automatically when used
    with the ``chartforge()` decorator.
    """
    name = None
    verbose_name = None
    template_name = None
    template = None
    _wrapped_func = None

    def __call__(self, **kwargs):
        """
        Simply calls ``get_template(**kwargs)``.

        :return: dict
        """
        return self.get_template(**kwargs)

    def get_template(self, **kwargs):
        """
        Override in subclasses to generate dynamic templates. By default, the
        ``template`` attribute is returned, otherwise the `template_name` is
        loaded.

        :return: dict
        """
        both_defined = self.template is not None and self.template_name is not None
        assert not both_defined, 'Only set template or template_name, set the other to None'

        if self.template is not None:
            assert isinstance(self.template, dict), 'Static template must be JSON serializable dict'
            return self.template

        if self.template_name is not None:
            return self.render_template(**kwargs)

        raise ImproperlyConfigured('Charts must set template or template_name')

    def render_template(self, **kwargs):
        """
        Simply renders the template file with the context from
        ``get_context_data()``. Chart templates can be more dynamic by using
        a chart template, but once a chart is created, the template is static.
        Use a custom ``get_data()`` method to add dynamic data sources.

        :return: dict
        """
        context = self.get_context_data(**kwargs)
        result = render_to_string(self.template_name, context)
        return json.loads(result)

    def get_context_data(self, **kwargs):
        """
        Get context data for rendering a chart template. Useful for urls, dates,
        or any other dynamic data needed for a chart template.

        :param kwargs: Kwargs passed when creating this chart
        :return: dict
        """
        return kwargs

    def get_editing_data(self, **kwargs):
        """
        Get data that is used when editing this report. Set to something cached
        or static. Calls ``get_data()`` by default.

        :param kwargs:
        :return:
        """
        return self.get_data(**kwargs)

    def get_data(self, **kwargs):
        """
        Override to do any querying or processing needed to make the chart data
        dynamic.
        :param kwargs:
        :return: dict
        """
        func = self._wrapped_func
        return func(**kwargs) if func is not None else kwargs

    def __str__(self):
        kwargs = OrderedDict([
            ('name', self.name),
            ('verbose_name', self.verbose_name)
        ])
        if self.template is not None:
            kwargs['template'] = self.template
        if self.template_name is not None:
            kwargs['template_name'] = self.template_name
        if self._wrapped_func is not None:
            kwargs['function'] = self._wrapped_func.__name__
        return '%s(%s)' % (
            self.name,
            ', '.join(map(lambda i: '%s=%s' % i, kwargs.items()))
        )


def chartforge(name=None, template_name=None, template=None, verbose_name=None):
    """
    A function or class decorator that registers a chart with the chartforge
    registry.

    Can be used on a function or class::

        from chartforge import chartforge

        @chartforge(
            name='MyCustomChart',
            template_name='example_chart.json',
            verbose_name='My Awesome Chart!')
        def my_chart(chart):
            # chart is an instance of ChartBase
            return {} # example data...

        @chartforge()
        def ChartClass:
            template_name = 'another_chart.json'

            def get_data(self):
                return {} # example data...

    :param name: The name of the chart, used with ``get_chart_class()``
    :param template_name: A name of a file to use for the template
    :param template: A dict to use as the template
    :param verbose_name: The name displayed to users in the admin
    :return:
    """
    def wrapper(cls_or_func):
        _name = cls_or_func.__name__ if name is None else name
        app = cls_or_func.__module__

        bases = (cls_or_func, ChartBase)
        wrapped_func = None
        if type(cls_or_func) is not type:
            bases = (ChartBase,)
            wrapped_func = cls_or_func

        attrs = {
            'name': _name,
            '_wrapped_func': wrapped_func,
            '__module__': app
        }
        if template_name is not None:
            attrs['template_name'] = template_name

        if template is not None:
            attrs['template'] = template

        if verbose_name is not None:
            attrs['verbose_name'] = verbose_name

        chart_class = type(_name, bases, attrs)
        chart_class.__doc__ = cls_or_func.__doc__
        charts_registry.register(app, _name, chart_class)

        return cls_or_func

    return wrapper
