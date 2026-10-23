import os
import tempfile
import pytest
## Testes para a aplicação Flask
@pytest.fixture()
def client():
    import app as app_module
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    app_module.DATABASE = __import__("pathlib").Path(db_path)
    app_module.app.config.update(TESTING=True, SECRET_KEY="test-secret")
    app_module.inicializar_banco()
    with app_module.app.test_client() as client:
        yield client
    os.unlink(db_path)

# Testes de rotas e funcionalidades da aplicação
def test_home_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Gest\xc3\xa3o de Registros" in response.data


def test_create_and_list_record(client):
    response = client.post("/registros/novo", data={
        "titulo": "Doação de materiais escolares",
        "categoria": "Doações",
        "descricao": "Materiais para a comunidade",
        "status": "Ativo",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Doação de materiais escolares".encode() in response.data


def test_title_is_required(client):
    response = client.post("/registros/novo", data={
        "titulo": " ", "categoria": "Doações", "descricao": "", "status": "Ativo"
    })
    assert response.status_code == 200
    assert "O título é obrigatório.".encode() in response.data


def test_form_exposes_native_validation_and_character_guidance(client):
    response = client.get("/registros/novo")

    assert response.status_code == 200
    assert b"required autofocus" in response.data
    assert b"maxlength=\"120\"" in response.data
    assert b"maxlength=\"1000\"" in response.data
    assert b"0 / 1.000 caracteres" in response.data
    assert b"novalidate" not in response.data


# Teste de validação de campos do formulário
def test_filter_by_category(client):
    client.post("/registros/novo", data={
        "titulo": "Mutirão comunitário", "categoria": "Atividades",
        "descricao": "Ação local", "status": "Ativo"
    })
    response = client.get("/registros?categoria=Atividades")
    assert response.status_code == 200
    assert "Mutirão comunitário".encode() in response.data


def test_empty_filtered_results_offer_to_clear_filters(client):
    response = client.get("/registros?q=inexistente")

    assert response.status_code == 200
    assert "Nenhum resultado encontrado".encode() in response.data
    assert "Limpar filtros".encode() in response.data
    assert "Cadastrar primeiro registro".encode() not in response.data


# Teste de exclusão de registro
def test_missing_record_returns_404(client):
    response = client.get("/registros/999/editar")
    assert response.status_code == 404
