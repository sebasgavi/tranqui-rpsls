from django import template

from ..constants import ROCK, PAPER, SCISSORS, LIZARD, SPOCK

register = template.Library()

@register.filter
def movetovariationclass(move):
    dic = {
        'ROCK': 'primary',
        'PAPER': 'success',
        'SCISSORS': 'warning',
        'LIZARD': 'danger',
        'SPOCK': 'info'
    }
    return dic.get(move, 'default')