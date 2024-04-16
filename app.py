from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_user, UserMixin, logout_user, login_required
from funcoes import *
from werkzeug.utils import secure_filename



app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:vWBwGMbsQIGFAqzFZsaiDYjJJnGpggpR@viaduct.proxy.rlwy.net:44033/railway'
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
    try:
        nome_carro_da_semana = carros_fila('ultimo').nome
    except:
        nome_carro_da_semana = Carros.query.filter_by(id=1)
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
    carros_geral = Carros.query.all()
    lst_marcas = []
    carros_escolha = [] 

    for carro in carros_geral:
        marca_carro = str(carro.nome.split()[0])
        if marca_carro not in lst_marcas:
            lst_marcas.append(marca_carro)


    if request.method == 'GET':
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

        

        carros_escolha = carros_lst
    return render_template('carros.html',carros=carros_escolha,lst_marcas=lst_marcas,anos=list(range(1956, 2025)))



@app.route('/carros/<string:carro_nome>',methods=['POST','GET'])
def carro_especifico(carro_nome):
    import os
    from pathlib import Path
    car = Carros.query.filter_by(nome=carro_nome).first()
    carro = dict_db(car,data_preco=True)
    marca_nome_carro = str(car.nome).replace(' ','-')
    marca_carro = str(car.nome).split()[0]

    pasta_atual = Path(__file__).parent
    CarrosSRC = Path(pasta_atual/'static'/'img'/'CarrosSRC')  
    carrinho = str(carro_nome).replace(' ','-')
    qtn_arquivos = len(os.listdir(CarrosSRC/carrinho))
    
    
    return render_template('carro_especifico.html',carro=carro,marca_nome_carro=marca_nome_carro,marca_carro=marca_carro,qtn_arquivos=qtn_arquivos)


@app.route('/editar/<string:carro_nome>')
def editar_carro(carro_nome):
    import os
    from pathlib import Path
    id = request.args.get('id')
    carro = Carros.query.filter_by(id=id).first()
    marca_nome_carro = str(carro.nome).replace(' ','-')
    pasta_atual = Path(__file__).parent
    CarrosSRC = Path(pasta_atual/'static'/'img'/'CarrosSRC')  
    carrinho = str(carro_nome).replace(' ','-')
    qtn_arquivos = len(os.listdir(CarrosSRC/carrinho))

    apagar = request.args.get('apagar_img')
    if apagar:
        try:
           os.remove(f"{CarrosSRC}/{carrinho}/{carrinho}-{apagar}.jpeg")
        except FileNotFoundError:
           print('arquivo já apagado')
    c = 0
    for arquivo in os.listdir(f"{CarrosSRC}/{carrinho}"):
        c += 1 
        os.chdir(f"{CarrosSRC}/{carrinho}")
        os.rename(arquivo,f"{remover_numeros(arquivo.split('.')[0])}{c}.jpeg")
    return render_template('editar_carro.html',carro=carro,qtn_arquivos=qtn_arquivos,marca_nome_carro=marca_nome_carro)


@app.route('/editar_carro',methods=['POST'])
def edit_car():
    Carro_att_dict = request.form.to_dict()
    nome = request.form.get('nome')
    modelo = request.form.get('modelo')
    id = request.form.get('id')
    id = int(id)
    carro = Carros.query.filter_by(id=id).first()
        
    
    carro.nome = nome
    carro.modelo = request.form.get('modelo')
    carro.preco = request.form.get('preco')
    carro.registro = request.form.get('registro')
    carro.combustivel = request.form.get('combustivel')
    carro.motor = request.form.get('motor')
    carro.transmissao = request.form.get('transmissao')
    carro.origem = request.form.get('origem')
    carro.Co2 = request.form.get('co2')
    carro.estado = request.form.get('estado')
    carro.quilometros = request.form.get('quilometros')
    carro.garantia = request.form.get('nome')
    carro.tipo = request.form.get('tipo')
    carro.portas = request.form.get('portas')
    carro.cor = request.form.get('cor')
    carro.lugares = request.form.get('lugares')
    
    db.session.add(carro)
    db.session.commit()



    return redirect(url_for('editar_carro',carro_nome=nome,id=id))

@app.route('/add_img_editar',methods=['POST'])
def editar_img_add():
    from pathlib import Path
    import os
    pasta_atual = Path(__file__).parent
    CarrosSRC = Path(pasta_atual/'static'/'img'/'CarrosSRC')
    arquivos_temp = os.listdir(f"{CarrosSRC}/temp")
    c = 0
    extensoes_img = ['.jpg', '.jpeg','.png','.gif','.bmp']
    extensoes_videos = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']   
    nome = request.form.get('nome')
    id = request.form.get('id')
    nome = nome.replace(' ','-')
    for arquivoTemp in arquivos_temp:
            c += 1
            os.chdir(f"{CarrosSRC}/temp")
            extensao = os.path.splitext(arquivoTemp)[1]
            if extensao in extensoes_img:
                try:
                    os.rename(arquivoTemp,f"{CarrosSRC}/{nome}/{nome}-{c}.jpeg")
                except FileExistsError:
                    print('alo')
                    pass
            if extensao in extensoes_videos:
                try:
                    os.rename(arquivoTemp,f"{CarrosSRC}/{nome}/{nome}-{c}.mp4")
                except FileExistsError:
                    pass
    return redirect(url_for('editar_carro',carro_nome=nome,id=id))
    
@app.route('/adicionar carro')
@login_required
def new_car():
    return render_template('add_carro.html')

@app.route('/processar_carro',methods=['POST'])
@login_required
def processa_carro():
    import os
    from pathlib import Path
    #pega dados dos inputs e faz um commit para o banco de dados
    #----------------------------------------------------------------------------------------------------------------------------------- 
    CD = request.form.to_dict()
    carro = Carros(
    nome=CD['nome'],modelo=CD['modelo'],preco=CD['preco'],registro=CD['registro'],combustivel=CD['combustivel'],
    motor=CD['motor'],transmissao=CD['transmissao'],origem=CD['origem'],Co2=CD['co2'],estado=CD['estado'],
    quilometros=CD['quilometros'],garantia=CD['garantia'],tipo=CD['tipo'],portas=CD['portas'],cor=CD['cor'],
    lugares=CD['lugares']
   )
    db.session.add(carro)
    db.session.commit()
    #cria diretório com nome do carro na pasta "Carros/SRC", arrasta imagens vindas da pasta temp (adicionadas pela rota processar_midia)
    #-----------------------------------------------------------------------------------------------------------------------------------
    pasta_atual = Path(__file__).parent
    CarrosSRC = Path(pasta_atual/'static'/'img'/'CarrosSRC')     
    
    #cria diretório com nome do carro
    nome = request.form.get('nome')
    nome = nome.replace(' ','-')
    if not os.path.exists(f"{CarrosSRC}/{nome}"):
        os.mkdir(f"{CarrosSRC}/{nome}")
    
    #arrasta arquivos de "temp" para diretório
        arquivos_temp = os.listdir(f"{CarrosSRC}/temp") #arquivos na pasta temp
        c = 0
        extensoes_img = ['.jpg', '.jpeg','.png','.gif','.bmp']
        extensoes_videos = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']

        for arquivoTemp in arquivos_temp:
            c += 1
            os.chdir(f"{CarrosSRC}/temp")
            extensao = os.path.splitext(arquivoTemp)[1]
            if extensao in extensoes_img:
                os.rename(arquivoTemp,f"{CarrosSRC}/{nome}/{nome}-{c}.jpeg")
            if extensao in extensoes_videos:
                os.rename(arquivoTemp,f"{CarrosSRC}/{nome}/{nome}-{c}.mp4")
    #-----------------------------------------------------------------------------------------------------------------------------------
    return redirect('/adicionar carro')




@app.route('/processar_midia',methods=['POST'])
@login_required
def processa_midia():
    import os 
    from pathlib import Path
    pasta_atual = Path(__file__).parent
    CarrosSRC = Path(pasta_atual/'static'/'img'/'CarrosSRC')
    
    #coloca arquivos na pasta temp
    arquivos = request.files.values()
    for file in arquivos:
            filename = secure_filename(file.filename)
            file.save(os.path.join(CarrosSRC/'temp', filename))
    return redirect(url_for('new_car'))

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