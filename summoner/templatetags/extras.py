from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0] + " ago"


@register.filter
@stringfilter
def norm_name(value):
    return value[0] + value[1:].lower()


upto.is_safe = True
