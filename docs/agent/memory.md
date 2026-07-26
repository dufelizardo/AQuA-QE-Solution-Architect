# Memory

> Estrutura conforme `../standards/memory_standard.md`. Decisão de produto nesta fase: **sem memória persistente** — cada execução é independente.

## Por que não há memória nesta fase

O agente processa uma fonte por execução (um PRD → um Solution Design). Diferente do Product Owner (que acumula contexto entre stories de um mesmo Epic), não há hoje um caso de uso real que exija lembrar decisões entre execuções distintas — construir memória sem esse consumidor real seria especulativo (mesmo princípio de "não construir sem consumidor" já aplicado a `services/` em PM/PO).

## Memória de sessão (curto prazo) — a única existente

- **O que**: as respostas do usuário durante o ciclo de refinamento (`--refinar`) da execução corrente.
- **Onde**: contexto da execução corrente, não persistido além dela.
- **Expiração**: descartada ao final da execução.

## Candidatos a memória futura (não implementados, não esquecidos)

- **Memória de projeto**: se o agente passar a processar múltiplos PRDs relacionados de um mesmo produto, lembrar decisões arquiteturais já tomadas (ex.: "já decidimos usar Microservices para este produto") evitaria recomendações inconsistentes entre Solution Designs irmãos.
- **Memória de longo prazo**: preferências de um arquiteto específico (ex.: nível de detalhe preferido nos ADRs).

## Relação com o manifesto do agente

`agent_manifest.yaml` reflete esta decisão: `vector`/`rag`/`knowledge_graph` todos `false` nesta fase.
