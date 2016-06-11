from django.db import models
from django.conf import settings


class ChartTemplate(models.Model):
    """
    Keeps track of all the available templates. Templates include all
    installed Chart classes, and any files in the charts template
    directory if configured.
    """
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='chartforge/tpl')
    example_data = models.TextField()
    chart_config = models.TextField()


class Chart(models.Model):
    """
    Holds the chart config and chart options. Each chart is based off a chart
    type which is really just a subclass of Chart or ModelChart.
    """
    name = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to='chartforge/chart', null=True)
    chart_type = models.ForeignKey(ChartTemplate, null=True)
    publish = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
