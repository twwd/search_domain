# Colorful stdout
import sys

RED = '\033[1;31m'
GREEN = '\033[0;32m'
GREY = '\033[1;30m'
RESET = '\033[0;0m'


class Logger:
    def __init__(self, verbosity) -> None:
        self.verbosity = verbosity

    def log_enabled(self):
        return self.verbosity > 0

    def log(self, message):
        if self.log_enabled():
            print(message)

    def free(self, domain):
        self.log('{}FREE: {}{}'.format(GREEN, domain, RESET))

    def occu(self, domain):
        self.log('{}OCCU: {}{}'.format(GREY, domain, RESET))

    def error(self, message, important=False):
        if self.log_enabled() or important:
            print('{}{}{}'.format(RED, message, RESET), end='', file=sys.stderr)
