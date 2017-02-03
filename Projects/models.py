from pony.orm import *
from datetime import datetime

def define_models(db):
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
		tasks = Set('Tasks')

		def __repr__(self):
			return str(self.contract_number)

	# dificultades tipo "construcción en altura"
	class Difficulties(db.Entity):
		id = PrimaryKey(int, auto=False)
		description = Required(str)
		projects = Set(Projects)

		def __repr__(self):
			return self.description

	# actividades tipo "licencia", "vacaciones", etc.
	class Activities(db.Entity):
		id = PrimaryKey(int, auto=False)
		description = Required(str)

		def __repr__(self):
			return self.description

	class Tasks(db.Entity):
		id = PrimaryKey(int, auto=False)
		id_skill = Required('Skills')
		id_proyect = Required(Projects)
		original_initial_date = Required(datetime)
		original_initial_date = Optional(datetime)
		original_end_date = Optional(datetime)
		efective_initial_date = Optional(datetime)
		efective_end_date = Optional(datetime)
		failed = Optional(bool)
		fail_cost = Optional(int)
		teams = Set('Tasks_Teams')

		def __repr__(self):
			return str(self.id)

	class Tasks_Teams(db.Entity):
		task = Required(Tasks)
		team = Required('Teams')
		PrimaryKey(task,team)
		initial_date = Optional(datetime)
		end_date = Optional(datetime)
		
		
		
		