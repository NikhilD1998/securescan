def parse_ports(port_string: str) -> list[int]:
    """
    Supports:

    80
    20-25
    22,80,443
    """

    ports = set()

    if "," in port_string:

        for part in port_string.split(","):
            ports.update(parse_ports(part))

        return sorted(ports)

    if "-" in port_string:

        start, end = map(int, port_string.split("-"))

        return list(range(start, end + 1))

    ports.add(int(port_string))

    return sorted(ports)