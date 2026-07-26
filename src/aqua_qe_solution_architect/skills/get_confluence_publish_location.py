import re

from ..services.confluence_service import get_page_parent_context


def get_confluence_publish_location(pagina: str) -> tuple[str, str | None]:
    """A partir da página de origem do PRD (URL ou ID), retorna (espaço, id do ancestral imediato) para publicar o Solution Design como página irmã no mesmo local."""
    match = re.search(r"/pages/(\d+)", pagina)
    page_id = match.group(1) if match else pagina
    return get_page_parent_context(page_id)
