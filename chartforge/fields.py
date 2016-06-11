from django.db.models.fields import CharField

from chartforge.registry import get_chart_class, is_chart_class


class ChartClassField(CharField):
    """
    Custom Django model field to support saving a chart class to a model.
    """

