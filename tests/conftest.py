import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db
from app.models.models import User, Book

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
    })

    with app.app_context():
        db.create_all()

        # Usuário de teste
        user = User(nome="Teste", sobrenome="User", email="teste@example.com")
        user.set_password("123456")
        db.session.add(user)

        # Livro de teste
        book = Book(title="Livro Teste", slug="livro-teste")
        db.session.add(book)

        db.session.commit()

    yield app

    # Teardown
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()