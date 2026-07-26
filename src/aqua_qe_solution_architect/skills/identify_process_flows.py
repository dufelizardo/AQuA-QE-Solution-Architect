from ..models import ProcessFlow
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica os principais fluxos de processo (ex.: fluxo de "
    "agendamento) a partir de um texto de requisitos, com os passos de "
    "cada fluxo em ordem. Um fluxo e seus passos só existem se "
    "evidenciados ou claramente inferíveis do texto — nunca invente um "
    "fluxo ou passo não sustentado por ele. Se não houver fluxos "
    "identificáveis, responda com uma lista vazia."
)


def identify_process_flows(texto: str) -> list[ProcessFlow]:
    """Identifica os principais fluxos de processo e seus passos (GR-SA-1: nunca inventar fluxo/passo sem lastro no texto)."""
    prompt = (
        f"Texto:\n{texto}\n\n"
        'Responda apenas em JSON: {"fluxos": [{"nome": "...", '
        '"passos": ["..."], "trecho_fonte": "..."}]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return [
        ProcessFlow(
            name=item.get("nome", ""),
            steps=item.get("passos", []),
            source_reference=item.get("trecho_fonte", ""),
        )
        for item in dados.get("fluxos", [])
    ]
