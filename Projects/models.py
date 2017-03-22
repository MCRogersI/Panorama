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
		engagements = Set('Engagements')
		crystal_leadtime = Optional(int, default = 15)


		def __repr__(self):
			return str(self.contract_number)

	# dificultades tipo "construcción en altura"
	class Difficulties(db.Entity):
		id = PrimaryKey(int, auto=False)
		description = Required(str)
		projects = Set(Projects)

		def __repr__(self):
			return self.description

	# actividades tipo "licencia", "vacaciones", etc. Una actividad necesariamente implica no trabajar.
	class Activities(db.Entity):
		id = PrimaryKey(int, auto=False)
		description = Required(str)
		projects = Set('Projects_Activities')
		employees = Set('Employees_Activities')

		def __repr__(self):
			return self.description
	
	class Projects_Activities(db.Entity):
		id = PrimaryKey(int, auto=True)
		project = Required(Projects)
		activity = Required(Activities)
		initial_date = Optional(date)
		end_date = Optional(date)
	
	class Projects_Delays(db.Entity):
		id = PrimaryKey(int, auto = True)
		project_id = Required(int)
		skill_id = Required(int)
		delay = Required(int)
	
	class Employees_Activities(db.Entity):
		id = PrimaryKey(int, auto=True)
		employee = Required('Employees')
		activity = Required(Activities)
		initial_date = Optional(date)
		end_date = Optional(date)

	class Tasks(db.Entity):
		id = PrimaryKey(int, auto=True)
		skill = Required('Skills')
		project = Required(Projects)
		original_initial_date = Required(date) #Esto debería ser optional,
		# dejarse vacío y luego ser llenado automáticamente por el programa.
		original_end_date = Required(date)#Esto debería ser optional,
		# dejarse vacío y luego ser llenado automáticamente por el programa.
		effective_initial_date = Optional(date)
		effective_end_date = Optional(date)
		failed = Optional(bool)
		fail_cost = Optional(int)
		employees = Set('Employees_Tasks')

		def __repr__(self):
			return str(self.id)

	class Employees_Tasks(db.Entity):
		task = Required(Tasks)
		employee = Required('Employees')
		PrimaryKey(employee, task)
		planned_initial_date = Optional(date)
		planned_end_date = Optional(date)
