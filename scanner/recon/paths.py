import re

from scanner.http.client import HTTPClient


PATHS = [
    "/robots.txt",
    "/security.txt",
    "/sitemap.xml",
    "/favicon.ico",
    "/login",
    "/admin",
    "/dashboard",
    "/api",
    "/graphql",
    "/phpmyadmin",
]


INTERESTING_STATUS = {
    200,
    201,
    204,
    301,
    302,
    307,
    308,
    401,
    403,
    405,
}


def enumerate_paths(client: HTTPClient) -> list[dict]:

    results = []

    for path in PATHS:

        try:

            response = client.get(path)

            if response.status not in INTERESTING_STATUS:
                continue

            title = ""

            match = re.search(
                r"<title>(.*?)</title>",
                response.text,
                re.I | re.S
            )

            if match:

                title = match.group(1).strip()

            results.append(
                {
                    "path": path,
                    "status": response.status,
                    "message": response.reason,
                    "title": title,
                }
            )

        except Exception:

            continue

    return results