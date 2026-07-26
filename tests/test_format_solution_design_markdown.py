from aqua_qe_solution_architect.models import ArchitectureDecision, NonFunctionalRequirement, SolutionDesign
from aqua_qe_solution_architect.skills.format_solution_design_markdown import format_solution_design_markdown


def test_format_solution_design_markdown_includes_all_fields():
    sdd = SolutionDesign(
        id="SDD-001",
        title="Consulta de Saldo",
        context_problem="Clientes precisam consultar saldo pelo app",
        architecture_pattern="Microservices",
        pattern_rationale="Equipes autonomas, dominios bem definidos",
        components=["servico de saldo"],
        integrations=["sistema legado de contas"],
        non_functional_requirements=[
            NonFunctionalRequirement(
                category="performance",
                requirement="responder em menos de 2s",
                rationale="experiencia do usuario",
                source_reference="trecho 1",
            )
        ],
        technical_risks=["indisponibilidade do sistema legado"],
        decisions=[
            ArchitectureDecision(
                id="ADR-001",
                title="Usar Microservices",
                context="multiplas equipes",
                decision="adotar Microservices",
                alternatives_considered=["Modular Monolith"],
                consequences="maior complexidade operacional",
                source_reference="trecho 1",
            )
        ],
        source_reference="texto fonte completo",
    )

    resultado = format_solution_design_markdown(sdd)

    assert "# Consulta de Saldo" in resultado
    assert "**ID**: SDD-001" in resultado
    assert "**Status**: pending_clarification" in resultado
    assert "Clientes precisam consultar saldo pelo app" in resultado
    assert "## Padrão Arquitetural\nMicroservices" in resultado
    assert "- servico de saldo" in resultado
    assert "- sistema legado de contas" in resultado
    assert "### performance" in resultado
    assert "Requisito: responder em menos de 2s" in resultado
    assert "- indisponibilidade do sistema legado" in resultado
    assert "### ADR-001: Usar Microservices" in resultado
    assert "Alternativas consideradas: - Modular Monolith" in resultado
    assert "> texto fonte completo" in resultado


def test_format_solution_design_markdown_omits_empty_sections_gracefully():
    sdd = SolutionDesign(
        id="SDD-002",
        title="t",
        context_problem="c",
        architecture_pattern="Modular Monolith",
        pattern_rationale="r",
    )

    resultado = format_solution_design_markdown(sdd)

    assert "## Componentes\n(nenhum)" in resultado
    assert "## Requisitos Não Funcionais\n\n(nenhum)" in resultado
    assert "## Decisões Arquiteturais (ADRs)\n\n(nenhum)" in resultado
