from flask import Blueprint, redirect,url_for, request
from werkzeug.utils import secure_filename
from flask_login import login_required
from ..models import Carros
from sqlalchemy import desc

bp = Blueprint('images', __name__)

@bp.route('/add_img_editar',methods=['POST'])
def edit_image():
    id = request.form.get('id')
    nome = request.form.get('nome')
    return redirect(url_for('cars.editar_carro',carro_nome=nome,id=id))

@bp.route('/processar_midia',methods=['POST'])
@login_required
def processa_midia():
    import os 
    from pathlib import Path

    origem = request.args.get('origem')
    id = request.args.get('id')
    carro = request.args.get('nome')
    app = Path(__file__).parent.parent
    arquivos = request.files.values()

    if origem == 'edit_car':
        pasta = Path(f"{app}/static/img/CarrosSRC/{id}-{carro}")
        qtn_arquivos = len(os.listdir(pasta))
        arquivos = request.files.values()
        for file in arquivos:
            qtn_arquivos += 1
            file.filename = f'{carro}-{qtn_arquivos}.jpeg'
            filename = secure_filename(file.filename)
            file.save(os.path.join(pasta, filename))
    

    if origem == 'add_car':
        temp = Path(f"{app}/static/img/CarrosSRC/.temp")
        temp.mkdir(parents=True, exist_ok=True)

        for file in arquivos:
            file.filename = secure_filename(file.filename)
            file.save(os.path.join(temp, file.filename))
        
        

        return redirect(url_for('cars.new_car'))