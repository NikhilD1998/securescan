from scanner.fingerprint.servers import detect_server
from scanner.fingerprint.frameworks import detect_backend
from scanner.fingerprint.frontend import detect_frontend
from scanner.fingerprint.cms import detect_cms
from scanner.fingerprint.cdn import detect_cdn


def fingerprint(http: dict) -> dict:
    """
    Generate a technology fingerprint from HTTP enumeration data.
    """

    return {
        "server": detect_server(http),
        "backend": detect_backend(http),
        "frontend": detect_frontend(http),
        "cms": detect_cms(http),
        "cdn": detect_cdn(http),
    }