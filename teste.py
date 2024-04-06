import os
from pathlib import Path
pasta_atual = Path(__file__).parent
CarrosSRC = Path(pasta_atual/'static'/'img'/'CarrosSRC')


print(os.listdir(pasta_atual/'static'/'img'))