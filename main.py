from rich.console import Console

from scanner.cli import get_arguments
from scanner.port_scanner import PortScanner
from scanner.utils import parse_ports

console = Console()


def main():

    args = get_arguments()

    ports = parse_ports(args.ports)

    console.print()

    scanner = PortScanner(args.target)

    scanner.scan(ports)


if __name__ == "__main__":
    main()