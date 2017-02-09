from pony.orm import *
from datetime import date

# varias funciones relacionadas con buscar fechas donde haya suficientes empleados para una tarea

def IsHoliday(dt):
	holidays = [date(2017, 9, 18)]
	if dt in holidays:
		return True

def IsNotWorkday(dt):
	if dt.weekday() >= 5 or IsHoliday(dt):
		return True



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
		
def shiftDown(db, project, place, original_place):
	with db_session:
		projects = select(p for p in db.Projects order_by(asc(priority)) if p.priority >= place)
		for p in projects:
			if p.priority == original_place -1:
				if p.fixed_priority:
					project.priority = original_place
				else:
					project.priority = p.priority
					p.priority = original_place
			if not p.fixed_priority:
				project.priority = p.priority
				shiftDown(db, p, p.priority + 1, original_place)
				break 
				
def shiftUp(db,upper, lower):
	with db_session:
		projects = select(p for p in db.Projects order_by(asc(priority)) if p.priority <= lower and p.priority > upper)
		for p in projects:
			p.priority = p.priority - 1
				
		
def ChangePriority(db, id_project, new_priority):
	with db_session:
		old_priority = db.Projects[id_project].priority
		if old_priority > new_priority:
			projects = select(p for p in db.Projects order_by(asc(priority)) if p.priority >= new_priority and p.priority < db.Projects[id_project].priority)
			for p in projects:
				if p.fixed_priority:
					p.priority = p.priority +1
				else:
					shiftDown(db,p, p.priority +1, old_priority)
					break
			db.Projects[id_project].priority = new_priority	
		
		if old_priority < new_priority:
			shiftUp(db, db.Projects[id_project].priority, new_priority)
			db.Projects[id_project].priority = new_priority
				
					
				
			

