from ..models import DomainEntity
from ..services.llm_service import complete_json

_SYSTEM = (
    "Você identifica as principais entidades do modelo de domínio (ex.: "
    "Paciente, Consulta) a partir de um texto de requisitos, com os "
    "atributos de cada uma. Uma entidade e seus atributos só existem se "
    "evidenciados ou claramente inferíveis do texto — nunca invente uma "
    "entidade ou atributo não sustentado por ele. Se não houver entidades "
    "identificáveis, responda com uma lista vazia."
)


def identify_domain_model(texto: str) -> list[DomainEntity]:
    """Identifica as principais entidades do modelo de domínio e seus atributos (GR-SA-1: nunca inventar entidade/atributo sem lastro no texto)."""
    prompt = (
        f"Texto:\n{texto}\n\n"
        'Responda apenas em JSON: {"entidades": [{"nome": "...", '
        '"atributos": ["..."], "trecho_fonte": "..."}]}'
    )
    dados = complete_json(prompt, system=_SYSTEM)
    return [
        DomainEntity(
            name=item.get("nome", ""),
            attributes=item.get("atributos", []),
            source_reference=item.get("trecho_fonte", ""),
        )
        for item in dados.get("entidades", [])
    ]
