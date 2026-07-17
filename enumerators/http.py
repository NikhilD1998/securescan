import socket
import re


def enumerate_http(ip: str, port: int, timeout: float):

    result = {
        "title": "",
        "server": "",
        "powered_by": "",
        "cookies": [],
        "location": "",
        "headers": {},
        "security_headers": {}
    }

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((ip, port))

        request = (
            f"GET / HTTP/1.1\r\n"
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

        response = response.decode(
            errors="ignore"
        )

        header_text = response.split(
            "\r\n\r\n",
            1
        )[0]

        body = ""

        if "\r\n\r\n" in response:
            body = response.split(
                "\r\n\r\n",
                1
            )[1]

        # -------------------------
        # Parse headers
        # -------------------------

        for line in header_text.split("\r\n")[1:]:

            if ":" not in line:
                continue

            key, value = line.split(
                ":",
                1
            )

            result["headers"][key.strip()] = value.strip()

        headers = result["headers"]

        result["server"] = headers.get(
            "Server",
            ""
        )

        result["powered_by"] = headers.get(
            "X-Powered-By",
            ""
        )

        result["location"] = headers.get(
            "Location",
            ""
        )

        # -------------------------
        # Cookies
        # -------------------------

        for key, value in headers.items():

            if key.lower() == "set-cookie":

                result["cookies"].append(value)

        # -------------------------
        # Security Headers
        # -------------------------

        security = [

            "Strict-Transport-Security",

            "Content-Security-Policy",

            "X-Frame-Options",

            "X-Content-Type-Options",

            "Referrer-Policy"

        ]

        for header in security:

            result["security_headers"][header] = headers.get(
                header,
                "Missing"
            )

        # -------------------------
        # HTML Title
        # -------------------------

        match = re.search(
            r"<title>(.*?)</title>",
            body,
            re.I | re.S
        )

        if match:

            result["title"] = match.group(1).strip()

        sock.close()

        return result

    except Exception:

        return result   