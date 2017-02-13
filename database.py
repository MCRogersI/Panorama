from pony.orm import *
import Projects.models as Pr, Employees.models as E, Planning.models as Pl

#genera la base de datos
db = Database()

E.define_models(db)
Pr.define_models(db)
Pl.define_models(db)

db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama') # estamos usando el puerto por defecto: 5432
db.generate_mapping(create_tables=True)
