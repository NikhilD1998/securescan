import re


def detect_cms(http: dict) -> list[str]:

    technologies = []

    headers = http.get("headers", {})
    body = http.get("body", "").lower()

    # ----------------------------
    # Headers
    # ----------------------------

    powered_by = headers.get("X-Powered-By", "").lower()

    if "wp" in powered_by:
        technologies.append("WordPress")

    # ----------------------------
    # Meta Generator
    # ----------------------------

    generators = {
        r'generator.*wordpress': "WordPress",
        r'generator.*joomla': "Joomla",
        r'generator.*drupal': "Drupal",
        r'generator.*ghost': "Ghost",
    }

    for pattern, cms in generators.items():

        if re.search(pattern, body):

            technologies.append(cms)

    # ----------------------------
    # WordPress
    # ----------------------------

    wordpress_patterns = [
        r"wp-content",
        r"wp-includes",
        r"/wp-json/",
        r"wordpress",
    ]

    if any(re.search(pattern, body) for pattern in wordpress_patterns):

        technologies.append("WordPress")

    # ----------------------------
    # Joomla
    # ----------------------------

    joomla_patterns = [
        r"/media/system/",
        r"com_content",
        r"joomla",
    ]

    if any(re.search(pattern, body) for pattern in joomla_patterns):

        technologies.append("Joomla")

    # ----------------------------
    # Drupal
    # ----------------------------

    drupal_patterns = [
        r"/sites/default/",
        r"drupal-settings-json",
        r"drupal",
    ]

    if any(re.search(pattern, body) for pattern in drupal_patterns):

        technologies.append("Drupal")

    # ----------------------------
    # Ghost
    # ----------------------------

    ghost_patterns = [
        r"/ghost/",
        r"ghost-content",
        r"ghost-sdk",
    ]

    if any(re.search(pattern, body) for pattern in ghost_patterns):

        technologies.append("Ghost")

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