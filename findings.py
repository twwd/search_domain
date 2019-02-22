from io import TextIOWrapper

from logger import Logger


class Findings:
    def __init__(self, log: Logger, free_file: TextIOWrapper, occu_file: TextIOWrapper) -> None:
        self.log = log
        self.free_file = free_file
        self.occu_file = occu_file
        self.occu = set()
        self.free = set()

    def persist(self):
        for item in self.occu:
            self.occu_file.write('{}\n'.format(item))
            self.occu = set()
        for item in self.free:
            self.free_file.write('{}\n'.format(item))
        self.free = set()

    def add_domain(self, domain, is_free=False):
        if is_free:
            self.log.free(domain)
            self.free.add(domain)
        else:
            self.log.occu(domain)
            self.occu.add(domain)

    def __del__(self):
        self.persist()
        self.occu_file.close()
        self.free_file.close()
