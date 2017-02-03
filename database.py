from pony.orm import *
import EmployeesTeams.models, Projects.models

db = Database()

EmployeesTeams.models.define_models(db)
Projects.models.define_models(db)

db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
db.generate_mapping(create_tables=True)
