from importlib import import_module
from chartforge.settings import ChartForgeSettings


class BackendBase:
    """
    Abstract base class for backends. Stubs out the backend api.

    Override any method to enable it's functionality. All backend classes
    should be included in the ``backends`` setting.
    """
    verbose_name = None

    def __init__(self):
        if self.verbose_name is None:
            self.verbose_name = self.__class__.__name__

    def get_chart_templates(self):
        """
        Get a list of chart templates.

        :return: list
        """
        return []
    get_chart_templates.disabled = True

    def get_chart_template(self, full_name=None):
        """
        Get a chart template by name.

        :return: template
        """
        return None
    get_chart_template.disabled = True

    def get_charts(self):
        """
        Get a list of all available charts.

        :return: list
        """
        return []
    get_charts.disabled = True

    def get_chart(self, slug=None):
        """
        Get a specific chart by its slug.

        :param slug: The chart's slug identifier
        :return: chart
        """
        return None
    get_chart.disabled = True

    def save_chart(self, chart):
        """
        Save a chart instance to remote or local persistent storage.

        :return: bool
        """
        return False
    save_chart.disabled = True

    def render_chart(self, chart, render_type=None):
        """
        Render a chart instance to a byte stream using the render type.

        :param chart:
        :param render_type:
        :return: bytes[]
        """
        return None
    render_chart.disabled = True

    def export_chart(self, chart, export_type=None):
        """
        Export a chart instance to a byte stream using the render type.

        :param chart:
        :param export_type:
        :return:
        """
        return None
    export_chart.disabled = True


def load_backends_from_settings():
    """
    Load all of the entries in the backends setting.
    """
    settings = ChartForgeSettings()
    backends = []
    for entry in settings.backends:
        mod_path, _, backend_name = entry.rpartition('.')
        backend_class = getattr(import_module(mod_path), backend_name)
        backends.append(backend_class())
    return backends


class BackendManager(BackendBase):
    """
    Primary interface for using backends. Has the same API as ``BackendBase``
    but underneath it delegates to functionality to the installed backends.
    """
    def __init__(self):
        """
        Load all backends.
        """
        self.loaded_backends = load_backends_from_settings()
        super().__init__()
