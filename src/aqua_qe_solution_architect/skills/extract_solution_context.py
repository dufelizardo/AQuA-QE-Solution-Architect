from ..services.llm_service import complete_json

_SYSTEM = (
    "Você extrai um título curto e um resumo do problema/contexto de "
    "negócio a partir de um texto de requisitos (ex.: um PRD). Baseie-se "
    "apenas no texto informado; nunca invente contexto que não esteja lá."
)


def extract_solution_context(texto: str) -> tuple[str, str]:
    """Extrai um título curto e o resumo do contexto/problema de negócio a partir do texto de entrada."""
    prompt = f"Texto:\n{texto}\n\n" + 'Responda apenas em JSON: {"titulo": "...", "contexto": "..."}'
    dados = complete_json(prompt, system=_SYSTEM)
    return dados.get("titulo", ""), dados.get("contexto", "")
