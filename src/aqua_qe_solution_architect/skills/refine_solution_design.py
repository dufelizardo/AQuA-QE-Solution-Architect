from ..models import ArchitectureDecision, NonFunctionalRequirement, SolutionDesign
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você refina um Solution Design existente com base nas respostas que "
    "quem propôs a solução deu às perguntas de esclarecimento levantadas "
    "por um revisor. Baseie-se apenas no Solution Design atual e nas "
    "respostas fornecidas; nunca invente padrão arquitetural, integração, "
    "NFR, risco ou decisão que não tenha sido informado neles. Nunca remova "
    "ou resuma um detalhe que já existe em um campo atual, a menos que uma "
    "resposta contradiga esse detalhe especificamente — preserve o texto "
    "existente nos campos que as respostas não abordam. Responda sempre em "
    "português."
)


def refine_solution_design(sdd: SolutionDesign, respostas: list[dict]) -> SolutionDesign:
    """Reescreve os campos do Solution Design usando as respostas do usuário às perguntas de esclarecimento."""
    nfrs_atuais = [
        {"categoria": n.category, "requisito": n.requirement, "rationale": n.rationale}
        for n in sdd.non_functional_requirements
    ]
    decisoes_atuais = [
        {
            "titulo": d.title,
            "contexto": d.context,
            "decisao": d.decision,
            "alternativas_consideradas": d.alternatives_considered,
            "consequencias": d.consequences,
        }
        for d in sdd.decisions
    ]
    perguntas_respostas = [f"P: {item['pergunta']}\nR: {item['resposta']}" for item in respostas]

    prompt = (
        f"Título atual: {sdd.title}\n"
        f"Contexto atual: {sdd.context_problem}\n"
        f"Padrão arquitetural atual: {sdd.architecture_pattern}\n"
        f"Justificativa atual: {sdd.pattern_rationale}\n"
        f"Componentes atuais: {sdd.components}\n"
        f"Integrações atuais: {sdd.integrations}\n"
        f"NFRs atuais: {nfrs_atuais}\n"
        f"Riscos técnicos atuais: {sdd.technical_risks}\n"
        f"Decisões atuais: {decisoes_atuais}\n\n"
        "Respostas às perguntas de esclarecimento:\n"
        + "\n".join(perguntas_respostas)
        + "\n\nReescreva os campos incorporando essas respostas, resolvendo "
        "as lacunas apontadas. Campos (ou itens de lista) que não têm "
        "relação com nenhuma das respostas acima devem manter o texto "
        "atual, com o mesmo nível de detalhe — nunca simplifique um item "
        "para menos palavras do que já tinha.\n\n"
        'Responda apenas em JSON: {"titulo": "...", "contexto": "...", '
        '"padrao_arquitetural": "...", "justificativa": "...", '
        '"componentes": ["..."], "integracoes": ["..."], "nfrs": '
        '[{"categoria": "...", "requisito": "...", "rationale": "..."}], '
        '"riscos": ["..."], "decisoes": [{"titulo": "...", "contexto": '
        '"...", "decisao": "...", "alternativas_consideradas": ["..."], '
        '"consequencias": "..."}]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)

    sdd.title = dados.get("titulo") or sdd.title
    sdd.context_problem = dados.get("contexto") or sdd.context_problem
    sdd.architecture_pattern = dados.get("padrao_arquitetural") or sdd.architecture_pattern
    sdd.pattern_rationale = dados.get("justificativa") or sdd.pattern_rationale
    sdd.components = dados.get("componentes") or sdd.components
    sdd.integrations = dados.get("integracoes") or sdd.integrations
    sdd.technical_risks = dados.get("riscos") or sdd.technical_risks

    novos_nfrs = [
        NonFunctionalRequirement(
            category=item.get("categoria", ""),
            requirement=item.get("requisito", ""),
            rationale=item.get("rationale", ""),
            source_reference=sdd.source_reference,
        )
        for item in dados.get("nfrs", [])
    ]
    sdd.non_functional_requirements = novos_nfrs or sdd.non_functional_requirements

    novas_decisoes = [
        ArchitectureDecision(
            id=f"ADR-{i + 1:03d}",
            title=item.get("titulo", ""),
            context=item.get("contexto", ""),
            decision=item.get("decisao", ""),
            alternatives_considered=item.get("alternativas_consideradas", []),
            consequences=item.get("consequencias", ""),
            source_reference=sdd.source_reference,
        )
        for i, item in enumerate(dados.get("decisoes", []))
    ]
    sdd.decisions = novas_decisoes or sdd.decisions

    return sdd
