from ..models import SolutionDesign


def validate_solution_design(sdd: SolutionDesign) -> list[str]:
    """Valida o Solution Design e retorna os motivos de reprovação (lista vazia = aprovado no checklist)."""
    motivos = []
    if not sdd.title:
        motivos.append("título ausente")
    if not sdd.context_problem:
        motivos.append("contexto do problema ausente")
    if not sdd.architecture_pattern:
        motivos.append("padrão arquitetural ausente")
    if not sdd.pattern_rationale:
        motivos.append("justificativa do padrão arquitetural ausente")
    if not sdd.non_functional_requirements:
        motivos.append("nenhum requisito não funcional identificado")
    if not sdd.decisions:
        motivos.append("nenhuma decisão arquitetural (ADR) registrada")
    return motivos
