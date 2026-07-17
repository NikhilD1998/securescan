def detect_backend(http: dict) -> list[str]:

    technologies = []

    headers = http.get("headers", {})
    powered_by = http.get("powered_by", "").lower()

    # ----------------------------
    # X-Powered-By
    # ----------------------------

    if powered_by:

        mappings = {
            "php": "PHP",
            "express": "Express.js",
            "asp.net": "ASP.NET",
            "aspnet": "ASP.NET",
            "django": "Django",
            "flask": "Flask",
            "laravel": "Laravel",
            "spring": "Spring Boot",
        }

        for signature, name in mappings.items():

            if signature in powered_by:

                technologies.append(name)

    # ----------------------------
    # Cookies
    # ----------------------------

    cookies = http.get("cookies", [])

    for cookie in cookies:

        cookie = cookie.lower()

        if "laravel_session" in cookie:

            technologies.append("Laravel")

        elif "phpsessid" in cookie:

            technologies.append("PHP")

        elif "jsessionid" in cookie:

            technologies.append("Java")

        elif "csrftoken" in cookie:

            technologies.append("Django")

        elif "connect.sid" in cookie:

            technologies.append("Express.js")

        elif ".aspxauth" in cookie:

            technologies.append("ASP.NET")

    # ----------------------------
    # Response Headers
    # ----------------------------

    if "X-AspNet-Version" in headers:

        technologies.append("ASP.NET")

    if "X-AspNetMvc-Version" in headers:

        technologies.append("ASP.NET MVC")

    # Remove duplicates while preserving order

    seen = set()

    unique = []

    for tech in technologies:

        if tech not in seen:

            unique.append(tech)

            seen.add(tech)

    return unique