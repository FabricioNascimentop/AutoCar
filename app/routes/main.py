from flask import Blueprint, render_template
from ..models import Carros
from ..utils import dict_db

bp = Blueprint('main', __name__, template_folder='../../templates')

@bp.route('/')
def home():
    nome_carro_da_semana = 'BMW 3 Series'
    carro_da_semana_class = Carros.query.filter_by(nome=nome_carro_da_semana).first()
    carro_semana = dict_db(carro_da_semana_class, data_preco=True)

    return render_template('home.html', carro_semana=carro_semana)

@bp.route('/sobre nós')
def about():
    return render_template('sobre.html')

@bp.route('/contatos')
def contacts():
    return render_template('contatos.html')

@bp.route('/teste')
def test():
    return render_template('teste.html')