from django import template

register = template.Library()

@register.filter
def value(h, key):
    return h[key]