# Colorful stdout
import datetime
import sys

RED = '\033[1;31m'
GREEN = '\033[0;32m'
GREY = '\033[1;30m'
RESET = '\033[0;0m'


class Logger:
    def __init__(self, verbosity) -> None:
        self.verbosity = verbosity
        self.start_time = datetime.datetime.now()
        self.last_print_time = self.start_time

    def start_timer(self):
        self.start_time = datetime.datetime.now()
        self.last_print_time = self.start_time

    def remaining_time(self, domains_index, iterations_between_printing, domains_len):
        if self.enabled():
            now = datetime.datetime.now()
            time_per_domain = (now - self.last_print_time) / iterations_between_printing * 0.66 + (now - self.start_time) / domains_index * 0.33
            remaining_time = time_per_domain * (domains_len - domains_index)
            remaining_time = remaining_time - datetime.timedelta(microseconds=remaining_time.microseconds)  # remove microseconds for printing
            self.log('{} of {} ({:.2f}%, approx. {} remaining)'.format(domains_index, domains_len, domains_index / domains_len * 100, remaining_time))
            self.last_print_time = now

    def enabled(self):
        return self.verbosity > 0

    def log(self, message):
        if self.enabled():
            print(message)

    def free(self, domain):
        self.log('{}FREE: {}{}'.format(GREEN, domain, RESET))

    def occu(self, domain):
        self.log('{}OCCU: {}{}'.format(GREY, domain, RESET))

    def error(self, message, important=False):
        if self.enabled() or important:
            print('{}{}{}'.format(RED, message, RESET), end='', file=sys.stderr)
