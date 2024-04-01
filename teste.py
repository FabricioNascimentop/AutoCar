from typing import Any
from funcoes import *
from datetime import date
hoje = date.today()





def carros_fila(*args):
    from datetime import date
    hoje = date.today()
    lst = []
    for carro in lista_carro_semanas():
        if (hoje - carro.data_inicio).days <= 0:
            lst.append(carro)
    if args == ():
        return lst
    if 'ultimo' in args:
        return lst[-1]
    
print(carros_fila())
