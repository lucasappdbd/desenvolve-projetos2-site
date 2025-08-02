import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site_dados.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'views.login'
    login_manager.login_message_category = 'warning'

    from app.models.models import User, Book
    from app.routes import views
    app.register_blueprint(views)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Criação do banco e livros se não existir
    if not os.path.exists('site_dados.db'):
        with app.app_context():
            db.create_all()

            livros = [
                {"title": "Diário de um Desenvolvedor Júnior", "slug": "diario"},
                {"title": "O Código da Persistência", "slug": "persistencia"},
                {"title": "O Algoritmo da Vida", "slug": "algoritmo"},
                {"title": "Do Zero a Full Stack", "slug": "fullstack"},
            ]

            for livro in livros:
                # Verifica se já existe antes de adicionar
                if not Book.query.filter_by(slug=livro['slug']).first():
                    db.session.add(Book(**livro))
            db.session.commit()
            print("Banco de dados criado e/ou acessado com sucesso.")

    return app