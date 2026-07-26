import re

from ..services.confluence_service import update_page


def update_confluence_page(pagina: str, texto: str) -> None:
    """Atualiza uma página do Solution Design já existente no Confluence Cloud (aceita URL completa ou apenas o ID)."""
    match = re.search(r"/pages/(\d+)", pagina)
    page_id = match.group(1) if match else pagina
    update_page(page_id, texto)
