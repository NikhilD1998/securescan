def detect_server(http: dict) -> list[str]:

    server = http.get("server", "").lower()

    technologies = []

    signatures = {
        "apache": "Apache",
        "nginx": "Nginx",
        "microsoft-iis": "Microsoft IIS",
        "iis": "Microsoft IIS",
        "caddy": "Caddy",
        "litespeed": "LiteSpeed",
        "openresty": "OpenResty",
        "gunicorn": "Gunicorn",
        "uvicorn": "Uvicorn",
        "tomcat": "Apache Tomcat",
    }

    for signature, name in signatures.items():

        if signature in server:

            version = ""

            if "/" in server:

                try:
                    version = server.split(signature, 1)[1]

                    if version.startswith("/"):
                        version = version[1:]

                    version = version.split(" ")[0].strip()

                except Exception:
                    version = ""

            technologies.append(
                f"{name} {version}".strip()
            )

            break

    return technologies