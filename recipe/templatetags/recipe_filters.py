from django import template
import re

register = template.Library()

@register.filter
def split(value, arg):
    return [x for x in value.split(arg) if x.strip()]

@register.filter
def strip(value):
    return value.strip()

@register.filter(name='split_lines')
def split_lines(value):
    if value:
        return value.split('\n')
    return []
