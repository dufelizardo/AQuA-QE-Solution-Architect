# Template — Solution Design Document (SDD)

> Estrutura padrão, sem conteúdo de domínio. Ver `../../docs/agent/output_schema.md` para o schema de dados exato.

## Campos

- **ID**: `<identificador único, ex.: SDD-001>`
- **Título**: `<nome da solução>`
- **Contexto e problema**: `<o problema de negócio que motiva esta solução, herdado do PRD/fonte de entrada>`
- **Padrão arquitetural escolhido**: `<um item do catálogo em knowledge/methodology/architecture_patterns.md>`
- **Justificativa do padrão**: `<por que este padrão, e não outro, atende ao contexto>`
- **Componentes**: `<lista de componentes/serviços de alto nível identificados>`
- **Integrações**: `<lista de sistemas/serviços externos com os quais a solução precisa se comunicar>`
- **Requisitos não funcionais**: `<lista de NFRs, cada um com categoria (ISO 25010), descrição e rationale>`
- **Riscos técnicos**: `<lista de riscos identificados na fonte de entrada>`
- **Decisões arquiteturais (ADRs)**: `<lista de ArchitectureDecision — título, contexto, decisão, alternativas consideradas, consequências>`

## Relação com a hierarquia de artefatos

```
PRD (Product Manager)
 └── Solution Design Document (Solution Architect)
      └── Épico / User Story (Product Owner)
```

O SDD não substitui o PRD nem o Épico — é a ponte técnica entre "o que construir" e "como transformar em trabalho executável", explicitando as decisões de arquitetura que o PO precisa conhecer antes de quebrar o trabalho em histórias.
