import socket


class Whois:
    """
    Stolen from https://github.com/jeremija/domainsearch/blob/master/domainsearch/main.py
    """

    def __init__(self):
        self.server = "whois.denic.de"  # "de.whois-servers.net"
        self.port = 43

    def is_available(self, domain, verbose=False):
        """Looks up the domain. Returns true if domain is not registered,
        false otherwise"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server, self.port))
        sock.send("-T dn,ace {}\r\n".format(domain).encode("utf-8"))

        try:
            value = self._recv(sock)
        finally:
            sock.close()

        if verbose:
            print(value)

        if "No match for nameserver" in value:
            return None
        if "Status: free" in value or "No match for" in value:
            return True
        return False

    @staticmethod
    def _recv(sock):
        buff = b""
        while True:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            buff += data
        return buff.decode("utf-8")
