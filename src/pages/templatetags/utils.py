import urllib.parse

from django import template

register = template.Library()


@register.simple_tag()
def decode_get_parameter(value):
    return urllib.parse.unquote(value)
