from pony.orm import *
from datetime import date

def define_models(db):
	class Employees_Restrictions(db.Entity):
		employee = Required('Employees')
		project = Required('Projects')
		PrimaryKey(employee, project)
		fixed = Required(bool)
		
	class Deadlines_Restrictions(db.Entity):
		id = PrimaryKey(int)
		project = Required('Projects')
		skill = Required('Skills')
		deadline = Required(date)
