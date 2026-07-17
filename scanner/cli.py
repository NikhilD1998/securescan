import argparse


def get_arguments():

    parser = argparse.ArgumentParser(
        prog="SecureScan",
        description="Simple TCP Port Scanner"
    )

    parser.add_argument(
        "target",
        help="Target IP Address or Hostname"
    )

    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help="Port(s): 80 | 20-80 | 22,80,443"
    )

    return parser.parse_args()