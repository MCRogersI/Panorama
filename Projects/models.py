from pony.orm import *
from datetime import date

def define_models(db):
	class Projects(db.Entity):
		contract_number = PrimaryKey(int, auto=False)
		client_address = Required(str)
		client_comuna = Required(str)
		client_name = Required(str)
		client_rut = Required(str)
		linear_meters = Required(float)
		deadline = Required(date)
		priority = Optional(int)
		real_linear_meters = Optional(float)
		estimated_cost = Optional(int)
		real_cost = Optional(int)
		difficulties = Set('Difficulties')
		tasks = Set('Tasks')
		employees = Set('Employees_Restrictions')
		restrictions = Set('Deadlines_Restrictions')
		activities = Set('Projects_Activities')
		fixed_planning = Optional(bool)
		fixed_priority = Optional(bool)


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
		projects = Set('Projects_Activities')
		employees = Set('Employees_Activities')

		def __repr__(self):
			return self.description
	
	class Projects_Activities(db.Entity):
		id = PrimaryKey(int, auto=False)
		project = Required(Projects)
		activity = Required(Activities)
		initial_date = Optional(date)
		end_date = Optional(date)
	
	class Employees_Activities(db.Entity):
		id = PrimaryKey(int, auto=False)
		employee = Required('Employees')
		activity = Required(Activities)
		initial_date = Optional(date)
		end_date = Optional(date)

	class Tasks(db.Entity):
		id = PrimaryKey(int, auto=False)
		skill = Required('Skills') #Arreglar la discrepancia de nombre
		# 'id_skill'
		id_project = Required(Projects)
		original_initial_date = Required(date) #Esto debería ser optional,
		# dejarse vacío y luego ser llenado automáticamente por el programa.
		original_end_date = Optional(date)#Esto debería ser optional,
		# dejarse vacío y luego ser llenado automáticamente por el programa.
		efective_initial_date = Optional(date)
		efective_end_date = Optional(date)
		failed = Optional(bool)
		fail_cost = Optional(int)
		employees = Set('Employees_Tasks')

		def __repr__(self):
			return str(self.id)

	class Employees_Tasks(db.Entity):
		task = Required(Tasks)
		employee = Required('Employees')
		PrimaryKey(employee, task)
		initial_date = Optional(date)
		end_date = Optional(date)
