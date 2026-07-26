from ..models import SolutionDesign
from ..workflow.generate_solution_design import generate_solution_design


def handle_request(entrada: str) -> SolutionDesign:
    """Ponto de entrada único do agente — gera o Solution Design Document a partir da entrada recebida."""
    return generate_solution_design(entrada)
