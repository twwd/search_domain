import argparse
import itertools

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'


def validator(value):
    if len(value) < 2:
        raise argparse.ArgumentTypeError('pattern must consist of at least 2 chars')

    if len(value) > 3 and value[-3:] == '.de':
        value = value[:-3]

    if value[0] is '-' or value[-1] is '-':
        raise argparse.ArgumentTypeError('{} is not allowed at the beginning or end'.format(value))

    for char in value:
        if char not in LETTERS + NUMBERS + 'LNA-':
            raise argparse.ArgumentTypeError('{} is not an allowed char'.format(char))

    return value


def generate_candiates(pattern):
    candiates = []

    [''.join(comb) + '.de' for comb in itertools.product((LETTERS + NUMBERS), (LETTERS + NUMBERS + '-'), (LETTERS + NUMBERS))]

    for c in pattern:
        if c is 'L':
            pass
        elif c is 'N':
            pass
        elif c is 'A':
            pass
        else:
            pass
    return candiates
