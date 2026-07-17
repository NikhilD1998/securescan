import re


def parse_http_banner(banner: str) -> dict:
    """
    Parse an HTTP response banner.

    Example Input:

    HTTP/1.1 200 OK
    Date: Fri, 17 Jul 2026 05:38:10 GMT
    Server: Apache/2.4.7 (Ubuntu)
    Content-Type: text/html

    Returns a structured dictionary.
    """

    parsed = {
        "protocol": "HTTP",
        "http_version": "",
        "status_code": "",
        "status_message": "",
        "software": "",
        "version": "",
        "os": "",
        "raw": banner,
    }

    if not banner:
        return parsed

    lines = banner.splitlines()

    # -------------------------------
    # Parse HTTP Status Line
    # -------------------------------

    if lines:
        status_match = re.search(
            r"HTTP/(?P<version>\d\.\d)\s+(?P<code>\d+)\s+(?P<message>.+)",
            lines[0],
        )

        if status_match:
            parsed["http_version"] = status_match.group("version")
            parsed["status_code"] = status_match.group("code")
            parsed["status_message"] = status_match.group("message")

    # -------------------------------
    # Parse Server Header
    # -------------------------------

    server_header = None

    for line in lines:
        if line.lower().startswith("server:"):
            server_header = line.split(":", 1)[1].strip()
            break

    if server_header:

        # Apache/2.4.7 (Ubuntu)

        match = re.search(
            r"(?P<software>[A-Za-z\-]+)"
            r"(?:/(?P<version>[^\s]+))?"
            r"(?:\s+\((?P<os>.*?)\))?",
            server_header,
        )

        if match:

            parsed["software"] = match.group("software") or ""
            parsed["version"] = match.group("version") or ""
            parsed["os"] = match.group("os") or ""

    return parsed