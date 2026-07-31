from aqua_qe_solution_architect.models import (
    ArchitectureDecision,
    DomainEntity,
    NonFunctionalRequirement,
    ProcessFlow,
    SolutionDesign,
)
from aqua_qe_solution_architect.skills.format_solution_design_markdown import format_solution_design_markdown


def test_format_solution_design_markdown_includes_all_fields():
    sdd = SolutionDesign(
        id="SDD-001",
        title="Consulta de Saldo",
        context_problem="Clientes precisam consultar saldo pelo app",
        architecture_pattern="Microservices",
        pattern_rationale="Equipes autonomas, dominios bem definidos",
        components=["servico de saldo"],
        domain_model=[
            DomainEntity(name="Conta", attributes=["numero", "saldo"], source_reference="trecho 1")
        ],
        integrations=["sistema legado de contas"],
        candidate_integrations=["sistema de notificacao"],
        process_flows=[
            ProcessFlow(
                name="Consulta de saldo",
                steps=["autenticar", "buscar saldo", "exibir resultado"],
                source_reference="trecho 1",
            )
        ],
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
    assert "### Conta" in resultado
    assert "- numero" in resultado
    assert "- saldo" in resultado
    assert "- sistema legado de contas" in resultado
    assert "## Integrações Candidatas (sugeridas, a confirmar)\n- sistema de notificacao" in resultado
    assert "### Consulta de saldo" in resultado
    assert "1. autenticar" in resultado
    assert "2. buscar saldo" in resultado
    assert "3. exibir resultado" in resultado
    assert "### performance" in resultado
    assert "Requisito: responder em menos de 2s" in resultado
    assert "- indisponibilidade do sistema legado" in resultado
    assert "### ADR-001: Usar Microservices" in resultado
    assert "Alternativas consideradas: - Modular Monolith" in resultado
    assert "| Entidade de Domínio: Conta | trecho 1 |" in resultado
    assert "| Fluxo Principal: Consulta de saldo | trecho 1 |" in resultado
    assert "| NFR: performance | trecho 1 |" in resultado
    assert "| ADR-001: Usar Microservices | trecho 1 |" in resultado


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
    assert "## Modelo de Domínio\n\n(nenhum)" in resultado
    assert "## Integrações Candidatas (sugeridas, a confirmar)\n(nenhum)" in resultado
    assert "## Fluxos Principais\n\n(nenhum)" in resultado
    assert "## Requisitos Não Funcionais\n\n(nenhum)" in resultado
    assert "## Decisões Arquiteturais (ADRs)\n\n(nenhum)" in resultado
    assert "(nenhum artefato com trecho de origem individual registrado)" in resultado
