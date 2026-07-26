from ..models import CATEGORIAS_NFR, NonFunctionalRequirement
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica requisitos não funcionais (NFRs) presentes ou "
    "claramente implícitos em um texto de requisitos, categorizando cada um "
    "conforme ISO/IEC 25010. Categorias válidas: performance, "
    "escalabilidade, seguranca, disponibilidade, observabilidade, "
    "manutenibilidade. Cada NFR deve ter uma justificativa (rationale) "
    "rastreável a uma necessidade de negócio ou restrição técnica presente "
    "no texto — nunca invente um NFR genérico sem essa rastreabilidade."
)


def generate_non_functional_requirements(texto: str) -> list[NonFunctionalRequirement]:
    """Identifica NFRs categorizados conforme ISO/IEC 25010, cada um rastreável a uma necessidade de negócio (GR-SA-6)."""
    prompt = (
        f"Texto:\n{texto}\n\n"
        'Responda apenas em JSON: {"requisitos": [{"categoria": "...", '
        '"requisito": "...", "rationale": "...", "trecho_fonte": "..."}]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return [
        NonFunctionalRequirement(
            category=item.get("categoria", "") if item.get("categoria") in CATEGORIAS_NFR else "",
            requirement=item.get("requisito", ""),
            rationale=item.get("rationale", ""),
            source_reference=item.get("trecho_fonte", ""),
        )
        for item in dados.get("requisitos", [])
    ]
