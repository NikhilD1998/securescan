import re


def detect_frontend(http: dict) -> list[str]:

    technologies = []

    body = http.get("body", "").lower()
    headers = http.get("headers", {})

    # ----------------------------
    # Response Headers
    # ----------------------------

    if headers.get("X-Powered-By", "").lower().startswith("next.js"):
        technologies.append("Next.js")

    # ----------------------------
    # Script Sources
    # ----------------------------

    script_patterns = {
        r"_next/": "Next.js",
        r"_next/static": "Next.js",
        r"/static/js/main": "React",
        r"react": "React",
        r"react-dom": "React",
        r"vue": "Vue.js",
        r"angular": "Angular",
        r"ng-app": "Angular",
        r"svelte": "Svelte",
        r"nuxt": "Nuxt.js",
        r"gatsby": "Gatsby",
    }

    for pattern, framework in script_patterns.items():

        if re.search(pattern, body):

            technologies.append(framework)

    # ----------------------------
    # HTML Attributes
    # ----------------------------

    html_patterns = {
        r'data-reactroot': "React",
        r'id="__next"': "Next.js",
        r'id="__nuxt"': "Nuxt.js",
        r'ng-version=': "Angular",
        r'ng-app=': "Angular",
        r'data-svelte': "Svelte",
    }

    for pattern, framework in html_patterns.items():

        if re.search(pattern, body):

            technologies.append(framework)

    # ----------------------------
    # Meta Tags
    # ----------------------------

    meta_patterns = {
        r'content="next\.js': "Next.js",
        r'generator.*gatsby': "Gatsby",
        r'generator.*vuepress': "VuePress",
    }

    for pattern, framework in meta_patterns.items():

        if re.search(pattern, body):

            technologies.append(framework)

    # ----------------------------
    # Remove Duplicates
    # ----------------------------

    seen = set()
    unique = []

    for tech in technologies:

        if tech not in seen:
            seen.add(tech)
            unique.append(tech)

    return unique