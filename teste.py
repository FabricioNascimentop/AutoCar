def alo():
    arquivo = open('carro_semanas.txt','r')
    try:
        ultima_linha = arquivo.readlines()[len(arquivo.readlines())-1]
        carro = ultima_linha.split()[0].replace('/',' ')
        inicio = ultima_linha.split()[1]
        fim = ultima_linha.split()[2] 
    finally:
      arquivo.close()
      return carro,inicio,fim
    
from datetime import date
from funcoes import *
hj = date.today()

for c in range(-1,-6,-1):
    print(lista_carro_semanas()[c])       
