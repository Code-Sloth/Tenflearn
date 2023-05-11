from django import template

register = template.Library()

@register.filter
def divide_by_five(value):
    return value / 5 * 100