from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica componentes de alto nível e integrações com sistemas "
    "externos mencionados ou claramente inferíveis a partir de um texto de "
    "requisitos. Nunca assuma uma integração que não tenha evidência no "
    "texto — se não houver integrações claras, responda com uma lista "
    "vazia."
)


def identify_components_and_integrations(texto: str) -> tuple[list[str], list[str]]:
    """Identifica componentes de alto nível e integrações citadas/inferíveis no texto (GR-SA-2: nunca assumir integração sem evidência documental)."""
    prompt = (
        f"Texto:\n{texto}\n\n"
        'Responda apenas em JSON: {"componentes": ["..."], "integracoes": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return dados.get("componentes", []), dados.get("integracoes", [])
