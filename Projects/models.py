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

    def __repr__(self):
        return str(self.contract_number)

db.generate_mapping(create_tables=True)
