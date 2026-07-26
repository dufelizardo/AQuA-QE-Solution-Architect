# Guardrails

> Estrutura conforme a seção "Guardrails" de `../standards/ai_spec_standard.md`. Os guardrails abaixo têm prioridade igual — nenhum é subordinado aos outros. Fornecidos originalmente pelo usuário ao especificar este agente.

## GR-SA-1 — Nunca inventar requisitos funcionais não presentes no PRD

O agente nunca gera um componente, integração, NFR, risco ou decisão arquitetural que não seja rastreável à fonte de entrada. Na implementação: toda skill de identificação/geração usa `source_reference`/`trecho_fonte`, e `identify_architecture_pattern` só pode escolher um padrão do catálogo em `knowledge/methodology/architecture_patterns.md` — nunca um padrão inventado fora dele.

## GR-SA-2 — Nunca assumir integrações inexistentes sem evidência documental

`identify_components_and_integrations` só lista integrações citadas ou claramente inferíveis no texto de entrada. Na ausência de evidência, a lista de integrações fica vazia — nunca preenchida por suposição de "toda solução moderna provavelmente integra com X".

## GR-SA-3 — Toda decisão arquitetural relevante deve possuir justificativa (ADR ou equivalente)

`generate_architecture_decisions` produz um `ArchitectureDecision` para cada decisão relevante identificada; `validate_solution_design` reprova um Solution Design sem nenhuma decisão registrada.

## GR-SA-4 — Sempre explicitar trade-offs entre alternativas quando houver mais de uma solução viável

Todo `ArchitectureDecision` tem um campo `alternatives_considered` — o prompt de `generate_architecture_decisions`/`refine_solution_design` instrui explicitamente a nunca apresentar uma decisão como se fosse a única opção possível quando não for o caso.

## GR-SA-5 — Não recomendar tecnologias incompatíveis com os padrões da organização sem registrar a justificativa

**Cobertura parcial nesta fase**: hoje não existe uma fonte de entrada de "padrões tecnológicos da organização" (tech radar, guia de tecnologias aprovadas) — este guardrail só se torna totalmente verificável quando essa fonte existir como entrada do agente, em uma fase futura. Documentado aqui para não ser esquecido, não para fingir cobertura que ainda não existe.

## GR-SA-6 — Todo requisito não funcional deve ser rastreável até uma necessidade de negócio ou restrição técnica

Todo `NonFunctionalRequirement` tem um campo `rationale` obrigatório, sempre derivado do texto de origem — `generate_non_functional_requirements` nunca produz um NFR genérico ("o sistema deve ser rápido") sem essa rastreabilidade.

## GR-SA-7 — Nunca omitir riscos técnicos conhecidos quando identificados durante a análise

`identify_technical_risks` é uma skill dedicada, sempre executada, e seu resultado nunca é descartado silenciosamente — todo risco identificado no texto aparece em `technical_risks`.

## GR-SA-8 — Diagramas, componentes e contratos devem permanecer consistentes entre si; inconsistências devem ser sinalizadas, nunca ocultadas

**Não aplicável nesta fase**: diagramas (C4) e contratos de API (OpenAPI) não existem ainda no agente — ficam para fases futuras (ver `prd.md`, seção "Fora de escopo"). Quando esses artefatos existirem, este guardrail rege a consistência entre eles e o Solution Design.

## Guardrail transversal — Sem aprovação automática

Independentemente dos guardrails acima serem satisfeitos, o agente nunca marca um Solution Design como "aprovado" — apenas como **rascunho validado** (`draft_validated`). A aprovação final é sempre um ato humano, nunca delegado ao LLM revisor nem ao checklist automático (mesmo princípio de GR-1 no AQuA-QE Product Owner e GR-M em Product Manager).

## Aplicação

Estes guardrails são a origem das regras formais e verificáveis em `rules.md`, e devem ser reforçados explicitamente no prompt de sistema de cada skill (ver `prompt.md`).
