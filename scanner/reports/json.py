import json
from pathlib import Path
from dataclasses import is_dataclass, asdict


class ReportEncoder(json.JSONEncoder):

    def default(self, obj):

        if is_dataclass(obj):
            return asdict(obj)

        return super().default(obj)


def export_json(
    target: str,
    ip: str,
    elapsed: float,
    results: list,
    output: str = "report.json"
):

    report = {
        "target": target,
        "ip": ip,
        "scan_time": round(elapsed, 2),
        "open_ports": []
    }

    for port, status, service, parsed in results:

        entry = {
            "port": port,
            "status": status,
            "service": service,
            "protocol": parsed.get("protocol"),
            "software": parsed.get("software"),
            "version": parsed.get("version"),
            "os": parsed.get("os"),
        }

        if parsed.get("http"):

            entry["http"] = parsed["http"]

        report["open_ports"].append(entry)

    Path(output).write_text(

        json.dumps(
            report,
            cls=ReportEncoder,
            indent=4
        ),

        encoding="utf-8"

    )

    return output