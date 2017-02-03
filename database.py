from pony.orm import *
import Projects.models as P, EmployeesTeams.models as ET

#genera la base de datos
db = Database()
ET.define_models(db)
P.define_models(db)
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
db.generate_mapping(create_tables=True)
