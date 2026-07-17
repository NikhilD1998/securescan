from dataclasses import dataclass, field


@dataclass(slots=True)
class HTTPResponse:

    status: int = 0

    reason: str = ""

    headers: dict = field(default_factory=dict)

    body: bytes = b""

    @property
    def text(self) -> str:

        return self.body.decode(
            errors="ignore"
        )