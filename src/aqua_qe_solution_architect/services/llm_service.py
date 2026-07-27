import json
import os

import ollama
from openai import OpenAI

_DEFAULT_MODEL = "mistral"
_DEFAULT_REVIEW_MODEL = "phi4"
_DEFAULT_NVIDIA_MODEL = "deepseek-ai/deepseek-v4-pro"
_DEFAULT_NVIDIA_REVIEW_MODEL = "meta/llama-3.3-70b-instruct"
_NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
# Fallback documentado se deepseek-v4-pro saturar por capacidade (mesma família do
# deepseek-v4-flash, que saturou no piloto do agente irmão AQuA-QE Product Manager):
# openai/gpt-oss-120b, confirmado acessível na mesma conta NVIDIA usada no piloto do PM —
# mas com status "Preview"/sem garantia lá. Motivou avaliar a Cerebras como provedor
# alternativo (ver LLM_PROVIDER=cerebras abaixo), onde gpt-oss-120b tem status "Production".

_DEFAULT_CEREBRAS_MODEL = "gpt-oss-120b"
_DEFAULT_CEREBRAS_REVIEW_MODEL = "zai-glm-4.7"
_CEREBRAS_BASE_URL = "https://api.cerebras.ai/v1"

# Sugestão a confirmar no Google AI Studio (aistudio.google.com) antes de confiar de
# verdade — não validado ao vivo ainda. gemini-2.5-flash (gerador, rápido/barato) e
# gemini-2.5-pro (revisor, mais forte em raciocínio/avaliação) — mesma família Gemini
# nos dois papéis (Google AI Studio não oferece modelos de terceiros como NVIDIA/Cerebras
# oferecem), mitigação de self-preference bias mais fraca aqui do que nos outros
# provedores, mas ainda são checkpoints/tiers distintos.
_DEFAULT_GOOGLE_MODEL = "gemini-2.5-flash"
_DEFAULT_GOOGLE_REVIEW_MODEL = "gemini-2.5-pro"
_GOOGLE_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Parâmetros de sampling recomendados pela NVIDIA por modelo NIM (build.nvidia.com/playground)
# — chaveados por nome do modelo, não por papel (gerador/revisor), para continuar corretos se
# um dos dois for trocado via NVIDIA_MODEL/NVIDIA_REVIEW_MODEL. Modelo sem entrada aqui usa a
# chamada sem parâmetros extras (só model/messages/response_format).
_NVIDIA_MODEL_PARAMS: dict[str, dict] = {
    "deepseek-ai/deepseek-v4-flash": {
        "temperature": 1,
        "top_p": 0.95,
        "max_tokens": 16384,
        "extra_body": {"chat_template_kwargs": {"thinking": True, "reasoning_effort": "high"}},
    },
}


def _nvidia_params(modelo: str) -> dict:
    return dict(_NVIDIA_MODEL_PARAMS.get(modelo, {}))


def _provider() -> str:
    return os.getenv("LLM_PROVIDER", "ollama")


def _ollama_client() -> ollama.Client:
    host = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return ollama.Client(host=host)


def _nvidia_client() -> OpenAI:
    return OpenAI(base_url=_NVIDIA_BASE_URL, api_key=os.environ["NVIDIA_API_KEY"])


def _cerebras_client() -> OpenAI:
    return OpenAI(base_url=_CEREBRAS_BASE_URL, api_key=os.environ["CEREBRAS_API_KEY"])


def _google_client() -> OpenAI:
    return OpenAI(base_url=_GOOGLE_BASE_URL, api_key=os.environ["GOOGLE_API_KEY"])


def generator_model() -> str:
    """Resolve o modelo gerador conforme o provedor ativo (LLM_PROVIDER=ollama|nvidia|cerebras|google)."""
    if _provider() == "nvidia":
        return os.getenv("NVIDIA_MODEL", _DEFAULT_NVIDIA_MODEL)
    if _provider() == "cerebras":
        return os.getenv("CEREBRAS_MODEL", _DEFAULT_CEREBRAS_MODEL)
    if _provider() == "google":
        return os.getenv("GOOGLE_MODEL", _DEFAULT_GOOGLE_MODEL)
    return os.getenv("OLLAMA_MODEL", _DEFAULT_MODEL)


def reviewer_model() -> str:
    """Resolve o modelo revisor conforme o provedor ativo (LLM_PROVIDER=ollama|nvidia|cerebras|google)."""
    if _provider() == "nvidia":
        return os.getenv("NVIDIA_REVIEW_MODEL", _DEFAULT_NVIDIA_REVIEW_MODEL)
    if _provider() == "cerebras":
        return os.getenv("CEREBRAS_REVIEW_MODEL", _DEFAULT_CEREBRAS_REVIEW_MODEL)
    if _provider() == "google":
        return os.getenv("GOOGLE_REVIEW_MODEL", _DEFAULT_GOOGLE_REVIEW_MODEL)
    return os.getenv("OLLAMA_REVIEW_MODEL", _DEFAULT_REVIEW_MODEL)


def _chat(modelo: str, messages: list[dict], json_mode: bool) -> str:
    provider = _provider()
    if provider in ("nvidia", "cerebras", "google"):
        kwargs = _nvidia_params(modelo) if provider == "nvidia" else {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        if provider == "nvidia":
            cliente = _nvidia_client()
        elif provider == "cerebras":
            cliente = _cerebras_client()
        else:
            cliente = _google_client()
        resposta = cliente.chat.completions.create(model=modelo, messages=messages, **kwargs)
        return resposta.choices[0].message.content

    kwargs = {"format": "json"} if json_mode else {}
    resposta = _ollama_client().chat(model=modelo, messages=messages, **kwargs)
    return resposta["message"]["content"]


def complete(prompt: str, system: str = "", model: str | None = None) -> str:
    """Envia um prompt ao provedor de LLM ativo (Ollama ou NVIDIA NIM) e retorna o texto de resposta."""
    modelo = model or generator_model()
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    return _chat(modelo, messages, json_mode=False)


def complete_json(prompt: str, system: str = "", model: str | None = None) -> dict:
    """Envia um prompt ao provedor de LLM ativo e retorna a resposta já parseada como JSON."""
    modelo = model or generator_model()
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": prompt})
    conteudo = _chat(modelo, messages, json_mode=True)
    try:
        return json.loads(conteudo)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Resposta do LLM não é um JSON válido: {conteudo!r}") from exc
