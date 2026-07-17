import socket


def grab_banner(ip: str, port: int, timeout: float = 2):

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((ip, port))

        if port in [80, 8080, 8000]:

            request = (
                "GET / HTTP/1.1\r\n"
                f"Host: {ip}\r\n"
                "Connection: close\r\n\r\n"
            )

            sock.send(request.encode())

        banner = sock.recv(1024).decode(
            errors="ignore"
        )

        sock.close()

        return banner

    except Exception:

        return ""