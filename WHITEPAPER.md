# AQuA-QE Solution Architect — Whitepaper

> Also available in [English](WHITEPAPER.en.md).

> Agente de arquitetura de soluções que gera Solution Design Documents (padrão arquitetural, componentes, integrações, requisitos não funcionais, riscos técnicos e decisões arquiteturais/ADRs) a partir de um PRD (gerado pelo agente irmão AQuA-QE Product Manager) ou fonte de requisitos equivalente — com rastreabilidade obrigatória à fonte, validação automática e revisão humana no centro do ciclo.

Repositório: [github.com/dufelizardo/AQuA-QE-Solution-Architect](https://github.com/dufelizardo/AQuA-QE-Solution-Architect)

---

## 1. Resumo executivo

Entre "temos um PRD aprovado" e "temos Épicos/User Stories prontos para o backlog" existe uma decisão que hoje é feita informalmente, na cabeça de quem escreve as histórias: qual padrão arquitetural usar, quais componentes e integrações o sistema precisa, quais requisitos não funcionais importam e por quê, quais riscos técnicos existem, e quais decisões de arquitetura foram tomadas — com quais alternativas descartadas e por quê. Quando essa decisão nunca é registrada explicitamente, o conhecimento fica preso na memória de quem participou da conversa, e as User Stories geradas a partir do PRD carregam suposições técnicas implícitas, nunca revisadas.

O AQuA-QE Solution Architect é um agente que estrutura essa decisão técnica em um artefato formal — o **Solution Design Document (SDD)** — sem remover a decisão humana do processo. A partir de uma fonte de requisitos (um PRD gerado pelo agente irmão AQuA-QE Product Manager, um arquivo `.txt`/Markdown, texto de chat, ticket Jira ou página Confluence), identifica o padrão arquitetural mais adequado (só entre um catálogo fechado de padrões reais, nunca inventado), os componentes e integrações citados/inferíveis no texto, os requisitos não funcionais categorizados conforme ISO/IEC 25010 com justificativa rastreável, os riscos técnicos identificáveis, e as decisões arquiteturais relevantes como ADRs com alternativas explícitas — valida automaticamente, submete a um segundo LLM como revisor independente, e só então apresenta o resultado para aprovação humana explícita. Nenhuma saída é aprovada pelo próprio agente.

Este é o terceiro agente da plataforma AQuA-QE, fechando a ponte que faltava entre o Product Manager (dono do PRD) e o Product Owner (dono de Épicos/Stories): "qual é a melhor solução técnica para atender este requisito de negócio?".

## 2. Fundamentação metodológica

Nenhum critério de qualidade usado pelo agente foi inventado. Cada um está documentado em `knowledge/methodology/` e é referenciado diretamente pelas regras e guardrails do agente:

| Framework | Papel no agente |
|---|---|
| **Catálogo de padrões arquiteturais** (`architecture_patterns.md`) | 14 padrões reais (Layered, Hexagonal, Clean, Onion, Microservices, Modular Monolith, Event-Driven, SOA, Serverless, CQRS, Event Sourcing, BFF, API Gateway, Sidecar), cada um com descrição, quando usar e trade-offs — a única fonte que `identify_architecture_pattern` pode escolher (GR-SA-1). |
| **ISO/IEC 25010** (`iso25010.md`) | As 6 categorias de requisito não funcional que `generate_non_functional_requirements` usa para categorizar cada NFR identificado. |
| **ADR / Architecture Decision Records** (`adr.md`) | Estrutura (contexto, decisão, alternativas consideradas, consequências) que `generate_architecture_decisions` segue para toda decisão arquitetural relevante. |

Esses documentos não são decoração: `identify_architecture_pattern` rejeita explicitamente (retorna `""`) qualquer resposta do LLM que não esteja no catálogo, e o formato de ADR é reforçado diretamente no prompt de `generate_architecture_decisions`/`refine_solution_design`.

## 3. Princípios de design (guardrails)

Oito guardrails, fornecidos originalmente como especificação do agente e de prioridade igual entre si — nenhum subordinado aos outros — governam o comportamento do agente (`docs/agent/guardrails.md`):

- **GR-SA-1 — Nunca inventar requisitos funcionais não presentes no PRD.** Todo componente, integração, NFR, risco ou decisão é rastreável à fonte; `identify_architecture_pattern` só escolhe entre o catálogo fechado.
- **GR-SA-2 — Nunca assumir integrações sem evidência documental.** `identify_components_and_integrations` deixa a lista vazia na ausência de evidência, em vez de supor "toda solução moderna provavelmente integra com X".
- **GR-SA-3 — Toda decisão arquitetural relevante deve possuir um ADR.** `validate_solution_design` reprova um Solution Design sem nenhuma decisão registrada.
- **GR-SA-4 — Sempre explicitar trade-offs entre alternativas.** Todo `ArchitectureDecision` tem `alternatives_considered`; o prompt nunca apresenta uma decisão como única opção possível quando não é o caso.
- **GR-SA-5 — Não recomendar tecnologias incompatíveis com os padrões da organização sem registrar a justificativa.** Cobertura parcial nesta fase: não existe ainda uma fonte de "padrões tecnológicos da organização" como entrada — documentado como guardrail que só se torna totalmente verificável em uma fase futura.
- **GR-SA-6 — Todo NFR deve ser rastreável a uma necessidade de negócio ou restrição técnica.** `rationale` é obrigatório em todo `NonFunctionalRequirement`.
- **GR-SA-7 — Nunca omitir riscos técnicos identificados.** `identify_technical_risks` é sempre executada e seu resultado nunca é descartado silenciosamente.
- **GR-SA-8 — Diagramas, componentes e contratos devem permanecer consistentes entre si.** Não aplicável nesta fase: diagramas (C4) e contratos de API não existem ainda no agente.
- **Guardrail transversal — Sem aprovação automática.** Independentemente dos oito acima serem satisfeitos, o agente nunca marca um Solution Design como "aprovado" — apenas como **rascunho validado** (`draft_validated`). A aprovação final é sempre um ato humano (mesmo princípio de GR-1 no Product Owner e GR-M no Product Manager).

Esses guardrails viram regras formais e verificáveis (`RULE-SA-1` a `RULE-SA-9` em `docs/agent/rules.md`).

## 4. Arquitetura

```
Entrada (.txt/Markdown/chat/Jira/Confluence)
   → read_text_file / parse_chat_transcript+format_chat_transcript (só chat) / read_jira_issue / read_confluence_page
   → extract_solution_context           (LLM gerador — título + contexto/problema)
   → identify_architecture_pattern      (LLM gerador — só entre o catálogo fechado, GR-SA-1)
   → identify_components_and_integrations (LLM gerador — GR-SA-2)
   → generate_non_functional_requirements  (LLM gerador — ISO/IEC 25010, GR-SA-6)
   → identify_technical_risks            (LLM gerador — GR-SA-7)
   → generate_architecture_decisions     (LLM gerador — ADRs com alternativas, GR-SA-3/GR-SA-4)
   → validate_solution_design            (checklist Python puro)
   → review_solution_design              (LLM revisor independente — phi4)
   → [se reprovado] generate_sdd_clarifying_questions → resposta humana → refine_solution_design → revalidar
   → aceite humano explícito
   → format_solution_design_markdown
```

Diferente do Product Owner (que processa em duas fases — Épico primeiro, Stories depois — para evitar gastar processamento caro antes de o Épico estar definido), o Solution Architect processa em uma única passada: não há uma unidade intermediária cara o suficiente para justificar um checkpoint de recepção antes da geração completa. `validate_solution_design` roda antes de `review_solution_design` pelo mesmo motivo de custo já estabelecido em PM/PO — nunca pagar o custo do LLM revisor por um Solution Design que já falha no checklist automático.

Camadas do código (`src/aqua_qe_solution_architect/`):

- **`models/`** — estruturas de dados: `SolutionDesign`, `NonFunctionalRequirement`, `ArchitectureDecision`, e o enum `ArtifactStatus` (`draft_validated` / `pending_clarification` / `accepted`).
- **`skills/`** — 16 funções, cada uma com um único efeito colateral e uma única responsabilidade (ver seção 5).
- **`workflow/generate_solution_design.py`** — `generate_solution_design` (gera o SDD do zero a partir do texto) e `finalize_solution_design` (aplica validate→review, reaproveitável também após `refine_solution_design`).
- **`orchestrator/solution_architect.py`** — ponto de entrada único (`handle_request(entrada)`).
- **`services/`** — integrações externas: `llm_service` (Ollama), `jira_service`/`confluence_service` (REST API + httpx, **apenas leitura** nesta fase — não há hoje um caso de uso real que exija escrever de volta em Jira/Confluence a partir deste agente).

Deliberadamente **não existem** nesta fase: uma camada de geração/renderização de diagramas C4, um parser de contratos de API/OpenAPI, parsers de UML/BPMN/Swagger/schema de banco, e as 7 categorias adicionais de patterns (design/integration/distributed/cloud/security/data) + biblioteca de anti-patterns que fizeram parte da especificação original completa do agente. Cada um desses itens tem valor real, mas depende de um consumidor real ainda inexistente (mesmo princípio de "não construir sem consumidor" já aplicado à camada `Feature` do Product Owner) — ver seção 11.

## 5. As 16 skills

Skills sem LLM (Python puro, determinísticas):

- `validate_solution_design` — checklist: título, contexto, padrão arquitetural com justificativa, ao menos um NFR, ao menos uma decisão arquitetural.
- `format_solution_design_markdown` — exporta o Solution Design Document em Markdown, seções conforme `knowledge/templates/solution_design.md`.
- `parse_chat_transcript`/`format_chat_transcript` — reconhecem e normalizam transcrições de chat multi-remetente na entrada `--texto`, sem alterar texto corrido sem remetente identificável.

Skills com LLM gerador (`OLLAMA_MODEL`, padrão `mistral`):

- `extract_solution_context`, `identify_architecture_pattern`, `identify_components_and_integrations`, `generate_non_functional_requirements`, `identify_technical_risks`, `generate_architecture_decisions`, `generate_sdd_clarifying_questions`, `refine_solution_design`.

Skills com LLM revisor independente (`OLLAMA_REVIEW_MODEL`, padrão `phi4` — deliberadamente um modelo diferente do gerador, para mitigar *self-preference bias*):

- `review_solution_design`.

Skills de I/O externo:

- `read_text_file` (disco), `read_jira_issue`/`read_confluence_page` (leitura, Jira/Confluence Cloud REST API — **nenhuma escrita nesta fase**, diferente do Product Owner, que também cria/atualiza tickets).

Detalhamento completo de entrada/saída/erros de cada skill em `docs/agent/skills.md`.

## 6. O ciclo de refinamento interativo

O mesmo princípio central do Product Owner se aplica aqui: quando a revisão aponta um problema, o agente não tenta se autocorrigir adivinhando a resposta certa.

1. `review_solution_design` reprova e produz `review_notes` — apontamentos concretos (ex.: "padrão escolhido não justifica bem o requisito de alta disponibilidade citado no PRD", "decisão sobre mensageria não registra alternativas consideradas").
2. `generate_sdd_clarifying_questions` transforma cada apontamento em uma pergunta objetiva e acionável.
3. O CLI (`run.py --refinar`) apresenta as perguntas no terminal; **um humano real responde**.
4. `refine_solution_design` reescreve os campos afetados usando as respostas como contexto real — preservando o texto/nível de detalhe dos campos que as respostas não abordam (mesmo cuidado aplicado desde o início do projeto, aprendido com um bug real corrigido em `refine_prd`/`refine_epic_metadata` no Product Owner).
5. O ciclo revalida (`validate_solution_design`/`review_solution_design`) e repete se necessário.
6. Ao final, um prompt pergunta explicitamente se o usuário **aceita** o Solution Design. Só esse aceite explícito muda o status para `accepted` — nunca o LLM, nunca o checklist automático (RULE-SA-9).

## 7. Modos de operação

- **Entrada única, artefato único** (`run.py`, sem `--modo`) — diferente de PM/PO, este agente não tem múltiplos modos de operação nesta fase: recebe uma fonte (`--arquivo`/`--texto`/`--jira`/`--confluence`) e produz um único Solution Design Document. O CLI sempre pergunta "Aceitar este Solution Design?" antes de exportar — só recusar o aceite impede a exportação.
- **`--refinar`** — liga o ciclo de perguntas/refinamento (seção 6), quando o Solution Design não sai aprovado na revisão, antes do aceite final (que é sempre perguntado, com ou sem esta flag).

## 8. Integrações reais

- **Jira Cloud** (REST API v3) — apenas leitura (`read_jira_issue`, convertendo Atlassian Document Format para texto puro). Sem escrita nesta fase — não há hoje um caso de uso real de write-back a partir de um Solution Design.
- **Confluence Cloud** (REST API v1) — apenas leitura de página (`read_confluence_page`), convertendo o storage format (XHTML) para texto puro via `html.parser.HTMLParser` da stdlib (sem dependência nova), mesmas credenciais do Jira.

## 9. Stack técnico

- **LLM local via Ollama** — `mistral` para geração, `phi4` como revisor independente. Escolha deliberada por modelos locais em vez de APIs de nuvem, configurável via `OLLAMA_MODEL`/`OLLAMA_REVIEW_MODEL`/`OLLAMA_BASE_URL`.
- **`uv`** para dependências — projeto standalone (repositório próprio, fora do monorepo que o originou), com `httpx` e `python-dotenv` declarados explicitamente em `pyproject.toml`.
- **Python 3.12+**, `src/` layout.
- **Sem banco vetorial/RAG nesta fase** — `knowledge/methodology/` tem apenas 3 arquivos, pequeno o suficiente para caber direto no prompt de cada skill sem necessidade de busca semântica (ver seção 11 e `docs/agent/context_engineering.md`).

## 10. Qualidade e cobertura de testes

46 testes automatizados cobrem todos os módulos implementados, todos com chamadas a Ollama/Jira/Confluence mockadas — rápidos, determinísticos, sem dependência de infraestrutura externa para rodar em CI. A avaliação do agente em produção combina três camadas que nunca se substituem (`docs/agent/evaluation.md`):

1. Checklist automático (`validate_solution_design`) — sem LLM.
2. LLM-como-juiz (`review_solution_design`) — modelo diferente do gerador.
3. Revisão humana obrigatória — único ato que efetivamente aprova um artefato.

## 11. O que ainda falta (deliberadamente adiado, não esquecido)

O usuário forneceu, ao especificar este agente, uma visão de produto madura e completa (14 responsabilidades, ~9 categorias de metodologia, 8 categorias de patterns + anti-patterns, 20+ artefatos, 12+ fontes de entrada, 15+ sistemas externos). A Fase 1 implementa deliberadamente só o núcleo — gerar o Solution Design Document a partir de texto — seguindo o mesmo princípio já aplicado a PM/PO: construir incrementalmente, um consumidor real de cada vez, nunca especulativamente. Fica para fases futuras:

- **Diagramas C4** e qualquer geração/renderização visual de arquitetura — GR-SA-8 (consistência entre diagramas/componentes/contratos) só se torna totalmente verificável quando esse artefato existir.
- **Contratos de API/OpenAPI/AsyncAPI/GraphQL** — nenhum parser ou gerador de contrato existe nesta fase.
- **Parsers de UML/BPMN/Swagger/schema de banco** — como fontes de entrada adicionais.
- **As 7 categorias adicionais de patterns** (design/integration/distributed/cloud/security/data) **e a biblioteca de anti-patterns** — só o catálogo de padrões arquiteturais (a categoria mais diretamente necessária para `identify_architecture_pattern`) foi construído nesta fase.
- **Integrações reais de escrita** — Jira/Confluence write-back, GitHub, GitLab, Kubernetes, Terraform, provedores de nuvem (AWS/Azure/GCP) — nenhuma tem hoje um consumidor real dentro do escopo da Fase 1.
- **`--sdd-existente`** (parser inverso do Markdown exportado) — mesmo padrão em que `--epic-existente`/`--story-existente` foram construídos como incremento *posterior* às features base no Product Owner, não desde o início.
- **GR-SA-5** (compatibilidade com padrões tecnológicos da organização) — não há hoje uma fonte de entrada de "padrões da empresa"; guardrail documentado, mas só totalmente verificável quando essa fonte existir.
- **RAG/memória de projeto** (`docs/agent/memory.md`) — `knowledge/methodology/` tem apenas 3 arquivos nesta fase, pequenos o suficiente para caber direto no prompt sem busca semântica; RAG fica para quando o catálogo de patterns crescer o suficiente para não caber mais.

## 12. Como executar

Ver `README.md`/`README.pt.md` para o passo a passo completo de instalação (Python 3.12+, `uv`, Ollama + modelos, `.env.example` → `.env`) e todos os exemplos de uso do `run.py` (`--arquivo`/`--texto`/`--jira`/`--confluence`, `--saida`, `--refinar`).

## 13. Conclusão

O AQuA-QE Solution Architect não busca substituir o arquiteto de soluções — busca eliminar o trabalho mecânico de estruturar uma decisão técnica que, sem ele, ficaria implícita na cabeça de quem escreve as histórias derivadas do PRD. Cada guardrail do projeto (nunca inventar, nunca omitir risco, sempre justificar trade-offs, nunca aprovar sozinho) existe para que a saída do agente seja sempre um ponto de partida confiável para revisão humana, nunca um substituto dela. A Fase 1, deliberadamente restrita ao núcleo, é o primeiro incremento de uma visão de produto muito maior — construída, como os outros dois agentes da plataforma, um consumidor real de cada vez.

---

**Eduardo Felizardo Cândido**
Senior QA Automation Engineer | AI-driven Testing | Robot Framework & Python
