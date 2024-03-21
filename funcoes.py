def data_preco(objs):
    try:
        for obj in objs:
            obj.registro = obj.registro.strftime('%d/%m/%Y')
            obj.preco = moedinha(obj.preco)
    except TypeError:
        objs.registro = objs.registro.strftime('%d/%m/%Y')
        objs.preco = moedinha(objs.preco)
    finally:
        return objs

def moedinha(numero):
    numero_formatado = '{:.2f}'.format(numero)
    parte_inteira, parte_decimal = numero_formatado.split('.')
    parte_inteira = '{:,}'.format(int(parte_inteira)).replace(',', '.')
    valor_formatado = f'R$ {parte_inteira},{parte_decimal}'
    return valor_formatado

def enviar_email(assunto, texto, remetente, destinatário):
    import smtplib
    import email.message  
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatário
    password = 'yohplhritxndnazq'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(texto)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('email enviado com sucesso')

def str_to_data(data_inicial,br=True):
    from datetime import date
    data_inicial = date(
                int(data_inicial.replace('-',' ').split()[0]),
                int(data_inicial.replace('-',' ').split()[1]),
                int(data_inicial.replace('-',' ').split()[2])
                )
    if br:
        data_inicial = data_inicial.strftime('%d/%m/%Y')
    return data_inicial


def procura_carro(*args,br=True):
    lst = []
    ret = []
    for bgl in args:
        print(bgl)
        lst.append(bgl)
    arquivo = open('carro_semanas.txt','r')
    try:
        ultima_linha = arquivo.readlines()[len(arquivo.readlines())-1]
        carro = ultima_linha.split()[0].replace('/',' ')
        inicio = ultima_linha.split()[1]
        fim = ultima_linha.split()[2] 
        if args == ():
            if br:
                ret.append(carro)
                ret.append(inicio)
                ret.append(fim)
            else:
                ret.append(carro,br=False)
                ret.append(inicio,br=False)
                ret.append(fim,br=False)
        if 'carro' in lst:
            ret.append(carro)
        if 'inicio' in lst:
            if br:
                ret.append(str_to_data(inicio))
            else:
                ret.append(str_to_data(inicio,br=False))
        if 'fim' in lst:
            if br:
                ret.append(str_to_data(fim))
            else:
                ret.append(str_to_data(fim,br=False))
    finally:
        arquivo.close()
        if len(ret) == 1:
            return ret[0]
        else:
            return ret

def lista_carro_semanas(*args,br=False):
    lst = []
    ret = []
    retado = []
    for bgl in args:
        lst.append(bgl)
    carros_nome = []
    carros_inicio = []
    carros_fim = []
    with open('carro_semanas.txt','r') as arquivo:
        arquivo = arquivo.readlines()
        for c in range(0,len(arquivo)):
            carro = arquivo[c].split()[0].replace('/',' ')
            data_inicio = arquivo[c].split()[1]
            data_fim = arquivo[c].split()[2]
            carros_nome.append(carro) #nome tratado dos carros
            if br:
                carros_inicio.append(str_to_data(data_inicio)) # datas de início com fortação Br
                carros_fim.append(str_to_data(data_fim)) # datas de fim com formatação Br
            else:
                carros_inicio.append(data_inicio) # datas de início sem fortação Br
                carros_fim.append(data_fim) # datas de fim sem formatação Br
    if args == ():
        for c in range(0,len(carros_nome)):
            linha = f"{carros_nome[c].replace(' ','/')} {carros_inicio[c]} {carros_fim[c]}"
            linha = linha.split()
            linha[0] = linha[0].replace('/',' ')
            linha_formatado = [linha[0],linha[1],linha[2]] 
            retado.append(linha_formatado)
        return retado
    if 'carros' in lst:
        return carros_nome
    if 'inicio' in lst:
        return carros_inicio
    if 'fim' in lst:
        return carros_fim
            


    
