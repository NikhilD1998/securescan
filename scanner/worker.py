import socket

from .services import get_service_name
from .banner import grab_banner


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

                banner = grab_banner(
                    self.ip,
                    port,
                    self.timeout
                )

                return (
                    port,
                    True,
                    get_service_name(port),
                    banner
                )

            return (
                port,
                False,
                "-",
                ""
            )

        except Exception:

            return (
                port,
                False,
                "-"
            )

        finally:

            sock.close()