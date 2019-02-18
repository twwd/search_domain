import socket


def has_ip(domain):
    """
    Check if DNS returns an IP for the given domain.
    :param domain: the target domain
    :return: whether there is a DNS result or not
    """
    try:
        socket.getaddrinfo(domain, port=None)
        return True
    except socket.gaierror:
        return False
