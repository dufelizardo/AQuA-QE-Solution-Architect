from ..models import SolutionDesign


def _lista_md(itens: list[str]) -> str:
    return "\n".join(f"- {item}" for item in itens) if itens else "(nenhum)"


def _nfrs_md(sdd: SolutionDesign) -> str:
    if not sdd.non_functional_requirements:
        return "(nenhum)"
    linhas = []
    for nfr in sdd.non_functional_requirements:
        linhas += [
            f"### {nfr.category}",
            "",
            f"- Requisito: {nfr.requirement}",
            f"- Justificativa: {nfr.rationale}",
            "",
        ]
    return "\n".join(linhas).rstrip()


def _decisoes_md(sdd: SolutionDesign) -> str:
    if not sdd.decisions:
        return "(nenhum)"
    linhas = []
    for decisao in sdd.decisions:
        linhas += [
            f"### {decisao.id}: {decisao.title}",
            "",
            f"- Contexto: {decisao.context}",
            f"- Decisão: {decisao.decision}",
            f"- Alternativas consideradas: {_lista_md(decisao.alternatives_considered)}",
            f"- Consequências: {decisao.consequences}",
            "",
        ]
    return "\n".join(linhas).rstrip()


def format_solution_design_markdown(sdd: SolutionDesign) -> str:
    """Formata o Solution Design Document em Markdown."""
    return (
        f"# {sdd.title or sdd.id}\n\n"
        f"**ID**: {sdd.id}\n"
        f"**Status**: {sdd.status.value}\n\n"
        f"## Contexto e Problema\n{sdd.context_problem}\n\n"
        f"## Padrão Arquitetural\n{sdd.architecture_pattern}\n\n"
        f"## Justificativa\n{sdd.pattern_rationale}\n\n"
        f"## Componentes\n{_lista_md(sdd.components)}\n\n"
        f"## Integrações\n{_lista_md(sdd.integrations)}\n\n"
        f"## Requisitos Não Funcionais\n\n{_nfrs_md(sdd)}\n\n"
        f"## Riscos Técnicos\n{_lista_md(sdd.technical_risks)}\n\n"
        f"## Decisões Arquiteturais (ADRs)\n\n{_decisoes_md(sdd)}\n\n"
        f"## Rastreabilidade\n\n> {sdd.source_reference}\n"
    )
