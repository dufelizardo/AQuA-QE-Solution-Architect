# Context Engineering

> Estrutura conforme `../standards/context_engineering_standard.md`.

## Fontes de contexto (Fase 1)

- **`knowledge/methodology/`** — sempre disponível; base para o catálogo de padrões arquiteturais, categorias de NFR (ISO/IEC 25010) e estrutura de ADR. Pequeno o suficiente (3 arquivos) para caber direto no prompt de cada skill — sem RAG nesta fase.
- **`knowledge/templates/`** — estrutura de saída (`solution_design.md`).
- **Saída de skills anteriores na mesma execução** — ex.: `identify_architecture_pattern` alimenta `generate_architecture_decisions`, que também recebe os componentes/integrações de `identify_components_and_integrations`.

## Fora desta fase

- **`knowledge/domain/`** e **`retrieve_chunks`** (RAG) — deferidos até o volume de conhecimento (ex.: catálogo completo de patterns/anti-patterns das 7 categorias adicionais) exceder o que cabe direto no prompt. Ver `WHITEPAPER.md`, seção 11.
- **Memória de projeto/longo prazo** — ver `memory.md`.

## Orçamento de tokens

- Prioridade de alocação: (1) instruções fixas de persona/regras (`prompt.md`), (2) fonte de entrada sendo processada, (3) catálogo de metodologia relevante à skill em execução (ex.: só a lista de padrões para `identify_architecture_pattern`, não todo `knowledge/methodology/`), (4) formato de saída esperado.

## Ordenação no prompt final

1. Persona e objetivos.
2. Regras/guardrails.
3. Conhecimento de metodologia relevante à skill.
4. Entrada do usuário/fonte a processar.
5. Formato de saída esperado.

## Atualização/invalidação

Conhecimento de `knowledge/` é reconsultado a cada execução (não cacheado entre sessões diferentes).
