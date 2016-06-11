from django.conf import settings


DEFAULTS = {
    'chart_apps': [],
    'backends': [
        'chartforge.backends.ChartClassBackend',
        'chartforge.backends.ChartModelBackend',
        'chartforge.backends.StaticChartBackend'
    ]
}


class ChartForgeSettings:
    """
    Simply loads the CHART_FORGE settings dictionary and sets any defaults, as
    well as checking for common errors.
    """
    def __init__(self):
        org = self._original = getattr(settings, 'CHART_FORGE', {})

        assert isinstance(org, dict), 'CHART_FORGE must be a dict'

        def _load(name):
            return org[name] if name in org else DEFAULTS[name]

        self.chart_apps = _load('chart_apps')
        self.backends = _load('backends')
