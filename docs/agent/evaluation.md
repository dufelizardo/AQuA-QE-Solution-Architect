# Evaluation

> Estrutura conforme `../standards/evaluation_standard.md`. Decisão de produto: avaliação combina checklist automático, revisão por um segundo LLM e revisão humana obrigatória (nenhum substitui o outro).

## Métricas

- **Taxa de aprovação automática** — % de Solution Designs gerados que passam no checklist (`validation_checklist.md`) sem interrupção por ambiguidade.
- **Taxa de aceitação sem retrabalho** — % de Solution Designs em `draft_validated` aceitos pelo arquiteto/PO sem edição substancial (métrica de sucesso do PRD).
- **Cobertura de rastreabilidade** — % de NFRs/riscos/decisões com `rationale`/`source_reference` preenchido a partir da fonte real, não vazio.
- **Taxa de explicitação de trade-offs** — % de decisões arquiteturais (`ArchitectureDecision`) com `alternatives_considered` não vazio (GR-SA-4).

## Casos de teste

- **Caminho feliz** — fonte clara (PRD com contexto, integrações e riscos explícitos); deve gerar um Solution Design `draft_validated` sem interrupção.
- **Padrão fora do catálogo** — se o LLM alucinar um padrão não listado em `architecture_patterns.md`, `identify_architecture_pattern` deve rejeitá-lo (retornar vazio), nunca aceitar (GR-SA-1).
- **Fonte sem integrações claras** — `identify_components_and_integrations` deve retornar lista vazia, nunca assumir uma integração "provável" (GR-SA-2).
- **NFR sem justificativa** — deve ser rejeitado/sinalizado; todo NFR aceito precisa de `rationale` (GR-SA-6).
- **Solution Design sem nenhuma decisão registrada** — `validate_solution_design` deve reprovar (GR-SA-3).
- **Risco técnico explícito no texto** — deve aparecer em `technical_risks`, nunca ser omitido (GR-SA-7).

## Método de avaliação

1. **Checklist automático** (`validate_solution_design`) — roda em toda execução, aplicando `validation_checklist.md`. Sem LLM.
2. **LLM-como-juiz** (`review_solution_design`) — roda após o checklist automático aprovar; usa um modelo diferente do gerador (`OLLAMA_REVIEW_MODEL`, padrão `phi4`, enquanto as skills de geração usam `mistral`) para evitar self-preference bias. Reprova Solution Designs com justificativa vaga, NFRs genéricos ou trade-offs não explicitados; os problemas apontados ficam em `SolutionDesign.review_notes`.
3. **Revisão humana obrigatória** — todo Solution Design `draft_validated` passa por aceite humano explícito antes de ser exportado; feedback da revisão alimenta a métrica de taxa de aceitação.

## Frequência

- Casos de teste automatizados rodam a cada mudança em prompt, regras ou skills que possam afetar comportamento (ver `prompt.md`, `rules.md`).
- Métricas de aceitação humana são agregadas continuamente a partir do uso real do agente.

## Critério de aprovação de uma nova versão do agente

Uma nova versão do prompt/regras/skills só substitui a anterior se não piorar a taxa de aceitação sem retrabalho nem a taxa de aprovação automática nos casos de teste de regressão.

## Registro de regressões

Toda falha encontrada em uso real (ex.: padrão fora do catálogo aceito, NFR sem rationale, decisão sem alternativas quando havia mais de uma opção viável) vira um novo caso de teste permanente nesta lista.
