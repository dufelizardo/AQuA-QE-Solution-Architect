# Validation Checklist

> Checklist aplicado pela skill `validate_solution_design` antes de qualquer Solution Design ser marcado como `draft_validated` (ver `output_schema.md` e RULE-SA-3/RULE-SA-9 em `rules.md`).

## 1. Rastreabilidade (GR-SA-1, GR-SA-2, GR-SA-6, GR-SA-7)

- [ ] Título e contexto do problema têm origem identificável na fonte de entrada.
- [ ] Nenhum campo foi preenchido por suposição não sinalizada.

## 2. Padrão arquitetural

- [ ] `architecture_pattern` é um item do catálogo em `../../knowledge/methodology/architecture_patterns.md` — nunca um padrão inventado.
- [ ] `pattern_rationale` está preenchido e não é genérico ("é o mais moderno").

## 3. Requisitos não funcionais (ISO/IEC 25010, `../../knowledge/methodology/iso25010.md`)

- [ ] Há ao menos um NFR.
- [ ] Cada NFR tem `category` válida (uma das 6 categorias definidas) e `rationale` não vazio.

## 4. Decisões arquiteturais (ADR, `../../knowledge/methodology/adr.md`)

- [ ] Há ao menos uma `ArchitectureDecision`.
- [ ] Cada decisão tem `context`, `decision` e `consequences` preenchidos.

## 5. Riscos técnicos (GR-SA-7)

- [ ] Riscos identificáveis no texto de origem não foram omitidos.

## 6. Formato

- [ ] A saída segue a estrutura de `../../knowledge/templates/solution_design.md`.
