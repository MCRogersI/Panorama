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
	teams = Set('Teams_Skills')

	def __repr__(self):
		return self.name

class Teams(db.Entity):
	id = PrimaryKey(int, auto=False)
	zone = Required(int)
	skills = Set('Teams_Skills')
	employees = Set(Employees)
	tasks = Set('Tasks_Teams')

	def __repr__(self):
		return str(self.id)

class Teams_Skills(db.Entity):
	team = Required(Teams)
	skill = Required(Skills)
	PrimaryKey(team, skill)
	performance = Required(float)

db.generate_mapping(create_tables=True)
