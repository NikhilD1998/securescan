import socket

from .services import get_service_name
from .enumerator import grab_banner

from parser.banner_parser import parse_banner

# NEW
from enumerators.http import enumerate_http


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

                # -------------------------
                # Grab Banner
                # -------------------------

                banner = grab_banner(
                    self.ip,
                    port,
                    self.timeout
                )

                parsed_banner = parse_banner(
                    port,
                    banner
                )

                # -------------------------
                # HTTP Enumeration
                # -------------------------

                if parsed_banner.get("protocol") == "HTTP":

                    http_info = enumerate_http(
                        self.ip,
                        port,
                        self.timeout
                    )

                    parsed_banner["http"] = http_info

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