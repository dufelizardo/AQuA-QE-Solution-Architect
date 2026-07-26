# PRD — AQuA-QE Solution Architect

> Estrutura conforme `../standards/prd_standard.md`.

## Contexto e problema

Decisões arquiteturais tomadas informalmente, sem registro de contexto e alternativas, geram retrabalho: padrões escolhidos sem justificativa, requisitos não funcionais esquecidos até tarde, riscos técnicos descobertos só na implementação. Falta uma ponte formal entre "o que construir" (PRD, do Product Manager) e "como transformar em trabalho executável" (Épicos/Stories, do Product Owner) — decisões técnicas relevantes ficam implícitas, dependendo de quem programa "adivinhar" a arquitetura certa durante o desenvolvimento.

## Objetivo do produto

Gerar um Solution Design Document (SDD) a partir de um PRD (ou fonte de requisitos equivalente), cobrindo escolha de padrão arquitetural com justificativa, componentes e integrações identificados, requisitos não funcionais rastreáveis, riscos técnicos e decisões arquiteturais (ADRs) com trade-offs explícitos — com rastreabilidade total à fonte e revisão humana obrigatória antes de qualquer aceite.

## Público-alvo / personas

- **Solution Architect / Tech Lead** — usa o SDD gerado como ponto de partida para validar/ajustar a arquitetura antes de repassar ao time.
- **Product Owner** — consome o SDD aceito como contexto técnico ao quebrar o trabalho em Épicos/Stories.
- **Desenvolvedor** — consulta o SDD como referência de decisões arquiteturais já tomadas e seus porquês.

## Escopo (Fase 1)

- Ler fontes de entrada em arquivo de texto (`.txt`/Markdown), chat, Jira (leitura) ou Confluence (leitura).
- Extrair título e contexto do problema a partir da fonte.
- Identificar o padrão arquitetural mais adequado, escolhido apenas entre os do catálogo (`knowledge/methodology/architecture_patterns.md`).
- Identificar componentes de alto nível e integrações citadas/inferíveis.
- Gerar requisitos não funcionais categorizados conforme ISO/IEC 25010, cada um rastreável.
- Identificar riscos técnicos.
- Gerar decisões arquiteturais (ADRs) com alternativas consideradas.
- Validar a saída contra um checklist automático antes de apresentá-la.
- Suportar ciclo de refinamento humano-no-loop (perguntas de esclarecimento → resposta humana → refino).
- Exportar o resultado em Markdown.

## Fora de escopo (Fase 1 — ver WHITEPAPER seção 11 para detalhe)

- Diagramas C4/UML/BPMN (geração ou leitura).
- Contratos de API (OpenAPI/Swagger), geração ou leitura.
- Parsers de UML, BPMN, Swagger, schema de banco de dados.
- Integrações reais com GitHub, GitLab, Azure DevOps, Kubernetes, Terraform, provedores de nuvem.
- Escrita/publicação em Jira ou Confluence (o agente só lê essas fontes).
- Carregar um SDD já existente para continuar dali (`--sdd-existente`) — parser inverso do exportador.
- As 7 categorias adicionais de patterns (design/integration/distributed/cloud/security/data) e `anti-patterns/`.
- RAG/memória de projeto ou longo prazo.

## Requisitos funcionais

1. Ler e interpretar entradas em arquivo de texto (`.txt`/Markdown), chat, Jira e Confluence.
2. Identificar título e contexto do problema a partir da fonte.
3. Identificar o padrão arquitetural mais adequado, só entre os do catálogo, com justificativa.
4. Identificar componentes de alto nível e integrações citadas/inferíveis.
5. Gerar requisitos não funcionais categorizados (ISO/IEC 25010), cada um com `rationale` rastreável.
6. Identificar riscos técnicos citados/inferíveis, sem omitir nenhum identificável.
7. Gerar decisões arquiteturais (ADRs) com alternativas consideradas e consequências.
8. Validar a saída contra um checklist automático (padrão + justificativa + ao menos 1 NFR + ao menos 1 ADR) antes de apresentá-la.
9. Revisar com um segundo LLM independente do gerador.
10. Quando a revisão reprovar, gerar perguntas de esclarecimento e refinar com as respostas humanas.
11. Exportar o resultado validado em Markdown.

## Requisitos não funcionais

- **Rastreabilidade** — todo campo gerado (padrão, componente, integração, NFR, risco, decisão) deve ser rastreável à fonte de entrada.
- **Nenhuma aprovação automática** — toda saída é um rascunho validado, sujeito a revisão humana obrigatória.
- **Consistência de formato** — toda saída segue o template em `../../knowledge/templates/solution_design.md`.

## Métricas de sucesso

- Redução do retrabalho arquitetural (decisões revisadas/revertidas após início da implementação).
- Taxa de aceitação sem retrabalho — % de Solution Designs gerados aceitos pelo time sem edição substancial.
- Cobertura de rastreabilidade — % de NFRs/riscos/decisões com `rationale`/`source_reference` preenchido a partir da fonte real.

## Riscos e premissas

- Premissa: a fonte de entrada (PRD ou equivalente) contém informação suficiente para identificar padrão arquitetural, componentes e NFRs na maioria dos casos; quando não contém, o agente deve refletir isso via justificativas fracas/vazias, sinalizadas na revisão, em vez de inventar.
- Risco: fontes de entrada muito informais ou incompletas podem limitar a qualidade da recomendação arquitetural.
- Risco: a ausência de uma fonte de "padrões tecnológicos da organização" (GR-SA-5) limita a capacidade do agente de avaliar compatibilidade organizacional nesta fase.
