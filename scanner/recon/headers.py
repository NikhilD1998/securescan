import socket


INTERESTING_HEADERS = {
    "server",
    "x-powered-by",
    "content-type",
    "content-length",
    "cache-control",
    "etag",
    "last-modified",
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
    "access-control-allow-origin",
    "access-control-allow-methods",
    "access-control-allow-headers",
    "set-cookie",
}


def enumerate_headers(ip: str, port: int, timeout: float) -> dict:

    headers = {}

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((ip, port))

        request = (
            "GET / HTTP/1.1\r\n"
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

        header_block = response.split("\r\n\r\n", 1)[0]

        for line in header_block.split("\r\n")[1:]:

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            if key.lower() in INTERESTING_HEADERS:

                headers[key] = value

        return headers

    except Exception:

        return {}