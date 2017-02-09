from pony.orm import *

def CreateEmployee(db, id, name, zone, perf_rect = None , perf_des = None, perf_fab = None, perf_inst = None):
	with db_session:
		db.Employees(id = id, name = name, zone = zone, )
		if perf_rect != None:
			db.Employees_Skills(employee = id, skill = 1, performance = perf_rect)
		if perf_des != None:
			db.Employees_Skills(employee = id, skill = 2, performance = perf_des)
		if perf_fab != None:
			db.Employees_Skills(employee = id, skill = 3, performance = perf_fab)
		if perf_inst != None:
			db.Employees_Skills(employee = id, skill = 4, performance = perf_inst)

def PrintEmployees(db):
	with db_session:
		db.Employees.select().show()	

def EditEmployee(db, id, new_name = None, new_zone = None, perf_rect = None, perf_des = None, perf_fab = None, perf_inst = None):
	with db_session:
		e = db.Employees[id]
		if new_zone != None:
			e.zone = new_zone
		if new_name != None:
			e.name = new_name
		if perf_rect != None and db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[1]) != None:
			db.Employees_Skills[(id, 1)].performance = perf_rect
		if perf_rect != None and db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[1]) == None:
			db.Employees_Skills(employee = id, skill = 1, performance = perf_rect)
		if perf_des != None:
			db.Employees_Skills[(id, 2)].performance = perf_des
		if perf_fab != None:
			db.Employees_Skills[(id, 3)].performance = perf_fab
		if perf_inst != None:
			db.Employees_Skills[(id, 4)].performance = perf_inst
			
def DeleteEmployee(db, id):
	with db_session:
		db.Employees[id].delete()

def PrintEmployeesSkills(db):
	with db_session:
		db.Employees_Skills.select().show()
		
def PrintSkills(db):
	with db_session:
		db.Skills.select().show()
	
def PrintSelectSkill(db, id_skill):
	with db_session:
		select(e for e in db.Employees if db.Skills[id_skill] in e.skills).show()

		
		
