# Output Schema

> Estrutura de dados retornada por `generate_solution_design` e exportada por `format_solution_design_markdown`, alinhada a `../../knowledge/templates/solution_design.md`. Implementada como dataclasses reais em `../../src/aqua_qe_solution_architect/models/` (`SolutionDesign`, `NonFunctionalRequirement`, `ArchitectureDecision`) — o JSON abaixo é a representação conceitual.

## Schema do Solution Design Document (SDD)

```
{
  "id": "<string, ex.: SDD-001>",
  "title": "<string — extraído por extract_solution_context>",
  "context_problem": "<string — resumo do problema de negócio, extraído da fonte>",
  "architecture_pattern": "<um item do catálogo em architecture_patterns.md — nunca inventado (GR-SA-1)>",
  "pattern_rationale": "<string — por que este padrão, não outro>",
  "components": ["<componente de alto nível identificado>"],
  "integrations": ["<integração citada/inferível — nunca assumida sem evidência (GR-SA-2)>"],
  "non_functional_requirements": [
    {
      "category": "performance | escalabilidade | seguranca | disponibilidade | observabilidade | manutenibilidade",
      "requirement": "<string>",
      "rationale": "<rastreável a uma necessidade de negócio — GR-SA-6>",
      "source_reference": "<trecho da fonte>"
    }
  ],
  "technical_risks": ["<risco identificado — nunca omitido quando identificável (GR-SA-7)>"],
  "decisions": [
    {
      "id": "<string, ex.: ADR-001>",
      "title": "<string>",
      "context": "<string>",
      "decision": "<string>",
      "alternatives_considered": ["<alternativa descartada e por quê — GR-SA-4>"],
      "consequences": "<string>",
      "source_reference": "<trecho da fonte>"
    }
  ],
  "source_reference": "<texto de origem completo, para rastreabilidade — GR-1>",
  "status": "draft_validated | pending_clarification | accepted",
  "review_notes": ["<apontamento do revisor (review_solution_design), se houver>"]
}
```

## Valores válidos de `status`

- **`draft_validated`** — passou no checklist automático (`validation_checklist.md`) e na revisão por LLM (`review_solution_design`); ainda não tem aceitação humana (ver RULE-SA-9 em `rules.md`).
- **`pending_clarification`** — o agente interrompeu por ambiguidade/incompletude na fonte, ou o revisor reprovou o Solution Design; use o par `generate_sdd_clarifying_questions`/`refine_solution_design` para endereçar os apontamentos.
- **`accepted`** — setado **apenas** pelo CLI (`run.py`), nunca pela lógica automática do agente, após confirmação explícita do usuário.

## Formato de exportação (`format_solution_design_markdown`)

A saída em Markdown segue diretamente a estrutura de `../../knowledge/templates/solution_design.md`, preenchida a partir deste schema.
