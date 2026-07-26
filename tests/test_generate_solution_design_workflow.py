from aqua_qe_solution_architect.models import (
    ArchitectureDecision,
    ArtifactStatus,
    NonFunctionalRequirement,
    SolutionDesign,
)
from aqua_qe_solution_architect.workflow import generate_solution_design as workflow_module


def _stub_geracao(monkeypatch, com_nfr=True, com_decisao=True):
    monkeypatch.setattr(
        workflow_module, "extract_solution_context", lambda texto: ("titulo", "contexto")
    )
    monkeypatch.setattr(
        workflow_module,
        "identify_architecture_pattern",
        lambda texto: ("Microservices", "justificativa"),
    )
    monkeypatch.setattr(
        workflow_module,
        "identify_components_and_integrations",
        lambda texto: (["componente"], ["integracao"]),
    )
    monkeypatch.setattr(
        workflow_module,
        "generate_non_functional_requirements",
        lambda texto: (
            [NonFunctionalRequirement(category="performance", requirement="r", rationale="ra", source_reference="f")]
            if com_nfr
            else []
        ),
    )
    monkeypatch.setattr(workflow_module, "identify_technical_risks", lambda texto: ["risco"])
    monkeypatch.setattr(
        workflow_module,
        "generate_architecture_decisions",
        lambda padrao, justificativa, componentes, integracoes, texto: (
            [
                ArchitectureDecision(
                    id="ADR-001", title="t", context="c", decision="d", consequences="co", source_reference="f"
                )
            ]
            if com_decisao
            else []
        ),
    )


def test_generate_solution_design_happy_path_marks_draft_validated_when_review_approves(monkeypatch):
    _stub_geracao(monkeypatch)
    monkeypatch.setattr(
        workflow_module, "review_solution_design", lambda sdd: {"aprovado": True, "problemas": []}
    )

    sdd = workflow_module.generate_solution_design("texto de entrada")

    assert sdd.status == ArtifactStatus.DRAFT_VALIDATED
    assert sdd.title == "titulo"
    assert sdd.architecture_pattern == "Microservices"
    assert sdd.components == ["componente"]
    assert sdd.review_notes == []


def test_generate_solution_design_review_rejection_marks_pending_clarification(monkeypatch):
    _stub_geracao(monkeypatch)
    monkeypatch.setattr(
        workflow_module,
        "review_solution_design",
        lambda sdd: {"aprovado": False, "problemas": ["justificativa vaga"]},
    )

    sdd = workflow_module.generate_solution_design("texto de entrada")

    assert sdd.status == ArtifactStatus.PENDING_CLARIFICATION
    assert sdd.review_notes == ["justificativa vaga"]


def test_generate_solution_design_validate_failure_skips_review(monkeypatch):
    """Sem NFR nem decisão, validate_solution_design reprova antes de chamar o revisor (custo de LLM evitado)."""
    _stub_geracao(monkeypatch, com_nfr=False, com_decisao=False)
    chamou_review = {"valor": False}

    def fake_review(sdd):
        chamou_review["valor"] = True
        return {"aprovado": True, "problemas": []}

    monkeypatch.setattr(workflow_module, "review_solution_design", fake_review)

    sdd = workflow_module.generate_solution_design("texto de entrada")

    assert sdd.status == ArtifactStatus.PENDING_CLARIFICATION
    assert chamou_review["valor"] is False


def _sdd_completo() -> SolutionDesign:
    return SolutionDesign(
        id="SDD-001",
        title="t",
        context_problem="c",
        architecture_pattern="Microservices",
        pattern_rationale="j",
        non_functional_requirements=[
            NonFunctionalRequirement(category="performance", requirement="r", rationale="ra", source_reference="f")
        ],
        decisions=[
            ArchitectureDecision(id="ADR-001", title="t", context="c", decision="d", consequences="co", source_reference="f")
        ],
    )


def test_finalize_solution_design_marca_pending_clarification_quando_validate_falha(monkeypatch):
    monkeypatch.setattr(workflow_module, "validate_solution_design", lambda sdd: False)

    sdd = SolutionDesign(id="SDD-001", title="", context_problem="", architecture_pattern="", pattern_rationale="")
    resultado = workflow_module.finalize_solution_design(sdd)

    assert resultado.status == ArtifactStatus.PENDING_CLARIFICATION


def test_finalize_solution_design_marca_draft_validated_quando_tudo_aprova(monkeypatch):
    monkeypatch.setattr(workflow_module, "validate_solution_design", lambda sdd: True)
    monkeypatch.setattr(
        workflow_module, "review_solution_design", lambda sdd: {"aprovado": True, "problemas": []}
    )

    resultado = workflow_module.finalize_solution_design(_sdd_completo())

    assert resultado.status == ArtifactStatus.DRAFT_VALIDATED


def test_refine_and_finalize_solution_design_revalida_e_revisa_apos_o_refino(monkeypatch):
    """Regressão: refinar sem revalidar deixava status/review_notes obsoletos para sempre (bug real, não escopo adiado)."""
    sdd = SolutionDesign(
        id="SDD-001",
        title="t",
        context_problem="c",
        architecture_pattern="",
        pattern_rationale="",
        review_notes=["padrão arquitetural ausente"],
    )
    monkeypatch.setattr(
        workflow_module,
        "_refinar_campos",
        lambda sdd, respostas: SolutionDesign(
            id="SDD-001",
            title="t",
            context_problem="c",
            architecture_pattern="Microservices",
            pattern_rationale="j",
            non_functional_requirements=[
                NonFunctionalRequirement(
                    category="performance", requirement="r", rationale="ra", source_reference="f"
                )
            ],
            decisions=[
                ArchitectureDecision(
                    id="ADR-001", title="t", context="c", decision="d", consequences="co", source_reference="f"
                )
            ],
        ),
    )
    monkeypatch.setattr(workflow_module, "validate_solution_design", lambda sdd: True)
    monkeypatch.setattr(
        workflow_module, "review_solution_design", lambda sdd: {"aprovado": True, "problemas": []}
    )

    resultado = workflow_module.refine_and_finalize_solution_design(sdd, [{"pergunta": "p", "resposta": "r"}])

    assert resultado.status == ArtifactStatus.DRAFT_VALIDATED
    assert resultado.review_notes == []
