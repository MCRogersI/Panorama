from pony.orm import *
import Projects.models as P, EmployeesTeams.models as ET

#genera la base de datos
db = Database()
ET.define_models(db)
P.define_models(db)
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
db.generate_mapping(create_tables=True)

with db_session:
	db.Skills(id=1, name='Rectifier')
	db.Skills(id=2, name='Designer')
	db.Skills(id=3, name='Fabricator')
	db.Skills(id=4, name='Installer')
