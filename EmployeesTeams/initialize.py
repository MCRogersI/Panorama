#corran este archivo después de correr models.py, y córranlo solo una vez, es para inicializar las Skills en la base de datos
from pony.orm import *

from models import Skills

with db_session:
	Skills(id=1, name='Rectifier')
	Skills(id=2, name='Designer')
	Skills(id=3, name='Fabricator')
	Skills(id=4, name='Installer')
