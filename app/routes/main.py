from flask import Blueprint, render_template, session, jsonify, redirect
from flask_login import login_user
from ..models import Carros, CarroSemana, Clientes
from ..utils import dict_db
from app import db


bp = Blueprint('main', __name__, template_folder='../../templates')

@bp.route('/')
def home():
    for carrinho in CarroSemana.query.all():
        if carrinho.ativo:
            id_carro_semana = carrinho.carro_id

    carro_da_semana_class = Carros.query.filter_by(id=id_carro_semana).first()
    carro_semana = dict_db(carro_da_semana_class, data_preco=True)

    return render_template('home.html', carro_semana=carro_semana)

@bp.route('/sobre nós')
def about():
    return render_template('sobre.html')

@bp.route('/contatos')
def contacts():
    return render_template('contatos.html')

@bp.route('/carro semana',methods=['POST','GET'])
def carro_semana():
    from flask import request
    from datetime import datetime

    carros = CarroSemana.query.all()
    print(carros)
    carros_tot = [carro.nome for carro in Carros.query.all()]
    if request.method == 'POST':
        carro_nome = request.form.get('carro')

        data_entrada = request.form.get('data_entrada')
        data_saida = request.form.get('data_saida')

        data_entrada = datetime.strptime(data_entrada, '%Y-%m-%d').date()
        data_saida = datetime.strptime(data_saida, '%Y-%m-%d').date()


        if data_entrada > data_saida:
            print('inválido')

        else:
            carro = Carros.query.filter_by(nome=carro_nome).first()
            novo_carro_semana = CarroSemana(
        carro_id=carro.id,
        data_entrada=data_entrada,
        data_saida=data_saida,
        ativo=True
    )

        db.session.add(novo_carro_semana)
        db.session.commit()
    return render_template('carro_semana.html',carros=carros,carros_tot=carros_tot)

@bp.route('/login recrutador')
def login_recrutador():
    recrutador = Clientes.query.filter_by(id='22').first()
    login_user(recrutador, remember=False)
    return redirect('/')


