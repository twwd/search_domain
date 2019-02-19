#!/usr/bin/env python3

import argparse
import datetime
import signal
import sys
import time

import dns
import pattern
import whois
from logger import Logger

parser = argparse.ArgumentParser(description='Find free .de domains. Requires either a wordlist or a pattern.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--wordlist', '-w', type=argparse.FileType('r', encoding='utf-8'), help='a file with a list of .de domains to test')
group.add_argument('--pattern', '-p', type=pattern.validator,
                   help='a pattern for .de domain generation. .de is automatically added. Allowed elements: lowercase letters, numbers, dash, '
                        'L for an arbitrary letter, N for an arbitrary number, and A for an arbitrary allowed char.')
parser.add_argument('--free', type=argparse.FileType('a', encoding='utf-8'), default='free_domains.txt',
                    help='a file for storing free domains (default: free_domains.txt)')
parser.add_argument('--occu', type=argparse.FileType('a', encoding='utf-8'), default='occu_domains.txt',
                    help='a file for storing occupied domains (default: occu_domains.txt)')
parser.add_argument('--skip', type=argparse.FileType('r', encoding='utf-8'), nargs='*', help='one or multiple files containing domains that should be skipped')
parser.add_argument('--verbose', '-v', action='count', help='enable logging')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')

args = parser.parse_args()

MIN_WAIT = 10
MAX_WAIT = 300
WAIT_REQ = 1  # time to wait between whois requests

PRINT_ITERATIONS = 50  # amount of iterations between status output

# Init
log = Logger(args.verbose)
wait = MIN_WAIT
domains = []
domains_index = 0
occu = set()
free = set()

if args.pattern is not None:
    domains = pattern.generate_candiates(args.pattern)
else:
    domains = [l.rstrip('\n') for l in args.wordlist.readlines()]


def skip_domains(domains_to_test, domains_to_skip):
    return sorted(set(domains_to_test) - set(domains_to_skip))


if args.skip is not None:
    domains_to_skip = []
    for file in args.skip:
        domains_to_skip.extend(l.rstrip('\n') for l in file.readlines())
        file.close()
    domains = skip_domains(domains, domains_to_skip)


def persist_findings():
    global occu, free
    for item in occu:
        args.occu.write('{}\n'.format(item))
    occu = set()
    for item in free:
        args.free.write('{}\n'.format(item))
    free = set()


def process_domain(domain, is_free=False):
    if is_free:
        log.free(domain)
        free.add(domain)
    else:
        log.occu(domain)
        occu.add(domain)


# Handle Ctrl + C
def signal_handler(sig, frame):
    persist_findings()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

domains_len = len(domains)

log.log('{} domains to test'.format(domains_len))

# stats
start_time = datetime.datetime.now()
last_print_time = start_time

while domains_index < domains_len:
    domain = domains[domains_index]
    try:
        if dns.has_ip(domain):
            process_domain(domain)
        else:
            time.sleep(WAIT_REQ)  # prevent rate limiting
            if whois.has_entry(domain):
                process_domain(domain)
            else:
                process_domain(domain, True)

        if domains_index != 0 and domains_index % (PRINT_ITERATIONS * 2) is 0:
            persist_findings()

        if domains_index != 0 and domains_index % PRINT_ITERATIONS is 0:
            now = datetime.datetime.now()
            time_per_domain = (now - last_print_time) / PRINT_ITERATIONS * 0.66 + (now - start_time) / domains_index * 0.33
            remaining_time = time_per_domain * (domains_len - domains_index)
            remaining_time = remaining_time - datetime.timedelta(microseconds=remaining_time.microseconds)  # remove microseconds for printing
            last_print_time = now

            print('{} of {} ({:.2f}%, approx. {} remaining)'.format(domains_index, domains_len, domains_index / domains_len * 100, remaining_time))

        domains_index += 1

    except ConnectionResetError as e:
        log.error(e)
        wait = min(MAX_WAIT, wait * 2)
        log.error('Wait {}s'.format(wait))
        time.sleep(wait)

    except Exception as e:
        log.error(e, True)
        persist_findings()
        exit(-1)

persist_findings()
