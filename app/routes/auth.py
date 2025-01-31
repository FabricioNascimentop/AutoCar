from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import Clientes
from .. import db

bp = Blueprint('auth', __name__)



@bp.route('/criar conta', methods=['POST'])
def cria_conta():
    nome = request.form.get('nome_criarconta')
    sobrenome = request.form.get('sobrenome_criarconta')
    email = request.form.get('email_criarconta')
    numero = request.form.get('telefone_criarconta')
    senha = request.form.get('senha_criarconta')
    administrador = request.form.get('administrador')
    
    if Clientes.query.filter_by(numero=numero).first():
        flash('numero já cadastrado','error')
    elif Clientes.query.filter_by(email=email).first():
        flash('email já cadastrado','error')
    else:
        nome = f"{nome} {sobrenome}"
        if administrador:
            cliente = Clientes(nome=nome,numero=numero,email=email,senha=senha,administrador=1)
        else:
            cliente = Clientes(nome=nome,numero=numero,email=email,senha=senha)
        db.session.add(cliente)
        db.session.commit()
        flash('conta criada com sucesso','okay')
    return redirect(url_for('home'))



@bp.route('/logar', methods=['POST'])
def processar_login():
    rota = request.args.get('rota')
    if '<' in rota:
        rota = request.url.replace('/',' ').split()[3]
    email = request.form.get('email_login')
    senha = request.form.get('senha_login')
    cliente = Clientes.query.filter_by(email=email).first()
    if cliente:
        if senha == cliente.senha:
            flash('parabéns, você está logado','okay')
            login_user(cliente,remember=True)
            redirect(url_for('cars.carros'))
        else:
            flash('senha incorreta','error')
    else:
         flash('este email não está cadastrado no sistema','error')
    return redirect(f"{rota}")



@bp.route('/logoff', methods=['POST'])
@login_required
def logout():
    rota = request.args.get('rota')
    if '<' in rota:
        rota = request.url.replace('/',' ').split()[3]
    btn = request.form.get('btn_supremo')
    if btn:
        return redirect('/')
    else:
        logout_user()
    flash('logout efetuado com sucesso','okay')
    return redirect(f"{rota}")
