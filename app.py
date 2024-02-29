from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from functions import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/carros_e_clientes'
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





@app.route('/')
def home():
    nome_carro_da_semana = 'Hyundai Tucson'
    #esta func_carro_da_semana faz alguns ajustes puramente estéticos nos dados
    carro_da_semana = Carros.query.filter_by(nome=nome_carro_da_semana).first()
    img_carro_da_semana = str(carro_da_semana.nome).replace(' ','-')
    return render_template('home.html',carro_da_semana=carro_da_semana, img_carro_da_semana=img_carro_da_semana)

@app.route('/sobre nós')
def sobre():
    return render_template('sobre.html')

@app.route('/carros')
def carros():
    lst_marcas_carros = []
    lst_marcas = []
    anos = list(range(1956, 2025))
    precos = list(range(30000,50000,2000)) 
    quilometragem = list(range(1000,30000,3000))
    carros = Carros.query.limit(10).all()

    for carro in carros:
        marca_nome_carro = str(carro.nome).replace(' ','-')
        marca_carro = str(carro.nome.split()[0])
        lst_marcas_carros.append(marca_nome_carro)
        if marca_carro not in lst_marcas:
            lst_marcas.append(marca_carro)
            
    return render_template('carros.html',
carros=carros,lst_marcas=lst_marcas,lst_marcas_carros=lst_marcas_carros, anos=anos,
precos=precos,quilometragem=quilometragem)

@app.route('/carros/<string:nome_carro>')
def carro_especifico(nome_carro):
    return render_template('carro_especifico')







if __name__ == "__main__":
    app.run(debug=True)