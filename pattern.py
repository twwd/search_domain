import argparse
import itertools

LETTERS = 'abcdefghijklmnopqrstuvwxyz'
NUMBERS = '0123456789'


def validator(value):
    if len(value) < 3 or value[-3:] != '.de':
        value = value + '.de'

    if len(value) < 4:
        raise argparse.ArgumentTypeError('pattern must consist of at least one char in the second-level part')

    if value[0] is '-' or value[-4] is '-':
        raise argparse.ArgumentTypeError('{} is not allowed at the beginning or end of the second-level part'.format(value))

    for char in value[:-3]:
        if char not in LETTERS + NUMBERS + 'LNA-':
            raise argparse.ArgumentTypeError('{} is not an allowed char'.format(char))

    return value


def generate_candiates(pattern: str):
    candiates = [""]

    tmp_part = ''

    def str_product(l1, l2):
        return map(lambda comb: ''.join(comb), itertools.product(l1, l2))

    def append_to_items(l, s):
        if len(s) > 0:
            return map(lambda elem: "{}{}".format(elem, s), l)
        else:
            return l

    for i in range(0, len(pattern)):
        c = pattern[i]
        if c in 'LNA':
            candiates = append_to_items(candiates, tmp_part)  # append chars that occured before
            if c is 'L':
                candiates = str_product(candiates, LETTERS)
            elif c is 'N':
                candiates = str_product(candiates, NUMBERS)
            elif c is 'A':
                # don't add dashes if not beginning or end of the second-level part
                if i is 0 or i is len(pattern) - 4:
                    candiates = str_product(candiates, LETTERS + NUMBERS)
                else:
                    candiates = str_product(candiates, LETTERS + NUMBERS + '-')
        else:
            tmp_part += c

    return list(append_to_items(candiates, tmp_part))
