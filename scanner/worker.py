import socket

from .services import get_service_name
from .enumerator import grab_banner

from parser.banner_parser import parse_banner


class Worker:

    def __init__(self, ip: str, timeout: float):
        self.ip = ip
        self.timeout = timeout

    def scan(self, port: int):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        try:

            result = sock.connect_ex((self.ip, port))

            if result == 0:

                service = get_service_name(port)

                # Grab raw banner
                banner = grab_banner(
                    self.ip,
                    port,
                    self.timeout
                )

                # Parse banner into structured data
                parsed_banner = parse_banner(
                    port,
                    banner
                )

                return (
                    port,
                    True,
                    service,
                    parsed_banner
                )

            return (
                port,
                False,
                "-",
                {}
            )

        except Exception:

            return (
                port,
                False,
                "-",
                {}
            )

        finally:

            sock.close()