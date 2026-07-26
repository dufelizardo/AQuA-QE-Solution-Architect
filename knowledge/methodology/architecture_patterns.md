# Catálogo de Padrões Arquiteturais

> Base consultada por `identify_architecture_pattern` — o agente só recomenda um padrão **desta lista**, nunca inventa um padrão fora dela (GR-SA-1). Cada entrada tem descrição, quando usar e trade-offs, para fundamentar `pattern_rationale` e os `alternatives_considered` de um ADR.

## Layered Architecture (Arquitetura em Camadas)

- **Descrição**: organiza o sistema em camadas horizontais (ex.: apresentação, aplicação, domínio, infraestrutura), cada uma dependendo apenas da camada imediatamente abaixo.
- **Quando usar**: sistemas de complexidade baixa a média, equipes pequenas, requisitos estáveis.
- **Trade-offs**: simples de entender e testar por camada; pode incentivar acoplamento vertical excessivo e dificultar mudanças que cruzam várias camadas.

## Hexagonal Architecture (Ports & Adapters)

- **Descrição**: isola a lógica de domínio no centro, comunicando-se com o mundo externo (banco, UI, filas, APIs) através de portas (interfaces) e adaptadores.
- **Quando usar**: quando é importante trocar/testar infraestrutura (banco, mensageria, provedores externos) sem alterar a lógica de negócio.
- **Trade-offs**: alta testabilidade e baixo acoplamento a frameworks; mais indireção e curva de aprendizado inicial.

## Clean Architecture

- **Descrição**: variação da Hexagonal com camadas concêntricas explícitas (entidades, casos de uso, adaptadores de interface, frameworks/drivers) e a regra de dependência sempre apontando para dentro.
- **Quando usar**: sistemas de longa vida, onde a lógica de negócio deve sobreviver a trocas de framework/UI/banco.
- **Trade-offs**: excelente separação de responsabilidades; overhead de estrutura para sistemas pequenos ou de vida curta.

## Onion Architecture

- **Descrição**: similar à Clean Architecture — domínio no centro, serviços de domínio, serviços de aplicação e infraestrutura nas camadas externas.
- **Quando usar**: domínios de negócio ricos e complexos (DDD), onde o modelo de domínio precisa ficar isolado de detalhes técnicos.
- **Trade-offs**: reforça DDD naturalmente; mais cerimônia do que necessário para CRUDs simples.

## Microservices

- **Descrição**: decompõe o sistema em serviços pequenos, independentes, cada um dono do seu próprio dado, comunicando-se via rede (REST, mensageria, eventos).
- **Quando usar**: múltiplas equipes autônomas, necessidade de escalar/deployar partes do sistema independentemente, domínios com fronteiras (bounded contexts) bem definidas.
- **Trade-offs**: escalabilidade e autonomia de deploy por serviço; complexidade operacional real (observabilidade, consistência distribuída, versionamento de contratos) — nunca recomendar sem essa contrapartida explícita.

## Modular Monolith

- **Descrição**: um único deployável, mas com módulos internos fortemente coesos e fracamente acoplados, com fronteiras de módulo explícitas (ex.: por bounded context).
- **Quando usar**: equipe única ou poucas equipes, domínio ainda não totalmente estável, quando a complexidade operacional de microservices não se justifica ainda.
- **Trade-offs**: simplicidade operacional de um monólito com disciplina de modularidade; exige disciplina de equipe para não degradar em "big ball of mud" (ver `anti_patterns` — fora desta fase).

## Event-Driven Architecture

- **Descrição**: componentes se comunicam publicando e reagindo a eventos, geralmente via um broker (Kafka, RabbitMQ, SNS/SQS), em vez de chamadas diretas.
- **Quando usar**: fluxos assíncronos por natureza, necessidade de desacoplar produtores/consumidores, múltiplos consumidores para o mesmo evento.
- **Trade-offs**: desacoplamento forte e escalabilidade; consistência eventual e depuração de fluxo mais difícil (rastrear um evento através de vários serviços).

## Service-Oriented Architecture (SOA)

- **Descrição**: serviços de granularidade maior que microservices, tipicamente integrados via um barramento corporativo (ESB) com contratos formais.
- **Quando usar**: integração de sistemas legados heterogêneos em ambientes corporativos já estruturados dessa forma.
- **Trade-offs**: reaproveitamento de serviços corporativos; o ESB pode virar gargalo/ponto único de falha se mal dimensionado.

## Serverless

- **Descrição**: funções ou serviços gerenciados pelo provedor de nuvem (FaaS), sem gestão direta de servidor, escalando automaticamente por invocação.
- **Quando usar**: cargas de trabalho esporádicas/variáveis, quando minimizar operação de infraestrutura é prioridade.
- **Trade-offs**: custo proporcional ao uso e zero gestão de servidor; cold starts, limites de execução do provedor e potencial vendor lock-in.

## CQRS (Command Query Responsibility Segregation)

- **Descrição**: separa o modelo de escrita (comandos) do modelo de leitura (queries), podendo inclusive usar armazenamentos diferentes para cada um.
- **Quando usar**: cargas de leitura e escrita muito assimétricas, ou quando o modelo de leitura precisa ser otimizado/desnormalizado de forma diferente do de escrita.
- **Trade-offs**: leituras otimizadas e escrita focada em regras de negócio; duplica a complexidade de manter dois modelos sincronizados.

## Event Sourcing

- **Descrição**: em vez de guardar o estado atual, guarda a sequência de eventos que levou a esse estado; o estado é reconstruído reproduzindo os eventos.
- **Quando usar**: quando auditoria completa/histórico de mudanças é um requisito de negócio, ou quando reconstituir estado passado é valioso.
- **Trade-offs**: auditabilidade total e rastreabilidade histórica; maior complexidade de leitura (geralmente combinado com CQRS) e de evolução de schema de eventos.

## Backend for Frontend (BFF)

- **Descrição**: uma camada de backend dedicada a um tipo específico de cliente (web, mobile), agregando/formatando chamadas a serviços de domínio para as necessidades daquele cliente.
- **Quando usar**: clientes com necessidades de dados/performance muito diferentes (ex.: mobile vs. web) consumindo os mesmos serviços de domínio.
- **Trade-offs**: evita que um único contrato genérico sirva mal a todos os clientes; mais um componente para manter e versionar.

## API Gateway

- **Descrição**: ponto de entrada único para clientes externos, cuidando de roteamento, autenticação, rate limiting e agregação de chamadas a serviços internos.
- **Quando usar**: arquiteturas com múltiplos serviços internos que precisam de uma fachada unificada para consumidores externos.
- **Trade-offs**: centraliza cross-cutting concerns (auth, rate limit, observabilidade); pode virar ponto único de falha ou gargalo se não dimensionado/replicado corretamente.

## Sidecar Pattern

- **Descrição**: um processo auxiliar roda ao lado do serviço principal (mesmo host/pod), cuidando de responsabilidades transversais (proxy, observabilidade, mTLS) sem alterar o código do serviço.
- **Quando usar**: ambientes com orquestração de containers (Kubernetes), quando se quer adicionar capacidades transversais sem tocar no código de cada serviço (ex.: service mesh).
- **Trade-offs**: reaproveitamento de infraestrutura transversal sem invadir o código do serviço; overhead operacional e de recursos por instância.
