from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@register.filter(name='range_plus')
def filter_range_plus(start, end):
    return range(start, end + 1)

@register.filter(name='array_item')
def filter_range_plus(array, item):
    return array[item]
