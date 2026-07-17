from scanner.http.client import HTTPClient

from scanner.recon.paths import enumerate_paths
from scanner.recon.methods import enumerate_methods
from scanner.recon.redirects import enumerate_redirects
from scanner.recon.headers import enumerate_headers
from scanner.recon.favicon import enumerate_favicon


def recon(ip: str, port: int, timeout: float) -> dict:

    client = HTTPClient(
        ip,
        port,
        timeout
    )

    return {
        "paths": enumerate_paths(client),
        "methods": enumerate_methods(client),
        "redirects": enumerate_redirects(client),
        "headers": enumerate_headers(client),
        "favicon": enumerate_favicon(client),
    }