from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from funcoes import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Hf3g6cEEDgDAg56h6e-dGG51GEF3256e@viaduct.proxy.rlwy.net:30899/railway'
db = SQLAlchemy(app)
app.secret_key = 'fabricio'

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
    c = 0
    data = request.form
    email_usuario = data.get('email_login')
    senha_usuario = data.get('senha_login')
    usuarios = Clientes.query.all()

    for usuario in usuarios:
        if email_usuario == usuario.email:
            c += 1
        if senha_usuario == usuario.senha:
            c += 1
    print(c)
    if c == 3:
        return redirect(url_for('carros'))
    else:
        return redirect(url_for('home'))


@app.route('/sobre nós')
def sobre():
    return render_template('sobre.html')

@app.route('/layout')
def lay():
    return render_template('layout.html')



@app.route('/processamento',methods=['POST'])
def processar():
    carros_list = []
    data = request.form
    carros = Carros.query.all()
    for carro in carros:
        marca_carro = str(carro.nome.split()[0])
        if marca_carro in data.getlist('marcas'):
            carros_list.append(carros)
            return url_for(carros)


@app.route('/carros')
def carros():
    lst_marcas_carros = []
    lst_marcas = []
    anos = list(range(1956, 2025))
    precos = list(range(30000,50000,2000)) 
    quilometragem = list(range(1000,30000,3000))
    carros = Carros.query.all()


    for carro in carros:
        marca_carro = str(carro.nome.split()[0]) # pega somente a marca do carro
        if marca_carro not in lst_marcas:
            lst_marcas.append(marca_carro)
        marca_nome_carro = str(carro.nome).replace(' ','-') #tira espaços do no nome do carro
        carro.registro = carro.registro.strftime('%d/%m/%Y') #corrige formato da data 
        carro.preco = moedinha(carro.preco) # corrige formatação do valor monetário do carro
        lst_marcas_carros.append(marca_nome_carro)

            
    return render_template('carros.html',carros=carros,lst_marcas=lst_marcas,lst_marcas_carros=lst_marcas_carros)

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


