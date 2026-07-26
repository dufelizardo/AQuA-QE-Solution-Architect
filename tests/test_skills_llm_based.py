from aqua_qe_solution_architect.models import ArchitectureDecision, NonFunctionalRequirement, SolutionDesign
from aqua_qe_solution_architect.skills import extract_solution_context as extract_solution_context_module
from aqua_qe_solution_architect.skills import (
    generate_architecture_decisions as generate_architecture_decisions_module,
)
from aqua_qe_solution_architect.skills import (
    generate_non_functional_requirements as generate_non_functional_requirements_module,
)
from aqua_qe_solution_architect.skills import (
    generate_sdd_clarifying_questions as generate_sdd_clarifying_questions_module,
)
from aqua_qe_solution_architect.skills import (
    identify_architecture_pattern as identify_architecture_pattern_module,
)
from aqua_qe_solution_architect.skills import (
    identify_components_and_integrations as identify_components_and_integrations_module,
)
from aqua_qe_solution_architect.skills import identify_technical_risks as identify_technical_risks_module
from aqua_qe_solution_architect.skills import refine_solution_design as refine_solution_design_module
from aqua_qe_solution_architect.skills import review_solution_design as review_solution_design_module


def _sdd(**overrides) -> SolutionDesign:
    base = {
        "id": "SDD-001",
        "title": "titulo",
        "context_problem": "contexto",
        "architecture_pattern": "Microservices",
        "pattern_rationale": "justificativa",
        "source_reference": "fonte",
    }
    base.update(overrides)
    return SolutionDesign(**base)


def test_extract_solution_context_maps_json_to_fields(monkeypatch):
    monkeypatch.setattr(
        extract_solution_context_module,
        "complete_json",
        lambda prompt, system="", model=None: {"titulo": "Consulta de saldo", "contexto": "contexto extraido"},
    )

    titulo, contexto = extract_solution_context_module.extract_solution_context("texto")

    assert titulo == "Consulta de saldo"
    assert contexto == "contexto extraido"


def test_identify_architecture_pattern_returns_pattern_from_catalog(monkeypatch):
    monkeypatch.setattr(
        identify_architecture_pattern_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "padrao": "Microservices",
            "justificativa": "equipes autonomas e dominios bem definidos",
        },
    )

    padrao, justificativa = identify_architecture_pattern_module.identify_architecture_pattern("texto")

    assert padrao == "Microservices"
    assert justificativa == "equipes autonomas e dominios bem definidos"


def test_identify_architecture_pattern_rejects_pattern_outside_catalog(monkeypatch):
    """Regressão (GR-SA-1): nunca aceitar um padrão fora do catálogo, mesmo que o LLM alucine um."""
    monkeypatch.setattr(
        identify_architecture_pattern_module,
        "complete_json",
        lambda prompt, system="", model=None: {"padrao": "Padrao Inventado XYZ", "justificativa": "j"},
    )

    padrao, _ = identify_architecture_pattern_module.identify_architecture_pattern("texto")

    assert padrao == ""


def test_identify_components_and_integrations_maps_json_to_lists(monkeypatch):
    monkeypatch.setattr(
        identify_components_and_integrations_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "componentes": ["servico de saldo"],
            "integracoes": ["sistema legado de contas"],
        },
    )

    componentes, integracoes = (
        identify_components_and_integrations_module.identify_components_and_integrations("texto")
    )

    assert componentes == ["servico de saldo"]
    assert integracoes == ["sistema legado de contas"]


def test_identify_components_and_integrations_defaults_to_empty(monkeypatch):
    monkeypatch.setattr(
        identify_components_and_integrations_module,
        "complete_json",
        lambda prompt, system="", model=None: {},
    )

    componentes, integracoes = (
        identify_components_and_integrations_module.identify_components_and_integrations("texto")
    )

    assert componentes == []
    assert integracoes == []


def test_generate_non_functional_requirements_maps_json_to_models(monkeypatch):
    monkeypatch.setattr(
        generate_non_functional_requirements_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "requisitos": [
                {
                    "categoria": "performance",
                    "requisito": "responder em menos de 2s",
                    "rationale": "experiencia do usuario",
                    "trecho_fonte": "trecho 1",
                }
            ]
        },
    )

    resultado = generate_non_functional_requirements_module.generate_non_functional_requirements("texto")

    assert resultado == [
        NonFunctionalRequirement(
            category="performance",
            requirement="responder em menos de 2s",
            rationale="experiencia do usuario",
            source_reference="trecho 1",
        )
    ]


def test_generate_non_functional_requirements_rejects_invalid_category(monkeypatch):
    monkeypatch.setattr(
        generate_non_functional_requirements_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "requisitos": [
                {
                    "categoria": "categoria_invalida",
                    "requisito": "r",
                    "rationale": "r",
                    "trecho_fonte": "f",
                }
            ]
        },
    )

    resultado = generate_non_functional_requirements_module.generate_non_functional_requirements("texto")

    assert resultado[0].category == ""


def test_identify_technical_risks_maps_json_to_list(monkeypatch):
    monkeypatch.setattr(
        identify_technical_risks_module,
        "complete_json",
        lambda prompt, system="", model=None: {"riscos": ["dependencia de sistema legado instavel"]},
    )

    assert identify_technical_risks_module.identify_technical_risks("texto") == [
        "dependencia de sistema legado instavel"
    ]


def test_identify_technical_risks_returns_empty_when_none_found(monkeypatch):
    monkeypatch.setattr(
        identify_technical_risks_module, "complete_json", lambda prompt, system="", model=None: {"riscos": []}
    )

    assert identify_technical_risks_module.identify_technical_risks("texto") == []


def test_generate_architecture_decisions_maps_json_to_models(monkeypatch):
    monkeypatch.setattr(
        generate_architecture_decisions_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "decisoes": [
                {
                    "titulo": "Usar Event-Driven para integracao",
                    "contexto": "multiplos consumidores do mesmo evento",
                    "decisao": "usar Event-Driven Architecture",
                    "alternativas_consideradas": ["REST sincrono"],
                    "consequencias": "desacoplamento maior, consistencia eventual",
                    "trecho_fonte": "trecho 1",
                }
            ]
        },
    )

    resultado = generate_architecture_decisions_module.generate_architecture_decisions(
        "Event-Driven Architecture", "justificativa", ["servico a"], ["sistema b"], "texto"
    )

    assert resultado == [
        ArchitectureDecision(
            id="ADR-001",
            title="Usar Event-Driven para integracao",
            context="multiplos consumidores do mesmo evento",
            decision="usar Event-Driven Architecture",
            consequences="desacoplamento maior, consistencia eventual",
            source_reference="trecho 1",
            alternatives_considered=["REST sincrono"],
        )
    ]


def test_review_solution_design_uses_review_model_and_maps_result(monkeypatch):
    captured = {}

    def fake_complete_json(prompt, system="", model=None):
        captured["model"] = model
        return {"aprovado": True, "problemas": []}

    monkeypatch.setattr(review_solution_design_module, "complete_json", fake_complete_json)

    resultado = review_solution_design_module.review_solution_design(_sdd())

    assert resultado == {"aprovado": True, "problemas": []}
    assert captured["model"] == "phi4"


def test_generate_sdd_clarifying_questions_returns_empty_without_review_notes():
    assert (
        generate_sdd_clarifying_questions_module.generate_sdd_clarifying_questions(_sdd()) == []
    )


def test_generate_sdd_clarifying_questions_maps_json_to_list(monkeypatch):
    monkeypatch.setattr(
        generate_sdd_clarifying_questions_module,
        "complete_json",
        lambda prompt, system="", model=None: {"perguntas": ["Qual o volume esperado de requisicoes?"]},
    )

    sdd = _sdd(review_notes=["NFR de performance sem numero especifico"])
    perguntas = generate_sdd_clarifying_questions_module.generate_sdd_clarifying_questions(sdd)

    assert perguntas == ["Qual o volume esperado de requisicoes?"]


def test_refine_solution_design_rewrites_fields_from_answers(monkeypatch):
    monkeypatch.setattr(
        refine_solution_design_module,
        "complete_json",
        lambda prompt, system="", model=None: {
            "titulo": "titulo refinado",
            "contexto": "contexto",
            "padrao_arquitetural": "Microservices",
            "justificativa": "justificativa",
            "componentes": ["c1"],
            "integracoes": ["i1"],
            "nfrs": [
                {"categoria": "performance", "requisito": "r", "rationale": "ra"}
            ],
            "riscos": ["risco 1"],
            "decisoes": [
                {
                    "titulo": "d1",
                    "contexto": "c",
                    "decisao": "d",
                    "alternativas_consideradas": [],
                    "consequencias": "co",
                }
            ],
        },
    )

    sdd = _sdd(title="titulo antigo")
    resultado = refine_solution_design_module.refine_solution_design(
        sdd, [{"pergunta": "qual o titulo?", "resposta": "titulo refinado"}]
    )

    assert resultado.title == "titulo refinado"
    assert resultado.non_functional_requirements[0].category == "performance"
    assert resultado.decisions[0].id == "ADR-001"
