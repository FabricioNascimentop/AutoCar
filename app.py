from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager
from funcoes import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/carros_e_clientes'
db = SQLAlchemy(app)
login_manager = login_manager()
login_manager.init_app(app)
app.secret_key = 'fabricio'

@login_manager.user_loader
def load_user(user_id):
    return Clientes.get(user_id)
    
class Carros(db.Model):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True) 
    nome = db.Column(db.String(60))
    modelo = db.Column(db.String(60))
    preco = db.Column(db.Float)
    registro = db.Column(db.Date())   
    combustivel = db.Column(db.Enum("gasolina","etanol","diesel","biodiesel","GNV","eletricidade","hibrido","flex"))
    motor = db.Column(db.String(20))
    transmissao = db.Column(db.Enum('automática','manual','automatizada')) 
    origem = db.Column(db.String(40))
    Co2 = db.Column(db.Integer)
    estado = db.Column(db.Enum('usado','novo')) 
    quilometros = db.Column(db.Integer)
    garantia = db.Column(db.String(40))
    tipo = db.Column(db.String(30))
    portas = db.Column(db.Integer)
    cor = db.Column(db.String(30))
    lugares = db.Column(db.Integer)

class Clientes(db.Model):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)  
    nome  = db.Column(db.String(50))
    numero = db.Column(db.String(20))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(64))
    administrador = db.Column(db.Integer)



nome_carro_da_semana = 'Kia Sorento'


@app.route('/')
def home():
    #esta data_preco ajusta a data e os valores para o padrão brasileiro
    carro_da_semana = data_preco(Carros.query.filter_by(nome=nome_carro_da_semana).first())
    img_carro_da_semana = str(carro_da_semana.nome).replace(' ','-')
    return render_template('home.html',carro_da_semana=carro_da_semana, img_carro_da_semana=img_carro_da_semana,nome_carro_da_semana=nome_carro_da_semana)



@app.route('/logar',methods=['POST'])
def processar_login():
    usuarios = Clientes.query.all()
    email = request.form.get('email_login')
    senha = request.form.get('senha_login')
    for usuario in usuarios:
        if usuario.email == email and usuario.senha == senha:
            session['login'] = usuario.nome
            flash('tudo certo, meu bom')
            return redirect(url_for('carros'))
        else:
            flash('algo deu errado')
            return redirect(url_for('home'))
   


@app.route('/sobre nós')
def sobre():
    return render_template('sobre.html')

@app.route('/layout')
def lay():
    return render_template('layout.html')





@app.route('/carros',methods=['GET','POST'])
def carros():
    #DP = definições padrão
    #DP Geral
    anos = list(range(1956, 2025))
    carros_totalidade = Carros.query.all()
    #DP GET
    diretorio_imagem_carro = []
    lst_marcas = []
    #DP POST
    query_dict = {}
    lst_carros = []
    data = request.form
    
    #laço percorrente os carros
    for carro in carros_totalidade:
        marca_carro = str(carro.nome.split()[0]) # pega somente a marca do carro
        diretorio_imagem_carro.append(str(carro.nome).replace(' ','-')) #lista com diretorio da imagem de seu carro
        if marca_carro not in lst_marcas: #adiciona marcas de carros sem repetição
            lst_marcas.append(marca_carro)
        
        #se o método por POST veja as marcas escolhidas, se o total for 0 adicione todas
        if request.method == 'GET':
            carros_escolha = data_preco(carros_totalidade)
        else:
            if len(data.getlist('marcas')) == 0:
                        query_dict['marcas'] = lst_marcas
            else:
                query_dict['marcas'] =  data.getlist('marcas')

        #FIM DO LAÇO
    if request.method == 'POST':






        #query_dict "registo,preço e quilômetro" estes sendo [0] como mínimo e [1] como máximo
        query_dict['registro'] = [int(data.get('select_registro_inicio')),int(data.get('select_registro_fim'))]
        query_dict['preco'] = [float(data.get('select_preco_inicio')),float(data.get('select_preco_fim'))]
        query_dict['quilometro'] = [int(data.get('select_quilometro_inicio')),int(data.get('select_quilometro_fim'))]

        #semelhante ao método das marcas veja os combustíveis escolhidos, se o total for 0 adicione todos
        if len(data.getlist('combustivel')) > 0:
            query_dict['combustivel'] = data.getlist('combustivel')
        else:
            query_dict['combustivel'] = ["gasolina","etanol","diesel","biodiesel","GNV","eletricidade","hibrido","flex"]
        #parecido a marcas e combustível com a diferença de que não se conta a quantidade (pois é um request.form.get e não um request.form.getlist, verifica se o resultado é None, se sim novo e usado são aceitos, caso não apenas um é adicionado no dicionário)
        if data.get('estado') == None:
            query_dict['estado'] = ['novo','usado']
        else:
            query_dict['estado'] = data.get('estado')
        #laço que corre os bgl tudo e faz a verificação (melhorar depois)
        
        
        for carro in carros_totalidade:
            if str(carro.nome.split()[0]) in query_dict['marcas']:
                if carro.combustivel in query_dict['combustivel']:
                    if carro.estado in query_dict['estado']:
                        if query_dict['registro'][0] <= carro.registro.year <= query_dict['registro'][1]:
                                if query_dict['preco'][0] <= carro.preco <= query_dict['preco'][1]:
                                    if query_dict['quilometro'][0] <= carro.quilometros <= query_dict['quilometro'][1]:
                                        lst_carros.append(data_preco(carro))
        carros_escolha = lst_carros

    
    #final
    return render_template('carros.html',carros=carros_escolha,lst_marcas=lst_marcas,diretorio_imagem_carro=diretorio_imagem_carro,anos=anos)

@app.route('/carros/<string:carro_nome>',methods=['POST','GET'])
def carro_especifico(carro_nome):
    carro = Carros.query.filter_by(nome=carro_nome).first()
    marca_nome_carro = str(carro.nome).replace(' ','-')
    marca_carro = str(carro.nome).split()[0]
    carro.preco = moedinha(carro.preco)
    carro.registro = carro.registro.strftime('%d/%m/%Y')
    return render_template('carro_especifico.html',carro=carro,marca_nome_carro=marca_nome_carro,marca_carro=marca_carro)

@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

@app.route('/email_processar',methods=['POST'])
def processar_email():
    selecao = request.form.get('email_selecao')
    titulo = request.form.get('email_titulo')
    remetente = request.form.get('email_remetente')
    corpo = request.form.get('email_corpo')
    enviar_email(assunto=f'-{selecao}- {titulo}',texto=corpo,remetente='testeconsilcar@gmail.com',destinatário='testeconsilcar@gmail.com')
    return redirect(url_for('contatos'))


