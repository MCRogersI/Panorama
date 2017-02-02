from pony.orm import *

db = Database()
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
#se definen las clases (tablas en las bases de datos)




db.generate_mapping(create_tables=True)