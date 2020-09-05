from django import template
from django.contrib.messages import constants

MESSAGE_TAGS = {
    constants.DEBUG: {
        'icon': 'icon-question',
        'text_color': 'g-color-white',
        'bg_color': 'g-bg-gray-dark-v2',
    },
    constants.INFO: {
        'icon': 'icon-question',
        'text_color': 'g-color-white',
        'bg_color': 'g-bg-gray-dark-v2',
    },
    constants.SUCCESS: {
        'icon': 'icon-check',
        'text_color': 'g-color-white',
        'bg_color': 'g-bg-teal',
    },
    constants.WARNING: {
        'icon': 'icon-info',
        'text_color': '',
        'bg_color': 'g-bg-yellow',
    },
    constants.ERROR: {
        'icon': 'icon-ban',
        'text_color': 'g-color-white',
        'bg_color': 'g-bg-red',
    },
}

register = template.Library()


@register.filter
def message_context(message):
    return MESSAGE_TAGS[message.level]
