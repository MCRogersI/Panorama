from pony.orm import *
import Projects.models as Pr, Employees.models as E, Planning.models as Pl, Users.models as U


# Esta parte del código busca sobreescribir la base de datos con una base de
#  datos vacía (limpiar/restart)
# Probablemente sea posible hacerlo usando el
# comando db.drop_all_tables(with_all_data=True)
#PENDIENTE
# db = Database()
# db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama') # estamos usando el puerto por defecto: 5432
# db.generate_mapping(create_tables=True)
# db.drop_all_tables(with_all_data=True)
# db.disconnect()

#Genera la base de datos
db = Database()
E.define_models(db)
Pr.define_models(db)
Pl.define_models(db)
U.define_models(db)
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama') # estamos usando el puerto por defecto: 5432
db.generate_mapping(create_tables=True)


