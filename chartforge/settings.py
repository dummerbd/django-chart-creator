from django.conf import settings


class ChartForgeSettings:
    """
    Simply loads the CHART_FORGE settings dictionary and sets any defaults, as
    well as checking for common errors.
    """
    def __init__(self):
        org = self._original = getattr(settings, 'CHART_FORGE', {})

        assert isinstance(org, dict), 'CHART_FORGE must be a dict'

        self.installed_charts = org.get('installed_charts', [])

        # TODO: add default settings
