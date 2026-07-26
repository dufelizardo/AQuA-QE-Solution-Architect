# Rules

> Estrutura conforme `../standards/rules_standard.md`. Cada regra deriva de um guardrail (`guardrails.md`).

## RULE-SA-1

- **Descrição**: nenhum componente, integração, NFR, risco, decisão arquitetural, entidade de modelo de domínio ou fluxo de processo pode ser gerado sem origem rastreável na fonte de entrada; `identify_architecture_pattern` só pode escolher um padrão do catálogo em `knowledge/methodology/architecture_patterns.md`.
- **Gatilho**: geração de qualquer campo do Solution Design.
- **Ação esperada**: se a origem não for identificável, o campo fica vazio (padrão do dataclass) — nunca preenchido por suposição.
- **Severidade**: bloqueante.
- **Origem**: GR-SA-1.

## RULE-SA-2

- **Descrição**: `identify_components_and_integrations` só lista integrações com evidência clara no texto.
- **Gatilho**: conclusão de `identify_components_and_integrations`.
- **Ação esperada**: retornar lista vazia quando não houver evidência, nunca inferir integração "provável".
- **Severidade**: bloqueante.
- **Origem**: GR-SA-2.

## RULE-SA-3

- **Descrição**: todo Solution Design deve ter ao menos uma decisão arquitetural (`ArchitectureDecision`) registrada antes de ser apresentado.
- **Gatilho**: `validate_solution_design`.
- **Ação esperada**: reprovar (`pending_clarification`) um Solution Design sem nenhuma decisão registrada.
- **Severidade**: bloqueante.
- **Origem**: GR-SA-3.

## RULE-SA-4

- **Descrição**: toda decisão arquitetural deve explicitar alternativas consideradas quando mais de uma solução for viável.
- **Gatilho**: `generate_architecture_decisions`/`refine_solution_design`.
- **Ação esperada**: preencher `alternatives_considered`; nunca apresentar a decisão como única opção possível sem justificar por quê.
- **Severidade**: recomendação (verificado por `review_solution_design`, não pelo checklist automático — nem toda decisão tem alternativa real).
- **Origem**: GR-SA-4.

## RULE-SA-5

- **Descrição**: recomendações tecnológicas incompatíveis com padrões organizacionais exigem justificativa registrada.
- **Gatilho**: N/A nesta fase — não há fonte de "padrões da organização" como entrada.
- **Ação esperada**: reavaliar quando essa fonte existir.
- **Severidade**: não verificável nesta fase.
- **Origem**: GR-SA-5.

## RULE-SA-6

- **Descrição**: todo `NonFunctionalRequirement` deve ter um `rationale` não vazio, rastreável ao texto de origem.
- **Gatilho**: `generate_non_functional_requirements`/`refine_solution_design`.
- **Ação esperada**: nunca produzir um NFR sem `rationale`.
- **Severidade**: bloqueante.
- **Origem**: GR-SA-6.

## RULE-SA-7

- **Descrição**: todo risco técnico identificável no texto de origem deve aparecer em `technical_risks`.
- **Gatilho**: conclusão de `identify_technical_risks`.
- **Ação esperada**: nunca descartar um risco identificado.
- **Severidade**: bloqueante.
- **Origem**: GR-SA-7.

## RULE-SA-8

- **Descrição**: diagramas, componentes e contratos devem permanecer consistentes entre si.
- **Gatilho**: N/A nesta fase — diagramas e contratos de API não existem ainda.
- **Ação esperada**: reavaliar quando esses artefatos existirem.
- **Severidade**: não verificável nesta fase.
- **Origem**: GR-SA-8.

## RULE-SA-9

- **Descrição**: nenhum artefato é marcado como "aprovado" pelo agente — apenas como "rascunho validado", independentemente de `finalize_solution_design` aprovar no checklist automático e na revisão.
- **Gatilho**: `validate_solution_design`/`review_solution_design` retornam aprovação.
- **Ação esperada**: rotular como rascunho validado (ver `output_schema.md`) e aguardar aceite humano explícito no CLI antes de qualquer exportação.
- **Severidade**: bloqueante.
- **Origem**: guardrail transversal "Sem aprovação automática" (`guardrails.md`).

## RULE-SA-10

- **Descrição**: publicar (`--publicar-confluence`) ou atualizar (`--atualizar-confluence`) uma página no Confluence nunca acontece automaticamente, e a página publicada é sempre irmã da página de origem do PRD (mesmo ancestral imediato), nunca em local arbitrário nem sobrescrevendo o PRD.
- **Gatilho**: `create_confluence_page`/`update_confluence_page` seriam chamadas.
- **Ação esperada**: o CLI (`run.py`) sempre pergunta confirmação explícita antes de publicar/atualizar; `get_confluence_publish_location` deriva espaço/ancestral da página de origem, nunca de configuração manual solta.
- **Severidade**: bloqueante.
- **Origem**: mesmo espírito do guardrail transversal "Sem aprovação automática" (`guardrails.md`), estendido às escritas no Confluence.

## RULE-SA-11

- **Descrição**: integrações candidatas (`candidate_integrations`, sugeridas por conhecimento de domínio) nunca são apresentadas como confirmadas ou evidenciadas — sempre distintas de `integrations` (que exige evidência textual, RULE-SA-2), sempre rotuladas como recomendação a confirmar.
- **Gatilho**: `identify_candidate_integrations`, `refine_solution_design`, `format_solution_design_markdown`.
- **Ação esperada**: manter `candidate_integrations` em campo e seção separados de `integrations`, nunca misturados; nunca afirmar que uma integração candidata é necessária ou decidida.
- **Severidade**: bloqueante.
- **Origem**: decisão de produto para cobrir integrações prováveis de domínio sem violar GR-SA-2 para integrações confirmadas.

## Resolução de conflitos

RULE-SA-1, RULE-SA-2, RULE-SA-3, RULE-SA-6, RULE-SA-7, RULE-SA-9, RULE-SA-10 e RULE-SA-11 são bloqueantes. RULE-SA-4 é recomendação verificada por revisão humana/LLM, não pelo checklist automático (nem toda decisão tem uma alternativa real a registrar). RULE-SA-5 e RULE-SA-8 ainda não são verificáveis nesta fase, por ausência das fontes/artefatos que as tornariam aplicáveis.
