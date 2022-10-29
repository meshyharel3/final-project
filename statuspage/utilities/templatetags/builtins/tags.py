from django.utils import timezone
from django import template
from metrics.models import MetricPoint
from django.db import models
from django.db.models import functions

register = template.Library()


@register.inclusion_tag('builtins/tag.html')
def tag(value, viewname=None):
    """
    Display a tag, optionally linked to a filtered list of objects.
    Args:
        value: A Tag instance
        viewname: If provided, the tag will be a hyperlink to the specified view's URL
    """
    return {
        'tag': value,
        'viewname': viewname,
    }


@register.inclusion_tag('builtins/badge.html')
def badge(value, bg_color=None, show_empty=False):
    """
    Display the specified number as a badge.
    Args:
        value: The value to be displayed within the badge
        bg_color: Background color CSS name
        show_empty: If true, display the badge even if value is None or zero
    """
    return {
        'value': value,
        'bg_color': bg_color or 'bg-gray-500',
        'show_empty': show_empty,
    }


@register.inclusion_tag('builtins/checkmark.html')
def checkmark(value, show_false=True, true='Yes', false='No'):
    """
    Display either a green checkmark or red X to indicate a boolean value.
    Args:
        value: True or False
        show_false: Show false values
        true: Text label for true values
        false: Text label for false values
    """
    return {
        'value': bool(value),
        'show_false': show_false,
        'true_label': true,
        'false_label': false,
    }


@register.inclusion_tag('builtins/metric.html')
def metric(metric, range):
    match range:
        case '30m':
            datenow = timezone.now().replace(microsecond=0, second=0)
            daterange = datenow - timezone.timedelta(minutes=30)
        case '1h':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0)
            daterange = datenow - timezone.timedelta(hours=1)
        case '12h':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0)
            daterange = datenow - timezone.timedelta(hours=12)
        case '24h':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0, hour=0)
            daterange = datenow - timezone.timedelta(days=1)
        case '2d':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0, hour=0)
            daterange = datenow - timezone.timedelta(days=2)
        case '3d':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0, hour=0)
            daterange = datenow - timezone.timedelta(days=3)
        case '7d':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0, hour=0)
            daterange = datenow - timezone.timedelta(days=7)
        case '30d':
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0, hour=0)
            daterange = datenow - timezone.timedelta(days=30)
        case _:
            datenow = timezone.now().replace(microsecond=0, second=0, minute=0)
            daterange = datenow - timezone.timedelta(hours=12)

    labels = metric.get_metric_labels_json(now=datenow, range=daterange)
    points = metric.get_metric_points_json(now=datenow, range=daterange)

    return {
        'metric': metric,
        'labels': labels,
        'points': points,
    }