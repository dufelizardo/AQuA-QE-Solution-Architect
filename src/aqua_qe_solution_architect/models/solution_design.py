from dataclasses import dataclass, field

from .architecture_decision import ArchitectureDecision
from .non_functional_requirement import NonFunctionalRequirement
from .status import ArtifactStatus


@dataclass
class SolutionDesign:
    """Solution Design Document (SDD), conforme docs/agent/output_schema.md."""

    id: str
    title: str
    context_problem: str
    architecture_pattern: str
    pattern_rationale: str
    components: list[str] = field(default_factory=list)
    integrations: list[str] = field(default_factory=list)
    non_functional_requirements: list[NonFunctionalRequirement] = field(default_factory=list)
    technical_risks: list[str] = field(default_factory=list)
    decisions: list[ArchitectureDecision] = field(default_factory=list)
    source_reference: str = ""
    status: ArtifactStatus = ArtifactStatus.PENDING_CLARIFICATION
    review_notes: list[str] = field(default_factory=list)
