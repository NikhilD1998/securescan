from scanner.recon.paths import enumerate_paths
from scanner.recon.methods import enumerate_methods
from scanner.recon.redirects import enumerate_redirects
from scanner.recon.headers import enumerate_headers
from scanner.recon.favicon import enumerate_favicon


def recon(ip: str, port: int, timeout: float) -> dict:

    return {
        "paths": enumerate_paths(ip, port, timeout),
        "methods": enumerate_methods(ip, port, timeout),
        "redirects": enumerate_redirects(ip, port, timeout),
        "headers": enumerate_headers(ip, port, timeout),
        "favicon": enumerate_favicon(ip, port, timeout),
    }