from pony.orm import *
from datetime import date, datetime, timedelta
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
import Stock.features as Sf


def createProject(db, contract_number, client_address, client_comuna,
				  client_name, client_rut, linear_meters, year, month,
				  day, real_linear_meters = None, estimated_cost = None,
				  real_cost = None, crystal_leadtime = 15):
	import Planning.features as PLf
	with db_session:
		deadline = date(int(year), int(month), int(day))
		p = db.Projects(contract_number = contract_number, client_address = client_address, client_comuna=client_comuna, client_name = client_name, client_rut = client_rut, linear_meters = linear_meters, deadline=deadline, estimated_cost = estimated_cost, crystal_leadtime = crystal_leadtime)
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
	PLf.doPlanning(db)
	
	
def printProjects(db):
    with db_session:
        db.Projects.select().show()

def editProject(db, contract_number, new_client_address = None, new_client_comuna = None, new_client_name = None, new_client_rut = None , new_linear_meters = None, new_real_linear_meters = None, new_deadline = None, new_estimated_cost = None, new_real_cost = None, new_crystal_leadtime = None):
	with db_session:
		try:
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
            if new_crystal_leadtime != None:
				p.crystal_leadtime = crystal_leadtime
		except ObjectNotFound as e:
			print('Object not found: {}'.format(e))
		except ValueError as e:
			print('Value error: {}'.format(e))
			
def deleteProject(db, contract_number):
	with db_session:
		db.Projects[contract_number].delete()

def getNumberConcurrentProjects(db, contract_number, date):
	''' Método que entrega la cantidad de proyectos que son realizados en la misma comuna,
	en la misma fecha, para calcular los costos de transporte si es que hay más de uno en un lugar
	en la misma fecha '''
	p = db.Projects[contract_number]
	candidates = select(pr for pr in db.Projects if pr.client_comuna == p.client_comuna and pr != p)
	quant = 1
	for pr in candidates:
		inst = db.Tasks.get(skill = 4, project = pr)
		et_ins = select(et for et in db.Employees_Tasks if et.task == inst)
		for et in et_ins:
			if(et.planned_initial_date == date):
				quant += 1
	return quant

def getCostRM(db, contract_number):#RM = Raw Materials
	''' Este método obtiene el costo de las materias primas según lo especificado en el Excel'''
	with db_session:
		p = db.Projects[contract_number]
		total_sum = 0

		for e in p.engagements:
			total_sum += e.sku.price*e.quantity*(1+e.sku.waste_factor)
	return total_sum
def getCostInstallation(db, contract_number, internal = True):
	''' Cálculo de los costos de instalación según lo especificado en el excel '''
	with db_session:
		total_cost = 0
		p = db.Projects[contract_number]
		price_ml = db.Operating_Costs['Costo por metro lineal de instalacion'].cost
		task_aux = db.Tasks.get(skill = 4, project = p)
		et_ins = select(et for et in db.Employees_Tasks if et.task == task_aux)
		aux = 1
		for et in et_ins:
			et_aux = et
			aux += 1
			if aux >= 1:
				break

		if internal:
			total_cost += p.linear_meters*price_ml
		else:
			total_cost += p.linear_meters*price_ml*1.5 #suponiendo que contratar un
			# instalador externo cuesta 1.5 veces más
		num_projects = getNumberConcurrentProjects(db, contract_number, et_aux.planned_initial_date)
		total_cost += db.Freight_Costs[p.client_comuna].freight_cost/num_projects
		total_cost += db.Operating_Costs['Viatical per day'].cost*len(et_ins)
		total_cost += db.Operating_Costs['Costo por metro lineal de instalacion'].cost*p.linear_meters
		total_cost = total_cost*db.Waste_Factors[5].factor
		return total_cost
def getCostFabrication(db, contract_number):
	'''Cálculo de costos de fabricación según lo especificado en el excel'''
	#hay que tener los metros lineales vendidos al mes, aqui los fijo según el excel
	monthly_selled_ml = 240
	monthly_income = 80000000 #venta promedio mensual, basada en el año
	total_cost = 0
	p = db.Projects[contract_number]
	total_cost += db.Operating_Costs['Remuneracion fija fabrica'].cost
	total_cost += db.Operating_Costs['Remuneracion variable fabrica'].cost
	total_cost += db.Operating_Costs['Porcentaje ventas para materiales'].cost*monthly_income
	total_cost += db.Operating_Costs['Arriendo fabrica'].cost
	total_cost += db.Operating_Costs['Costos operacion'].cost
	total_cost = total_cost/monthly_selled_ml
	total_cost = total_cost*p.linear_meters
	return total_cost




def getCostProject(db, contract_number):
	''' Obtención de los costos de un proyecto '''
	with db_session:
		rmc = getCostRM(db, contract_number)
		ic = getCostInstallation(db, contract_number, internal = True)
		fc = getCostFabrication(db, contract_number)
		return rmc + ic + fc
def createTask(db, id_skill, contract_number, original_initial_date, original_end_date, effective_initial_date = None, effective_end_date = None):
	with db_session:
		t = db.Tasks(skill = id_skill, project = contract_number, original_initial_date = original_initial_date, original_end_date = original_end_date)

		
def editTask(db, id , id_skill = None, contract_number = None, original_initial_date = None, original_end_date = None, effective_initial_date = None, effective_end_date = None, fail_cost = None):
	with db_session:
		try:
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
		except ObjectNotFound as e:
			print('Object not found: {}'.format(e))
		except ValueError as e:
			print('Value error: {}'.format(e))

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

def createDelay(db, project_id, skill_id, delay):
	'''Este método ingresa un delay en la tarea con id skill = skill_id del proyecto con id = project_id, alargando el end date en delay días. 		
	Todo está con ints porque si no, había problemas con los reverses, ver aquí: https://docs.ponyorm.com/relationships.html '''
	with db_session:
		try:
			if skill_id < 4:
				p = db.Projects[project_id]
				t = db.Tasks.get(skill = db.Skills[skill_id], project = p)
				db.Projects_Delays(project_id = project_id, skill_id = skill_id, delay = delay)
				et = db.Employees_Tasks.get(task = t)
				et.planned_end_date = et.planned_end_date+timedelta(delay)
				skill_aux = skill_id + 1
				while skill_aux <= 4:#si es una actividad anterior a instalación, atrasa todas las 
				#tareas que le siguen
					t_aux = db.Tasks.get(skill = db.Skills[skill_aux], project = p)
					et_aux = db.Employees_Tasks.get(task = t_aux)
					et_aux.planned_initial_date = et_aux.planned_initial_date + timedelta(delay)
					et_aux.planned_end_date = et_aux.planned_end_date+timedelta(delay)
					skill_aux += 1
			else:
				p = db.Projects[project_id]
				t = db.Tasks.get(skill = db.Skills[skill_id], project = p)
				db.Projects_Delays(project_id = project_id, skill_id = skill_id, delay = delay)
				et = db.Employees_Tasks.get(task = t)#si es una instalación con varios trabajadores
				#asignados podría no funcionar esta línea
				et.planned_end_date = et.planned_end_date+timedelta(delay)
		except ObjectNotFound as e:
			print('Object not found: {}'.format(e))
		except ValueError as e:
			print('Value error: {}'.format(e))



# métodos asociados a Employees_Activities (llamados en usuario.py de carpeta Employees)
def createEmployeeActivity(db, employee, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day):
	'''
	Crea una actividad para un empleado de tipo licencia, vacaciones u otros. en caso de que el empleado tenga asignada una tarea en las fechas de la actividad, se replanifica
	'''
	import Planning.features as PLf
	initial_date = date(int(initial_year), int(initial_month), int(initial_day))
	end_date = date(int(end_year), int(end_month), int(end_day))
	with db_session:
		db.Employees_Activities(employee = employee, activity = activity, initial_date = initial_date, end_date = end_date)
	if updateEmployeeProjects(db, employee, initial_date, end_date):
		PLf.doPlanning(db)
		
def updateEmployeeProjects(db, employee, initial_date, end_date):
	'''
	Este metodo revisa si un empleado tiene tareas asignadas durante las fechas impuestas y ,de ser cierto, deja móviles dichas actividades para una
	futura replanificación. Es un método auxiliar, por lo que no es recomendable usarlo directamente.
	'''
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
        commit()
        
def printEmployeesActivities(db):
	with db_session:
		db.Employees_Activities.select().show()
		

		
# métodos asociados a Projects_Activities (llamados en usuario.py de carpeta Projects)
def createProjectActivity(db, project, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day):
	import Planning.features as PLf
	initial_date = date(int(initial_year), int(initial_month), int(initial_day))
	end_date = date(int(end_year), int(end_month), int(end_day))
	with db_session:
		db.Projects_Activities(project = project, activity = activity, initial_date = initial_date, end_date = end_date)
	if updateProjectActivities(db, project, initial_date, end_date):
		PLf.doPlanning(db)

def updateProjectActivities(db, project, initial_date, end_date):
	'''
	Este metodo revisa si un proyecto tiene tareas asignadas durante las fechas impuestas y ,de ser cierto, deja móviles dichas actividades para una
	futura replanificación. Es un método auxiliar, por lo que no es recomendable usarlo directamente.
	'''
	changed = False
	with db_session:
		tasks_project = select(tp for tp in db.Employees_Tasks if tp.task.project.contract_number == project and tp.task.skill.id in [1,4])
		for tp in tasks_project:
			if (initial_date >= tp.planned_initial_date and initial_date <= tp.planned_end_date)\
					or (end_date >= tp.planned_initial_date and end_date <= tp.planned_end_date):
				tp.task.project.fixed_planning = False
				##aqui se va a desfijar el proyecto para que no haga planificaciones infactibles
				changed = True
	return changed
		
def deleteProjectActivity(db, id_project_activity):
	with db_session:
		db.Projects_Activities[id_project_activity].delete()
		
def printProjectsActivities(db):
	with db_session:
		db.Projects_Activities.select().show()
def getListProducts(db):
	with db_session:
		wb = load_workbook('Products.xlsx')
		ws = wb['Hoja2']
		r = 13
		while ws.cell(row = r, column = 2 ).value != None:
			stock_id = int(ws.cell(row = r, column = 2).value)
			stock_engname = ws.cell(row = r, column = 4).value
			stock_europrice = ws.cell(row = r, column = 5).value
			stock_packingquantity = int(ws.cell(row = r, column = 7).value)
			Sf.createSku(db, stock_id, stock_engname, stock_europrice, stock_packingquantity*50, stock_packingquantity*75, 0.03)
			#Asumimos que el nivel crítico es 50 veces el packing quantity, por mientras. 0 = estaba vacío en el excel. 
			#Asumimos además que la cantidad real (para hacer correr el programa, en realidad al comenzar a usar el 
			#software se debería saber las cantidades reales de todos los SKUs) es 1.5 veces el nivel crítico.
			#Asumimos que el factor de pérdida es 0.03 para todos los SKUs, eventualmente la tabla Products debería tener 
			#el factor de pérdida asociado al código del SKU.
			r += 1


def getProjectFeatures(db, contract_number):
	''' Método para obtener los parámetros de un proyecto desde un archivo de excel estandarizado '''
	wb = load_workbook('EjemploPropuestaProyecto '+str(contract_number)+'.xlsx')
	ws = wb['Edif A_Hoja Corte']
	
	
	
	with db_session:
		#Asumiremos, para fijar una fecha inicial, que los engagement se realizarán al comienzo de la fabricación
		p = db.Projects[contract_number]
		task_aux = db.Tasks.get(skill = 3, project = p)
		et_fab = db.Employees_Tasks.get(task = task_aux)
		withdrawal = et_fab.planned_initial_date
		glass_id = int(ws.cell(row = 16, column = 2).value)
		glass_m2 = ws.cell(row = 50, column  = 3).value
		Sf.createEngagement(db, contract_number, [(glass_id, glass_m2)], withdrawal_date = withdrawal)
		# glass_ml = ws.cell(row = 51, column  = 3).value#no es necesario
		upper_profile_id = int(ws.cell(row = 58, column  = 2).value)
		upper_profile_ml = ws.cell(row = 70, column  = 3).value
		Sf.createEngagement(db, contract_number, [(upper_profile_id, upper_profile_ml)], withdrawal_date = withdrawal)
		lower_profile_id = int(ws.cell(row = 72, column  = 2).value)
		lower_profile_ml = ws.cell(row = 84, column  = 3).value
		Sf.createEngagement(db, contract_number, [(lower_profile_id, lower_profile_ml)], withdrawal_date = withdrawal)
		teles_profile_id = int(ws.cell(row = 86, column  = 2).value)
		teles_profile_ml = ws.cell(row = 98, column  = 3).value
		Sf.createEngagement(db, contract_number, [(teles_profile_id, teles_profile_ml)], withdrawal_date = withdrawal)
		glassing_bead_id = int(ws.cell(row = 98, column = 14).value)
		glassing_bead_ml = ws.cell(row = 100, column  = 14).value
		glassing_bead_price = ws.cell(row = 105, column  = 15).value#no sé donde podría utilizarse
		Sf.createEngagement(db, contract_number, [(glassing_bead_id, glassing_bead_ml)], withdrawal_date = withdrawal)

		#hasta acá no debería ser un problema mantener el formato.
		#Components to glass panes:
		c1 = 142
		while ws.cell(row = c1, column = 1).value != None:
			ide =  ws.cell(row = c1, column = 1).value
			quantity  =  ws.cell(row = c1, column = 6).value
			Sf.createEngagement(db, contract_number, [(ide, quantity)], withdrawal_date = withdrawal)
			c1 +=1
		# Components to component box or profiles:
		c2 = c1+1
		while  ws.cell(row = c2, column = 1).value != None:
			ide =  ws.cell(row = c2, column = 1).value
			quantity  =  ws.cell(row = c2, column = 6).value
			Sf.createEngagement(db, contract_number, [(ide, quantity)], withdrawal_date = withdrawal)
			c2 +=1
		#Components to component box
		c3 = 142
		while  ws.cell(row = c3, column = 8).value != None:
			ide =  ws.cell(row = c2, column = 8).value
			quantity  =  ws.cell(row = c2, column = 14).value
			Sf.createEngagement(db, contract_number, [(ide, quantity)], withdrawal_date = withdrawal)
			c3 +=1
		#Sealings:
		c4 = 181
		while ws.cell(row = c4, column = 1).value != None:
			ide =  ws.cell(row = c4, column = 1).value
			quantity  =  ws.cell(row = c4, column = 3).value
			Sf.createEngagement(db, contract_number, [(ide, quantity)], withdrawal_date = withdrawal)
			c4 += 1







	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
