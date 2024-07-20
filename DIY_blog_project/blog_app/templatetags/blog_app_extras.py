from django import template

register = template.Library()

@register.filter()
def values(items, attr_name):
    return [getattr(i, attr_name) for i in items]


@register.filter()
def distinct(items):
    return set(items)