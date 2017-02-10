from pony.orm import *
from datetime import date, timedelta

#################################################################################################################
# Acá empieza: varias funciones relacionadas con buscar fechas donde haya suficientes empleados para una tarea: #

# checked
def IsHoliday(dt):
	holidays = [date(2017, 9, 18), date(2017, 9, 20)]
	if dt in holidays:
		return True
	return False

#checked
def IsNotWorkday(dt):
	if dt.weekday() >= 5 or IsHoliday(dt):
		return True
	return False

#checked
def SumDays(dt, days):
	new_dt = dt
	delta = timedelta(days = 1)
	while(days > 0):
		new_dt = new_dt + delta
		while(IsNotWorkday(new_dt)):
			new_dt = new_dt + delta
		days = days - 1
	return new_dt

#checked
def GetAveragePerformance(db, id_skill):
	with db_session:
		emp_skills = select(es for es in db.Employees_Skills if es.skill == db.Skills[id_skill])
		perf = 0
		if len(emp_skills) > 0:
			for es in emp_skills:
				perf = perf + es.performance
			perf = perf/len(emp_skills)
		return perf

#notar que asume que siempre perf > 0, si no, se cae: o sea, asume que para cada skill hay al menos un empleado capaz de realizarla 
#checked
def GetDays(db, id_skill, contract_number, num_workers):
	with db_session:
		project = db.Projects[contract_number]
		linear_meters = project.linear_meters
		if project.real_linear_meters != None:
			linear_meters = project.real_linear_meters
		
		perf = GetAveragePerformance(db, id_skill)
		days = linear_meters/(num_workers * perf)
		return days

#checked with only one project_activity
#checked with several project_activity
def ClientAvailable(db, contract_number, initial_date, end_date):
	with db_session:
		proj_acts = select(pa for pa in db.Projects_Activities if pa.project == db.Projects[contract_number])
		for pa in proj_acts:
			if (pa.initial_date >= initial_date and pa.initial_date <= end_date) or (pa.end_date >= initial_date and pa.end_date <= end_date):
				return False
		return True

#checked
def EmployeesBySkill(db, id_skill):
	with db_session:
		ids_employees = []
		emps = select(e for e in db.Employees)
		for e in emps:
			es = db.Employees_Skills.get(employee = db.Employees[e.id], skill = db.Skills[id_skill])
			if es != None and es.performance > 0:
				ids_employees.append(e.id)
		return ids_employees

# ¿?
def EmployeesByStatus(db, contract_number, this_project, fixed):
	with db_session:
		ids_employees = []
		emps = select(e for e in db.Employees)
		for e in emps:
			es = db.Employees_Restrictions.get(employee = db.Employees[e.id])
			if es != None and this_project and es.contract_number = 
				ids_employees.append(e.id)
			return ids_employees
# ¿?
def FindEmployees(db, id_skill, num_workers, initial_date, end_date):
	with db_session:
		ids_employees = EmployeesBySkill(db, id_skill)
		emps = select(e for e in db.Employees if e.id in ids_employees and db.Employees_Restrictions)
		num_workers = num_workers - len(emps)
		if num_workers <= 0:
			return emps
		
		possible = 
		

def FindDatesEmployees(db, id_skill, contract_number, num_workers, current_date):
	days_from_current = 1
	task_days = GetDays(db, id_skill, contract_number, num_workers)
	while(True):
		initial_date = SumDays(initial_date, days_from_current)
		initial_date = SumDays(initial_date, days_from_current + task_days)
		if ClientAvailable(db, contract_number, initial_date, end_date):
			emps = FindEmployees(db, id_skill, initial_date, end_date)
			if len(emps) > 0:
				return initial_date, end_date, emps
			else:
				days_from_current = days_from_current + 1

# Acá termina: varias funciones relacionadas con buscar fechas donde haya suficientes empleados para una tarea: #
#################################################################################################################



#####################################################################
# Acá empieza: funciones para asignar/desasignar tareas a empleados #

def AssignTask(db, ids_employees, id_task, initial_date = None, end_date = None):
	with db_session:
		for id_employee in ids_employees:
			et = db.Employees_Tasks(employee = id_employee, task = id_task)
			et.initial_date = initial_date
			et.end_date = end_date
	
def UnassignTask(db, id_employee, id_task):
	with db_session:
		db.Employees_Tasks[(id_employee, id_task)].delete()
	
# Acá termina: funciones para asignar/desasignar tareas a empleados	#
#####################################################################	
	
def AvailabilityUpdate(db):
	with db_session:
		select(et for et in db.Employees_Tasks if et.task.efective_initial_date == None and not db.Projects[et.tasks.id].fixed_planning ).delete()
		
def shiftDown(db, project, place, original_place):
	with db_session:
		projects = select(p for p in db.Projects if p.priority >= place).order_by(lambda p: asc(p.priority))
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
		projects = select(p for p in db.Projects if p.priority <= lower and p.priority > upper).order_by(asc(priority))
		for p in projects:
			p.priority = p.priority - 1
				
		
def ChangePriority(db, id_project, new_priority):
	with db_session:
		old_priority = db.Projects[id_project].priority
		if old_priority > new_priority:
			projects = select(p for p in db.Projects if p.priority >= new_priority and p.priority < db.Projects[id_project].priority).order_by(asc(priority))
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
				
					
				
			

