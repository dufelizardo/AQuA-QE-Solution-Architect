from ..models import ArtifactStatus, SolutionDesign
from ..skills.extract_solution_context import extract_solution_context
from ..skills.generate_architecture_decisions import generate_architecture_decisions
from ..skills.generate_non_functional_requirements import generate_non_functional_requirements
from ..skills.identify_architecture_pattern import identify_architecture_pattern
from ..skills.identify_components_and_integrations import identify_components_and_integrations
from ..skills.identify_technical_risks import identify_technical_risks
from ..skills.review_solution_design import review_solution_design
from ..skills.validate_solution_design import validate_solution_design


def finalize_solution_design(sdd: SolutionDesign) -> SolutionDesign:
    """Aplica o checklist automático e a revisão por LLM, decidindo o status final do Solution Design."""
    if not validate_solution_design(sdd):
        sdd.status = ArtifactStatus.PENDING_CLARIFICATION
        return sdd

    revisao = review_solution_design(sdd)
    sdd.review_notes = revisao["problemas"]
    sdd.status = (
        ArtifactStatus.DRAFT_VALIDATED if revisao["aprovado"] else ArtifactStatus.PENDING_CLARIFICATION
    )
    return sdd


def generate_solution_design(texto: str) -> SolutionDesign:
    """Gera o Solution Design Document a partir de uma fonte de texto (PRD ou equivalente), orquestrando a sequência padrão de skills."""
    titulo, contexto = extract_solution_context(texto)
    padrao, justificativa = identify_architecture_pattern(texto)
    componentes, integracoes = identify_components_and_integrations(texto)
    nfrs = generate_non_functional_requirements(texto)
    riscos = identify_technical_risks(texto)
    decisoes = generate_architecture_decisions(padrao, justificativa, componentes, integracoes, texto)

    sdd = SolutionDesign(
        id="SDD-001",
        title=titulo,
        context_problem=contexto,
        architecture_pattern=padrao,
        pattern_rationale=justificativa,
        components=componentes,
        integrations=integracoes,
        non_functional_requirements=nfrs,
        technical_risks=riscos,
        decisions=decisoes,
        source_reference=texto,
    )
    return finalize_solution_design(sdd)
