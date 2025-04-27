from flask import Blueprint, render_template, request, redirect, url_for
from ..models import Carros
from ..utils import dict_db
from flask_login import login_required
from .. import db


bp = Blueprint('cars', __name__)


@bp.route('/carros', methods=['GET', 'POST'])
def carros():
    import os
    from pathlib import Path

    carros_geral = Carros.query.all()
    lst_marcas = []
    carros_escolha = [] 

    for carro in carros_geral:
        marca_carro = str(carro.nome.split()[0])
        if marca_carro not in lst_marcas:
            lst_marcas.append(marca_carro)


    app = Path(__file__).parent.parent
    CarrosSRC = app/'static'/'img'/'CarrosSRC'

    if request.method == 'GET':
        for carro in carros_geral:
            dictCarro = dict_db(carro, data_preco=True)
            img = os.listdir(f"{CarrosSRC}/{carro.id}-{str(carro.nome).replace(' ','-')}")[0]
            dictCarro['img'] = img
            carros_escolha.append(dictCarro)
        

    if request.method == 'POST':
        data = request.form
        carros_lst = []

        if len(data.getlist('marcas')) > 0:
            marcas = data.getlist('marcas')
        else:
            marcas = lst_marcas
            
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
            ano_registro = int(carro.registro.split('-')[0])
            if carro.nome.split(' ')[0] in marcas:
                if registro[0] <= ano_registro and ano_registro <= registro[1]:
                    if preco[0] <= carro.preco and carro.preco <= preco[1]:
                        if quilometro[0] <= carro.quilometros and carro.quilometros <= quilometro[1]:
                            if carro.combustivel in combustivel:
                                if carro.estado in estado:
                                    carroDB = dict_db(carro, data_preco=True)
                                    img = os.listdir(f"{CarrosSRC}/{carro.id}-{str(carro.nome).replace(' ','-')}")[0]
                                    carroDB['img'] = img
                                    carros_lst.append(carroDB)
        
        carros_escolha = carros_lst
    return render_template('carros.html',carros=carros_escolha,lst_marcas=lst_marcas,anos=list(range(1956, 2026)))



@bp.route('/carros/<string:carro_nome>',methods=['POST','GET'])
def carro_especifico(carro_nome):
    import os
    from pathlib import Path
    app = Path(__file__).parent.parent
    CarrosSRC = app/'static'/'img'/'CarrosSRC'
    id = request.args.get('id')
    car = Carros.query.filter_by(id=id).first()
    carro = dict_db(car,data_preco=True)
    
    marca_carro = str(car.nome).split()[0]
    pasta_imagens = CarrosSRC/f"{id}-{str(carro_nome).replace(' ','-')}"
    images = [
        img.name for img in pasta_imagens.iterdir() 
        if img.is_file() and img.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif'}]

    
    return render_template('carro_especifico.html',carro=carro,marca_carro=marca_carro, images=images)


@bp.route('/adicionar carro')
def new_car():
    return render_template('add_carro.html')

@bp.route('/editar/<string:carro_nome>')
def editar_carro(carro_nome):
    import os
    from pathlib import Path
    if request.method == 'GET':
        id = request.args.get('id')
        carro = Carros.query.filter_by(id=id).first()
        marca_nome_carro = str(carro.nome).replace(' ','-')
        
        app = Path(__file__).parent.parent
        CarrosSRC = Path(app/'static'/'img'/'CarrosSRC')  
        carrinho = str(carro_nome).replace(' ','-')

        apagar = request.args.get('apagar_img')
        pasta_imagens = Path(f'{CarrosSRC}/{id}-{carrinho}')
        qtn_arquivos = len(os.listdir(pasta_imagens))

        images = [
        img.name for img in pasta_imagens.iterdir() 
        if img.is_file() and img.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif'}]
        if apagar:
            try:
                os.remove(f"{CarrosSRC}/{id}-{carrinho}/{apagar}")
            except FileNotFoundError:
                print(f'{CarrosSRC}/{id}-{carrinho}/{carrinho}-{apagar} - arquivo já apagado')
        
        return render_template('editar_carro.html',carro=carro,qtn_arquivos=qtn_arquivos,marca_nome_carro=marca_nome_carro,images=images)




@bp.route('/processar_carro', methods=['POST'])
def processa_carro():
    import os
    from pathlib import Path

    type = request.args.get('type')
    id = request.form.get('id')

    app = Path(__file__).parent.parent
    pasta_base = app / "static/img/CarrosSRC"

    if type == 'editar':
        carro = Carros.query.get(id)
        nome_carro = str(carro.nome).replace(' ','-')
        if not carro:
            return "Carro não encontrado!", 404

        for key, value in request.form.items():
            if hasattr(carro, key) and value:
                setattr(carro, key, value)

        pastaCarro = Path(f"{pasta_base}/{id}-{nome_carro}")
        new_name = request.form.get('nome')
        destino = f"{pasta_base}/{id}-{new_name.replace(' ','-')}"
        os.rename(pastaCarro, destino)

        db.session.commit()

        return redirect(f'/carros/{new_name}?id={id}')

    if type == 'adicionar':
        CD = request.form.to_dict()
        carro = Carros(
            nome=CD['nome'], modelo=CD['modelo'], preco=CD['preco'], registro=CD['registro'],
            combustivel=CD['combustivel'], motor=CD['motor'], transmissao=CD['transmissao'],
            origem=CD['origem'], Co2=CD['co2'], estado=CD['estado'], quilometros=CD['quilometros'],
            garantia=CD['garantia'], tipo=CD['tipo'], portas=CD['portas'], cor=CD['cor'], lugares=CD['lugares']
        )

        db.session.add(carro)
        db.session.commit()
        pasta_carro = f'{pasta_base}/{carro.id}-{str(carro.nome).replace(" ", "-")}'

        os.makedirs(pasta_carro, exist_ok=True) 

        temp = Path(f"{app}/static/img/CarrosSRC/.temp")
        c = 1

        for arquivo in os.listdir(temp):
            temp_arquivo = temp / arquivo
            novo_nome = f"{carro.nome.replace(' ', '-')}-{c}{temp_arquivo.suffix}"
            destino_arquivo = Path(pasta_carro) / novo_nome

            if temp_arquivo.exists():
                os.rename(temp_arquivo, destino_arquivo)
            
            c += 1

        return redirect(f'/carros/{carro.nome.replace(" ", "-")}?id={carro.id}')
        
        
    if type == 'excluir':
        import shutil
        from pathlib import Path

        id = request.form.get('id')
        carro_nome = request.form.get('carro_nome')
        carro = Carros.query.get(id)
        app = Path(__file__).parent.parent
        shutil.rmtree(f"{app}/static/img/CarrosSRC/{id}-{carro_nome.replace(' ','-')}")

        if carro:
            db.session.delete(carro)
            db.session.commit()


        return redirect(f'/carros')
        
