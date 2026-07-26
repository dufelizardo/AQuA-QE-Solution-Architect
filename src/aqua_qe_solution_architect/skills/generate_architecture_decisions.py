from ..models import ArchitectureDecision
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você registra decisões arquiteturais relevantes como Architecture "
    "Decision Records (ADR), a partir do padrão arquitetural escolhido, dos "
    "componentes/integrações identificados e do contexto informado. Toda "
    "decisão relevante precisa de um ADR. Sempre que houver mais de uma "
    "alternativa viável, liste-as em 'alternativas_consideradas' — nunca "
    "apresente a decisão como se fosse a única opção possível quando não "
    "for o caso."
)


def generate_architecture_decisions(
    padrao: str,
    justificativa_padrao: str,
    componentes: list[str],
    integracoes: list[str],
    texto: str,
) -> list[ArchitectureDecision]:
    """Gera os ADRs da solução — toda decisão relevante precisa de um (GR-SA-3), com alternativas explícitas quando houver mais de uma opção viável (GR-SA-4)."""
    prompt = (
        f"Padrão arquitetural escolhido: {padrao}\n"
        f"Justificativa: {justificativa_padrao}\n"
        f"Componentes: {componentes}\n"
        f"Integrações: {integracoes}\n\n"
        f"Contexto:\n{texto}\n\n"
        'Responda apenas em JSON: {"decisoes": [{"titulo": "...", '
        '"contexto": "...", "decisao": "...", "alternativas_consideradas": '
        '["..."], "consequencias": "...", "trecho_fonte": "..."}]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return [
        ArchitectureDecision(
            id=f"ADR-{i + 1:03d}",
            title=item.get("titulo", ""),
            context=item.get("contexto", ""),
            decision=item.get("decisao", ""),
            alternatives_considered=item.get("alternativas_consideradas", []),
            consequences=item.get("consequencias", ""),
            source_reference=item.get("trecho_fonte", ""),
        )
        for i, item in enumerate(dados.get("decisoes", []))
    ]
