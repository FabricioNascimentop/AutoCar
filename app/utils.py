def dict_db(self, data_preco=False):
    data = {}

    for attr, value in self.__dict__.items():
        data[attr] = value

        if data_preco:
            if attr == 'registro' and value:
                data[attr] = value.strftime("%d/%m/%Y")

            if attr == 'preco' and value:
                data['preco'] = moedinha(float(value))

    return data
    

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
    else:
        data_inicial = data_inicial.strftime('%Y/%m/%d')
    return data_inicial




def busca_carros_semana(passados=False):
    #retorna lista de carros no bagulho das semanas lá
    #passado ou futuro pra filtrar se a lista vai retornar todos ou só alguns
    import csv
    from collections import namedtuple
    from datetime import date,datetime
    prox_carros = []
    pass_carros = []
    Carro_semana = namedtuple('Carro_semana',['Nome_carro','Data_entrada','Data_saida'])
    with open('carro_semanas.csv','r') as carros_semana:
        reader = csv.DictReader(carros_semana)
        for linha in reader:
            dado = Carro_semana(Nome_carro=linha['Nome_carro'], Data_entrada=linha['Data_entrada'],Data_saida=linha['Data_saida'])
            print(dado.Nome_carro,dado.Data_entrada)
            if datetime.strptime(dado.Data_entrada,"%Y-%m-%d").date() > date.today():
                print('vai aparecer \n')
            if datetime.strptime(dado.Data_entrada,"%Y-%m-%d").date() == date.today():
                print('está aparecendo \n')
            else:
                print('já apareceu \n')
    
        return prox_carros

def remover_numeros(texto):
    texto_sem_numeros = ''
    for caractere in texto:
        if not caractere.isdigit():
            texto_sem_numeros += caractere
    return texto_sem_numeros

        
def get_car_imagens(base_path, carro_id, carro_nome):
    pasta = base_path / f"{carro_id}-{carro_nome.replace(' ','-')}"
    fallback = "img/erro.png"

    try:
        if pasta.exists():
            imagens = [
                img.name for img in pasta.iterdir()
                if img.is_file() and img.suffix.lower() in {'.jpg','.jpeg','.png','.gif'}
            ]
            if imagens:
                return f"img/CarrosSRC/{carro_id}-{carro_nome.replace(' ','-')}/{imagens[0]}"
    except Exception:
        pass

    return fallback