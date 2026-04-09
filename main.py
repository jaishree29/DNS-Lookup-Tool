import dns.resolver
import ipaddress
import socket
import ssl
import struct
import dns.message

def read_targets(filename):
    targets = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line:
                targets.append(line)
    return targets

# targets = read_targets('data.txt')
# print(targets)

def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
    
def resolve_to_ip(hostname):
    if is_ip(hostname):
        return hostname
    try:
        answers = dns.resolver.resolve(hostname, 'A')
        return str(answers[0])
    except Exception:
        return None
    
# print(resolve_to_ip('dns.google'))

def test_dot(ip):
    try:
        query = dns.message.make_query('google.com', 'A')
        wire = query.to_wire()
        data = struct.pack('!H', len(wire)) + wire

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((ip, 853), timeout=5) as sock:
            with context.wrap_socket(sock) as tls:
                tls.sendall(data)
                response = tls.recv(1024)
                return len(response) > 2
    except Exception:
        return False
    
# print(test_dot('dns.google'))