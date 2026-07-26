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
from aqua_qe_solution_architect.skills.create_confluence_page import create_confluence_page  # noqa: E402
from aqua_qe_solution_architect.skills.format_chat_transcript import format_chat_transcript  # noqa: E402
from aqua_qe_solution_architect.skills.format_solution_design_markdown import (  # noqa: E402
    format_solution_design_markdown,
)
from aqua_qe_solution_architect.skills.generate_sdd_clarifying_questions import (  # noqa: E402
    generate_sdd_clarifying_questions,
)
from aqua_qe_solution_architect.skills.get_confluence_publish_location import (  # noqa: E402
    get_confluence_publish_location,
)
from aqua_qe_solution_architect.skills.parse_chat_transcript import parse_chat_transcript  # noqa: E402
from aqua_qe_solution_architect.skills.read_confluence_page import read_confluence_page  # noqa: E402
from aqua_qe_solution_architect.skills.read_jira_issue import read_jira_issue  # noqa: E402
from aqua_qe_solution_architect.skills.read_text_file import read_text_file  # noqa: E402
from aqua_qe_solution_architect.skills.update_confluence_page import update_confluence_page  # noqa: E402
from aqua_qe_solution_architect.workflow.generate_solution_design import (  # noqa: E402
    refine_and_finalize_solution_design,
)


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
    print(f"modelo de domínio: {len(sdd.domain_model)} entidade(s)")
    print(f"integrações: {sdd.integrations}")
    print(f"integrações candidatas (sugeridas, a confirmar): {sdd.candidate_integrations}")
    print(f"fluxos principais: {len(sdd.process_flows)}")
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

        sdd = refine_and_finalize_solution_design(sdd, respostas)
        print("\n--- Solution Design refinado ---")
        _imprimir_sdd(sdd)

        if sdd.status != ArtifactStatus.DRAFT_VALIDATED and not _perguntar_sim_nao(
            "\nTentar refinar de novo?"
        ):
            break
    return sdd


def _publicar_ou_atualizar_confluence(
    sdd: SolutionDesign,
    pagina_origem: str | None,
    publicar_confluence: bool,
    atualizar_confluence: str | None,
) -> None:
    """Cria uma página nova (irmã do PRD de origem) ou atualiza uma existente no Confluence, sempre sob confirmação humana explícita."""
    texto_formatado = format_solution_design_markdown(sdd)

    if atualizar_confluence:
        if not _perguntar_sim_nao(
            f"\nAtualizar a página {atualizar_confluence} no Confluence com este Solution Design?"
        ):
            return
        update_confluence_page(atualizar_confluence, texto_formatado)
        print(f"página atualizada no Confluence: {atualizar_confluence}")
        return

    if publicar_confluence:
        if not _perguntar_sim_nao(
            "\nPublicar no Confluence como página irmã do PRD de origem?"
        ):
            return
        titulo = input("Título da página no Confluence: ").strip()
        space_key, parent_page_id = get_confluence_publish_location(pagina_origem)
        url = create_confluence_page(texto_formatado, titulo, space_key, parent_page_id)
        print(f"publicado no Confluence: {url}")


def _rodar(
    texto: str,
    saida: str | None,
    refinar: bool,
    pagina_origem: str | None,
    publicar_confluence: bool,
    atualizar_confluence: str | None,
) -> None:
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

    if publicar_confluence or atualizar_confluence:
        _publicar_ou_atualizar_confluence(
            sdd, pagina_origem, publicar_confluence, atualizar_confluence
        )


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
    publicacao = parser.add_mutually_exclusive_group()
    publicacao.add_argument(
        "--publicar-confluence",
        action="store_true",
        dest="publicar_confluence",
        help=(
            "Após aceitar o Solution Design, pergunta o título e publica "
            "como página nova no Confluence, irmã da página de origem "
            "(só válido com --confluence)."
        ),
    )
    publicacao.add_argument(
        "--atualizar-confluence",
        dest="atualizar_confluence",
        help=(
            "Após aceitar o Solution Design, atualiza a página existente "
            "informada (URL completa ou ID) no Confluence, em vez de criar "
            "uma nova (só válido com --confluence)."
        ),
    )
    args = parser.parse_args()

    if (args.publicar_confluence or args.atualizar_confluence) and not args.confluence:
        parser.error(
            "--publicar-confluence/--atualizar-confluence só são válidos com --confluence "
            "(é preciso uma página de origem para publicar ao lado dela)."
        )

    texto = _ler_entrada(args)
    _rodar(
        texto,
        args.saida,
        args.refinar,
        args.confluence,
        args.publicar_confluence,
        args.atualizar_confluence,
    )


if __name__ == "__main__":
    main()
