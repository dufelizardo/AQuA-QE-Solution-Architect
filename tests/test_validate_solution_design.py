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
    assert validate_solution_design(_sdd_completo()) == []


def test_missing_title_fails():
    assert "título ausente" in validate_solution_design(_sdd_completo(title=""))


def test_missing_context_fails():
    assert "contexto do problema ausente" in validate_solution_design(_sdd_completo(context_problem=""))


def test_missing_pattern_fails():
    assert "padrão arquitetural ausente" in validate_solution_design(_sdd_completo(architecture_pattern=""))


def test_missing_pattern_rationale_fails():
    motivos = validate_solution_design(_sdd_completo(pattern_rationale=""))
    assert "justificativa do padrão arquitetural ausente" in motivos


def test_no_nfrs_fails():
    motivos = validate_solution_design(_sdd_completo(non_functional_requirements=[]))
    assert "nenhum requisito não funcional identificado" in motivos


def test_no_decisions_fails():
    motivos = validate_solution_design(_sdd_completo(decisions=[]))
    assert "nenhuma decisão arquitetural (ADR) registrada" in motivos


def test_multiplos_motivos_acumulam_em_vez_de_parar_no_primeiro():
    motivos = validate_solution_design(_sdd_completo(title="", decisions=[]))
    assert "título ausente" in motivos
    assert "nenhuma decisão arquitetural (ADR) registrada" in motivos
