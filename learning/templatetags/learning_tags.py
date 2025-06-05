from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divisibleby(value, arg):
    """Divide the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def percentage(correct, total):
    """Calculates the percentage of correct attempts out of total attempts"""
    try:
        if float(total) > 0:
            return (float(correct) / float(total)) * 100
        else:
            return 0
    except (ValueError, TypeError, ZeroDivisionError):
        return 0 