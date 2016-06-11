import json


class RenderType:
    """
    Defines the chart render types.
    """
    PNG = 'image/png'
    JPEG = 'image/jpeg'
    PDF = 'application/pdf'
    SVG = 'image/svg+xml'


class ExportType:
    """
    Defines the chart export types.
    """
    IFRAME = 'iframe'
    PLAIN_JS = 'javascript'
    REQUIRE_JS = 'require'
    UMD_JS = 'umd'


class Chart:
    """
    Holds the chart config for a ready to render chart instance.
    """
    def __init__(self, slug, config):
        self.slug = slug
        self.config = config

    def serialize(self):
        """
        Serialize to a JSON encoded string.

        :return: str
        """
        return json.dumps({
            'slug': self.slug,
            'config': self.config
        })

    @classmethod
    def parse(cls, data):
        """
        Create a Chart instance for a serialized chart.

        :param data: JSON encoded chart config
        :return: Chart()
        """
        return cls(**json.loads(data))


class ChartTemplate:
    """
    Holds a chart config template and related data.
    """
    def __init__(self, name, template_config, verbose_name=None, editing_data=None):
        self.name = name
        self.config = config
        self.verbose_name = verbose_name
        self.editing_data = editing_data

    def render_to_chart(self, config):
        """
        Merge together this template with the passed in ``config`` data and
        create a Chart() instance.

        :param config: The chart config data to apply to the template
        :return: Chart()
        """
        # TODO: merge configs
        return Chart(config)

    def serialize(self):
        """
        Serialize to a JSON encoded string.

        :return: str
        """
        return json.dumps({
            'name': self.name,
            'config': self.config,
            'verbose_name': self.verbose_name,
            'editing_data': self.editing_data
        })

    @classmethod
    def parse(cls, data):
        """
        Create a ChartTemplate instance for a serialized template.

        :param data: JSON encoded template data
        :return: ChartTemplate()
        """
        return cls(**json.loads(data))
