from ..services.llm_service import complete_json

_PADROES_DISPONIVEIS = [
    "Layered Architecture",
    "Hexagonal Architecture (Ports & Adapters)",
    "Clean Architecture",
    "Onion Architecture",
    "Microservices",
    "Modular Monolith",
    "Event-Driven Architecture",
    "Service-Oriented Architecture (SOA)",
    "Serverless",
    "CQRS",
    "Event Sourcing",
    "Backend for Frontend (BFF)",
    "API Gateway",
    "Sidecar Pattern",
]

# Resumo de knowledge/methodology/architecture_patterns.md (descrição + quando usar),
# reaproveitado também por identify_components_and_integrations e generate_architecture_decisions
# para fundamentar decomposição de componentes e alternativas de ADR — nunca inventado à parte do catálogo.
_DESCRICOES_PADROES: dict[str, str] = {
    "Layered Architecture": (
        "Organiza o sistema em camadas horizontais (ex.: apresentação, aplicação, domínio, "
        "infraestrutura), cada uma dependendo só da camada abaixo. Indicado para sistemas de "
        "complexidade baixa a média, equipes pequenas, requisitos estáveis."
    ),
    "Hexagonal Architecture (Ports & Adapters)": (
        "Isola a lógica de domínio no centro, comunicando-se com banco/UI/filas/APIs via portas "
        "(interfaces) e adaptadores. Indicado quando é importante trocar/testar infraestrutura sem "
        "alterar a lógica de negócio."
    ),
    "Clean Architecture": (
        "Variação da Hexagonal com camadas concêntricas explícitas (entidades, casos de uso, "
        "adaptadores de interface, frameworks/drivers), dependência sempre apontando para dentro. "
        "Indicado para sistemas de longa vida."
    ),
    "Onion Architecture": (
        "Domínio no centro, serviços de domínio, serviços de aplicação e infraestrutura nas camadas "
        "externas. Indicado para domínios de negócio ricos e complexos (DDD)."
    ),
    "Microservices": (
        "Decompõe o sistema em serviços pequenos, independentes, cada um dono do seu próprio dado, "
        "comunicando-se via rede (REST, mensageria, eventos). Indicado para múltiplas equipes "
        "autônomas e domínios com bounded contexts bem definidos."
    ),
    "Modular Monolith": (
        "Um único deployável, com módulos internos fortemente coesos e fracamente acoplados, "
        "fronteiras de módulo explícitas (ex.: por bounded context). Indicado para equipe única ou "
        "poucas equipes, domínio ainda não totalmente estável."
    ),
    "Event-Driven Architecture": (
        "Componentes se comunicam publicando e reagindo a eventos via um broker (Kafka, RabbitMQ, "
        "SNS/SQS), em vez de chamadas diretas. Indicado para fluxos assíncronos por natureza e "
        "múltiplos consumidores para o mesmo evento."
    ),
    "Service-Oriented Architecture (SOA)": (
        "Serviços de granularidade maior que microservices, integrados via um barramento corporativo "
        "(ESB) com contratos formais. Indicado para integração de sistemas legados heterogêneos."
    ),
    "Serverless": (
        "Funções/serviços gerenciados pelo provedor de nuvem (FaaS), sem gestão direta de servidor. "
        "Indicado para cargas de trabalho esporádicas/variáveis."
    ),
    "CQRS": (
        "Separa o modelo de escrita (comandos) do modelo de leitura (queries), podendo usar "
        "armazenamentos diferentes para cada um. Indicado para cargas de leitura/escrita muito "
        "assimétricas."
    ),
    "Event Sourcing": (
        "Guarda a sequência de eventos que levou ao estado atual, em vez do estado em si; o estado é "
        "reconstruído reproduzindo os eventos. Indicado quando auditoria completa/histórico de "
        "mudanças é requisito de negócio."
    ),
    "Backend for Frontend (BFF)": (
        "Uma camada de backend dedicada a um tipo específico de cliente (web, mobile), agregando "
        "chamadas a serviços de domínio. Indicado quando clientes têm necessidades de dados/"
        "performance muito diferentes."
    ),
    "API Gateway": (
        "Ponto de entrada único para clientes externos, cuidando de roteamento, autenticação, rate "
        "limiting e agregação de chamadas a serviços internos."
    ),
    "Sidecar Pattern": (
        "Um processo auxiliar roda ao lado do serviço principal (mesmo host/pod), cuidando de "
        "responsabilidades transversais (proxy, observabilidade, mTLS) sem alterar o código do "
        "serviço. Indicado em ambientes com orquestração de containers (Kubernetes)."
    ),
}

_SYSTEM = (
    "Você é um arquiteto de soluções. Escolha, entre os padrões arquiteturais "
    "listados abaixo, o que melhor atende ao contexto descrito. Nunca "
    "recomende um padrão fora desta lista. Justifique a escolha com base no "
    "contexto informado, nunca com suposições não sustentadas pelo texto."
)


def identify_architecture_pattern(texto: str) -> tuple[str, str]:
    """Identifica o padrão arquitetural mais adequado — só entre os do catálogo (GR-SA-1) — e sua justificativa."""
    descricoes = "\n".join(f"- {nome}: {desc}" for nome, desc in _DESCRICOES_PADROES.items())
    prompt = (
        f"Padrões disponíveis:\n{descricoes}\n\n"
        f"Contexto:\n{texto}\n\n"
        'Responda apenas em JSON: {"padrao": "...", "justificativa": "..."}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    padrao = dados.get("padrao", "")
    if padrao not in _PADROES_DISPONIVEIS:
        padrao = ""
    return padrao, dados.get("justificativa", "")
