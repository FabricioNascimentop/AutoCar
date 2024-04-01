from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user, UserMixin, logout_user, login_required
from funcoes import *



app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Hf3g6cEEDgDAg56h6e-dGG51GEF3256e@viaduct.proxy.rlwy.net:30899/railway'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
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
    
class Clientes(db.Model,UserMixin):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)  
    nome  = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(63), nullable=False)
    administrador = db.Column(db.Boolean, nullable=False, default=0)
    def __init__(self,nome,numero,email,senha, administrador=0):
        self.nome = nome
        self.numero = numero
        self.email = email
        self.senha = senha
        self.administrador = administrador
 




@login_manager.user_loader
def load_user(Clientes_id):
    return Clientes.query.filter_by(id=Clientes_id).first()



@app.route('/')
def home():
    nome_carro_da_semana = carros_fila('ultimo').nome
    carro_da_semana_class = Carros.query.filter_by(nome=nome_carro_da_semana).first()
    carro_da_semana = dict_db(carro_da_semana_class,data_preco=True)
    img_carro_da_semana = str(carro_da_semana['nome']).replace(' ','-')
    return render_template('home.html',carro_da_semana=carro_da_semana, img_carro_da_semana=img_carro_da_semana,nome_carro_da_semana=nome_carro_da_semana)


@app.route('/criar conta',methods=['POST'])
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



@app.route('/logar',methods=['POST'])
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
            redirect(url_for('carros'))
        else:
            flash('senha incorreta','error')
    else:
         flash('este email não está cadastrado no sistema','error')
    return redirect(f"{rota}")

@app.route('/logoff',methods=['POST'])
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
        


@app.route('/sobre nós')
def sobre():
    return render_template('sobre.html')

@app.route('/teste')
def testar():
    return render_template('teste.html')

@app.route('/carros',methods=['GET','POST'])
def carros():
    anos = list(range(1956, 2025))
    carros_geral = Carros.query.all()
    diretorio_imagem_carro = []
    lst_marcas = []


    for carro in carros_geral:
        marca_carro = str(carro.nome.split()[0])
        if marca_carro not in lst_marcas:
            lst_marcas.append(marca_carro)


        diretorio_imagem_carro.append(str(carro.nome).replace(' ','-'))

    if request.method == 'GET':
        carros_escolha = []
        for carro in carros_geral:
            carros_escolha.append(dict_db(carro,data_preco=True))



    if request.method == 'POST':


        data = request.form
        carros_lst = []
        marcas = data.getlist('marcas')


        if len(data.getlist('combustivel')) > 0:
            combustivel = data.getlist('combustivel')
        else:
            combustivel = ["gasolina","etanol","diesel","biodiesel","GNV","eletricidade","hibrido","flex"]

        if data.get('estado') == None:
            estado = ['novo','usado']
        else:
            estado = data.get('estado')
        
        
        registro = [int(data.get('select_registro_inicio')),int(data.get('select_registro_fim'))]
        preco = [float(data.get('select_preco_inicio')),float(data.get('select_preco_fim'))]
        quilometro = [int(data.get('select_quilometro_inicio')),int(data.get('select_quilometro_fim'))]


        for carro in carros_geral:
            if carro.nome.split()[0] in marcas:
                if registro[0] <= carro.registro.year and carro.registro.year <= registro[1]:
                    if preco[0] <= carro.preco and carro.preco <= preco[1]:
                        if quilometro[0] <= carro.quilometros and carro.quilometros <= quilometro[1]:
                            if carro.combustivel in combustivel:
                                if carro.estado in estado:
                                    carros_lst.append(dict_db(carro,data_preco=True))

        

        print(carros_lst)
        carros_escolha = carros_lst
    return render_template('carros.html',carros=carros_escolha,lst_marcas=lst_marcas,diretorio_imagem_carro=diretorio_imagem_carro,anos=anos)



@app.route('/carros/<string:carro_nome>',methods=['POST','GET'])
def carro_especifico(carro_nome):
    car = Carros.query.filter_by(nome=carro_nome).first()
    carro = dict_db(car,data_preco=True)
    marca_nome_carro = str(car.nome).replace(' ','-')
    marca_carro = str(car.nome).split()[0]
    return render_template('carro_especifico.html',carro=carro,marca_nome_carro=marca_nome_carro,marca_carro=marca_carro)


@app.route('/adicionar carro')
@login_required
def new_car():
    return render_template('add_carro.html')


@app.route('/carro semana',methods=['GET','POST'])
@login_required
def week_car():
    lst = []
    if request.method == 'GET':
        carros = Carros.query.all()
        for carro in carros:
            lst.append(dict_db(carro,data_preco=True))

        prox_carros = carros_fila()
        qtn_carros = len(carros)
        hist_carros = lista_carro_semanas()
        return render_template('modify_carro.html',qtn_carros=qtn_carros,carros_lista=lst,prox_carros=prox_carros,hist_carros=hist_carros)
    if request.method == 'POST':
        from datetime import date
        carro_semana = request.form.get('carro_semana')
        
        inicio = request.form.get('dia_hoje')
        inicio = date.fromisoformat(inicio)

        fim = request.form.get('dia_semanaqvem')
        fim = date.fromisoformat(fim)


        with open('carro_semanas.txt','a') as arquivo :
            arquivo.write(F"{carro_semana.replace(' ','/')} {inicio} {fim}\n")

        return redirect('/carro semana')


@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

@app.route('/email_processar',methods=['POST'])
def processar_email():
    selecao = request.form.get('email_selecao')
    titulo = request.form.get('email_titulo')
    remetente = request.form.get('email_remetente')
    corpo = request.form.get('email_corpo')
    enviar_email(assunto=f'-{selecao}- {titulo}',texto=f"{corpo}<br><br><br>{remetente} aguarda resposta",remetente='testeconsilcar@gmail.com',destinatário='testeconsilcar@gmail.com')
    return redirect(url_for('contatos'))

if __name__ == "__main__":
    app.run(debug=True)