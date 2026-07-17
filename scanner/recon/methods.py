from scanner.http.client import HTTPClient


def enumerate_methods(client: HTTPClient) -> list[str]:
    try:

        response = client.options("/")

        allow = (
            response.headers.get("Allow")
            or response.headers.get("Public")
            or ""
        )

        if not allow:
            return []

        return [
            method.strip()
            for method in allow.split(",")
            if method.strip()
        ]

    except Exception:

        return []