# CLAUDE.md

Este arquivo orienta o Claude Code ao trabalhar neste repositório.

## O que é este projeto

Agente que gera Solution Design Documents (padrão arquitetural, componentes, integrações, requisitos não funcionais, riscos técnicos e decisões arquiteturais/ADRs) a partir de um PRD, documento de requisitos, ticket Jira ou página Confluence — com rastreabilidade obrigatória à fonte, validação automática e revisão humana no centro do ciclo. Ver `WHITEPAPER.md` (também em inglês: `WHITEPAPER.en.md`) para a visão completa.

Este é um **repositório standalone**, próprio, independente de qualquer monorepo — não assuma dependências herdadas de um workspace pai.

## Comandos essenciais

```bash
# Instalar/sincronizar dependências
uv sync

# Rodar toda a suíte de testes (mockada, sem chamadas reais a Ollama/Jira/Confluence)
uv run pytest

# Rodar um teste único
uv run pytest tests/test_generate_solution_design_workflow.py::test_nome_do_teste

# Gerar um Solution Design a partir de um arquivo
uv run python run.py --arquivo prd.txt --saida sdd.md

# Ver todas as opções (--texto, --jira, --confluence, --refinar, --publicar-confluence, --atualizar-confluence)
uv run python run.py --help
```

Não há configuração própria de lint/type-check (`ruff`/`basedpyright`) neste `pyproject.toml` — isso existe apenas na raiz do monorepo que originou este projeto, não neste repositório standalone.

## Setup local

Ver a seção "Setup"/"Configuração" em `README.md`/`README.pt.md`: requer Python 3.12+, `uv`, Ollama instalado com os modelos `mistral` e `phi4` baixados, e um `.env` preenchido a partir de `.env.example`.

## Arquitetura (resumo — detalhe completo em `docs/agent/system_design.md` e `WHITEPAPER.md`)

```
Entrada (.txt/Markdown/chat/Jira/Confluence)
  → CLI (run.py) → orchestrator/solution_architect.py → workflow/generate_solution_design.py → skills/* → models/* → services/*
```

- `src/aqua_qe_solution_architect/models/` — `SolutionDesign`, `NonFunctionalRequirement`, `ArchitectureDecision`, enum `ArtifactStatus`.
- `src/aqua_qe_solution_architect/skills/` — 19 funções de responsabilidade única (ver `docs/agent/skills.md`).
- `src/aqua_qe_solution_architect/workflow/generate_solution_design.py` — `generate_solution_design` (gera do zero), `finalize_solution_design` (validate→review, reaproveitável após refino) e `refine_and_finalize_solution_design` (refina + revalida).
- `src/aqua_qe_solution_architect/orchestrator/solution_architect.py` — ponto de entrada único, `handle_request(entrada)`.
- `src/aqua_qe_solution_architect/services/` — integrações externas: `llm_service` (Ollama), `jira_service` (REST API + httpx, **apenas leitura**), `confluence_service` (REST API + httpx, **leitura e escrita** — `get_page_text`/`get_page_parent_context` leem, `create_page`/`update_page` escrevem).

## Convenções críticas

- **Nunca inventar** (GR-SA-1, `docs/agent/guardrails.md`): componente, integração, NFR, risco ou decisão arquitetural só existem se rastreáveis à fonte de entrada. `identify_architecture_pattern` só pode escolher um padrão do catálogo fechado em `knowledge/methodology/architecture_patterns.md` — nunca um padrão inventado; retorna `""` se o LLM devolver algo fora da lista.
- **Nunca assumir integrações sem evidência** (GR-SA-2): `identify_components_and_integrations` deixa a lista de integrações vazia na ausência de evidência textual, nunca preenchida por suposição.
- **Toda decisão arquitetural relevante precisa de um ADR** (GR-SA-3) **com alternativas explícitas quando houver mais de uma opção viável** (GR-SA-4): `ArchitectureDecision.alternatives_considered` nunca fica implícito.
- **Todo NFR precisa de `rationale` rastreável** (GR-SA-6): `generate_non_functional_requirements` nunca produz um NFR genérico sem justificativa ligada ao texto de origem; categoria fica `""` se fora das 6 válidas de `CATEGORIAS_NFR`.
- **Nunca omitir risco técnico identificável** (GR-SA-7): `identify_technical_risks` sempre roda; seu resultado nunca é descartado.
- **Sem aprovação automática** (RULE-SA-9, guardrail transversal): nenhuma skill/workflow define `ArtifactStatus.ACCEPTED`. Esse status só é atribuído pelo CLI (`run.py`), após confirmação humana explícita no terminal — sempre pedida, com ou sem `--refinar`.
- **Dois LLMs sempre diferentes**: `OLLAMA_MODEL` (padrão `mistral`) gera; `OLLAMA_REVIEW_MODEL` (padrão `phi4`) revisa. Deliberado — mitiga *self-preference bias* de um modelo aprovar a própria saída.
- **Piloto de provedor via toggle** (`LLM_PROVIDER=ollama|nvidia|cerebras|google`, padrão `ollama`): `llm_service.generator_model()`/`reviewer_model()` resolvem o modelo certo conforme o provedor ativo; `complete`/`complete_json` mantêm assinatura inalterada e despacham internamente para Ollama ou para um dos três provedores em nuvem (NVIDIA NIM, Cerebras Inference, Google AI Studio — todos com API compatível com OpenAI via pacote `openai`). Toggle NVIDIA validado ao vivo primeiro no agente irmão AQuA-QE Product Manager, replicado aqui — modelos confirmados na mesma conta: `deepseek-ai/deepseek-v4-pro` (gerador), `meta/llama-3.3-70b-instruct` (revisor). Ao testar ao vivo neste agente, o NVIDIA NIM se mostrou instável (503 de capacidade, 404 de entitlement, timeout de leitura em tentativas sucessivas) — motivou adicionar Cerebras (`api.cerebras.ai`) como terceiro provedor, com `gpt-oss-120b` (gerador, status "Production" na Cerebras) e `zai-glm-4.7` (revisor, família diferente); teste ao vivo da Cerebras deu 402 (billing/quota pendente na conta, não bug). Google AI Studio (`generativelanguage.googleapis.com/v1beta/openai/`) adicionado como quarto provedor — `gemini-2.5-flash`/`gemini-2.5-pro` são sugestão a confirmar no dashboard, ainda não validados ao vivo. Ollama continua o padrão sem `LLM_PROVIDER` definido, e nenhuma skill geradora precisa saber do provedor (só `complete`/`complete_json`).
- **`refine_solution_design` preserva o detalhe de campos não abordados pelas respostas do usuário** — cuidado incorporado desde o início do projeto, aprendido com um bug real corrigido em `refine_prd`/`refine_epic_metadata` no agente irmão AQuA-QE Product Owner.
- **`jira_service` é apenas leitura nesta fase** — não há `create_*`/`update_*`. Diferente do Product Owner, que também escreve de volta no Jira; aqui não existe hoje um caso de uso real que justifique isso.
- **`confluence_service` ganhou escrita** (`create_page`/`update_page`, portados do AQuA-QE Product Manager): publicar (`--publicar-confluence`) ou atualizar (`--atualizar-confluence`) sempre exige confirmação humana explícita no CLI (RULE-SA-10) e sempre cria a página como **irmã da página de origem do PRD** — `get_confluence_publish_location` deriva o espaço/ancestral diretamente da página de origem via `get_page_parent_context`, nunca de configuração manual. Por isso, ao contrário de PM/PO, **não há env var `CONFLUENCE_SPACE_KEY`** — o espaço é sempre derivado da fonte. Ambas as flags só são válidas com `--confluence` (sem página de origem, não há "ao lado de quem" publicar).
- **Este agente nunca gera nem edita um PRD** (papel exclusivo do agente irmão AQuA-QE Product Manager) **e nunca gera Épicos/User Stories** (papel exclusivo do agente irmão AQuA-QE Product Owner). Consome um PRD já pronto e produz um único artefato técnico intermediário, o Solution Design Document.
- **Testes sempre mockam** Ollama/Jira/Confluence — nenhum teste em `tests/` faz chamada real de rede. Ao adicionar um teste para uma skill/service novo, siga esse padrão.
- **`knowledge/methodology/` tem só 3 arquivos nesta fase** (`architecture_patterns.md`, `iso25010.md`, `adr.md`), deliberadamente pequeno o suficiente para caber direto no prompt de cada skill, sem RAG. As 7 categorias adicionais de patterns + anti-patterns da especificação original completa **não** foram implementadas — ver seção 11 do `WHITEPAPER.md`.
- **Sem `--modo`** (diferente de PM/PO): este agente produz um único tipo de artefato nesta fase, então `run.py` não tem flag de modo — só `--arquivo`/`--texto`/`--jira`/`--confluence` (mutuamente exclusivos), `--refinar` e `--publicar-confluence`/`--atualizar-confluence` (mutuamente exclusivos entre si).

## Onde procurar mais detalhe

- `docs/agent/` — PRD, System Design, Agent Design, Rules, Guardrails, Persona, Objectives, Skills, Evaluation (a spec formal completa do agente).
- `knowledge/methodology/` — os frameworks reais que fundamentam os critérios de qualidade (catálogo de padrões arquiteturais, ISO/IEC 25010, ADR) — nenhum critério do agente foi inventado à parte desses documentos.
- `WHITEPAPER.md` / `WHITEPAPER.en.md` — visão consolidada, inclui o que foi deliberadamente deixado fora da Fase 1 (seção 11).
