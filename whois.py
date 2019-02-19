import socket


def has_entry(domain):
    server = "whois.denic.de"  # "de.whois-servers.net"
    port = 43
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    sock.send("-T dn,ace {}\r\n".format(domain).encode("utf-8"))

    try:
        buff = b""
        while True:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            buff += data
        value = buff.decode("utf-8")
    finally:
        sock.close()

    if "Status: free" in value:
        return False
    return True
