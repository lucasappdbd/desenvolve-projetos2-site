import pytest

# Testes página inicial e cadastro/login básicos

def login(client, email, senha):
    return client.post("/login", data={"email": email, "senha": senha}, follow_redirects=True)

def logout(client):
    return client.get("/logout", follow_redirects=True)

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Página Inicial" in response_text

def test_cadastro_usuario(client):
    response = client.post("/cadastro", data={
        "nome": "Novo",
        "sobrenome": "Usuario",
        "email": "novo@example.com",
        "senha": "senha123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Cadastro realizado com sucesso" in response_text

def test_login_sucesso(client):
    response = login(client, "teste@example.com", "123456")
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Página Inicial" in response_text

def test_login_falha(client):
    response = login(client, "teste@example.com", "senha_errada")
    response_text = response.data.decode('utf-8')
    assert "Email ou senha inválidos" in response_text

def test_logout(client):
    login(client, "teste@example.com", "123456")
    response = logout(client)
    response_text = response.data.decode('utf-8')
    assert "Você saiu da sua conta" in response_text

# Testes para avaliações

def test_avaliacao_com_login(client, app):
    login(client, "teste@example.com", "123456")

    response = client.post("/avaliacoes", data={
        "livro": "livro-teste",
        "nota": "5",
        "comentario": "Ótimo livro!"
    }, follow_redirects=True)

    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert "Avaliação enviada com sucesso" in response_text

def test_editar_avaliacao(client, app):
    login(client, "teste@example.com", "123456")
    
    from app.models.models import Review, Book, User, db
    with app.app_context():
        user = User.query.filter_by(email="teste@example.com").first()
        book = Book.query.first()
        review = Review.query.filter_by(user_id=user.id, book_id=book.id).first()
        if not review:
            review = Review(rating=3, comment="Comentário inicial", author=user, book=book)
            db.session.add(review)
            db.session.commit()
        review_id = review.id

    response = client.post("/avaliacoes/editar", data={
        "avaliacao_id": review_id,
        "nota": 4,
        "comentario": "Comentário editado"
    }, follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Avaliação atualizada com sucesso" in response_text

def test_excluir_avaliacao(client, app):
    login(client, "teste@example.com", "123456")

    from app.models.models import Review, Book, User, db
    with app.app_context():
        user = User.query.filter_by(email="teste@example.com").first()
        book = Book.query.first()
        review = Review.query.filter_by(user_id=user.id, book_id=book.id).first()
        if not review:
            review = Review(rating=3, comment="Comentário para exclusão", author=user, book=book)
            db.session.add(review)
            db.session.commit()
        review_id = review.id

    response = client.post(f"/avaliacoes/{review_id}/delete", follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Avaliação excluída com sucesso" in response_text

# Testes para perfil do usuário

def test_acesso_perfil_sem_login(client):
    response = client.get("/perfil", follow_redirects=True)
    response_text = response.data.decode('utf-8')
    assert "Login" in response_text  # redireciona para login


def test_atualizar_perfil(client):
    login(client, "teste@example.com", "123456")

    response = client.post("/perfil", data={
        "nome": "NomeEditado",
        "sobrenome": "SobrenomeEditado",
        "email": "teste@example.com",
        "senha": ""
    }, follow_redirects=True)

    response_text = response.data.decode('utf-8')
    assert "Perfil atualizado com sucesso" in response_text