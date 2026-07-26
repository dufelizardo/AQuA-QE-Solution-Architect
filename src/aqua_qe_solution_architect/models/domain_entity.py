from dataclasses import dataclass, field


@dataclass
class DomainEntity:
    """Uma entidade do modelo de domínio — nome e atributos só existem se evidenciados/inferíveis do texto de origem (GR-SA-1)."""

    name: str
    source_reference: str
    attributes: list[str] = field(default_factory=list)
