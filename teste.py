from app.models import Carros


import os
lst = '''1 Nissan Altima
2 BMW 3 Series
3 Audi A4
4 Mercedes-Benz C-Class
5 Hyundai Sonata
6 Kia Optima
7 Jaguar XF
8 Lexus ES
9 Volvo S60
10 Infiniti Q50
11 Renault Megane
12 Hyundai Elantra
13 BMW X3
14 Kia Seltos
15 Mercedes-Benz A-Class
16 Toyota Camry
17 Mazda CX-5
18 Acura MDX
19 Nissan Rogue
20 Chevrolet Equinox
21 Ford Explorer
22 Subaru Outback
23 Volkswagen Tiguan
24 Jeep Grand Cherokee
25 Mitsubishi Outlander
26 Audi Q5
27 Hyundai Tucson
28 Kia Sorento
29 Tesla Model Y
30 Lexus RX
31 Ford Explorer
32 Subaru Outback
33 Volkswagen Tiguan
34 Jeep Grand Cherokee
35 Mitsubishi Outlander
36 Audi Q5
37 Hyundai Tucson
38 Kia Sorento
39 Tesla Model Y
40 Lexus RX
41 Nissan Altima'''

carros = lst.splitlines()
os.chdir(r'C:\TheBigPython\PyProjects\Portifolio\SiteCarro\app\static\img\CarrosSRC')
for carro in carros:
    os.makedirs(carro.replace(' ','-'))
