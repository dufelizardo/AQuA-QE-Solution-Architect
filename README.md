# AQuA-QE Solution Architect

> Também disponível em [Português](README.pt.md).

Agent that generates Solution Design Documents (architecture pattern, components, integrations, non-functional requirements, technical risks and architecture decisions/ADRs) from a PRD or equivalent requirements source — following the agent engineering flow:

```
PRD → System Design → Agent Design → AI Specs/Rules/Skills → Context Engineering → Memory/MCP → Agents → Outputs
```

## Relationship with the sibling agents

This agent, the AQuA-QE Product Manager and the AQuA-QE Product Owner are **independent** — separate repositories, no shared runtime, no direct call between them. The intended flow across all three is:

```
Product Manager → PRD → Solution Architect → Solution Design Document → Product Owner → Epics/Stories
```

The Solution Architect answers a question neither of the other two answers: **what is the best technical solution to address this business requirement?** It never generates or edits a PRD (the Product Manager's role) and never generates Epics/User Stories (the Product Owner's role) — it consumes a finished PRD and produces a single intermediate technical artifact, the Solution Design Document, which the Product Owner could (in a future, not-yet-implemented phase) use as an additional input.

## Structure

- **`docs/standards/`** — platform-wide standards (how to write an AI Spec, a Rule, a PRD, etc.). Change rarely.
- **`docs/agent/`** — this agent's full specification: PRD, System Design, Agent Design, AI Spec, Rules, Persona, Objectives, Output Schema, Guardrails, Evaluation, Prompt, and `agent_manifest.yaml` (the agent manifest — inputs, outputs, skills, memory, rules).
- **`knowledge/methodology/`** — methodological material grounding the agent: architecture pattern catalog (`architecture_patterns.md`), ISO/IEC 25010 quality categories (`iso25010.md`), and ADR structure (`adr.md`).
- **`knowledge/templates/`** — pure structure, no content (Solution Design Document template).
- **`src/aqua_qe_solution_architect/skills/`** — the agent's skills in Python (reading a text file, parsing/formatting a chat transcript, reading a Jira ticket/Confluence page, extracting solution context, identifying architecture pattern/components/integrations, generating non-functional requirements/technical risks/architecture decisions, validating/reviewing/refining the Solution Design, exporting to Markdown).
- **`src/aqua_qe_solution_architect/models/`** — the agent's data structures (`SolutionDesign`, `NonFunctionalRequirement`, `ArchitectureDecision`, `ArtifactStatus`).
- **`src/aqua_qe_solution_architect/workflow/`** — orchestration of the skill sequence (`generate_solution_design`, `finalize_solution_design`).
- **`src/aqua_qe_solution_architect/orchestrator/`** — single entry point (`handle_request`).
- **`src/aqua_qe_solution_architect/services/`** — external integrations: `llm_service` (local Ollama, generation/review), `jira_service`/`confluence_service` (REST API, **read-only** in this phase).

## Setup

This is a standalone repository (not part of any monorepo) — `uv sync` here resolves and installs its own dependencies.

1. Install [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/).
2. Install [Ollama](https://ollama.com) and pull the two local models this agent uses:
   ```bash
   ollama pull mistral   # generation
   ollama pull phi4      # independent reviewer
   ```
3. Clone this repository and install dependencies:
   ```bash
   git clone https://github.com/dufelizardo/AQuA-QE-Solution-Architect.git
   cd AQuA-QE-Solution-Architect
   uv sync
   ```
4. Copy `.env.example` to `.env` and fill in the required values (Ollama works with the defaults; Jira/Confluence credentials are only needed for `--jira`/`--confluence`):
   ```bash
   cp .env.example .env
   ```
5. Run the test suite (fully mocked, no real calls to Ollama/Jira/Confluence) to confirm the setup:
   ```bash
   uv run pytest
   ```

## Usage

```bash
# A Solution Design from a PRD in a .txt/.md file
uv run python run.py --arquivo prd.txt --saida sdd.md

# From direct text (chat)
uv run python run.py --texto "We need a system that..." --saida sdd.md

# From a Jira Cloud ticket
uv run python run.py --jira PROJ-123 --saida sdd.md

# From a Confluence Cloud page
uv run python run.py --confluence "https://your-site.atlassian.net/wiki/.../pages/163841/..." --saida sdd.md

# With the interactive refinement cycle (questions, final acceptance)
uv run python run.py --arquivo prd.txt --saida sdd.md --refinar
```

`--saida` is optional (without it, the result is only printed to the terminal). To use `--jira`/`--confluence`, fill in `JIRA_BASE_URL`, `JIRA_EMAIL` and `JIRA_API_TOKEN` in `.env` (the token is generated at `id.atlassian.com/manage-profile/security/api-tokens`).

A prompt always asks whether you accept the Solution Design, with or without `--refinar` — export (`--saida`) only happens after that explicit acceptance, never before. `--refinar` turns on the interactive cycle that runs *before* that prompt: if the Solution Design isn't approved on review, the agent generates clarifying questions from the review notes, you answer them in the terminal, and the answers become real context to rewrite the design (instead of the LLM guessing on its own). See `run.py --help` for all options.

## Status

`docs/agent/`, `docs/standards/` and `knowledge/methodology/`/`knowledge/templates/` are filled with real content.

In `src/`, all 16 skills and the single workflow are implemented and work end-to-end with local models via Ollama:

- `read_text_file`, `read_jira_issue`, `read_confluence_page` (read-only) and `parse_chat_transcript`/`format_chat_transcript` (chat normalization, pure Python, no LLM) prepare the input text.
- `extract_solution_context` (LLM `mistral`) extracts a title and context/problem statement.
- `identify_architecture_pattern` (LLM `mistral`) picks a pattern only from the closed catalog in `knowledge/methodology/architecture_patterns.md` — never invents a pattern outside it (GR-SA-1).
- `identify_components_and_integrations` (LLM `mistral`) identifies components and integrations cited/inferable from the text (GR-SA-2: never assume an integration without documented evidence).
- `generate_non_functional_requirements` (LLM `mistral`) generates NFRs categorized per ISO/IEC 25010, each with a traceable `rationale` (GR-SA-6).
- `identify_technical_risks` (LLM `mistral`) identifies technical risks, never omitting one cited in the source (GR-SA-7).
- `generate_architecture_decisions` (LLM `mistral`) generates the ADRs, with explicit alternatives whenever more than one viable option exists (GR-SA-4).
- `validate_solution_design` (pure Python) runs the automatic checklist before paying the cost of LLM review.
- `review_solution_design` (reviewer LLM `phi4`, independent from the generator) evaluates the Solution Design.
- `generate_sdd_clarifying_questions`/`refine_solution_design` (LLM `mistral`) implement the human-in-the-loop refinement cycle.
- `format_solution_design_markdown` (pure Python) exports the final result.
- `workflow/generate_solution_design.py` (`generate_solution_design`, `finalize_solution_design`) orchestrates the full sequence; `orchestrator/solution_architect.py::handle_request` is the single entry point.

Still missing (deliberately deferred, see `WHITEPAPER.en.md`, section 11): C4/diagrams, API/OpenAPI contracts, UML/BPMN/Swagger/DB-schema parsers, real write integrations (Jira/Confluence/GitHub/GitLab/Kubernetes/Terraform/cloud), the 7 additional pattern categories (design/integration/distributed/cloud/security/data) + anti-patterns library, `--sdd-existente` (inverse parser, same pattern as `--epic-existente`/`--story-existente` in the Product Owner), RAG/project memory. `tests/` covers every implemented module (46 tests, LLM/HTTP mocked — fast and deterministic, never call Ollama, Jira or Confluence for real).

This project has its own git repository, independent from the root monorepo (per the "every new project gets a separate repository" convention — see the root `CLAUDE.md`): [github.com/dufelizardo/AQuA-QE-Solution-Architect](https://github.com/dufelizardo/AQuA-QE-Solution-Architect).

---

**Eduardo Felizardo Cândido**
Senior QA Automation Engineer | AI-driven Testing | Robot Framework & Python
