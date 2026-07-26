from ..services.llm_service import complete_json

_SYSTEM = (
    "Você sugere integrações comuns para o domínio descrito em um texto de "
    "requisitos, mesmo quando não citadas explicitamente — ex.: um sistema "
    "de saúde pública brasileiro tipicamente considera integração com SUS/"
    "CNES/e-SUS, autenticação, notificação por SMS/e-mail. Estas são "
    "SUGESTÕES a confirmar com quem decide, nunca fatos: nunca afirme que "
    "uma integração candidata é necessária, decidida ou já confirmada — "
    "isso é papel exclusivo de 'integrações confirmadas' (evidenciadas no "
    "texto), não desta lista. Se o domínio não sugerir nenhuma integração "
    "adicional razoável, responda com uma lista vazia."
)


def identify_candidate_integrations(texto: str) -> list[str]:
    """Sugere integrações candidatas (por conhecimento de domínio, não por evidência textual) — sempre uma recomendação a confirmar, nunca um fato; distinto de identify_components_and_integrations (GR-SA-2)."""
    prompt = (
        f"Texto:\n{texto}\n\n"
        'Responda apenas em JSON: {"integracoes_candidatas": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return dados.get("integracoes_candidatas", [])
