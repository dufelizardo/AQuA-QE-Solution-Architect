import os

from ..models import SolutionDesign
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você é um revisor crítico de Solution Design Documents, independente de "
    "quem os gerou. Avalie se o padrão arquitetural escolhido é coerente com "
    "o contexto e os componentes/integrações identificados, se os requisitos "
    "não funcionais são específicos e rastreáveis (não genéricos), se os "
    "riscos técnicos relevantes foram cobertos, e se as decisões "
    "arquiteturais têm alternativas e consequências explícitas quando "
    "cabível. Aponte problemas reais; nunca aprove uma solução com "
    "justificativa vaga ou trade-offs não explicitados."
)

_DEFAULT_REVIEW_MODEL = "phi4"


def review_solution_design(sdd: SolutionDesign) -> dict:
    """Revisa o Solution Design com um LLM diferente do gerador, avaliando coerência, rastreabilidade dos NFRs e explicitação de trade-offs."""
    modelo = os.getenv("OLLAMA_REVIEW_MODEL", _DEFAULT_REVIEW_MODEL)
    nfrs = [
        {"categoria": n.category, "requisito": n.requirement, "rationale": n.rationale}
        for n in sdd.non_functional_requirements
    ]
    decisoes = [
        {"titulo": d.title, "decisao": d.decision, "alternativas": d.alternatives_considered}
        for d in sdd.decisions
    ]
    prompt = (
        f"Título: {sdd.title}\n"
        f"Contexto: {sdd.context_problem}\n"
        f"Padrão arquitetural: {sdd.architecture_pattern}\n"
        f"Justificativa: {sdd.pattern_rationale}\n"
        f"Componentes: {sdd.components}\n"
        f"Integrações: {sdd.integrations}\n"
        f"Requisitos não funcionais: {nfrs}\n"
        f"Riscos técnicos: {sdd.technical_risks}\n"
        f"Decisões arquiteturais: {decisoes}\n\n"
        'Responda apenas em JSON: {"aprovado": true ou false, "problemas": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM, model=modelo)
    return {
        "aprovado": bool(dados.get("aprovado", False)),
        "problemas": dados.get("problemas", []),
    }
