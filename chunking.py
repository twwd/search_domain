import argparse
import collections


def validator(string):
    value = int(string)

    if value < 1:
        raise argparse.ArgumentTypeError('{} must be at least 1'.format(value))

    return value


def get(l: collections.abc.Sequence, chunk: int, chunks: int):
    if chunks == 1:
        return l

    part_size = int(len(l) / chunks)

    if chunk == 1:
        return l[:part_size]
    else:
        start = part_size * (chunk - 1)
        if chunk == chunks:
            return l[start:]
        else:
            return l[start: start + part_size]
