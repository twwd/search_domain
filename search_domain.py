#!/usr/bin/env python3

import datetime
import itertools
import signal
import sys
import time
from pathlib import Path

from dns import has_ip
from whois import Whois

CHARS = "abcdefghijklmnopqrstuvwxyz"
NUMS = "0123456789"

LEN = 3
WORDLIST = Path("./wordlist.txt")

MIN_WAIT = 10
MAX_WAIT = 300
WAIT_REQ = 1  # time to wait between whois requests

FREE_DOMAINS_FILE = Path("./free_domains.txt")
OCCU_DOMAINS_FILE = Path("./occu_domains.txt")  # cache for already checked domains

PRINT_ITERATIONS = 50  # amount of iterations between status output

# Colorful stdout
RED = "\033[1;31m"
GREEN = "\033[0;32m"
GREY = "\033[1;30m"
RESET = "\033[0;0m"

# Init
whois = Whois()
wait = MIN_WAIT
words = []
words_i = 0
occu = set()
free = set()


def process_domain(domain, is_free=False):
    if is_free:
        print("{}FREE: {}{}".format(GREEN, domain, RESET))
        free.add(domain)
    else:
        print("{}OCCU: {}{}".format(GREY, domain, RESET))
        occu.add(domain)


def restore_state():
    global occu, free
    if OCCU_DOMAINS_FILE.is_file():
        with open(str(OCCU_DOMAINS_FILE)) as fp:
            occu = set(l.rstrip("\n") for l in fp.readlines())

    if FREE_DOMAINS_FILE.is_file():
        with open(str(FREE_DOMAINS_FILE)) as fp:
            free = set(l.rstrip("\n") for l in fp.readlines())


def store_state():
    global occu, free
    with open(str(OCCU_DOMAINS_FILE), "a", newline="\n") as fp:
        for item in occu:
            fp.write("{}\n".format(item))
    occu = set()
    with open(str(FREE_DOMAINS_FILE), "a", newline="\n") as fp:
        for item in free:
            fp.write("{}\n".format(item))
    free = set()


# Handle Ctrl + C
def signal_handler(sig, frame):
    store_state()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

#################
# Words to test #
#################

restore_state()

if WORDLIST.is_file():
    with open(str(WORDLIST)) as fp:
        words = [l.rstrip("\n") for l in fp.readlines()]
else:
    words = ["".join(comb) + ".de" for comb in itertools.product((CHARS + NUMS), (CHARS + NUMS + "-"), (CHARS + NUMS))]

# Shrink words
words = sorted(set(words) - occu - free)
free = set()
occu = set()

# Split to servers
# half_of_the_words = int(len(words) / 2)
#
# if "alfahosting" in socket.gethostname():
#     print("Upper half")
#     words = words[:half_of_the_words]
# elif "mail" in socket.gethostname():
#     print("Lower half")
#     words = words[half_of_the_words:]

words_len = len(words)

print("{} domains to test".format(words_len))

# stats
start_time = datetime.datetime.now()
last_print_time = start_time

while words_i < words_len:
    domain = words[words_i]
    try:
        if has_ip(domain):
            process_domain(domain)
        else:
            time.sleep(WAIT_REQ)
            if whois.is_available(domain):
                process_domain(domain, True)
            else:
                process_domain(domain)

        if words_i != 0 and words_i % (PRINT_ITERATIONS * 2) is 0:
            store_state()

        if words_i != 0 and words_i % PRINT_ITERATIONS is 0:
            now = datetime.datetime.now()
            time_per_domain = (now - last_print_time) / PRINT_ITERATIONS * 0.66 + (now - start_time) / words_i * 0.33
            remaining_time = time_per_domain * (words_len - words_i)
            remaining_time = remaining_time - datetime.timedelta(microseconds=remaining_time.microseconds)  # remove microseconds for printing
            last_print_time = now

            print("{} of {} ({:.2f}%, approx. {} remaining)".format(words_i, words_len, words_i / words_len * 100, remaining_time))

        words_i += 1

    except ConnectionResetError as e:
        print("{}".format(RED), end="", file=sys.stderr)
        print(e, file=sys.stderr)

        wait = min(MAX_WAIT, wait * 2)
        print("Wait {}s{}".format(wait, RESET), file=sys.stderr)
        time.sleep(wait)

    except Exception as e:
        print(e, file=sys.stderr)
        store_state()
        exit(-1)

store_state()
