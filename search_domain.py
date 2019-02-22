#!/usr/bin/env python3
import time
from io import TextIOWrapper

import chunking
import cli
import dns
import pattern
import whois
from findings import Findings
from logger import Logger

args = cli.args

MIN_WAIT = 10
MAX_WAIT = 300
WAIT_REQ = 1  # time to wait between whois requests

MAINTENANCE_ITERATIONS = 50  # number of iterations between status output and finding persitence


def generate_domain_list(pattern_str: str, wordlist_file: TextIOWrapper, skip_files: list, chunk: int, chunks: int, l: Logger):
    if pattern_str is not None:
        d = pattern.generate_candiates(pattern_str)
    else:
        d = [l.rstrip('\n') for l in wordlist_file.readlines()]
        wordlist_file.close()

    l.log('{} domains to test (initially)'.format(len(d)))

    if skip_files is not None:
        domains_to_skip = []
        for file in skip_files:
            domains_to_skip.extend(l.rstrip('\n') for l in file.readlines())
            file.close()
        d = sorted(set(d) - set(domains_to_skip))

    if chunk is not None and chunks is not None:
        # find the chunk of the list
        l.log("Take chunk {} of {}".format(chunk, chunks))
        d = chunking.get(d, chunk, chunks)

    length = len(d)

    l.log('{} domains to test (after skipping and chunking)'.format(length))

    return d, length


# Init
log = Logger(args.verbose)
wait = MIN_WAIT
domains_index = 0
findings = Findings(log, args.free, args.occu)

domains, domains_len = generate_domain_list(args.pattern, args.wordlists, args.skip, args.chunk, args.chunks, log)

log.start_timer()

while domains_index < domains_len:
    domain = domains[domains_index]
    try:
        if dns.has_ip(domain):
            findings.add_domain(domain)
        else:
            time.sleep(WAIT_REQ)  # prevent rate limiting
            if whois.has_entry(domain):
                findings.add_domain(domain)
            else:
                findings.add_domain(domain, True)

        if domains_index != 0 and domains_index % MAINTENANCE_ITERATIONS is 0:
            findings.persist()
            log.remaining_time(domains_index, MAINTENANCE_ITERATIONS, domains_len)

        domains_index += 1

    except ConnectionResetError as e:
        log.error(e)
        wait = min(MAX_WAIT, wait * 2)
        log.error('Wait {}s'.format(wait))
        time.sleep(wait)

    except Exception as e:
        log.error(e, True)
        exit(-1)
