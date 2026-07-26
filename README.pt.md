# AQuA-QE Solution Architect

> Também disponível em [English](README.md).

Agente que gera Solution Design Documents (padrão arquitetural, componentes, integrações, requisitos não funcionais, riscos técnicos e decisões arquiteturais/ADRs) a partir de um PRD ou fonte de requisitos equivalente — seguindo o fluxo de engenharia de agentes:

```
PRD → System Design → Agent Design → AI Specs/Rules/Skills → Context Engineering → Memory/MCP → Agents → Outputs
```

## Relação com os agentes irmãos

Este agente, o AQuA-QE Product Manager e o AQuA-QE Product Owner são **independentes** — repositórios separados, sem runtime compartilhado, sem chamada direta entre eles. O fluxo pretendido entre os três é:

```
Product Manager → PRD → Solution Architect → Solution Design Document → Product Owner → Épicos/Stories
```

O Solution Architect responde a uma pergunta que nenhum dos outros dois responde: **qual é a melhor solução técnica para atender este requisito de negócio?** Ele nunca gera nem edita um PRD (papel do Product Manager) e nunca gera Épicos/User Stories (papel do Product Owner) — consome um PRD já pronto e produz um único artefato técnico intermediário, o Solution Design Document, que o Product Owner poderia (em uma fase futura, não implementada) usar como entrada adicional.

## Estrutura

- **`docs/standards/`** — padrões da plataforma (como escrever um AI Spec, uma Rule, um PRD, etc.). Mudam pouco.
- **`docs/agent/`** — especificação completa deste agente: PRD, System Design, Agent Design, AI Spec, Rules, Persona, Objectives, Output Schema, Guardrails, Evaluation, Prompt e o `agent_manifest.yaml` (manifesto do agente — inputs, outputs, skills, memory, rules).
- **`knowledge/methodology/`** — material metodológico que orienta o agente: catálogo de padrões arquiteturais (`architecture_patterns.md`), categorias de qualidade da ISO/IEC 25010 (`iso25010.md`) e estrutura de ADR (`adr.md`).
- **`knowledge/templates/`** — estrutura pura, sem conhecimento (template do Solution Design Document).
- **`src/aqua_qe_solution_architect/skills/`** — skills do agente em Python (ler arquivo de texto, parsear/formatar transcrição de chat, ler ticket Jira/página Confluence, extrair contexto da solução, identificar padrão arquitetural/componentes/integrações, gerar requisitos não funcionais/riscos técnicos/decisões arquiteturais, validar/revisar/refinar o Solution Design, exportar em Markdown).
- **`src/aqua_qe_solution_architect/models/`** — estruturas de dados do agente (`SolutionDesign`, `NonFunctionalRequirement`, `ArchitectureDecision`, `ArtifactStatus`).
- **`src/aqua_qe_solution_architect/workflow/`** — orquestração da sequência de skills (`generate_solution_design`, `finalize_solution_design`).
- **`src/aqua_qe_solution_architect/orchestrator/`** — ponto de entrada único (`handle_request`).
- **`src/aqua_qe_solution_architect/services/`** — integrações externas: `llm_service` (Ollama local, geração/revisão), `jira_service`/`confluence_service` (API REST, **apenas leitura** nesta fase).

## Configuração

Este é um repositório independente (não faz parte de nenhum monorepo) — o `uv sync` aqui resolve e instala suas próprias dependências.

1. Instale [Python 3.12+](https://www.python.org/) e [uv](https://docs.astral.sh/uv/).
2. Instale o [Ollama](https://ollama.com) e baixe os dois modelos locais usados por este agente:
   ```bash
   ollama pull mistral   # geração
   ollama pull phi4      # revisor independente
   ```
3. Clone este repositório e instale as dependências:
   ```bash
   git clone https://github.com/dufelizardo/AQuA-QE-Solution-Architect.git
   cd AQuA-QE-Solution-Architect
   uv sync
   ```
4. Copie `.env.example` para `.env` e preencha os valores necessários (o Ollama funciona com os padrões; as credenciais de Jira/Confluence só são necessárias para `--jira`/`--confluence`):
   ```bash
   cp .env.example .env
   ```
5. Rode a suíte de testes (totalmente mockada, sem chamadas reais a Ollama/Jira/Confluence) para confirmar a configuração:
   ```bash
   uv run pytest
   ```

## Uso

```bash
# Um Solution Design a partir de um PRD em arquivo .txt/.md
uv run python run.py --arquivo prd.txt --saida sdd.md

# A partir de texto direto (chat)
uv run python run.py --texto "Precisamos de um sistema que..." --saida sdd.md

# A partir de um ticket Jira Cloud
uv run python run.py --jira PROJ-123 --saida sdd.md

# A partir de uma página do Confluence Cloud
uv run python run.py --confluence "https://seu-site.atlassian.net/wiki/.../pages/163841/..." --saida sdd.md

# Com ciclo interativo de refinamento (perguntas, aceite final)
uv run python run.py --arquivo prd.txt --saida sdd.md --refinar
```

`--saida` é opcional (sem ela, o resultado só é impresso no terminal). Para usar `--jira`/`--confluence`, preencha `JIRA_BASE_URL`, `JIRA_EMAIL` e `JIRA_API_TOKEN` no `.env` (o token é gerado em `id.atlassian.com/manage-profile/security/api-tokens`).

Um prompt sempre pergunta se você aceita o Solution Design, com ou sem `--refinar` — a exportação (`--saida`) só acontece depois desse aceite explícito, nunca antes. `--refinar` ativa o ciclo interativo que roda *antes* desse prompt: se o Solution Design não sair aprovado na revisão, o agente gera perguntas de esclarecimento a partir dos apontamentos, você responde no terminal, e as respostas viram contexto real para reescrever o design (em vez do LLM adivinhar sozinho). Ver `run.py --help` para todas as opções.

## Status

`docs/agent/`, `docs/standards/` e `knowledge/methodology/`/`knowledge/templates/` estão com conteúdo real preenchido.

Em `src/`, as 16 skills e o único workflow estão implementados e funcionam de ponta a ponta com modelos locais via Ollama:

- `read_text_file`, `read_jira_issue`, `read_confluence_page` (leitura apenas) e `parse_chat_transcript`/`format_chat_transcript` (normalização de chat, Python puro, sem LLM) preparam o texto de entrada.
- `extract_solution_context` (LLM `mistral`) extrai título e contexto/problema.
- `identify_architecture_pattern` (LLM `mistral`) escolhe um padrão só entre os do catálogo fechado em `knowledge/methodology/architecture_patterns.md` — nunca inventa um padrão fora dele (GR-SA-1).
- `identify_components_and_integrations` (LLM `mistral`) identifica componentes e integrações citados/inferíveis no texto (GR-SA-2: nunca assumir integração sem evidência).
- `generate_non_functional_requirements` (LLM `mistral`) gera NFRs categorizados conforme ISO/IEC 25010, cada um com `rationale` rastreável (GR-SA-6).
- `identify_technical_risks` (LLM `mistral`) identifica riscos técnicos, sem omitir nenhum citado na fonte (GR-SA-7).
- `generate_architecture_decisions` (LLM `mistral`) gera os ADRs, com alternativas explícitas quando houver mais de uma opção viável (GR-SA-4).
- `validate_solution_design` (Python puro) roda o checklist automático antes de pagar o custo da revisão por LLM.
- `review_solution_design` (LLM revisor `phi4`, independente do gerador) avalia o Solution Design.
- `generate_sdd_clarifying_questions`/`refine_solution_design` (LLM `mistral`) implementam o ciclo de refinamento humano-no-loop.
- `format_solution_design_markdown` (Python puro) exporta o resultado final.
- `workflow/generate_solution_design.py` (`generate_solution_design`, `finalize_solution_design`) orquestra a sequência completa; `orchestrator/solution_architect.py::handle_request` é o ponto de entrada único.

Ainda faltam (deliberadamente adiados, ver `WHITEPAPER.md`, seção 11): C4/diagramas, contratos de API/OpenAPI, parsers de UML/BPMN/Swagger/schema de banco, integrações reais de escrita (Jira/Confluence/GitHub/GitLab/Kubernetes/Terraform/nuvem), as 7 categorias adicionais de patterns (design/integração/distribuído/cloud/segurança/dados) + biblioteca de anti-patterns, `--sdd-existente` (parser inverso, mesmo padrão de `--epic-existente`/`--story-existente` no Product Owner), RAG/memória de projeto. `tests/` cobre todos os módulos implementados (46 testes, mocks de LLM/HTTP — rápidos e determinísticos, não chamam Ollama nem Jira/Confluence de verdade).

Este projeto tem repositório git próprio, independente do monorepo raiz (conforme a convenção "todo projeto novo recebe repositório separado" — ver `CLAUDE.md` raiz): [github.com/dufelizardo/AQuA-QE-Solution-Architect](https://github.com/dufelizardo/AQuA-QE-Solution-Architect).

---

**Eduardo Felizardo Cândido**
Senior QA Automation Engineer | AI-driven Testing | Robot Framework & Python
