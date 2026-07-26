# Architecture Decision Records (ADR)

> Base consultada por `generate_architecture_decisions` — todo ADR gerado pelo agente segue esta estrutura, com trade-offs sempre explícitos (GR-SA-4).

## O que é

Prática popularizada por Michael Nygard (2011) para registrar decisões arquiteturais relevantes de forma curta, versionável e datada, junto do código-fonte ou da documentação do projeto. Um ADR não é um documento de arquitetura completo — é o registro de **uma** decisão específica, o contexto que a motivou e as alternativas consideradas.

## Estrutura de um ADR

- **Título** — frase curta descrevendo a decisão (ex.: "Usar Event-Driven Architecture para integração entre módulos de pedido e estoque").
- **Contexto** — a situação/problema que exige uma decisão; forças em jogo (restrições técnicas, de negócio, de equipe).
- **Decisão** — a escolha feita, de forma direta e afirmativa.
- **Alternativas consideradas** — outras opções viáveis que foram avaliadas e não escolhidas, com o porquê (GR-SA-4: sempre explicitar trade-offs quando houver mais de uma solução viável — nunca apresentar a decisão como se fosse a única possível).
- **Consequências** — o que passa a ser verdade depois da decisão, incluindo trade-offs aceitos (não só benefícios).

## Por que existe

Decisões arquiteturais tomadas sem registro tendem a ser questionadas ou revertidas por falta de contexto ("por que fizemos assim?"), especialmente quando quem decidiu já não está mais no time. O ADR torna a decisão auditável e revisável no futuro, com o contexto da época preservado.

## Relevância para este agente

GR-SA-3 exige que toda decisão arquitetural relevante tenha um ADR (ou equivalente) — `generate_architecture_decisions` é a skill responsável por produzir esses registros como parte do Solution Design Document, nunca deixando uma escolha de arquitetura sem justificativa registrada.
