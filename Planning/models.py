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
		task_id = Required(int)
		deadline = Required(datetime)
