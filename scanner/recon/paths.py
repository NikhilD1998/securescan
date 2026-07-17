import socket
import re


PATHS = [
    "/robots.txt",
    "/security.txt",
    "/sitemap.xml",
    "/favicon.ico",
    "/login",
    "/admin",
    "/dashboard",
    "/api",
    "/graphql",
    "/phpmyadmin",
]


def enumerate_paths(ip: str, port: int, timeout: float) -> list[dict]:

    results = []

    for path in PATHS:

        try:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            sock.connect((ip, port))

            request = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {ip}\r\n"
                f"Connection: close\r\n\r\n"
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

            header, _, body = response.partition("\r\n\r\n")

            first_line = header.split("\r\n")[0]

            match = re.search(
                r"HTTP/\d\.\d\s+(\d+)\s+(.*)",
                first_line
            )

            status_code = 0
            status_text = ""

            if match:

                status_code = int(match.group(1))
                status_text = match.group(2)

            title = ""

            title_match = re.search(
                r"<title>(.*?)</title>",
                body,
                re.I | re.S
            )

            if title_match:

                title = title_match.group(1).strip()

            results.append(
                {
                    "path": path,
                    "status": status_code,
                    "message": status_text,
                    "title": title,
                }
            )

        except Exception:

            continue

    return results