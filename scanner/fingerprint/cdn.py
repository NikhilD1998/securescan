def detect_cdn(http: dict) -> list[str]:

    technologies = []

    headers = {
        k.lower(): v.lower()
        for k, v in http.get("headers", {}).items()
    }

    server = http.get("server", "").lower()

    # --------------------------------
    # Cloudflare
    # --------------------------------

    if (
        "cf-ray" in headers
        or "cf-cache-status" in headers
        or "cloudflare" in server
    ):
        technologies.append("Cloudflare")

    # --------------------------------
    # AWS CloudFront
    # --------------------------------

    if (
        "x-amz-cf-id" in headers
        or "x-cache" in headers
        and "cloudfront" in headers["x-cache"]
    ):
        technologies.append("AWS CloudFront")

    # --------------------------------
    # Fastly
    # --------------------------------

    if (
        "x-served-by" in headers
        and "cache" in headers.get("via", "")
    ):
        technologies.append("Fastly")

    # --------------------------------
    # Akamai
    # --------------------------------

    if (
        "akamai" in headers.get("server", "")
        or "akamai" in headers.get("via", "")
        or "x-akamai-transformed" in headers
    ):
        technologies.append("Akamai")

    # --------------------------------
    # Vercel
    # --------------------------------

    if (
        "x-vercel-id" in headers
        or "vercel" in server
    ):
        technologies.append("Vercel")

    # --------------------------------
    # Netlify
    # --------------------------------

    if (
        "x-nf-request-id" in headers
        or "netlify" in server
    ):
        technologies.append("Netlify")

    # --------------------------------
    # BunnyCDN
    # --------------------------------

    if (
        "bunnycdn" in server
        or "cdn-pullzone" in headers
    ):
        technologies.append("BunnyCDN")

    # --------------------------------
    # Azure Front Door
    # --------------------------------

    if (
        "x-azure-ref" in headers
        or "azure" in server
    ):
        technologies.append("Azure Front Door")

    # --------------------------------
    # Remove Duplicates
    # --------------------------------

    seen = set()
    unique = []

    for tech in technologies:

        if tech not in seen:
            seen.add(tech)
            unique.append(tech)

    return unique