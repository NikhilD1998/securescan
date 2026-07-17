import socket

from .services import get_service_name


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

                return (
                    port,
                    True,
                    get_service_name(port)
                )

            return (
                port,
                False,
                "-"
            )

        except Exception:

            return (
                port,
                False,
                "-"
            )

        finally:

            sock.close()