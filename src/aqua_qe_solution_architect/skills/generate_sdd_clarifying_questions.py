from ..models import SolutionDesign
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você transforma apontamentos de um revisor de arquitetura em perguntas "
    "diretas e acionáveis para quem propôs a solução responder."
)


def generate_sdd_clarifying_questions(sdd: SolutionDesign) -> list[str]:
    """Transforma os review_notes do Solution Design em perguntas diretas e acionáveis."""
    if not sdd.review_notes:
        return []
    prompt = (
        f"Apontamentos do revisor:\n{sdd.review_notes}\n\n"
        'Responda apenas em JSON: {"perguntas": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return dados.get("perguntas", [])
