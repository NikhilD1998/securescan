import re


def parse_ssh_banner(banner: str) -> dict:
    """
    Parse an SSH banner into structured information.

    Example:
    SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13
    """

    parsed = {
        "protocol": "SSH",
        "software": "",
        "version": "",
        "os": "",
        "raw": banner,
    }

    if not banner:
        return parsed

    pattern = r"SSH-\d+\.\d+-(?P<software>[A-Za-z]+)[_ ](?P<version>[^\s]+)(?:\s+(?P<os>.+))?"

    match = re.search(pattern, banner)

    if not match:
        return parsed

    parsed["software"] = match.group("software")

    parsed["version"] = match.group("version")

    if match.group("os"):
        parsed["os"] = match.group("os")

    return parsed