import socket
import time

from rich.console import Console
from rich.table import Table

from .services import get_service_name

console = Console()


class PortScanner:

    def __init__(self, target: str):

        self.target = target
        self.timeout = 0.5

    def scan_port(self, port: int) -> bool:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(self.timeout)

        result = sock.connect_ex((self.target, port))

        sock.close()

        return result == 0

    def scan(self, ports: list[int]):

        table = Table(title=f"Scan Results - {self.target}")

        table.add_column("Port")
        table.add_column("Status")
        table.add_column("Service")

        start = time.time()

        open_ports = 0

        total = len(ports)

        for index, port in enumerate(ports, start=1):

            print(f"\rScanning Port {port} ({index}/{total})...", end="", flush=True)

            if self.scan_port(port):

                open_ports += 1

                table.add_row(
                    str(port),
                    "[green]OPEN[/green]",
                    get_service_name(port)
                )

        print()  # Move to the next line

        elapsed = time.time() - start

        console.print(table)
        console.print(f"\nOpen Ports : {open_ports}")
        console.print(f"Scan Time : {elapsed:.2f}s")