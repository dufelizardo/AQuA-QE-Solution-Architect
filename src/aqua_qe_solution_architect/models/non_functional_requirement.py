from dataclasses import dataclass

CATEGORIAS_NFR = (
    "performance",
    "escalabilidade",
    "seguranca",
    "disponibilidade",
    "observabilidade",
    "manutenibilidade",
)


@dataclass
class NonFunctionalRequirement:
    """Um requisito não funcional, categorizado conforme ISO/IEC 25010 (ver knowledge/methodology/iso25010.md)."""

    category: str
    requirement: str
    rationale: str
    source_reference: str
