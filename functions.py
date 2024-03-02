def data_preco(obj_carro):
    obj_carro.registro = obj_carro.registro.strftime('%d/%m/%Y')
    obj_carro.preco = moedinha(obj_carro.preco)
    return obj_carro

def moedinha(numero):
    numero_formatado = '{:.2f}'.format(numero)
    parte_inteira, parte_decimal = numero_formatado.split('.')
    parte_inteira = '{:,}'.format(int(parte_inteira)).replace(',', '.')
    valor_formatado = f'R$ {parte_inteira},{parte_decimal}'
    return valor_formatado




