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


def procura_carro(Carro=False,Inicio=False,Fim=False,br=True):
    arquivo = open('carro_semanas.txt','r')
    try:
        ultima_linha = arquivo.readlines()[len(arquivo.readlines())-1]
        carro = ultima_linha.split()[0].replace('/',' ')
        inicio = ultima_linha.split()[1]
        fim = ultima_linha.split()[2] 
        if Carro:
            return carro
        if Inicio:
            if br:
                return str_to_data(inicio)
            else:
                return str_to_data(inicio,br=False)
        if Fim:
            if br:
                return str_to_data(fim)
            else:
                return str_to_data(fim,br=False)
        if not Carro and not Inicio and not Fim:
            return 'nada escolhido'
    finally:
        arquivo.close()

def lista_carro_semanas(Carros=False,Inicios=False,Fims=False,br=False):
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
    if Carros:
        return carros_nome
    if Inicios:
        return carros_inicio
    if Fims:
        return carros_fim
            


    
