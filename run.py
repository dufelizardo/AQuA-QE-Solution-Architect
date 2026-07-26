"""CLI simples para rodar o AQuA-QE Solution Architect sem precisar mexer em sys.path manualmente."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

_RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(_RAIZ / "src"))
load_dotenv(_RAIZ / ".env")

from aqua_qe_solution_architect.models import ArtifactStatus, SolutionDesign  # noqa: E402
from aqua_qe_solution_architect.orchestrator.solution_architect import handle_request  # noqa: E402
from aqua_qe_solution_architect.skills.format_chat_transcript import format_chat_transcript  # noqa: E402
from aqua_qe_solution_architect.skills.format_solution_design_markdown import (  # noqa: E402
    format_solution_design_markdown,
)
from aqua_qe_solution_architect.skills.generate_sdd_clarifying_questions import (  # noqa: E402
    generate_sdd_clarifying_questions,
)
from aqua_qe_solution_architect.skills.parse_chat_transcript import parse_chat_transcript  # noqa: E402
from aqua_qe_solution_architect.skills.read_confluence_page import read_confluence_page  # noqa: E402
from aqua_qe_solution_architect.skills.read_jira_issue import read_jira_issue  # noqa: E402
from aqua_qe_solution_architect.skills.read_text_file import read_text_file  # noqa: E402
from aqua_qe_solution_architect.skills.refine_solution_design import refine_solution_design  # noqa: E402


def _ler_entrada(args: argparse.Namespace) -> str:
    if args.arquivo:
        return read_text_file(args.arquivo)
    if args.jira:
        return read_jira_issue(args.jira)
    if args.confluence:
        return read_confluence_page(args.confluence)
    # chat (--texto): normaliza a transcrição (remetente por linha), quando houver;
    # texto corrido sem remetentes volta inalterado (ver parse_chat_transcript).
    return format_chat_transcript(parse_chat_transcript(args.texto))


def _imprimir_sdd(sdd: SolutionDesign) -> None:
    print(f"status: {sdd.status.value}")
    print(f"título: {sdd.title}")
    print(f"padrão arquitetural: {sdd.architecture_pattern}")
    print(f"justificativa: {sdd.pattern_rationale}")
    print(f"componentes: {sdd.components}")
    print(f"integrações: {sdd.integrations}")
    print(f"NFRs: {len(sdd.non_functional_requirements)}")
    print(f"riscos técnicos: {sdd.technical_risks}")
    print(f"decisões arquiteturais (ADRs): {len(sdd.decisions)}")
    if sdd.review_notes:
        print("observações da revisão:")
        for nota in sdd.review_notes:
            print(f"  - {nota}")


def _perguntar_sim_nao(mensagem: str) -> bool:
    resposta = input(f"{mensagem} (s/n): ").strip().lower()
    return resposta in ("s", "sim", "y", "yes")


def _ciclo_de_refinamento(sdd: SolutionDesign) -> SolutionDesign:
    """Gera perguntas, pede respostas ao usuário, refina e reavalia até aprovar ou o usuário desistir."""
    while sdd.status != ArtifactStatus.DRAFT_VALIDATED and sdd.review_notes:
        perguntas = generate_sdd_clarifying_questions(sdd)
        if not perguntas:
            break

        print("\nO revisor apontou problemas. Responda para ajudar a refinar o Solution Design:")
        respostas = []
        for pergunta in perguntas:
            resposta = input(f"  {pergunta}\n  > ")
            respostas.append({"pergunta": pergunta, "resposta": resposta})

        sdd = refine_solution_design(sdd, respostas)
        print("\n--- Solution Design refinado ---")
        _imprimir_sdd(sdd)

        if sdd.status != ArtifactStatus.DRAFT_VALIDATED and not _perguntar_sim_nao(
            "\nTentar refinar de novo?"
        ):
            break
    return sdd


def _rodar(texto: str, saida: str | None, refinar: bool) -> None:
    sdd = handle_request(texto)
    _imprimir_sdd(sdd)

    if refinar:
        sdd = _ciclo_de_refinamento(sdd)

    if not _perguntar_sim_nao("\nAceitar este Solution Design?"):
        return

    sdd.status = ArtifactStatus.ACCEPTED

    if saida:
        with open(saida, "w", encoding="utf-8") as arquivo:
            arquivo.write(format_solution_design_markdown(sdd))
        print(f"exportado para: {saida}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o AQuA-QE Solution Architect.")
    entrada = parser.add_mutually_exclusive_group(required=True)
    entrada.add_argument("--arquivo", help="Caminho de um arquivo .txt/.md de entrada (ex.: um PRD).")
    entrada.add_argument("--texto", help="Texto de entrada direto (chat).")
    entrada.add_argument("--jira", help="Chave do ticket Jira (ex.: PROJ-123).")
    entrada.add_argument(
        "--confluence", help="URL completa ou ID de uma página do Confluence Cloud."
    )
    parser.add_argument("--saida", help="Caminho do .md exportado.")
    parser.add_argument(
        "--refinar",
        action="store_true",
        help=(
            "Ativa o ciclo interativo de perguntas/refinamento para o "
            "Solution Design não aprovado, antes do aceite humano (que é "
            "sempre perguntado, com ou sem esta flag)."
        ),
    )
    args = parser.parse_args()

    texto = _ler_entrada(args)
    _rodar(texto, args.saida, args.refinar)


if __name__ == "__main__":
    main()
