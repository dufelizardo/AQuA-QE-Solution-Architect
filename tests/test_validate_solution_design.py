from aqua_qe_solution_architect.models import ArchitectureDecision, NonFunctionalRequirement, SolutionDesign
from aqua_qe_solution_architect.skills.validate_solution_design import validate_solution_design


def _sdd_completo(**overrides) -> SolutionDesign:
    base = {
        "id": "SDD-001",
        "title": "titulo",
        "context_problem": "contexto",
        "architecture_pattern": "Microservices",
        "pattern_rationale": "justificativa",
        "non_functional_requirements": [
            NonFunctionalRequirement(
                category="performance", requirement="r", rationale="ra", source_reference="f"
            )
        ],
        "decisions": [
            ArchitectureDecision(
                id="ADR-001",
                title="t",
                context="c",
                decision="d",
                consequences="co",
                source_reference="f",
            )
        ],
    }
    base.update(overrides)
    return SolutionDesign(**base)


def test_valid_solution_design_passes():
    assert validate_solution_design(_sdd_completo()) is True


def test_missing_title_fails():
    assert validate_solution_design(_sdd_completo(title="")) is False


def test_missing_context_fails():
    assert validate_solution_design(_sdd_completo(context_problem="")) is False


def test_missing_pattern_fails():
    assert validate_solution_design(_sdd_completo(architecture_pattern="")) is False


def test_missing_pattern_rationale_fails():
    assert validate_solution_design(_sdd_completo(pattern_rationale="")) is False


def test_no_nfrs_fails():
    assert validate_solution_design(_sdd_completo(non_functional_requirements=[])) is False


def test_no_decisions_fails():
    assert validate_solution_design(_sdd_completo(decisions=[])) is False
