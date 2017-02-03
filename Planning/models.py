from pony.orm import *
from datetime import datetime

def define_models(db):
	class Teams_Restrictions(db.Entity):
		team = Required('Teams')
		task = Required('Tasks')
		PrimaryKey(team, task)
		fixed = Required(bool)
		
		
	class Deadlines_Restrictions(db.Entity):
		id = PrimaryKey(int, auto=False)
		task_id = Required(int)
		deadline = Required(datetime)