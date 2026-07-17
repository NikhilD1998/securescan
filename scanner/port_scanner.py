import socket
import time
import queue
import threading

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from .config import THREADS, TIMEOUT
from .worker import Worker

console = Console()


class PortScanner:

    def __init__(self, target: str):

        self.target = target
        self.ip = socket.gethostbyname(target)

        self.timeout = TIMEOUT
        self.thread_count = THREADS

        self.port_queue = queue.Queue()
        self.results = []

        self.lock = threading.Lock()

    def worker(self, progress, task):

        scanner = Worker(
            self.ip,
            self.timeout
        )

        while True:

            try:
                port = self.port_queue.get_nowait()

            except queue.Empty:
                break

            result = scanner.scan(port)

            if result[1]:

                with self.lock:
                    self.results.append(result)

            progress.update(task, advance=1)

            self.port_queue.task_done()

    def scan(self, ports: list[int]):

        for port in ports:
            self.port_queue.put(port)

        start = time.perf_counter()

        with Progress() as progress:

            task = progress.add_task(
                "[cyan]Scanning...",
                total=len(ports)
            )

            threads = []

            for _ in range(self.thread_count):

                thread = threading.Thread(
                    target=self.worker,
                    args=(progress, task)
                )

                thread.start()

                threads.append(thread)

            for thread in threads:
                thread.join()

        elapsed = time.perf_counter() - start

        self.results.sort()

        table = Table(
            title=f"Scan Results - {self.target}"
        )

        table.add_column("Port", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Service", justify="center")
        table.add_column("Protocol", justify="center")
        table.add_column("Software", justify="center")
        table.add_column("Version", justify="center")
        table.add_column("OS", justify="center")

        for port, _, service, parsed in self.results:

            table.add_row(
                str(port),
                "[green]OPEN[/green]",
                service,
                parsed.get("protocol", "-"),
                parsed.get("software", "-"),
                parsed.get("version", "-"),
                parsed.get("os", "-"),
            )

        console.print()
        console.print(table)
        console.print()

        self.print_service_details()

        console.print(
            f"[cyan]Target[/cyan] : {self.target}"
        )

        console.print(
            f"[cyan]Resolved IP[/cyan] : {self.ip}"
        )

        console.print(
            f"[green]Open Ports[/green] : {len(self.results)}"
        )

        console.print(
            f"[yellow]Ports Scanned[/yellow] : {len(ports)}"
        )

        console.print(
            f"[magenta]Threads[/magenta] : {self.thread_count}"
        )

        console.print(
            f"[blue]Timeout[/blue] : {self.timeout}s"
        )

        console.print(
            f"[white]Scan Time[/white] : {elapsed:.2f}s"
        )

    def print_service_details(self):

        console.print("[bold cyan]Service Details[/bold cyan]\n")

        for port, _, service, parsed in self.results:

            console.rule(f"[green]Port {port} ({service})")

            console.print(
                f"[bold]Software:[/bold] {parsed.get('software', '-')}"
            )

            console.print(
                f"[bold]Version:[/bold] {parsed.get('version', '-')}"
            )

            console.print(
                f"[bold]Platform:[/bold] {parsed.get('os', '-')}"
            )

            # -----------------------------
            # HTTP Details
            # -----------------------------

            if parsed.get("protocol") == "HTTP":

                http = parsed.get("http", {})

                console.print()
                console.print("[bold yellow]HTTP Enumeration[/bold yellow]")

                console.print(f"Title        : {http.get('title') or '-'}")
                console.print(f"Server       : {http.get('server') or '-'}")
                console.print(f"Powered By   : {http.get('powered_by') or '-'}")
                console.print(f"Redirect     : {http.get('location') or '-'}")

                cookies = http.get("cookies", [])

                console.print(
                    f"Cookies      : {', '.join(cookies) if cookies else '-'}"
                )

                # ----------------------------------
                # Technology Fingerprint
                # ----------------------------------

                fp = http.get("fingerprint", {})

                console.print()
                console.print("[bold cyan]Technology Fingerprint[/bold cyan]")

                sections = [
                    ("Server", "server"),
                    ("Backend", "backend"),
                    ("Frontend", "frontend"),
                    ("CMS", "cms"),
                    ("CDN", "cdn"),
                ]

                for title, key in sections:

                    console.print(f"\n[bold]{title}[/bold]")

                    values = fp.get(key, [])

                    if values:

                        for tech in values:
                            console.print(f"[green]✓[/green] {tech}")

                    else:

                        console.print("[dim]None Detected[/dim]")

                # ----------------------------------
                # Security Headers
                # ----------------------------------

                console.print()
                console.print("[bold yellow]Security Headers[/bold yellow]")

                for header, value in http.get(
                    "security_headers",
                    {}
                ).items():

                    if value == "Missing":

                        console.print(
                            f"[red]✘[/red] {header}"
                        )

                    else:

                        console.print(
                            f"[green]✔[/green] {header}"
                        )

                # ----------------------------------
                # Security Findings
                # ----------------------------------

                findings = http.get("findings", [])

                if findings:

                    console.print()
                    console.print("[bold red]Security Findings[/bold red]")

                    severity_colors = {
                        "Critical": "bold red",
                        "High": "red",
                        "Medium": "yellow",
                        "Low": "cyan",
                        "Info": "white"
                    }

                    counts = {
                        "Critical": 0,
                        "High": 0,
                        "Medium": 0,
                        "Low": 0,
                        "Info": 0
                    }

                    for finding in findings:
                        counts[finding.severity] = counts.get(finding.severity, 0) + 1

                    console.print()
                    console.print("[bold]Summary[/bold]")

                    for severity in ["Critical", "High", "Medium", "Low", "Info"]:

                        color = severity_colors[severity]

                        console.print(
                            f"[{color}]{severity:<8}[/{color}] : {counts[severity]}"
                        )

                    console.print(f"\nTotal Findings : {len(findings)}")

                    for index, finding in enumerate(findings, start=1):

                        color = severity_colors.get(
                            finding.severity,
                            "white"
                        )

                        console.rule(
                            f"[{color}]Finding {index}[/{color}]"
                        )

                        console.print(
                            f"[bold]Severity[/bold]      : [{color}]{finding.severity}[/{color}]"
                        )

                        console.print(
                            f"[bold]Title[/bold]         : {finding.title}"
                        )

                        console.print(
                            f"[bold]Description[/bold]   : {finding.description}"
                        )

                        console.print(
                            f"[bold]Recommendation[/bold]: {finding.recommendation}"
                        )

                else:

                    console.print()
                    console.print("[green]No security findings detected.[/green]")

            console.print()