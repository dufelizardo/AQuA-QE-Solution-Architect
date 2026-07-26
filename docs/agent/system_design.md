# System Design

> Estrutura conforme `../standards/system_design_standard.md`.

## Visão geral da arquitetura

O agente é um pipeline de skills orquestrado sequencialmente, com dois pontos de checagem antes de qualquer saída ser considerada válida: validação automática (checklist estrutural) e revisão humana obrigatória — mesmo padrão de PM/PO. Não há aprovação automática (ver `guardrails.md`).

```
Entrada (.txt/Markdown/chat/Jira/Confluence)
   → read_text_file / parse_chat_transcript+format_chat_transcript (só chat) / read_jira_issue / read_confluence_page
   → extract_solution_context (título + contexto)
   → identify_architecture_pattern (só entre os do catálogo)
   → identify_components_and_integrations
   → generate_non_functional_requirements (categorizados ISO/IEC 25010)
   → identify_technical_risks
   → generate_architecture_decisions (ADRs, com alternativas)
   → validate_solution_design (checklist automático)
   → review_solution_design (LLM revisor independente — phi4)
   → [se reprovado] generate_sdd_clarifying_questions → resposta humana → refine_solution_design → revalidar
   → aceite humano explícito
   → format_solution_design_markdown (export)
```

## Componentes

- **Orquestrador** — ponto de entrada único (`handle_request`), decide a sequência de skills (ordem fixa do `agent_manifest.yaml`). Implementado em `../../src/aqua_qe_solution_architect/orchestrator/solution_architect.py`.
- **Workflow** — orquestração da sequência de skills (`generate_solution_design`, `finalize_solution_design`), implementado em `../../src/aqua_qe_solution_architect/workflow/`.
- **Skills** — funções descritas em `skills.md`, implementadas em `../../src/aqua_qe_solution_architect/skills/`.
- **Modelos de dados** — `SolutionDesign`, `NonFunctionalRequirement`, `ArchitectureDecision`, `ChatMessage`, enum `ArtifactStatus`, implementados em `../../src/aqua_qe_solution_architect/models/`, conforme `output_schema.md`.
- **Fontes de conhecimento** — `knowledge/methodology/` (catálogo de padrões arquiteturais, ISO/IEC 25010, ADR), consumido diretamente no prompt de cada skill (sem RAG nesta fase — o volume cabe direto no contexto).
- **Interfaces externas** — entrada: arquivo `.txt`/Markdown, texto de chat, ticket Jira (leitura) ou página Confluence (leitura); saída: arquivo Markdown exportado (`format_solution_design_markdown`), consumível pelo Product Owner como contexto técnico.

## Fluxo de dados

1. A entrada é normalizada em texto (`read_text_file` quando for arquivo; passagem direta quando for chat/Jira/Confluence).
2. `extract_solution_context` identifica título e contexto do problema.
3. `identify_architecture_pattern` escolhe um padrão do catálogo, com justificativa.
4. `identify_components_and_integrations` identifica componentes e integrações.
5. `generate_non_functional_requirements` e `identify_technical_risks` cobrem qualidade e riscos.
6. `generate_architecture_decisions` produz os ADRs, usando o padrão/componentes/integrações já definidos como contexto.
7. `validate_solution_design` aplica o checklist automático; se reprovar, o Solution Design fica `pending_clarification`.
8. Se aprovado no checklist, `review_solution_design` (LLM independente) avalia coerência e explicitação de trade-offs.
9. Se a revisão reprovar, o ciclo de refinamento humano-no-loop (mesmo padrão de PM/PO) entra em ação.
10. A aprovação final é sempre um ato humano, fora da responsabilidade do agente — só então o Solution Design é exportado.

## Modos de operação

Um único fluxo nesta fase — gerar o Solution Design Document a partir de uma fonte de texto. Não há distinção "unitário/lote" como em PM/PO, porque só existe um artefato (o SDD) nesta fase.

## Restrições técnicas

- Dois LLMs locais via Ollama (`OLLAMA_MODEL` gerador, `OLLAMA_REVIEW_MODEL` revisor) — mesma convenção de PM/PO.
- Sem RAG/embeddings nesta fase — `knowledge/methodology/` é pequeno o suficiente para caber direto no prompt de cada skill.
- Serviços externos (Jira, Confluence) introduzidos só como leitura, sem escrita — mesmo princípio de "nenhum serviço construído sem consumidor real" já aplicado em PM/PO.

## Observabilidade

- Cada execução deve registrar: fonte de entrada, padrão arquitetural escolhido e justificativa, NFRs/riscos/decisões identificados, resultado do checklist automático e da revisão, e se houve ciclo de refinamento — necessário para auditar rastreabilidade (ver `guardrails.md`) e para os casos de teste de `evaluation.md`.
