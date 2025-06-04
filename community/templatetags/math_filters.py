from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """Divides the value by the argument."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def percentage(value, total):
    """Calculates percentage of value from total."""
    try:
        if total == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, ZeroDivisionError):
        return 0
