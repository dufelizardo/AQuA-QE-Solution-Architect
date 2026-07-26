from ..services.llm_service import complete_json
from .identify_architecture_pattern import _DESCRICOES_PADROES

_SYSTEM = (
    "Você identifica componentes de alto nível e integrações com sistemas "
    "externos mencionados ou claramente inferíveis a partir de um texto de "
    "requisitos. Estruture os componentes de acordo com a decomposição "
    "típica do padrão arquitetural já escolhido (ex.: camadas para Layered/"
    "Clean/Onion, serviços independentes para Microservices, portas/"
    "adaptadores para Hexagonal, módulos para Modular Monolith, produtores/"
    "consumidores/broker para Event-Driven) — nunca uma lista solta e "
    "genérica. Cada componente e cada integração devem ser uma única "
    "string de texto (ex.: 'Agendamento: agendamento automatizado de "
    "consultas'), nunca um objeto/dicionário com campos separados. Nunca "
    "assuma uma integração que não tenha evidência no texto — se não "
    "houver integrações claras, responda com uma lista vazia."
)


def _para_string(item) -> str:
    """Defesa contra o LLM devolver um objeto em vez de string (ex.: {"nome": ..., "descricao": ...})."""
    if isinstance(item, dict):
        nome = item.get("nome", "")
        descricao = item.get("descricao", "")
        return f"{nome}: {descricao}" if descricao else nome
    return str(item)


def identify_components_and_integrations(texto: str, padrao: str) -> tuple[list[str], list[str]]:
    """Identifica componentes (estruturados conforme o padrão arquitetural escolhido) e integrações citadas/inferíveis no texto (GR-SA-2: nunca assumir integração sem evidência documental)."""
    descricao_padrao = _DESCRICOES_PADROES.get(padrao, "")
    prompt = (
        f"Padrão arquitetural escolhido: {padrao}\n"
        f"Descrição do padrão: {descricao_padrao}\n\n"
        f"Texto:\n{texto}\n\n"
        'Responda apenas em JSON: {"componentes": ["..."], "integracoes": ["..."]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    componentes = [_para_string(item) for item in dados.get("componentes", [])]
    integracoes = [_para_string(item) for item in dados.get("integracoes", [])]
    return componentes, integracoes
