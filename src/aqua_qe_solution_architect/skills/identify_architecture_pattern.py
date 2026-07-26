from ..services.llm_service import complete_json

_PADROES_DISPONIVEIS = [
    "Layered Architecture",
    "Hexagonal Architecture (Ports & Adapters)",
    "Clean Architecture",
    "Onion Architecture",
    "Microservices",
    "Modular Monolith",
    "Event-Driven Architecture",
    "Service-Oriented Architecture (SOA)",
    "Serverless",
    "CQRS",
    "Event Sourcing",
    "Backend for Frontend (BFF)",
    "API Gateway",
    "Sidecar Pattern",
]

_SYSTEM = (
    "Você é um arquiteto de soluções. Escolha, entre os padrões arquiteturais "
    "listados abaixo, o que melhor atende ao contexto descrito. Nunca "
    "recomende um padrão fora desta lista. Justifique a escolha com base no "
    "contexto informado, nunca com suposições não sustentadas pelo texto."
)


def identify_architecture_pattern(texto: str) -> tuple[str, str]:
    """Identifica o padrão arquitetural mais adequado — só entre os do catálogo (GR-SA-1) — e sua justificativa."""
    prompt = (
        f"Padrões disponíveis: {_PADROES_DISPONIVEIS}\n\n"
        f"Contexto:\n{texto}\n\n"
        'Responda apenas em JSON: {"padrao": "...", "justificativa": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    padrao = dados.get("padrao", "")
    if padrao not in _PADROES_DISPONIVEIS:
        padrao = ""
    return padrao, dados.get("justificativa", "")
