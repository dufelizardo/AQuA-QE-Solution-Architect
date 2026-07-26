from aqua_qe_solution_architect.skills import create_confluence_page as create_confluence_page_module
from aqua_qe_solution_architect.skills.create_confluence_page import create_confluence_page


def test_create_confluence_page_monta_url_a_partir_do_id(monkeypatch):
    monkeypatch.setenv("JIRA_BASE_URL", "https://example.atlassian.net/")

    def fake_create_page(space_key, title, texto, parent_page_id=None):
        assert space_key == "AQuAQE"
        assert title == "SAD - Mais Saúde Pública"
        assert parent_page_id == "1212417"
        return "999999"

    monkeypatch.setattr(create_confluence_page_module, "create_page", fake_create_page)

    url = create_confluence_page(
        "# texto", "SAD - Mais Saúde Pública", "AQuAQE", "1212417"
    )

    assert url == "https://example.atlassian.net/wiki/pages/viewpage.action?pageId=999999"
