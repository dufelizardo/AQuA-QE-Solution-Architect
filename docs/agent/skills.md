# Skills

> Documentação das skills implementadas em `../../src/aqua_qe_solution_architect/skills/`, no formato definido em `../standards/skill_standard.md`. Ordem conforme `agent_manifest.yaml`. Tipos de entrada/saída referem-se às estruturas de `../../src/aqua_qe_solution_architect/models/`.
>
> `extract_solution_context`, `identify_architecture_pattern`, `identify_components_and_integrations`, `generate_non_functional_requirements`, `identify_technical_risks`, `generate_architecture_decisions`, `generate_sdd_clarifying_questions` e `refine_solution_design` usam um LLM local via Ollama (`../../src/aqua_qe_solution_architect/services/llm_service.py`, modelo configurável por `OLLAMA_MODEL`, padrão `mistral`). `validate_solution_design` e `format_solution_design_markdown` são Python puro, sem LLM (ver `evaluation.md`). `review_solution_design` usa um segundo LLM, diferente do gerador (`OLLAMA_REVIEW_MODEL`, padrão `phi4`), como revisor independente (LLM-como-juiz). `read_jira_issue`/`read_confluence_page` usam a API REST do Jira/Confluence Cloud — **apenas leitura**, nunca escrevem de volta.

## read_text_file

- **Descrição**: lê um arquivo de texto (`.txt` ou `.md`) e retorna seu conteúdo.
- **Entrada**: `caminho: str`.
- **Saída**: `str` — conteúdo do arquivo.
- **Efeitos colaterais**: leitura de arquivo em disco.
- **Erros esperados**: arquivo inexistente, ilegível ou com encoding inválido.
- **Dependências**: nenhuma outra skill.

## parse_chat_transcript

- **Descrição**: separa uma transcrição de chat em mensagens por remetente (ex.: `"Arquiteto: ..."`, `"Dev: ..."`). Puro Python (regex), sem LLM.
- **Entrada**: `texto: str`.
- **Saída**: `list[ChatMessage]`.
- **Efeitos colaterais**: nenhum.
- **Erros esperados**: nenhum.
- **Dependências**: nenhuma outra skill.

## format_chat_transcript

- **Descrição**: reconstrói uma transcrição normalizada a partir das mensagens de `parse_chat_transcript`.
- **Entrada**: `mensagens: list[ChatMessage]`.
- **Saída**: `str`.
- **Efeitos colaterais**: nenhum.
- **Erros esperados**: nenhum.
- **Dependências**: consome a saída de `parse_chat_transcript`.

## read_jira_issue

- **Descrição**: busca um ticket no Jira Cloud (resumo + descrição) e retorna como texto simples.
- **Entrada**: `issue_key: str`.
- **Saída**: `str`.
- **Efeitos colaterais**: chamada HTTP à API REST do Jira Cloud; requer `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`.
- **Erros esperados**: credenciais ausentes (`KeyError`); ticket inexistente ou sem permissão (erro HTTP).
- **Dependências**: nenhuma outra skill.

## read_confluence_page

- **Descrição**: busca uma página do Confluence Cloud (título + corpo) e retorna como texto simples. Aceita URL completa ou ID.
- **Entrada**: `pagina: str`.
- **Saída**: `str`.
- **Efeitos colaterais**: chamada HTTP à API REST do Confluence Cloud; mesmas credenciais do Jira.
- **Erros esperados**: credenciais ausentes; página inexistente ou sem permissão.
- **Dependências**: nenhuma outra skill.

## extract_solution_context

- **Descrição**: extrai um título curto e um resumo do contexto/problema de negócio a partir do texto de entrada.
- **Entrada**: `texto: str`.
- **Saída**: `tuple[str, str]` — (título, contexto).
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: nenhuma outra skill; primeira etapa de `workflow/generate_solution_design.py::generate_solution_design`.

## identify_architecture_pattern

- **Descrição**: identifica o padrão arquitetural mais adequado ao contexto, só entre os do catálogo em `../../knowledge/methodology/architecture_patterns.md` (GR-SA-1) — nunca inventa um padrão fora da lista, mesmo que o LLM tente.
- **Entrada**: `texto: str`.
- **Saída**: `tuple[str, str]` — (padrão, justificativa); padrão fica `""` se o LLM devolver algo fora do catálogo.
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: nenhuma outra skill.

## identify_components_and_integrations

- **Descrição**: identifica componentes de alto nível e integrações citadas/inferíveis no texto (GR-SA-2: nunca assumir integração sem evidência documental).
- **Entrada**: `texto: str`.
- **Saída**: `tuple[list[str], list[str]]` — (componentes, integrações).
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: nenhuma outra skill.

## generate_non_functional_requirements

- **Descrição**: identifica NFRs categorizados conforme ISO/IEC 25010 (`../../knowledge/methodology/iso25010.md`), cada um com `rationale` rastreável a uma necessidade de negócio (GR-SA-6).
- **Entrada**: `texto: str`.
- **Saída**: `list[NonFunctionalRequirement]`; categoria fica `""` se o LLM devolver uma categoria fora das 6 válidas.
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: nenhuma outra skill.

## identify_technical_risks

- **Descrição**: identifica riscos técnicos citados/inferíveis no texto — nunca omite um risco identificável (GR-SA-7).
- **Entrada**: `texto: str`.
- **Saída**: `list[str]`.
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: nenhuma outra skill.

## generate_architecture_decisions

- **Descrição**: gera os ADRs da solução (`../../knowledge/methodology/adr.md`) a partir do padrão escolhido, componentes/integrações e contexto — toda decisão relevante precisa de um ADR (GR-SA-3), com alternativas explícitas quando houver mais de uma opção viável (GR-SA-4).
- **Entrada**: `padrao: str`, `justificativa_padrao: str`, `componentes: list[str]`, `integracoes: list[str]`, `texto: str`.
- **Saída**: `list[ArchitectureDecision]`.
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: consome as saídas de `identify_architecture_pattern` e `identify_components_and_integrations`.

## validate_solution_design

- **Descrição**: valida se o Solution Design tem título, contexto, padrão arquitetural com justificativa, ao menos um NFR e ao menos uma decisão arquitetural registrada.
- **Entrada**: `sdd: SolutionDesign`.
- **Saída**: `list[str]` — motivos específicos de reprovação (lista vazia = aprovado no checklist; não decide aceitação humana). `finalize_solution_design` grava esses motivos em `sdd.review_notes` quando o checklist reprova, para que o usuário sempre veja por que — inclusive antes de qualquer revisão por LLM rodar.
- **Efeitos colaterais**: nenhum — Python puro, sem LLM.
- **Erros esperados**: nenhum.
- **Dependências**: consome a saída de `generate_solution_design`/`refine_solution_design`.

## review_solution_design

- **Descrição**: revisa o Solution Design com um segundo LLM, diferente do gerador, avaliando coerência do padrão com o contexto, rastreabilidade dos NFRs e explicitação de trade-offs nas decisões.
- **Entrada**: `sdd: SolutionDesign`.
- **Saída**: `dict` no formato `{"aprovado": bool, "problemas": list[str]}`.
- **Efeitos colaterais**: chamada ao LLM local de revisão (`OLLAMA_REVIEW_MODEL`, padrão `phi4`).
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: consome a saída de `generate_solution_design`, após `validate_solution_design` aprovar o checklist automático.

## generate_sdd_clarifying_questions

- **Descrição**: transforma os `review_notes` do Solution Design em perguntas diretas e acionáveis para quem propôs a solução responder.
- **Entrada**: `sdd: SolutionDesign`.
- **Saída**: `list[str]`; vazia se não houver `review_notes`.
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: consome `review_notes`, preenchido por `validate_solution_design` (motivos do checklist) ou `review_solution_design` (apontamentos do revisor), via `finalize_solution_design`.

## refine_solution_design

- **Descrição**: reescreve os campos do Solution Design usando as respostas do usuário às perguntas de esclarecimento — não o LLM adivinhando sozinho a correção. Preserva o texto/nível de detalhe de campos que as respostas não abordam (mesmo cuidado adotado desde o início, aprendido com um bug real corrigido em `refine_prd`/`refine_epic_metadata` no AQuA-QE Product Owner).
- **Entrada**: `sdd: SolutionDesign`, `respostas: list[dict]` (cada item: `{"pergunta": str, "resposta": str}`).
- **Saída**: `SolutionDesign` — mesmo objeto, campos atualizados; `status`/`review_notes` só são recalculados pelo workflow.
- **Efeitos colaterais**: chamada ao LLM local.
- **Erros esperados**: resposta do LLM não é JSON válido (`ValueError`).
- **Dependências**: consome as perguntas de `generate_sdd_clarifying_questions` e as respostas do usuário (coletadas no CLI, `run.py`).

## format_solution_design_markdown

- **Descrição**: formata o Solution Design Document em Markdown, seções conforme `../../knowledge/templates/solution_design.md`.
- **Entrada**: `sdd: SolutionDesign`.
- **Saída**: `str`.
- **Efeitos colaterais**: nenhum — Python puro, sem LLM.
- **Erros esperados**: nenhum.
- **Dependências**: consome a saída de `generate_solution_design`/`refine_solution_design`, tipicamente após aceitação humana.
