def dict_db(self,data_preco=False):
        dict = {}
        for attr, value in self.__dict__.items():
            dict[attr] = value
            if data_preco == True:
                if attr == 'registro':
                    dict[attr] = value.strftime('%d/%m/%Y')
                if attr == 'preco':
                    dict['preco'] = moedinha(float(value))
        return dict
    

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
class CarrosMeus:
    def __init__(self,nome,data_inicio,data_final):
        from datetime import date
        hoje = date.today()
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_final = data_final
        
        self.tempo_inicio = data_inicio - hoje
        self.tempo_fim = data_final - hoje
    def __repr__(self) -> str:
        return '<'+self.nome+'>'
        
def carros_fila():
    lst = []
    from datetime import date
    hoje = date.today()
    for c in range(0,len(lista_carro_semanas())):
        if hoje <= lista_carro_semanas()[c][1]:
            nome = lista_carro_semanas()[c][0]
            nome = str(nome).replace('/',' ') 
            data_inicio = lista_carro_semanas()[c][1] 
            data_fim = lista_carro_semanas()[c][2]
            tempo = data_inicio - hoje
            carro = CarrosMeus(nome,data_inicio,data_fim,tempo)
            lst.append(carro)
            
    if len(lst) > 0:
        return lst
    else:
        return 'não há carros a adicionar'

def lista_carro_semanas(*args):
    from datetime import date
    lst = []
    with open('carro_semanas.txt','r') as arquivo:
        arquivo = arquivo.readlines()
        for elemento in arquivo:
            elemento = elemento.split() 
            elemento[0] = elemento[0].replace('/', ' ') #nome
            elemento[1] = date.fromisoformat(elemento[1])#data inicial
            elemento[2] =  date.fromisoformat(elemento[2])#data final

            carro = CarrosMeus(elemento[0],elemento[1],elemento[2])
            lst.append(carro)
    return lst

def carros_fila(*args):
    #coloca todos os carros a ir pra página principal em uma lista
    from datetime import date
    hoje = date.today()
    lst = []
    for carro in lista_carro_semanas():
        #se a data já passou ou se a data em que o carro sumir for depois de hoje
        if (hoje - carro.data_inicio).days <= 0 or hoje <= carro.data_final:
            lst.append(carro)
    if args == ():
        return lst
    if 'ultimo' in args:
        return lst[-1]

def remover_numeros(texto):
    texto_sem_numeros = ''
    for caractere in texto:
        if not caractere.isdigit():
            texto_sem_numeros += caractere
    return texto_sem_numeros

        
            

    
