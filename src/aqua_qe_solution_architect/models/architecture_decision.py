from dataclasses import dataclass, field


@dataclass
class ArchitectureDecision:
    """Um Architecture Decision Record (ADR) — toda decisão arquitetural relevante precisa de um (GR-SA-3), conforme knowledge/methodology/adr.md."""

    id: str
    title: str
    context: str
    decision: str
    consequences: str
    source_reference: str
    alternatives_considered: list[str] = field(default_factory=list)
