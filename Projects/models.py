from pony.orm import *
from datetime import datetime

db = Database()
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
#se definen las clases (tablas en las bases de datos)


class Tasks(db.Entity):
	id = PrimaryKey(int, auto=False)
	id_skill = Required(Skill)
	id_proyect = Required('Proyect')
	original_initial_date = Required(datetime)
	


db.generate_mapping(create_tables=True)