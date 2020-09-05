from book import choices

from django import template

register = template.Library()


@register.filter()
def book_status(value):
    statuses = dict(choices.BOOK_STATUSES)
    return statuses[value]
