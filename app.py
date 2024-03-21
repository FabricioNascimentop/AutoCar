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
    senha = db.Column(db.String(64), nullable=False)
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
    print('\n\n\n\n\n')
    print(procura_carro())
    print('\n\n\n\n\n')
    nome_carro_da_semana = procura_carro('carro')
    #este data_preco ajusta a data e os valores para o padrão brasileiro
    carro_da_semana = data_preco(Carros.query.filter_by(nome=nome_carro_da_semana).first())
    img_carro_da_semana = str(carro_da_semana.nome).replace(' ','-')
    return render_template('home.html',carro_da_semana=carro_da_semana, img_carro_da_semana=img_carro_da_semana,nome_carro_da_semana=nome_carro_da_semana)


@app.route('/criar conta',methods=['POST'])
def cria_conta():
    nome = request.form.get('nome_criarconta')
    sobrenome = request.form.get('sobrenome_criarconta')
    email = request.form.get('email_criarconta')
    numero = request.form.get('telefone_criarconta')
    senha = request.form.get('senha_criarconta')
    administrador = request.form.get('administrador')
    print(administrador)
    
    if Clientes.query.filter_by(numero=numero).first():
        flash('numero já cadastrado','error')
    elif Clientes.query.filter_by(email=email).first():
        print('a')
        flash('email já cadastrado','error')
    else:
        nome = f"{nome} {sobrenome}"
        if administrador:
            print('alo')
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
        print(rota)
        rota = request.url.replace('/',' ').split()[3]
        print(rota)
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
    #Definições Geral
    anos = list(range(1956, 2025))
    carros_totalidade = Carros.query.all()
    #Definições GET
    diretorio_imagem_carro = []
    lst_marcas = []
    #Definições POST
    query_dict = {}
    lst_carros = []
    data = request.form
    
    #laço percorrente os carros para buscar as marcas e o diretório da imagem
    for carro in carros_totalidade:
        marca_carro = str(carro.nome.split()[0]) # pega somente a marca do carro
        diretorio_imagem_carro.append(str(carro.nome).replace(' ','-')) #lista com diretorio da imagem de seu carro
        if marca_carro not in lst_marcas: #adiciona marcas de carros sem repetição
            lst_marcas.append(marca_carro)
        #se o método for GET a escolha de carros para aparecer são todos os carros
        if request.method == 'GET':
            carros_escolha = data_preco(carros_totalidade)
        #se o método for POST veja as marcas escolhidas, se o total for 0 adicione todas
        if request.method == 'POST':
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
        #se o input do estado do veículo for nenhum qualquer estado é válido, se não o estado é apenas o escolhido
        if data.get('estado') == None:
            query_dict['estado'] = ['novo','usado']
        else:
            query_dict['estado'] = data.get('estado')
       
        #laço que corre os bgl tudo e faz a verificação (melhorar depois) 
        for carro in carros_totalidade:
            #se a (variável) estiver dentro de sua respectiva parte do dicionário "query_dict" adicione na lista carro
            if str(marca_carro) in query_dict['marcas']:
                if carro.combustivel in query_dict['combustivel']:
                    if carro.estado in query_dict['estado']:
                        #se (variável) estiver entre o máximo e o mínimo de sua categoria adicione na lista carro
                        if query_dict['registro'][0] <= carro.registro.year <= query_dict['registro'][1]:
                                if query_dict['preco'][0] <= carro.preco <= query_dict['preco'][1]:
                                    if query_dict['quilometro'][0] <= carro.quilometros <= query_dict['quilometro'][1]:
                                        lst_carros.append(data_preco(carro))
        #escolha de carros é igual a lista com query
        carros_escolha = lst_carros

    #final
    return render_template('carros.html',carros=carros_escolha,lst_marcas=lst_marcas,diretorio_imagem_carro=diretorio_imagem_carro,anos=anos)



@app.route('/carros/<string:carro_nome>',methods=['POST','GET'])
def carro_especifico(carro_nome):
    carro = data_preco(Carros.query.filter_by(nome=carro_nome).first())
    marca_nome_carro = str(carro.nome).replace(' ','-')
    marca_carro = str(carro.nome).split()[0]
    return render_template('carro_especifico.html',carro=carro,marca_nome_carro=marca_nome_carro,marca_carro=marca_carro)


@app.route('/adicionar carro')
@login_required
def new_car():
    return render_template('add_carro.html')
@app.route('/carro semana',methods=['GET','POST'])
@login_required
def week_car():
    import datetime
    if request.method == 'GET':
        carros = data_preco(Carros.query.all())
        all_carros_nome = []
        all_carros_inicio = []
        all_carros_fim = []
        carros_dict = {}
        with open('carro_semanas.txt','r') as arquivo:
            arquivo = arquivo.readlines()
            qtn_itens = len(arquivo)
            for c in range(0,qtn_itens): #um laço que percorre cada letra de cada linha do "carro_semanas.txt"
                nome = arquivo[c].split()[0].replace('/',' ') #pega o primeiro item de cada linha (nome do carro) e o deixa legível
                data_inicial = str_to_data(arquivo[c].split()[1]) #pega o segundo item de cada linha (data_inicial) 
                data_final = str_to_data(arquivo[c].split()[2])#pega o terceiro item de cada linha (data_final) 
               #str_to_data transforma o dado do tipo str para um do tipo date
                all_carros_nome.append(nome)
                all_carros_inicio.append(data_inicial)
                all_carros_fim.append(data_final)
        carros_dict['nomes'] = all_carros_nome
        carros_dict['inicio'] = all_carros_inicio
        carros_dict['fim'] = all_carros_fim        
        return render_template('modify_carro.html',carros=carros,carros_dict=carros_dict,qtn_elementos=qtn_itens)
    else:
        comeco = str_to_data(request.form.get('dia_hoje'),br=False)
        fim = str_to_data(request.form.get('dia_semanaqvem'),br=False)
        carro = request.form.get('carro_semana')
        hoje = datetime.date.today()
        if hoje > comeco:
             flash('data de início é posterior a data atual','error')
             return redirect('/carro semana')
        else:
            with open('carro_semanas.txt','a') as arquivo:
                arquivo.writelines(f"{carro.replace(' ','/')} {comeco} {fim}\n")
            flash('até agora tudo certo')
            return redirect('/')


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