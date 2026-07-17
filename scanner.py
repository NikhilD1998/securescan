import socket
import time

from utils import COMMON_PORTS, get_service_name, print_headers


def scan_port(target: str, port: int) -> bool:
    """
    Scan a single TCP port.

    Returns:
        True if the port is open, otherwise False.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))

    sock.close()

    return result == 0


def main():

    print_headers()

    target = input("Enter Target IP/Hostname: ").strip()

    print(f"\nScanning {target}...\n")

    start = time.time()

    print(f"{'PORT':<10}{'STATUS':<10}{'SERVICE'}")
    print("-" * 35)

    open_ports = 0

    for port in COMMON_PORTS:

        if scan_port(target, port):

            service = get_service_name(port)

            print(f"{port:<10}OPEN{'':<6}{service}")

            open_ports += 1

    end = time.time()

    print("\n-----------------------------------")
    print(f"Open Ports : {open_ports}")
    print(f"Time Taken : {end-start:.2f} sec")


if __name__ == "__main__":
    main()