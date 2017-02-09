from pony.orm import *
from datetime import date

def define_models(db):
	class Employees_Restrictions(db.Entity):
		employee = Required('Employees')
		task = Required('Tasks')
		PrimaryKey(employee, task)
		fixed = Required(bool)
		
	class Deadlines_Restrictions(db.Entity):
		task_id = PrimaryKey('Tasks')
		deadline = Required(date)
