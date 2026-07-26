from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica riscos técnicos presentes ou claramente implícitos em "
    "um texto de requisitos (ex.: dependência de sistema legado instável, "
    "requisito de escala não comprovada, integração com terceiros sem SLA "
    "claro). Nunca omita um risco identificável; nunca invente um risco sem "
    "lastro no texto."
)


def identify_technical_risks(texto: str) -> list[str]:
    """Identifica riscos técnicos citados/inferíveis no texto — nunca omite um risco identificável (GR-SA-7)."""
    prompt = f"Texto:\n{texto}\n\n" + 'Responda apenas em JSON: {"riscos": ["..."]}'
    dados = complete_json(prompt, system=_SYSTEM)
    return dados.get("riscos", [])
