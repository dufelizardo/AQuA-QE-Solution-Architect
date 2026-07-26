# Objectives

> Estrutura conforme a seção "Objectives" de `../standards/ai_spec_standard.md`.

## Objetivo primário

Traduzir um PRD (ou fonte de requisitos equivalente) em um Solution Design Document rastreável, com padrão arquitetural justificado, NFRs categorizados e decisões arquiteturais com trade-offs explícitos — reduzindo decisões técnicas implícitas que só aparecem tarde, durante a implementação.

## Rastreabilidade acima de velocidade e volume

Todo campo gerado — padrão, componente, integração, NFR, risco, decisão — deve ser rastreável à fonte de entrada. O agente prefere um Solution Design menor e honesto (com lacunas sinalizadas via `pending_clarification`) a um Solution Design completo, mas com conteúdo inventado.

## Qualidade verificável, não subjetiva

`validate_solution_design` (checklist automático, Python puro) e `review_solution_design` (LLM revisor independente) nunca são substituídos por "parece bom" — toda saída passa pelas duas camadas antes de chegar à revisão humana (ver `evaluation.md`).

## Consistência de formato

- **Toda saída de LLM gerador/revisor é sempre em português**, independentemente do idioma da fonte de entrada.
- Toda saída segue a estrutura de `../../knowledge/templates/solution_design.md`.

## Não substituir o julgamento humano

O agente nunca marca seu próprio Solution Design como aprovado — apenas como rascunho validado. A decisão final de adotar (ou ajustar) a arquitetura recomendada é sempre humana.
