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

# checked
def EmployeesByStatus(db, contract_number, ids_employees, this_project, fixed):
	with db_session:
		ids_status = []
		for id in ids_employees:
			emp_rests = select(er for er in db.Employees_Restrictions if er.employee == db.Employees[id])
			for es in emp_rests:
				if es != None and this_project and es.project == db.Projects[contract_number] and es.fixed == fixed:
					ids_status.append(id)
				elif es != None and (not this_project) and es.project != db.Projects[contract_number] and es.fixed == fixed:
					ids_status.append(id)
		return ids_status

#checked
def EmployeesAvailable(db, ids_employees, initial_date, end_date):
	with db_session:
		emp_acts = select(ea for ea in db.Employees_Activities if ea.employee.id in ids_employees)
		for ea in emp_acts:
			if (ea.initial_date >= initial_date and ea.initial_date <= end_date) or (ea.end_date >= initial_date and ea.end_date <= end_date):
				return False
		return True		

#checked
def HasNOnes(chosen, n):
	ones = 0
	for c in chosen:
		if c == 1:
			ones = ones + 1
	if ones == n:
		return True
	return False

#checked
def StringToList(as_string, chosen):
	for i in range(1, len(as_string) - 1):
		if as_string[-i] == '0':
			chosen[-i] = 0
		if as_string[-i] == '1':
			chosen[-i] = 1
	return chosen

#checked
def Successor(chosen, num_workers):
	as_string = ''
	last = [] # definimos la última combinación posible de elegidos para saber cuando parar
	for _ in range(0, num_workers): last.append(1)
	for _ in range(0, len(chosen) - num_workers): last.append(0)
	
	for c in chosen:
		if c == 0: as_string = as_string + '0'
		if c == 1: as_string = as_string + '1'
	
	chosen = StringToList(as_string, chosen)
	as_string = str(bin(int(as_string,2) + int('1',2)))
	
	while not HasNOnes(chosen, num_workers) and chosen != last:
		chosen = StringToList(as_string, chosen)
		as_string = str(bin(int(as_string,2) + int('1',2)))
	return chosen

#checked
def GetChosenIds(possibilities, chosen):
	ids = []
	for i in range(0, len(possibilities)):
		if chosen[i] == 1:
			ids.append(possibilities[i])
	return ids
	
#checked (kind of)
def FindEmployees(db, id_skill, contract_number, num_workers, initial_date, end_date):
	with db_session:		
		ids_employees = EmployeesBySkill(db, id_skill) # elegimos a los empleados con el skill necesario
		
		cluster1 = EmployeesByStatus(db, contract_number, ids_employees, True, True) # empleados fijos en este proyecto
		cluster2 = EmployeesByStatus(db, contract_number, ids_employees, True, False) # empleados vetados en este proyecto
		cluster3 = EmployeesByStatus(db, contract_number, ids_employees, False, True) # empleados fijos en otros proyectos
		cluster4 = EmployeesByStatus(db, contract_number, ids_employees, False, False) # empleados vetados en otros proyectos
		
		ids_employees = list(id for id in ids_employees if id not in cluster1 and id not in cluster2) # sacamos a todos los empleados vetados en este proyecto
		ids_found = cluster1  # incluimos sí o sí a los empleados que están fijos en el proyecto
		
		num_workers = num_workers - len(ids_found)
		if num_workers <= 0 and EmployeesAvailable(db, ids_found, initial_date, end_date): #revisamos si con los empleados fijos basta y si ellos están disponibles en las fechas necesarias
			return ids_found
		
		priority1 = list(id for id in ids_employees if id not in cluster3 and id in cluster4) # priorizamos empleados vetados en otros proyectos y NO fijos en otros proyectos
		priority2 = list(id for id in ids_employees if id not in cluster3 and id not in cluster4) # después, empleados ni fijos ni vetados en otros proyectos
		priority3 = list(id for id in ids_employees if id in cluster3 and id in cluster4) # después, empleados fijos en unos proyectos y vetados en otros
		priority4 = list(id for id in ids_employees if id in cluster3 and id not in cluster4) # por último, empleados fijos en otros proyectos y no vetados en ninguno
		
		possibilities = [] # ahora listamos todas las posibilidades, en orden de menos prioritario a más prioritario
		for id in priority4: possibilities.append(id)
		for id in priority3: possibilities.append(id)
		for id in priority2: possibilities.append(id)
		for id in priority1: possibilities.append(id)
		
		if num_workers > len(possibilities): # si no hay suficientes trabajadores nov etados para el trabajo, se devuelve lista vacía
			return []
		
		chosen = [] # elegimos (marcamos con 1) por defecto a los más prioritarios, si no tienen disponibilidad, vamos considerando a los menos prioritarios
		for _ in range(0, len(possibilities) - num_workers): chosen.append(0)
		for _ in range(0, num_workers): chosen.append(1)
		
		while(not EmployeesAvailable(db, ids_found + GetChosenIds(possibilities, chosen), initial_date, end_date)):
			if chosen == Succesor(chosen):
				return []
			chosen = Succesor(chosen)
			
		return ids_found + GetChosenIds(possibilities, chosen)
		

def FindDatesEmployees(db, id_skill, contract_number, num_workers, current_date):
	days_from_current = 1
	task_days = GetDays(db, id_skill, contract_number, num_workers)
	while(True):
		initial_date = SumDays(current_date, days_from_current)
		end_date = SumDays(current_date, days_from_current + task_days)
		if ClientAvailable(db, contract_number, initial_date, end_date):
			ids_found = FindEmployees(db, id_skill, contract_number, num_workers, initial_date, end_date)
			if len(ids_found) > 0:
				return initial_date, end_date, ids_found
			else:
				days_from_current = days_from_current + 1
		else:
			days_from_current+=1
		# else:
		# 	task_days = GetDays(db, id_skill, contract_number,
		# num_workers+1) #Esta opción debe estudiarse en la heurística que
		# se encuentra en el método "DoPlanning".

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
		
# Esta funcion borra las actividades que no están fijas y que no han empezado
#####################################################################
# Las siguientes funciones son para cambiar la prioridad
		
def shiftDown(db, project, place, original_place):
	with db_session:
		projects = select(p for p in db.Projects if p.priority >= place).order_by(lambda p: p.priority)
		for p in projects:
			if p.priority == original_place -1:
				if p.fixed_priority:
					project.priority = original_place
					break
				else:
					project.priority = p.priority
					p.priority = original_place
					break
			if not p.fixed_priority:
				project.priority = p.priority
				shiftDown(db, p, p.priority + 1, original_place)
				break 
# Función auxiliar. "empuja" la prioridad cuando es puede cambiar por no ser fijada por el usuario. Al tener que revisar esto
# preferí hacerlo recursivo y empujar de uno en uno
#check

				
def shiftUp(db,upper, lower):
	with db_session:
		projects = select(p for p in db.Projects if p.priority <= lower and p.priority > upper).order_by(lambda p: p.priority)
		for p in projects:
			p.priority = p.priority - 1
			
#Función auxiliar. Empuja hacia arriba las prioridades. En este caso la prioridad de todos cambia ya que mejora.
#check		
		
def ChangePriority(db, contract_number, new_priority):
	with db_session:
		old_priority = db.Projects[contract_number].priority
		if old_priority > new_priority:
			projects = select(p for p in db.Projects if p.priority >= new_priority and p.priority < db.Projects[contract_number].priority).order_by(lambda p: p.priority)
			for p in projects:
				if p.fixed_priority:
					p.priority = p.priority +1
				else:
					shiftDown(db,p, p.priority +1, old_priority)
					break
			db.Projects[contract_number].priority = new_priority
			db.Projects[contract_number].fixed_priority = True
		if old_priority < new_priority:
			shiftUp(db, db.Projects[contract_number].priority, new_priority)
			db.Projects[contract_number].priority = new_priority
			db.Projects[contract_number].fixed_priority = True
			db.Projects.select().order_by(lambda p: p.contract_number)
#Funcion para cambiar la prioridad de manera manual. Luego de cambiarla, la prioridad se marca como fijada por el usuario.
#check


##########################
# Hacer la planificación #
##########################
def DoPlanning(db):
	with db_session:
		projects = select(p for p in db.Projects).order_by(lambda p : p.priority)
		for p in projects:
			d_t=date.today()#+timedelta(date(2017,2,18).day-date.today().day)			
			
			tasks = select(t for t in db.Tasks if t.id_project.contract_number == p.contract_number).order_by(lambda t : t.id_skill)
			for t in tasks:
				if(t.skill.id<4 and t.efective_initial_date ==
					None):#obtiene el id del skill correspondiente a esa
					# tarea y revisa que no corresponda a una 'Instalación'.
					#  También revisa que la realización de la tarea aún no
					# haya comenzado (que sea 'planificable').
					(initial, ending, emps) = FindDatesEmployees(db,
																  t.id_skill.id, p.contract_number,1, d_t)
					days=ending.day-initial.day
					AssignTask(db,emps,t.id,initial,ending)
					d_t=d_t+timedelta(days)
					
					if(d_t > p.deadline):
						AvailabilityUpdate(db)
						#ShowDelayed(db)
				if(t.id_skill.id == 4 and t.efective_initial_date == None):
					num_workers=1
					while (num_workers<=4):
						(initial,ending,emps)=FindDatesEmployees(db, t.id_skill.id, p.contract_number, num_workers, d_t)
						days=ending.day-initial.day
						AssignTask(db, emps, t.id, initial, ending)
						if(num_workers==4 and d_t+timedelta(days)>p.deadline):
							AvailabilityUpdate(db)
							#ShowDelayed(db)
							break
						if(num_workers < 4 and d_t+timedelta(days)>p.deadline):
							num_workers=num_workers+1
						



			

