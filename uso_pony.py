from pony.orm import *

db = Database()


class Employees(db.Entity):
	id = PrimaryKey(int, auto=False)
	name = Required(str)
	team_id = Required(int)

#class Skills (db.Entity):
#	di = Required(int)
#	name = Required(str)

	
db.bind('postgres', user='postgres', password='hxq54ght3', host='localhost', database='panorama')

sql_debug(True)

db.generate_mapping(create_tables=True)
