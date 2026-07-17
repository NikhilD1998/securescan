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

                t = threading.Thread(
                    target=self.worker,
                    args=(progress, task)
                )

                t.start()

                threads.append(t)

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

        for port, _, service in self.results:

            table.add_row(
                str(port),
                "[green]OPEN[/green]",
                service
            )

        console.print()
        console.print(table)
        console.print()

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