from dataclasses import dataclass, field


@dataclass
class ProcessFlow:
    """Um fluxo de processo principal — passos só existem se evidenciados/inferíveis do texto de origem (GR-SA-1)."""

    name: str
    source_reference: str
    steps: list[str] = field(default_factory=list)
