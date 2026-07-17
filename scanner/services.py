import socket


def get_service_name(port: int) -> str:
    """
    Returns the well-known service name for a port.
    """

    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"