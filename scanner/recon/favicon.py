import hashlib

from scanner.http.client import HTTPClient


def enumerate_favicon(client: HTTPClient) -> dict:
    result = {
        "found": False,
        "size": 0,
        "md5": "",
        "sha1": "",
        "sha256": ""
    }

    try:

        response = client.get("/favicon.ico")

        if response.status != 200:
            return result

        body = response.body

        result["found"] = True
        result["size"] = len(body)

        result["md5"] = hashlib.md5(body).hexdigest()
        result["sha1"] = hashlib.sha1(body).hexdigest()
        result["sha256"] = hashlib.sha256(body).hexdigest()

        return result

    except Exception:

        return result