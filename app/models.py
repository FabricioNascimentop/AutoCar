from . import db
from flask_login import UserMixin

class Carros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60))
    modelo = db.Column(db.String(60))
    preco = db.Column(db.Float)
    registro = db.Column(db.Date())
    combustivel = db.Column(db.Enum("gasolina", "etanol", "diesel", "biodiesel", "GNV", "eletricidade", "hibrido", "flex"))
    motor = db.Column(db.String(20))
    transmissao = db.Column(db.Enum('automática', 'manual', 'automatizada'))
    origem = db.Column(db.String(40))
    Co2 = db.Column(db.Integer)
    estado = db.Column(db.Enum('usado', 'novo'))
    quilometros = db.Column(db.Integer)
    garantia = db.Column(db.String(40))
    tipo = db.Column(db.String(30))
    portas = db.Column(db.Integer)
    cor = db.Column(db.String(30))
    lugares = db.Column(db.Integer)

class Clientes(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(63), nullable=False)
    administrador = db.Column(db.Boolean, nullable=False, default=0)
