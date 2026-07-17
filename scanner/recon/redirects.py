from scanner.http.client import HTTPClient


def enumerate_redirects(client: HTTPClient) -> dict:

    result = {
        "redirect": False,
        "status": None,
        "location": ""
    }

    try:

        response = client.get("/")

        if response.status not in (301, 302, 303, 307, 308):
            return result

        result["redirect"] = True
        result["status"] = response.status
        result["location"] = response.headers.get("Location", "")

        return result

    except Exception:

        return result