import socket


def enumerate_methods(ip: str, port: int, timeout: float) -> list[str]:

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((ip, port))

        request = (
            "OPTIONS / HTTP/1.1\r\n"
            f"Host: {ip}\r\n"
            "Connection: close\r\n\r\n"
        )

        sock.send(request.encode())

        response = b""

        while True:

            chunk = sock.recv(4096)

            if not chunk:
                break

            response += chunk

        sock.close()

        response = response.decode(errors="ignore")

        headers = response.split("\r\n\r\n", 1)[0]

        allow = ""

        for line in headers.split("\r\n"):

            if (
                line.lower().startswith("allow:")
                or line.lower().startswith("public:")
            ):

                allow = line.split(":", 1)[1].strip()
                break

        if not allow:

            return []

        methods = []

        for method in allow.split(","):

            method = method.strip()

            if method:
                methods.append(method)

        return methods

    except Exception:

        return []