from pony.orm import *

def FindDateEmployees(db, id_task, num_workers):
	

def AssignTask(db, id_employee, id_task, initial_date = None, end_date = None):
	with db_session:
		et = db.Employees_Tasks(employee = id_employee, task = id_task)
		if initial_date != None:
			et.initial_date = initial_date
		if end_date != None:
			et.end_date = end_date
	
def UnassignTask(db, id_employee, id_task):
	db.Employees_Tasks[(id_employee, id_task)].delete()
	# (task = id_task, team = id_team)
	
def AvailavilityUpdate(db)
	with db_session:
		select(et for et in db.Employees_Tasks if db.Tasks[et.task].efective_initial_date == None).delete()