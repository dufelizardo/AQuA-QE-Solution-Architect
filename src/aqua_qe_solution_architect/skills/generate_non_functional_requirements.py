from ..models import CATEGORIAS_NFR, NonFunctionalRequirement
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica requisitos não funcionais (NFRs) presentes ou "
    "claramente implícitos em um texto de requisitos, categorizando cada um "
    "conforme ISO/IEC 25010. Categorias válidas, com suas definições "
    "(nunca confunda uma categoria com outra):\n"
    "- performance: tempo de resposta, throughput, uso de recursos (CPU, "
    "memória, rede) sob carga esperada.\n"
    "- escalabilidade: capacidade de crescer em carga/volume de dados sem "
    "degradar as demais características.\n"
    "- seguranca: confidencialidade, integridade, não-repúdio, "
    "accountability e autenticidade — inclui conformidade legal/regulatória "
    "sobre proteção de dados (ex.: LGPD), que é sempre segurança, nunca "
    "observabilidade.\n"
    "- disponibilidade: maturidade, tolerância a falhas, capacidade de "
    "recuperação (recoverability).\n"
    "- observabilidade: capacidade de inspecionar o comportamento do "
    "sistema em produção — logs, métricas, rastreamento/tracing. Não é "
    "sobre conformidade legal nem sobre proteção de dados.\n"
    "- manutenibilidade: modularidade, reusabilidade, capacidade de ser "
    "analisado, modificado e testado sem introduzir defeitos.\n"
    "Cada NFR deve ter uma justificativa (rationale) rastreável a uma "
    "necessidade de negócio ou restrição técnica presente no texto — nunca "
    "invente um NFR genérico sem essa rastreabilidade. Quando o texto "
    "sustentar, quantifique o requisito (ex.: tempo de resposta em "
    "segundos, % de disponibilidade, RPO/RTO) — nunca invente uma métrica "
    "não sustentada pelo texto."
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
