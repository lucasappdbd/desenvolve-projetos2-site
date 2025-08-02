from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user, login_user, logout_user
from urllib.parse import urlparse
from sqlalchemy.exc import IntegrityError
from app.models.models import db, User, Review, Book
from sqlalchemy import func
from datetime import timedelta

views = Blueprint('views', __name__)

# Página inicial
@views.route('/')
def index():
    return render_template('index.html', title='Página Inicial')

# Sobre o autor
@views.route('/sobre-o-autor')
def sobre_autor():
    return render_template('autor.html', title='Sobre o Autor')

# Cadastro
@views.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já cadastrado. Faça login ou use outro email.', 'warning')
            return redirect(url_for('views.cadastro'))

        novo_usuario = User(nome=nome, sobrenome=sobrenome, email=email)
        novo_usuario.set_password(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('views.login'))

    return render_template('cadastro.html', title='Cadastro')

# Login
@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    
    next_page = request.args.get('next')

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(senha):
            flash('Email ou senha inválidos.', 'danger')
            return redirect(url_for('views.login'))

        login_user(user)

        next_page = request.form.get('next')
        if not next_page or next_page == 'None' or urlparse(next_page).netloc != '':
            next_page = url_for('views.index')
        return redirect(next_page)

    return render_template('login.html', title='Login', next=next_page)

# Logout
@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('views.index'))


@views.route('/avaliacoes', methods=['GET', 'POST'])
def avaliacoes():
    if request.method == 'POST':
        # Só permite enviar avaliação se estiver logado
        if not current_user.is_authenticated:
            flash("Você precisa estar logado para enviar uma avaliação.", "warning")
            return redirect(url_for('views.login'))
        
        livro_slug = request.form.get('livro')
        nota = request.form.get('nota')
        comentario = request.form.get('comentario')

        if not livro_slug or not nota or not comentario:
            flash("Todos os campos são obrigatórios.", "warning")
            return redirect(url_for('views.avaliacoes'))

        livro = Book.query.filter_by(slug=livro_slug).first()
        if not livro:
            flash("Livro não encontrado.", "danger")
            return redirect(url_for('views.avaliacoes'))

        avaliacao_existente = Review.query.filter_by(user_id=current_user.id, book_id=livro.id).first()
        if avaliacao_existente:
            flash("Você já avaliou esse livro. Edite ou exclua sua avaliação existente.", "info")
            return redirect(url_for('views.avaliacoes'))

        try:
            nova_avaliacao = Review(
                rating=int(nota),
                comment=comentario,
                author=current_user,
                book=livro
            )
            db.session.add(nova_avaliacao)
            db.session.commit()
            flash("Avaliação enviada com sucesso!", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Erro ao enviar avaliação. Tente novamente.", "danger")

        return redirect(url_for('views.avaliacoes'))

    livros = Book.query.all()
    avaliacoes = Review.query.order_by(Review.created_at.desc()).limit(10).all() # carrega somente as últimas 10 avaliações publicadas

    from sqlalchemy import func
    media = db.session.query(func.avg(Review.rating)).scalar()
    media = round(media, 1) if media else 0

    return render_template("avaliacoes.html", title='Avaliações', livros=livros, avaliacoes=avaliacoes, media=media, timedelta=timedelta)

###### Editar avaliações #######
@views.route('/avaliacoes/editar', methods=['POST'])
@login_required
def editar_avaliacao_modal():
    id = request.form.get('avaliacao_id')
    nova_nota = request.form.get('nota')
    novo_comentario = request.form.get('comentario')

    avaliacao = Review.query.get_or_404(id)

    if avaliacao.author != current_user:
        flash("Você não tem permissão para editar esta avaliação.", "danger")
        return redirect(url_for('views.avaliacoes'))

    avaliacao.rating = int(nova_nota)
    avaliacao.comment = novo_comentario
    db.session.commit()
    flash("Avaliação atualizada com sucesso!", "success")
    return redirect(url_for('views.avaliacoes'))

###### Rota para exclusão de avaliações
@views.route('/avaliacoes/<int:avaliacao_id>/delete', methods=['POST'])
@login_required
def excluir_avaliacao(avaliacao_id):
    avaliacao = Review.query.get_or_404(avaliacao_id)

    if avaliacao.author != current_user:
        flash("Você não tem permissão para excluir esta avaliação.", "danger")
        return redirect(url_for('views.avaliacoes'))

    db.session.delete(avaliacao)
    db.session.commit()
    flash("Avaliação excluída com sucesso.", "success")
    return redirect(url_for('views.avaliacoes'))

###### Rota para página de perfil do usuário
@views.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not sobrenome or not email:
            flash("Nome, sobrenome e e-mail são obrigatórios.", "warning")
            return redirect(url_for('views.perfil'))

        # Verifica se email já existe e não é o do usuário atual
        usuario_existente = User.query.filter(User.email == email, User.id != current_user.id).first()
        if usuario_existente:
            flash("Este e-mail já está em uso por outro usuário.", "warning")
            return redirect(url_for('views.perfil'))

        current_user.nome = nome
        current_user.sobrenome = sobrenome
        current_user.email = email

        if senha:
            current_user.set_password(senha)

        try:
            db.session.commit()
            flash("Perfil atualizado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar o perfil. Tente novamente.", "danger")

        return redirect(url_for('views.perfil'))
    
    avaliacoes_usuario = Review.query.filter_by(user_id=current_user.id).order_by(Review.created_at.desc()).all()
    
    return render_template("perfil.html", title='Meu Perfil', avaliacoes=avaliacoes_usuario, timedelta=timedelta)

###### Rotas para cada livro
@views.route('/livro/diario')
def livro_diario():
    return render_template('livro/diario.html', title='Diário de um Desenvolvedor Júnior')

@views.route('/livro/persistencia')
def livro_persistencia():
    return render_template('livro/persistencia.html', title='O Código da Persistência')

@views.route('/livro/algoritmo')
def livro_algoritmo():
    return render_template('livro/algoritmo.html', title='O Algoritmo da Vida')

@views.route('/livro/fullstack')
def livro_fullstack():
    return render_template('livro/fullstack.html', title='Do Zero a Full Stack')