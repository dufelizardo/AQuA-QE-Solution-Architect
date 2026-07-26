# Acceptance Patterns

> Padrões estruturais que distinguem uma saída aceitável de uma inaceitável, conforme `validation_checklist.md` e `guardrails.md`. Exemplos concretos de domínio (few-shot) ficariam em `knowledge/examples/` — ainda não criado nesta fase (ver `WHITEPAPER.md`, seção 11).

## Padrão aceitável

Um Solution Design é aceitável quando:

- `architecture_pattern` é um item do catálogo (`knowledge/methodology/architecture_patterns.md`), com `pattern_rationale` específico ao contexto (GR-SA-1).
- Toda integração listada tem evidência no texto de origem (GR-SA-2).
- Há ao menos uma `ArchitectureDecision`, cada uma com contexto/decisão/consequências preenchidos (GR-SA-3).
- Decisões com mais de uma alternativa viável têm `alternatives_considered` preenchido (GR-SA-4).
- Todo NFR tem `rationale` rastreável a uma necessidade de negócio (GR-SA-6).
- Nenhum risco técnico citado na fonte foi omitido (GR-SA-7).
- O campo `status` reflete corretamente o resultado da validação (`draft_validated` ou `pending_clarification`).

## Padrão inaceitável

Uma saída é inaceitável quando apresenta qualquer um dos sinais abaixo:

- **Padrão arquitetural fora do catálogo** ou justificativa genérica ("é o mais usado no mercado") sem relação com o contexto específico (viola GR-SA-1).
- **Integração assumida sem evidência** — "provavelmente se integra com X" sem menção no texto (viola GR-SA-2).
- **Decisão arquitetural sem ADR** — uma escolha relevante mencionada só en passant, sem registro formal (viola GR-SA-3).
- **Decisão apresentada como única opção possível** quando claramente havia alternativas razoáveis não mencionadas (viola GR-SA-4).
- **NFR genérico sem rationale** — "o sistema deve ser seguro" sem explicar por que, a partir de quê (viola GR-SA-6).
- **Risco técnico citado na fonte, mas ausente do Solution Design** (viola GR-SA-7).
- **Solution Design marcado como aprovado** pelo próprio agente, sem passar por revisão humana (viola RULE-SA-9).

## Como usar este documento

Ao avaliar (`evaluation.md`) ou revisar manualmente uma saída do agente, comparar contra os dois padrões acima antes de aceitar o Solution Design como rascunho válido para o Product Owner consumir.
