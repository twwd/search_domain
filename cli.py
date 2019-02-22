import argparse

import chunking
import pattern

parser = argparse.ArgumentParser(description='Find free .de domains. Requires either a wordlist or a pattern.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--wordlist', '-w', type=argparse.FileType('r', encoding='utf-8'), help='a file with a list of .de domains to test')
group.add_argument('--pattern', '-p', type=pattern.validator,
                   help='a pattern for the domain generation. Allowed elements: lowercase letters, numbers, dash, '
                        'L for an arbitrary letter, D for an arbitrary digit, and A for an arbitrary allowed char.')
parser.add_argument('--free', type=argparse.FileType('a', encoding='utf-8', bufsize=16), default='data/free.txt',
                    help='a file for storing free domains (default: data/free.txt)')
parser.add_argument('--occu', type=argparse.FileType('a', encoding='utf-8', bufsize=16), default='data/occu.txt',
                    help='a file for storing occupied domains (default: data/occu.txt)')
parser.add_argument('--skip', type=argparse.FileType('r', encoding='utf-8'), nargs='*', help='one or multiple files containing domains that should be skipped')
parser.add_argument('--part', type=chunking.validator, help='if you want to chunk the domains to test, this specifies which chunk should be processed')
parser.add_argument('--chunks', type=chunking.validator, help='the number of chunks')
parser.add_argument('--verbose', '-v', action='count', help='enable logging')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

if bool(args.chunk) ^ bool(args.chunks):
    parser.error('--chunk and --chunks must be given together')

if args.chunk is not None and args.chunks is not None and args.chunk > args.chunks:
    parser.error("--chunk must be equal or less than --chunks")
