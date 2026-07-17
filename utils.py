import socket

COMMON_PORTS = [
     20,
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    143,
    443,
    3306,
    3389,
]

def print_headers():
    print("=" * 40)
    print("     SecureScan v1.0")
    print("=" * 40)

def get_service_name(port: int) -> str:
    try:
        return socket.getservbyport(port)
    except OSError:
        return 'Unknown' 