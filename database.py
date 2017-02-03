from pony.orm import *
import Projects.models as P, EmployeesTeams.models as ET

db = Database()
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')

ET.define_models(db)
P.define_models(db)

db.generate_mapping(create_tables=True)
