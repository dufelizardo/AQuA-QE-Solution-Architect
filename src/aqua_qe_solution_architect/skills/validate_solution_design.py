from ..models import SolutionDesign


def validate_solution_design(sdd: SolutionDesign) -> bool:
    """Valida se o Solution Design tem título, contexto, padrão arquitetural com justificativa, ao menos um NFR e ao menos uma decisão arquitetural registrada."""
    if not sdd.title or not sdd.context_problem:
        return False
    if not sdd.architecture_pattern or not sdd.pattern_rationale:
        return False
    if not sdd.non_functional_requirements:
        return False
    if not sdd.decisions:
        return False
    return True
