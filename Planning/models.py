from pony.orm import *
from datetime import datetime

def define_models(db):
	class Employees_Restrictions(db.Entity):
		employee = Required('Employees')
		task = Required('Tasks')
		PrimaryKey(employee, task)
		fixed = Required(bool)
		
	class Deadlines_Restrictions(db.Entity):
		id = PrimaryKey(int, auto=False)
		project_id = Required('Projects')
		skill_id = Required('Skill')
		deadline = Required(datetime)
