import socket
import hashlib


def enumerate_favicon(ip: str, port: int, timeout: float) -> dict:

    result = {
        "found": False,
        "size": 0,
        "md5": "",
        "sha1": "",
        "sha256": ""
    }

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((ip, port))

        request = (
            "GET /favicon.ico HTTP/1.1\r\n"
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

        parts = response.split(b"\r\n\r\n", 1)

        if len(parts) != 2:
            return result

        headers = parts[0].decode(errors="ignore")
        body = parts[1]

        status = headers.split("\r\n")[0]

        if "200" not in status:
            return result

        result["found"] = True
        result["size"] = len(body)

        result["md5"] = hashlib.md5(body).hexdigest()
        result["sha1"] = hashlib.sha1(body).hexdigest()
        result["sha256"] = hashlib.sha256(body).hexdigest()

        return result

    except Exception:

        return result