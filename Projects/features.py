from pony.orm import *
from datetime import date, datetime


def createProject(db, contract_number, client_address, client_comuna,
				  client_name, client_rut, linear_meters, deadline,
				  real_linear_meters = None, estimated_cost = None,
				  real_cost = None):
	import Planning.features as Pf
	with db_session:
		p = db.Projects(contract_number = contract_number, client_address = client_address, client_comuna=client_comuna, client_name = client_name, client_rut = client_rut, linear_meters = linear_meters, deadline=deadline, estimated_cost = estimated_cost)
		if real_linear_meters != None:
			p.real_linear_meters = real_linear_meters
		if real_cost != None:
			p.real_cost = real_cost
		
		############################################################
		# La siguiente función es para asignar la prioridad al crear el proyecto. por ahora se hará FIFO ya que no sabemos estimar la holgura, pero debe cambiar después.
		#DEBE CAMBIAR DESPUES
		db.Projects[contract_number].priority = db.Projects.select().count()
		#NO ES BROMA!!
	#?????????????????????????????	
		#############################################################
	Pf.doPlanning(db)
	
	
def printProjects(db):
    with db_session:
        db.Projects.select().show()

def editProject(db, contract_number, new_client_address = None, new_client_comuna = None, new_client_name = None, new_client_rut = None , new_linear_meters = None, new_real_linear_meters = None, new_deadline = None, new_estimated_cost = None, new_real_cost = None):
	with db_session:
		p = db.Projects[contract_number]
		if new_client_address != None:
			p.client_addres = new_client_address
		if new_client_comuna != None:
			p.client_comuna = new_client_comuna
		if new_client_name != None:
			p.client_name = new_client_name
		if new_client_rut != None:
			p.client_rut = new_client_rut
		if new_linear_meters != None:
			p.linear_meters = new_linear_meters
		if new_deadline != None:
			p.deadline = new_deadline
		if new_real_linear_meters != None:
			p.real_linear_meters = new_real_linear_meters
		if new_estimated_cost != None:
			p.estimated_cost = new_estimated_cost
		if new_real_cost != None:
			p.real_cost = new_real_cost
			
def deleteProject(db, contract_number):
	with db_session:
		db.Projects[contract_number].delete()

def getCostProject(db, contract_number, fixed_cost, variable_cost):
	''' Este método entrega el costo de un proyecto considerando que hay un costo fijo y además 
		un costo variable que depende de los metros lineales del proyecto, hasta el momento 
		estos parámetros se ingresan cada vez que se quiera calcular el costo de un proyecto'''
	with db_session:
		try:	
			engagements = select(e for e in db.Engagements if e.project == db.Projects[contract_number])
			cost=fixed_cost+variable_cost*db.Projects[contract_number].linear_meters
			for e in engagements:
				cost=cost + e.sku.price*e.quantity
			return cost
		except ObjectNotFound as e:
			print('Object not found: {}'.format(e))
		except ValueError as e:
			print('Value error: {}'.format(e))


def createTask(db, id_skill, contract_number, original_initial_date, original_end_date, effective_initial_date = None, effective_end_date = None):
	with db_session:
		t = db.Tasks(skill = id_skill, project = contract_number, original_initial_date = original_initial_date, original_end_date = original_end_date)

		
def editTask(db, id , id_skill = None, contract_number = None, original_initial_date = None, original_end_date = None, effective_initial_date = None, effective_end_date = None, fail_cost = None):
	with db_session:
		t = db.Tasks[id]
		if id_skill != None:
			t.skill = id_skill #pendiente: revisar si funciona así o si tiene que ser como t.skill = db.Skills[id_skill]
		if contract_number != None: 
			t.project = contract_number #pendiente: revisar si funciona así o si tiene que ser como t.project = db.Projects[contract_number]
		if original_initial_date != None:
			t.original_initial_date = original_initial_date
		if original_end_date != None:
			t.original_end_date = original_end_date
		if effective_initial_date != None:
			t.effective_initial_date = effective_initial_date
		if effective_end_date != None:
			t.effective_end_date = effective_end_date
		if fail_cost != None:
			t.fail_cost = fail_cost

def deleteTask(db, id_task):
	with db_session:
		db.Tasks[id_task].delete()

def printTasks(db):
	with db_session:
		db.Tasks.select().show()

def failedTask(db, contract_number, id_skill, fail_cost):
	import Planning.features as PLf
	with db_session:

		tasks = select(t for t in db.Tasks if t.skill >= db.Skills[id_skill] and t.project == db.Projects[contract_number] and t.failed == None)
		for t in tasks:
			t.failed = True
			if t.skill == db.Skills[id_skill]:
				t.fail_cost = fail_cost
		
		tasks = select(t for t in db.Tasks if t.skill.id > id_skill and t.project == db.Projects[contract_number] and t.effective_end_date == None)
		for t in tasks:
			t.delete()

		PLf.doPlanning(db)

		
		
		
		
# métodos asociados a Employees_Activities (llamados en usuario.py de carpeta Employees)
def createEmployeeActivity(db, employee, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day):
	import Planning.features as PLf
	initial_date = date(int(initial_year), int(initial_month), int(initial_day))
	end_date = date(int(end_year), int(end_month), int(end_day))
	with db_session:
		db.Employees_Activities(employee = employee, activity = activity, initial_date = initial_date, end_date = end_date)
	if updateEmployeeProjects(db, employee, initial_date, end_date):
		PLf.doPlanning(db)
		
def updateEmployeeProjects(db, employee, initial_date, end_date):
	changed = False
	with db_session:
		emp_tasks = select(et for et in db.Employees_Tasks if et.employee.id == employee)
		for et in emp_tasks:
			if (initial_date >= et.planned_initial_date and initial_date <= et.planned_end_date)\
					or (end_date >= et.planned_initial_date and end_date <= et.planned_end_date):
				et.task.project.fixed_planning = False
				##aqui se va a desfijar el proyecto para que no haga planificaciones infactibles
				delete(er for er in db.Employees_Restrictions if er.employee.id == employee and er.project == et.task.project and er.fixed == True)
				## esto desfija al empleado de un proyecto si se va de vacaciones, privilegiando la fecha de entrega sobre la preferencia del cliente
				changed = True
	return changed

		
def deleteEmployeeActivity(db, id_employee_activity):
	with db_session:
		db.Employees_Activities[id_employee_activity].delete()
		
def printEmployeesActivities(db):
	with db_session:
		db.Employees_Activities.select().show()
		
		
		
		
		
# métodos asociados a Projects_Activities (llamados en usuario.py de carpeta Projects)
def createProjectActivity(db, project, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day):
	initial_date = datetime.strptime(initial_year + '-' + initial_month + '-' + initial_day, '%Y-%m-%d')
	end_date = datetime.strptime(end_year + '-' + end_month + '-' + end_day, '%Y-%m-%d')
	with db_session:
		db.Projects_Activities(project = project, activity = activity, initial_date = initial_date, end_date = end_date)
		
def deleteProjectActivity(db, id_project_activity):
	with db_session:
		db.Projects_Activities[id_project_activity].delete()
		
def printProjectsActivities(db):
	with db_session:
		db.Projects_Activities.select().show()