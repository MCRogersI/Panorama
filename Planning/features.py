from pony.orm import *
import datetime as datetime

def FindDateEmployees(db, id_task, num_workers, current_date):
	

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
	
def AvailabilityUpdate(db):
	with db_session:
		select(et for et in db.Employees_Tasks if et.task.efective_initial_date == None and not db.Projects[et.tasks.id].fixed_planning ).delete()
		
		
		
# def ChangePriority(db, id_project, new_priority):
	# with db_session:
		# if db.Projects[id_project].priority > new_priority:
			# projects = select(p for p in db.Projects order_by(asc(priority)) if p.priority <= new_priority)
			# for p in projects:
				
			

