def func_carro_da_semana(obj_carro):
    obj_carro.nome = str(obj_carro.nome).upper()
    obj_carro.modelo = str(obj_carro.modelo).upper()
    obj_carro.registro = obj_carro.registro.strftime('%d/%m/%Y')
    obj_carro.combustivel = str(obj_carro.combustivel).capitalize()
    obj_carro.preco = f"{str(obj_carro.preco).replace('.',',')}"
    return obj_carro




