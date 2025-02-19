from . import db
from flask_login import UserMixin
from datetime import date

class Carros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(60))
    modelo = db.Column(db.String(60))
    preco = db.Column(db.Float)
    registro = db.Column(db.Date())
    combustivel = db.Column(db.String(40))
    motor = db.Column(db.String(20))
    transmissao = db.Column(db.String(20))
    origem = db.Column(db.String(40))
    Co2 = db.Column(db.Integer)
    estado = db.Column(db.String(10))
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

class CarroSemana(db.Model):
    __tablename__ = 'carro_semana'

    carro_id = db.Column(db.Integer, db.ForeignKey('carros.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    data_entrada = db.Column(db.Date, nullable=False, default=date.today)
    data_saida = db.Column(db.Date, nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    carro = db.relationship('Carros', backref=db.backref('semanas', lazy=True))

    def __repr__(self):
        return f"<carro_id={self.carro_id}, entrada={self.data_entrada}, saida={self.data_saida} ativo={self.ativo}>"
