import argparse


def validator(string):
    value = int(string)

    if value < 1:
        raise argparse.ArgumentTypeError('{} must be at least 1'.format(value))

    return value


def get(l: list, chunk: int, chunks: int):
    if chunks == 1:
        return l

    chunk_size, _ = divmod(len(l), chunks)

    # Append the surplus items to the last chunk
    if chunk != chunks:
        return l[(chunk - 1) * chunk_size:chunk * chunk_size]
    else:
        return l[(chunk - 1) * chunk_size:]
