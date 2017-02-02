from pony.orm import *

db = Database()
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
#se definen las clases (tablas en las bases de datos)

class Projects(db.Entity):
    contract_number = PrimaryKey(int, auto=False)
    client_address = Required(str)
    client_name = Required(str)
    client_rut = Required(str)
    linear_meters = Required(float)
    real_linear_meters = Required(float)
    estimated_cost = Required(int)
    real_cost = Required(int)
    difficulties = Set('Difficulties')
    
    def __repr__(self):
        return str(self.contract_number)

#dificultades tipo "construcción en altura"
class Difficulties(db.Entity):
    id = PrimaryKey(int, auto=False)
    description = Required(str)
    projects = Set(Projects)

    def __repr__(self):
        return self.description

#actividades tipo "licencia", "vacaciones", etc.
class Activities(db.Entity):
    id = PrimaryKey(int, auto=False)
    description = Required(str)

    def __repr__(self):
        return self.description

#clase intermedia entre Activities y Teams, con fechas iniciales y finales

db.generate_mapping(create_tables=True)
