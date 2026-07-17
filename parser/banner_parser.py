from .ssh_parser import parse_ssh_banner
from .http_parser import parse_http_banner


def parse_banner(port: int, banner: str) -> dict:
    """
    Dispatch banner parsing to the correct protocol parser.

    Returns a standardized dictionary regardless of protocol.
    """

    if not banner:
        return {
            "protocol": "UNKNOWN",
            "software": "",
            "version": "",
            "os": "",
            "raw": "",
        }

    # -----------------------------
    # SSH
    # -----------------------------
    if port == 22 or banner.startswith("SSH-"):
        return parse_ssh_banner(banner)

    # -----------------------------
    # HTTP
    # -----------------------------
    if (
        port in (80, 8080, 8000)
        or banner.startswith("HTTP/")
    ):
        return parse_http_banner(banner)

    # -----------------------------
    # Unknown protocol
    # -----------------------------
    return {
        "protocol": "UNKNOWN",
        "software": "",
        "version": "",
        "os": "",
        "raw": banner,
    }