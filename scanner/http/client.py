import socket
import ssl

from .response import HTTPResponse


class HTTPClient:

    def __init__(

        self,

        ip: str,

        port: int,

        timeout: float

    ):

        self.ip = ip
        self.port = port
        self.timeout = timeout

    def _connect(self):

        sock = socket.create_connection(
            (
                self.ip,
                self.port
            ),
            timeout=self.timeout
        )

        if self.port == 443:

            context = ssl.create_default_context()

            sock = context.wrap_socket(
                sock,
                server_hostname=self.ip
            )

        return sock

    def request(

        self,

        method: str,

        path: str = "/",

        headers: dict | None = None

    ) -> HTTPResponse:

        if headers is None:
            headers = {}

        sock = self._connect()

        request = (
            f"{method} {path} HTTP/1.1\r\n"
            f"Host: {self.ip}\r\n"
            "Connection: close\r\n"
        )

        for key, value in headers.items():

            request += f"{key}: {value}\r\n"

        request += "\r\n"

        sock.sendall(
            request.encode()
        )

        response = b""

        while True:

            chunk = sock.recv(4096)

            if not chunk:
                break

            response += chunk

        sock.close()

        header_bytes, _, body = response.partition(
            b"\r\n\r\n"
        )

        header_text = header_bytes.decode(
            errors="ignore"
        )

        lines = header_text.split("\r\n")

        status = 0
        reason = ""

        if lines:

            first = lines[0].split(
                " ",
                2
            )

            if len(first) >= 2:

                status = int(first[1])

                if len(first) == 3:
                    reason = first[2]

        parsed_headers = {}

        for line in lines[1:]:

            if ":" not in line:
                continue

            key, value = line.split(
                ":",
                1
            )

            parsed_headers[key.strip()] = value.strip()

        return HTTPResponse(

            status=status,

            reason=reason,

            headers=parsed_headers,

            body=body

        )

    def get(

        self,

        path="/",

        headers=None

    ):

        return self.request(
            "GET",
            path,
            headers
        )

    def options(

        self,

        path="/"

    ):

        return self.request(
            "OPTIONS",
            path
        )

    def head(

        self,

        path="/"

    ):

        return self.request(
            "HEAD",
            path
        )