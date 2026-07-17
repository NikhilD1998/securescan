from scanner.http.client import HTTPClient


INTERESTING_HEADERS = {
    "server",
    "x-powered-by",
    "content-type",
    "content-length",
    "cache-control",
    "etag",
    "last-modified",
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
    "access-control-allow-origin",
    "access-control-allow-methods",
    "access-control-allow-headers",
    "set-cookie",
}


def enumerate_headers(client: HTTPClient) -> dict:
    try:

        response = client.get("/")

        return {
            key: value
            for key, value in response.headers.items()
            if key.lower() in INTERESTING_HEADERS
        }

    except Exception:

        return {}