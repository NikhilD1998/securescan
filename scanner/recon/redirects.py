import socket
import re


def enumerate_redirects(ip: str, port: int, timeout: float) -> dict:

    result = {
        "redirect": False,
        "status": None,
        "location": ""
    }

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

        headers = response.split("\r\n\r\n", 1)[0]

        first_line = headers.split("\r\n")[0]

        match = re.search(
            r"HTTP/\d\.\d\s+(\d+)",
            first_line
        )

        if not match:

            return result

        status = int(match.group(1))

        if status not in (301, 302, 303, 307, 308):

            return result

        result["redirect"] = True
        result["status"] = status

        for line in headers.split("\r\n"):

            if line.lower().startswith("location:"):

                result["location"] = line.split(
                    ":",
                    1
                )[1].strip()

                break

        return result

    except Exception:

        return result