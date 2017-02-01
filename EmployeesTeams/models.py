from pony.orm import *

db = Database()
db.bind('postgres', user='postgres', password='panorama', host='localhost', database='panorama')
#se definen las clases (tablas en las bases de datos)

class Employees(db.Entity):
	id = PrimaryKey(int, auto=False)
	name = Required(str)
	team_id = Optional('Teams')
	skills = Set('Skills')

class Skills (db.Entity):
	id = PrimaryKey(int, auto=False)
	name = Required(str)
	employees = Set(Employees)
	team_skill = Set('Teams_Skills')


class Teams(db.Entity):
	id = PrimaryKey(int, auto=False)
	zone = Required(int)
	team_skills = Set('Teams_Skills')
	Employees = Set(Employees)
	

class  Teams_Skills(db.Entity):
	team = Required(Teams)
	skill = Required(Skills)
	PrimaryKey(team, skill)
	performance = Required(float)

db.generate_mapping(create_tables=True)