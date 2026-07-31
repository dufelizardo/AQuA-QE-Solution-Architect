from ..models import SolutionDesign


def _lista_md(itens: list[str]) -> str:
    return "\n".join(f"- {item}" for item in itens) if itens else "(nenhum)"


def _dominio_md(sdd: SolutionDesign) -> str:
    if not sdd.domain_model:
        return "(nenhum)"
    linhas = []
    for entidade in sdd.domain_model:
        linhas += [
            f"### {entidade.name}",
            "",
            _lista_md(entidade.attributes),
            "",
        ]
    return "\n".join(linhas).rstrip()


def _fluxos_md(sdd: SolutionDesign) -> str:
    if not sdd.process_flows:
        return "(nenhum)"
    linhas = []
    for fluxo in sdd.process_flows:
        linhas.append(f"### {fluxo.name}")
        linhas.append("")
        linhas += [f"{i + 1}. {passo}" for i, passo in enumerate(fluxo.steps)]
        linhas.append("")
    return "\n".join(linhas).rstrip()


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


def _rastreabilidade_md(sdd: SolutionDesign) -> str:
    """Tabela de/para: cada artefato gerado, ligado ao trecho da fonte que o originou (GR-SA-1)."""
    linhas = ["| Artefato | Trecho de origem |", "|---|---|"]
    for entidade in sdd.domain_model:
        linhas.append(f"| Entidade de Domínio: {entidade.name} | {entidade.source_reference or '(não informado)'} |")
    for fluxo in sdd.process_flows:
        linhas.append(f"| Fluxo Principal: {fluxo.name} | {fluxo.source_reference or '(não informado)'} |")
    for nfr in sdd.non_functional_requirements:
        linhas.append(f"| NFR: {nfr.category} | {nfr.source_reference or '(não informado)'} |")
    for decisao in sdd.decisions:
        linhas.append(f"| {decisao.id}: {decisao.title} | {decisao.source_reference or '(não informado)'} |")
    if len(linhas) == 2:
        return "(nenhum artefato com trecho de origem individual registrado)"
    return "\n".join(linhas)


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
        f"## Modelo de Domínio\n\n{_dominio_md(sdd)}\n\n"
        f"## Integrações\n{_lista_md(sdd.integrations)}\n\n"
        f"## Integrações Candidatas (sugeridas, a confirmar)\n{_lista_md(sdd.candidate_integrations)}\n\n"
        f"## Fluxos Principais\n\n{_fluxos_md(sdd)}\n\n"
        f"## Requisitos Não Funcionais\n\n{_nfrs_md(sdd)}\n\n"
        f"## Riscos Técnicos\n{_lista_md(sdd.technical_risks)}\n\n"
        f"## Decisões Arquiteturais (ADRs)\n\n{_decisoes_md(sdd)}\n\n"
        f"## Rastreabilidade\n\n{_rastreabilidade_md(sdd)}\n"
    )
