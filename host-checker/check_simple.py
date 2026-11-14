import socket

def is_up(address, port, timeout=2):
    try:
        with socket.create_connection((address, port), timeout=timeout):
            return True
    except OSError:
        return False

print(is_up("8.8.8.8", 53))
print(is_up("192.168.1.1", 80))