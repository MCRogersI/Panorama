from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from Planning.reports import createReport

#################################################################################################################
# Acá empieza: varias funciones relacionadas con buscar fechas donde haya suficientes empleados para una tarea: #

# checked
def isHoliday(dt):
    holidays = [date(2017, 4, 14), date(2017, 4, 15), date(2017, 4, 19), date(2017, 5, 1), \
                date(2017, 5, 21), date(2017, 6, 26), date(2017, 7, 2), date(2017, 7, 16), \
                date(2017, 8, 15), date(2017, 9, 18), date(2017, 9, 19), date(2017, 10, 9), \
                date(2017, 10, 27), date(2017, 11, 1), date(2017, 11, 19), date(2017, 12, 8), \
                date(2017, 12, 17), date(2017, 12, 25)]
    if dt in holidays:
        return True
    return False

#checked
def isNotWorkday(dt):
    if dt.weekday() >= 5 or isHoliday(dt):
        return True
    return False

#checked
def sumDays(dt, days):
    new_dt = dt
    delta = timedelta(days = 1)
    while(days > 0):
        new_dt = new_dt + delta
        while(isNotWorkday(new_dt)):
            new_dt = new_dt + delta
        days = days - 1
    return new_dt

#checked
def getAveragePerformance(db, id_skill):
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
#pendiente: en el caso de fabricación, hay que tomar el máximo entre el valor calculado acá y los 15 días de los cristales
#pendiente: como los cristales pueden ser otro número aparte de 15 días, eso debiera ser una columna en Projects, que por defecto sea 15, pero que el usuario pueda cambiar
def getDays(db, id_skill, contract_number, num_workers):
    with db_session:
        # rectificadores y disenadores solo demoran un día, funcionan en base a proyectos/día.
        if id_skill == 1 or id_skill == 2:
            return 1
        project = db.Projects[contract_number]
        linear_meters = project.linear_meters
        if project.real_linear_meters != None:
            linear_meters = project.real_linear_meters
        
        perf = getAveragePerformance(db, id_skill)
        days = linear_meters/(num_workers * perf)
        return days

#checked with only one project_activity
#checked with several project_activity
def clientAvailable(db, contract_number, initial_date, end_date):
    with db_session:
        proj_acts = select(pa for pa in db.Projects_Activities if pa.project == db.Projects[contract_number])
        for pa in proj_acts:
            if (pa.initial_date >= initial_date and pa.initial_date <= end_date) or (pa.end_date >= initial_date and pa.end_date <= end_date):
                return False
        return True

#checked
def employeesBySkill(db, id_skill, senior):
    with db_session:
        ids_employees = []
        emps = select(e for e in db.Employees)
        for e in emps:
            es = db.Employees_Skills.get(employee = db.Employees[e.id], skill = db.Skills[id_skill])
            if es != None and es.performance > 0:
                # en el caso de instaladores, revisamos que además sean senior
                if id_skill == 4:
                    if e.senior == senior:
                        ids_employees.append(e.id)
                else:
                    ids_employees.append(e.id)
        return ids_employees

# checked
def employeesByStatus(db, contract_number, ids_employees, this_project, fixed):
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

# checked
def datesOverlap(initial_date_1, end_date_1, initial_date_2, end_date_2):
    if initial_date_1 <= initial_date_2 and end_date_1 >= initial_date_2:
        return True
    elif initial_date_1 >= initial_date_2 and end_date_1 <= end_date_2:
        return True
    elif initial_date_1 <= end_date_2 and end_date_1 >= end_date_2:
        return True
    return False

def fillCommitments(commitments, initial_date, end_date, planned_initial_date, planned_end_date):
    # si las fechas no se solapan entonces no hay commitments que agregar
    if not datesOverlap(initial_date, end_date, planned_initial_date, planned_end_date):
        return commitments
    # si las fechas sí se solapan, entonces los siguientes minimos y maximos tienen sentido
    initial_index = max(0, (planned_initial_date - initial_date).days)
    end_index = min(len(commitments) - 1, len(commitments) - (end_date - planned_end_date).days - 1)
    while(initial_index <= end_index):
        commitments[initial_index] = commitments[initial_index] + 1
        initial_index = initial_index + 1
    return commitments

#checked
def employeesAvailable(db, ids_employees, initial_date, end_date, id_skill):
    with db_session:
        emp_acts = select(ea for ea in db.Employees_Activities if ea.employee.id in ids_employees)

        for ea in emp_acts:
            if 9 in ids_employees:
                print(ea.initial_date + " " + ea.end_date)
            if datesOverlap(initial_date, end_date, ea.initial_date, ea.end_date):
                return False
        # acá los rectificadores y disenadores se diferencian de los otros dos, porque pueden estar en más de un proyecto por día
        if id_skill == 3 or id_skill == 4:
            emp_tasks = select(et for et in db.Employees_Tasks if et.employee.id in ids_employees)
            for et in emp_tasks:
                if datesOverlap(initial_date, end_date, et.planned_initial_date, et.planned_end_date):
                    return False
            return True
        # asi, para rectificadores y disenadores, hay que revisar para cada empleado que no se pase en ningún día la cantidad de proyectos/día
        else:
            emps = select(e for e in db.Employees if e.id in ids_employees)
            # los Tasks asociados a Skills 3 y 4 no pueden solaparse nunca con otros Tasks, asi que eso lo revisamos primero
            emp_tasks = select(et for et in db.Employees_Tasks if et.employee.id in ids_employees and et.task.skill.id >= 3)
            for et in emp_tasks:
                if datesOverlap(initial_date, end_date, et.planned_initial_date, et.planned_end_date):
                    return False
            # ahora si revisamos que no se supere la cantidad de proyectos por dia
            for e in emps:
                # creamos un arreglo de puros 0's de largo el lapso de tiempo entre initial_date y end_date, y lo vamos llenando con las tareas que tienen
                commitments_skill_1 = np.zeros( abs((end_date - initial_date).days) + 1 )
                commitments_skill_2 = np.zeros( abs((end_date - initial_date).days) + 1 )
                emp_tasks_skill_1 = select(et for et in db.Employees_Tasks if et.employee == e and et.task.skill.id == 1)
                emp_tasks_skill_2 = select(et for et in db.Employees_Tasks if et.employee == e and et.task.skill.id == 2)
                for et in emp_tasks_skill_1:
                    commitments_skill_1 = fillCommitments(commitments_skill_1, initial_date, end_date, et.planned_initial_date, et.planned_end_date)
                for et in emp_tasks_skill_2:
                    commitments_skill_2 = fillCommitments(commitments_skill_2, initial_date, end_date, et.planned_initial_date, et.planned_end_date)
                
                # vemos cuánto es lo máximo que puede hacer por día, entre ambos Skills (si alguno es 0, solo entre un Skill)
                es = db.Employees_Skills.get(employee = db.Employees[e.id], skill = db.Skills[id_skill])
                limit = np.floor(es.performance)
                es_skill_1 = db.Employees_Skills.get(employee = db.Employees[e.id], skill = db.Skills[1])
                es_skill_2 = db.Employees_Skills.get(employee = db.Employees[e.id], skill = db.Skills[2])
                # en este caso nos fijamos solo en los Tasks del Skill 2
                if es_skill_1 == None:
                    limit_skill_2 = np.floor(es_skill_2.performance)
                    for c in commitments_skill_2:
                        if c >= limit_skill_2:
                            return False
                # en este caso nos fijamos solo en los Tasks del Skill 1
                elif es_skill_2 == None:
                    limit_skill_1 = np.floor(es_skill_1.performance)
                    for c in commitments_skill_1:
                        if c >= limit_skill_1:
                            return False
                # en este caso nos fijamos en los Tasks del Skill 1 y tambien del Skill 2
                else:
                    limit_skill_1 = np.floor(es_skill_1.performance)
                    limit_skill_2 = np.floor(es_skill_2.performance)
                    for i in range(0, len(commitments_skill_1)):
                        proportion = commitments_skill_1[i]/limit_skill_1 + commitments_skill_2[i]/limit_skill_2 + 1/limit
                        if proportion > 1:
                            return False
            return True

#checked
def hasNOnes(chosen, n):
    ones = 0
    for c in chosen:
        if c == 1:
            ones = ones + 1
    if ones == n:
        return True
    return False

#checked
def stringToList(as_string, chosen):
    for i in range(1, len(as_string) - 1):
        if as_string[-i] == '0':
            chosen[-i] = 0
        if as_string[-i] == '1':
            chosen[-i] = 1
    return chosen

#checked
def successor(chosen, num_workers):
    as_string = ''
    last = [] # definimos la última combinación posible de elegidos para saber cuando parar
    for _ in range(0, num_workers): last.append(1)
    for _ in range(0, len(chosen) - num_workers): last.append(0)
    
    if chosen == last:
        return chosen
    
    for c in chosen:
        if c == 0: as_string = as_string + '0'
        if c == 1: as_string = as_string + '1'
    
    as_string = str(bin(int(as_string,2) + int('1',2)))
    chosen = stringToList(as_string, chosen)
    
    while not hasNOnes(chosen, num_workers) and chosen != last:
        as_string = str(bin(int(as_string,2) + int('1',2)))
        chosen = stringToList(as_string, chosen)
    return chosen

#checked
def getChosenIds(possibilities, chosen):
    ids = []
    for i in range(0, len(possibilities)):
        if chosen[i] == 1:
            ids.append(possibilities[i])
    return ids
    
#checked (kind of)

def findEmployees(db, id_skill, contract_number, num_workers, initial_date, end_date, senior):
    with db_session:
        ids_employees = employeesBySkill(db, id_skill, senior) # elegimos a los empleados con el skill necesario
        cluster1 = employeesByStatus(db, contract_number, ids_employees, True, True) # empleados fijos en este proyecto
        cluster2 = employeesByStatus(db, contract_number, ids_employees, True, False) # empleados vetados en este proyecto
        cluster3 = employeesByStatus(db, contract_number, ids_employees, False, True) # empleados fijos en otros proyectos
        cluster4 = employeesByStatus(db, contract_number, ids_employees, False, False) # empleados vetados en otros proyectos
        
        ids_employees = list(id for id in ids_employees if id not in cluster1 and id not in cluster2) # sacamos a todos los empleados vetados en este proyecto
        ids_found = cluster1  # incluimos sí o sí a los empleados que están fijos en el proyecto
        
        num_workers = num_workers - len(ids_found)
        if num_workers <= 0: #revisamos si con los empleados fijos basta y si ellos están disponibles en las fechas necesarias
            if employeesAvailable(db, ids_found, initial_date, end_date, id_skill):
                return ids_found
            else:
                return []
        
        priority1 = list(id for id in ids_employees if id not in cluster3 and id in cluster4) # priorizamos empleados vetados en otros proyectos y NO fijos en otros proyectos
        priority2 = list(id for id in ids_employees if id not in cluster3 and id not in cluster4) # después, empleados ni fijos ni vetados en otros proyectos
        priority3 = list(id for id in ids_employees if id in cluster3 and id in cluster4) # después, empleados fijos en unos proyectos y vetados en otros
        priority4 = list(id for id in ids_employees if id in cluster3 and id not in cluster4) # por último, empleados fijos en otros proyectos y no vetados en ninguno
        
        possibilities = [] # ahora listamos todas las posibilidades, en orden de menos prioritario a más prioritario
        for id in priority4: possibilities.append(id)
        for id in priority3: possibilities.append(id)
        for id in priority2: possibilities.append(id)
        for id in priority1: possibilities.append(id)
        
        if num_workers > len(possibilities): # si no hay suficientes trabajadores no vetados para el trabajo, se devuelve el código False
            return False
        
        chosen = [] # elegimos (marcamos con 1) por defecto a los más prioritarios, si no tienen disponibilidad, vamos considerando a los menos prioritarios
        for _ in range(0, len(possibilities) - num_workers): chosen.append(0)
        for _ in range(0, num_workers): chosen.append(1)
        
        last = [] # definimos la última combinación posible de elegidos para saber cuando parar
        for _ in range(0, num_workers): last.append(1)
        for _ in range(0, len(chosen) - num_workers): last.append(0)
        
        while(not employeesAvailable(db, ids_found + getChosenIds(possibilities, chosen), initial_date, end_date, id_skill)):
            if chosen == last:
                return []
            chosen = successor(chosen, num_workers)
        
        # en el caso de los instaladores, junto con los seniors hay que mandar a los juniors
        if id_skill == 4:
            if senior:
                ids_juniors = findEmployees(db, id_skill, contract_number, num_workers, initial_date, end_date, False)
                if ids_juniors == False:
                    return False
                elif len(ids_juniors) > 0:
                    return ids_found + getChosenIds(possibilities, chosen) + ids_juniors
                else:
                    return []
            else:
                return ids_found + getChosenIds(possibilities, chosen)
        else:
            return ids_found + getChosenIds(possibilities, chosen)
        
#checked (kind of)
def findDatesEmployees(db, id_skill, contract_number, num_workers, current_date):
    days_from_current = 1
    task_days = getDays(db, id_skill, contract_number, num_workers)
    while(True):
        initial_date = sumDays(current_date, days_from_current)
        end_date = sumDays(current_date, days_from_current + task_days - 1)
        
        condition1 = (id_skill == 1 or id_skill == 4) and clientAvailable(db, contract_number, initial_date, end_date)
        condition2 = (id_skill == 2 or id_skill == 3)
        if condition1 or condition2:
            ids_found = findEmployees(db, id_skill, contract_number, num_workers, initial_date, end_date, True)
            if ids_found == False:
                return None, None, None
            elif len(ids_found) > 0:
                return initial_date, end_date, ids_found
            else:
                days_from_current = days_from_current + 1
        else:
            days_from_current = days_from_current + 1
        # else:
        #     task_days = GetDays(db, id_skill, contract_number,
        # num_workers+1) #Esta opción debe estudiarse en la heurística que
        # se encuentra en el método "DoPlanning".

# Acá termina: varias funciones relacionadas con buscar fechas donde haya suficientes empleados para una tarea: #
#################################################################################################################



#####################################################################
# Acá empieza: funciones para asignar/desasignar tareas a empleados #

def assignTask(db, ids_employees, id_task, initial_date = None, end_date = None):
    with db_session:
        if (type(ids_employees) != int):
            for id_employee in ids_employees:
                et = db.Employees_Tasks(employee = id_employee, task = id_task)
                et.planned_initial_date = initial_date
                et.planned_end_date = end_date
        else:
            et = db.Employees_Tasks(employee=ids_employees, task=id_task)
            et.planned_initial_date = initial_date
            et.planned_end_date = end_date

    
def unassignTask(db, id_employee, id_task):
    with db_session:
        db.Employees_Tasks[(id_employee, id_task)].delete()
    
# Acá termina: funciones para asignar/desasignar tareas a empleados    #
#####################################################################

def eraseTasks(db):
    with db_session:
        employees_tasks_to_delete = select(employee_task for employee_task in db.Employees_Tasks)
        for employee_task in employees_tasks_to_delete:
            task = employee_task.task
            #Este 'if', para verificar si el proyecto está fijo, está fuera del 'select' porque
            # pony parece no aceptar esa expresión como condición adicional.
            if (task.effective_initial_date == None and not task.project.fixed_planning):
                employee_task.delete()

def cleanTasks(db):
    with db_session:
        employees_tasks_to_delete = select(employee_task for employee_task in db.Employees_Tasks)
        for employee_task in employees_tasks_to_delete:
            task= employee_task.task
            if (task.effective_initial_date == None and  not task.project.fixed_planning):
                employee_task.delete()

###################################################################################
        #Cambiar en las tablas id_skill y id_project por skill y project !!!
                # !!!!
                ###############################
        # task.project.contract_number
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
        
def changePriority(db, contract_number, new_priority):
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
            
############
#Este evento debe gatillar una replanificación
    # doPlanning(db)
###########
#Funcion para cambiar la prioridad de manera manual. Luego de cambiarla, la prioridad se marca como fijada por el usuario.
#check


##########################
# Hacer la planificación #
##########################
def addDelayed(db, Delayed, contract_number, task, num_workers, initial, ending, deadline):
    Delayed =  Delayed.append({'contract number': contract_number, 'task': task, 'num workers': num_workers, 'initial date': initial, 'ending date': ending, 'deadline': deadline}, ignore_index = True)
    return Delayed

def checkVeto(db, contract_number, skill_id):
    Veto = True
    Veto1 = True
    with db_session:
        project = db.Projects.get(contract_number = contract_number)
        employees = select(es.employee for es in db.Employees_Skills if es.skill.id == skill_id)
        if skill_id == 1:
            for e in employees:
                er = db.Employees_Restrictions.get(employee = e,project =project)
                if er != None:
                    if er.fixed == True :
                        Veto = False
                        break
                else:
                    Veto = False
                    break

        elif skill_id == 4:
            for e in employees:
                er = db.Employees_Restrictions.get(employee = e,project =project)
                if er != None:
                    if er.fixed == True and e.senior == True:
                        Veto = False
                        break
                elif e.senior == True:
                    Veto = False
                    break
            for e in employees:
                er = db.Employees_Restrictions.get(employee = e,project =project)
                if er != None:
                    if er.fixed == True and e.senior == False:
                        Veto1 = False
                        break
                elif e.senior == False:
                    Veto1 = False
                    break
    if  not Veto and not Veto1 and skill_id ==4:
        return Veto
    elif skill_id ==4:
        return True
    else:
        return Veto
    

def doPlanning(db):
    import Projects.features as Pf
    import Stock.features as Sf
    Delayed = pd.DataFrame(np.nan, index=[], columns = ['contract number', 
'task', 'num workers', 'initial date', 'ending date', 'deadline'])#Esto debería
    # estar encapsulado en otro método.
    cleanTasks(db) #Aquí se borran todas las tasks de planificaciones anteriores (las 'borrables')
    with db_session:
        for i in range(1,5):
            if i == 4:
                employees1 = select(es.employee for es in db.Employees_Skills if es.skill.id == i and es.employee.senior == True)
                if len(employees1) < 1:
                    return('\n No se puede hacer la planificación porque no hay instaladores senior \n')
                employees2 = select(es.employee for es in db.Employees_Skills if es.skill.id == i and es.employee.senior == False)
                if len(employees2) < 1:
                    return('\n No se puede hacer la planificación porque no hay instaladores junior \n')
            else:
                employees = select(es.employee for es in db.Employees_Skills if es.skill.id == i)
                if len(employees) < 1:
                    return('\n No se puede hacer la planificación porque hay tareas que nadie sabe hacer \n')
            
        projects = select(p for p in db.Projects).order_by(lambda p : p.priority)
        # projects.show()
        for p in projects:
            last_release_date = date.today()
            if not p.fixed_planning:
                skills = select(s for s in db.Skills).order_by(lambda s : s.id)
                num_workers = 1
                for s in skills:
                    if s.id < 4:
                        # obtiene el id del skill correspondiente a esa tarea y revisa que no corresponda a una 'Instalación'.
                        task = db.Tasks.get(skill = s, project = p, failed = None)
                        employees_tasks = select(et for et in db.Employees_Tasks if et.task == task)

                        if task == None or (task != None and task.effective_initial_date == None):
                            # arriba revisamos que la effective_initial_date sea None, si no, no la cambiamos
                            initial, ending, emps = findDatesEmployees(db, s.id, p.contract_number, num_workers, last_release_date)
                            if task == None:
                                Pf.createTask(db, s.id, p.contract_number, initial, ending)
                                task = db.Tasks.get(skill = s, project = p, failed = None)
                            
                            #el siguiente IF no debiera ir, por eso la comenté, solo se debe agregar a Delayed después del skill 4, si no,
                            #se agrega dos veces
                            #if ending > p.deadline :
#                                print("Se pasó la tarea  " +str(s) +" del proyecto "+str(p.contract_number))
                                #aquí se podría o no avisar que el proyecto estaría fuera de plazo
                            #    Delayed = addDelayed(db, Delayed, p.contract_number, s, num_workers, initial, ending, p.deadline)
                            
                            assignTask(db, emps, task, initial, ending)
                            commit()
                            # si la tarea es de fabricación, entonces hay que considerar el tiempo en que llegan los cristales para el last_release_date:
                            if s.id == 3:
                                crystal_release_date = sumDays(last_release_date, p.crystal_leadtime)
                                last_release_date = max(ending, crystal_release_date)
                            else:
                                last_release_date = ending
                        else:     # asume que el et.planned_end_date está bien actualizado, si no, habría que calcular el last_release_days como
                                # task.effective_initial_date + los días que se demora el trabajo según la cantidad de trabajadores
                            # si la tarea es de fabricación, entonces hay que considerar el tiempo en que llegan los cristales para el last_release_date:
                            if s.id == 3:
                                crystal_release_date = sumDays(last_release_date, p.crystal_leadtime)
                                for et in employees_tasks:
                                    last_release_date = max(et.planned_end_date, crystal_release_date)
                            else:
                                for et in employees_tasks:
                                    last_release_date = et.planned_end_date
                                # initial, ending, emps = findDatesEmployees(db, s.id, p.contract_number, num_workers, last_release_date)        
                                # last_release_date = et.task.effective_initial_date + timedelta(3)

                        
                    elif s.id == 4:
                        task = db.Tasks.get(skill = s, project = p, failed = None)
                        employees_tasks = select(et for et in db.Employees_Tasks if et.task == task)
                        ending = [None, None, None, None]
                        
                        if len(employees_tasks) == 0 and (task == None or (task != None and task.effective_initial_date == None)):
                            initial, ending[num_workers-1], emps = findDatesEmployees(db, s.id, p.contract_number, num_workers, last_release_date)
                            while(ending[num_workers-1] > p.deadline and num_workers < 4):
                                num_workers = num_workers + 1
                                initial, ending[num_workers-1], emps = findDatesEmployees(db, s.id, p.contract_number, num_workers, last_release_date)
                                if ending[num_workers-1] == None:
                                    num_workers = num_workers - 1
                                    break
    
                            if(ending[num_workers-1] > p.deadline):
                                #print("Se pasó el proyecto " +str(p.contract_number) +" con "+str(num_workers)+" trabajadores y fecha de término "+str(ending[num_workers-1]))
                                num_workers = 1 # nos quedamos con la menor fecha
                                for n in range(2, 5):#ahora si revisa 2,3 y 4
                                    if ending[n-1] != None and ending[n-1] < ending[num_workers-1]:
                                        num_workers = n
                                
                                initial, ending[num_workers-1], emps = findDatesEmployees(db, s.id, p.contract_number, num_workers, last_release_date)
                                #aquí ya no hay nada que hacer y se le debería mostrar la tabla Delayed
                                Delayed = addDelayed(db, Delayed, p.contract_number, s, num_workers, initial, ending[num_workers-1], p.deadline)
                                if task == None:
                                    Pf.createTask(db, s.id, p.contract_number, initial, ending[num_workers-1])
                                    task = db.Tasks.get(skill = s, project = p)
                                assignTask(db, emps, task, initial, ending[num_workers-1])
                                commit()
                            else:
                                if task == None:
                                    Pf.createTask(db, s.id, p.contract_number, initial, ending[num_workers-1])
                                    task = db.Tasks.get(skill = s, project = p)
                                assignTask(db, emps, task, initial, ending[num_workers-1])
                                commit()
            for e in p.engagements:
                Sf.updateEngagements(db, e.sku.id)
        createReport(db, Delayed)
        
        

                # if(s.id < 4 and t.effective_initial_date == None):#obtiene el id del
                #     # skill correspondiente a esa
                #     # tarea y revisa que no corresponda a una 'Instalación'.
                #     #  También revisa que la realización de la tarea aún no
                #     # haya comenzado (que sea 'planificable').
                #     (initial, ending, emps) = FindDatesEmployees(db, t.skill.id, p.contract_number,1, d_t)
                #     days=ending.day-initial.day
                #     AssignTask(db,emps,t.id,initial,ending)
                #     d_t=d_t+timedelta(days)
                #
                #     if(d_t > p.deadline):
                #         AvailabilityUpdate(db, p.contract_number)
                #         #Delayed = addDelayed(db, Delayed, p.contract_number, t.skill, initial, ending, p.deadline)
                #         #print(Delayed)
                # if(t.skill.id == 4 and t.effective_initial_date == None):
                #     num_workers=1
                #     while (num_workers<=4):
                #         (initial,ending,emps)=FindDatesEmployees(db, t.skill.id, p.contract_number, num_workers, d_t)
                #         days=ending.day-initial.day
                #         AssignTask(db, emps, t.id, initial, ending)
                #         if(num_workers==4 and d_t+timedelta(days)>p.deadline):
                #             AvailabilityUpdate(db)
                #             #ShowDelayed(db)
                #             break
                #         if(num_workers < 4 and d_t+timedelta(days)>p.deadline):
                #             num_workers=num_workers+1
                #
##########
#eventos que gatillan una replanificación deben ser especificados
##########
        
        
        
        
###########################################################
##Métodos relacionados a los informes post-planificación #
########################################################### 

# def createReport(db, Delayed):
    # with db_session:
        # wb = Workbook()
        # createDelayedReport(wb, Delayed)
        # createPlanningReport(db, wb)
        # wb.save('ReportePlanificacion.xlsx')
        # print('\n El reporte de la última planificación se encuentra en el archivo ReportePlanificacion.xlsx.')


        
# def createDelayedReport(wb, Delayed):
    # ws = wb.create_sheet("Reporte atrasos") #aquí se pueden agregar otras restricciones no cumplidas
    
    ##cambiar ancho de columnas
    # widths = {"A": 20, "B": 30, "C": 30}
    # columns = ["A", "B", "C"]
    # for c in columns:
        # ws.column_dimensions[c].width = widths[c]
    
    ##escribir texto en algunas celdas, en negrita
    # rows = [1, 3, 3, 3]
    # columns = [1, 1, 2, 3]
    # texts = ["Reporte de atrasos", "Número de contrato", "Fecha de entrega comprometida", "Fecha de entrega planificada"]
    # for i in range(0, len(rows)):
        # cell = ws.cell(row = rows[i], column = columns[i], value = texts[i])
        # cell.font = Font(bold = True)
    
    ##llenar con los datos de Delayed
    # next_row = 4
    # for index, row in Delayed.iterrows():
        # ws.cell(row = next_row, column = 1, value = row['contract number'])
        # ws.cell(row = next_row, column = 2, value = row['deadline'])
        # ws.cell(row = next_row, column = 3, value = row['ending date'])
        # next_row = next_row + 1

        

# def createPlanningReport(db, wb):
    # ws = wb.create_sheet("Reporte planificación") #aquí se pueden agregar otras restricciones no cumplidas
    
    ##cambiar ancho de columnas
    # widths = {"A": 20, "B": 30, "C": 30, "D": 30, "E": 30, "F": 30, "G": 30, "H": 30, "I": 30, "J": 30, "K": 30, "L": 30, "M": 30}
    # columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    # for c in columns:
        # ws.column_dimensions[c].width = widths[c]
    
    ##escribir texto en algunas celdas, en negrita
    # rows = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    # columns = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    # texts = ["Reporte de planificación", "Número de contrato", 
                # "Fecha inicio rectificación", "Fecha término rectificación", "Empleado encargado rectificación", 
                # "Fecha inicio diseño", "Fecha término diseño", "Empleado encargado diseño", 
                # "Fecha inicio fabricación", "Fecha término fabricación", "Empleado encargado fabricación", 
                # "Fecha inicio instalación", "Fecha término instalación", "Empleados encargados instalación"]
    # for i in range(0, len(rows)):
        # cell = ws.cell(row = rows[i], column = columns[i], value = texts[i])
        # cell.font = Font(bold = True)
    
    ##llenar con los datos de Delayed
    # next_row = 4
    # with db_session:
        # projects = select(p for p in db.Projects).order_by(lambda p : p.contract_number)
        # for p in projects:
            ##primero seleccionamos el Task asociado a este Project y a cada Skill, sabemos que es solo una con failed != True, así que tomamos first():
            # task_rect = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[1] and (t.failed == None or t.failed == False)).first()
            # task_des = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[2] and (t.failed == None or t.failed == False)).first()
            # task_fab = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[3] and (t.failed == None or t.failed == False)).first()
            # task_inst = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[4] and (t.failed == None or t.failed == False)).first()

            ##sabemos que para las Skills 1,2,3 solamente puede haber un empleado encargado, así que tomamos el primero. Para la Skill 4 es distinto:
            # employees_tasks_rect = select(et for et in db.Employees_Tasks if et.task == task_rect).first()
            # employees_tasks_des = select(et for et in db.Employees_Tasks if et.task == task_des).first()
            # employees_tasks_fab = select(et for et in db.Employees_Tasks if et.task == task_fab).first()
            # employees_tasks_inst = select(et for et in db.Employees_Tasks if et.task == task_inst)
            
            ##para el Skill 4, pueden ser varios empleados:
            # instalation_planned_initial_date = employees_tasks_inst.first().planned_initial_date
            # instalation_planned_end_date = employees_tasks_inst.first().planned_end_date
            # instalation_employees = ""
            # for et in employees_tasks_inst:
                # instalation_employees = instalation_employees + str(et.employee) + " ;"
            
            ##finalmente, escribimos en el Excel el resumen de la planificación:
            # values = [p.contract_number, 
                        # employees_tasks_rect.planned_initial_date, employees_tasks_rect.planned_end_date, employees_tasks_rect.employee.id, 
                        # employees_tasks_des.planned_initial_date, employees_tasks_des.planned_end_date, employees_tasks_des.employee.id, 
                        # employees_tasks_fab.planned_initial_date, employees_tasks_fab.planned_end_date, employees_tasks_fab.employee.id, 
                        # instalation_planned_initial_date, instalation_planned_end_date, instalation_employees[0:-2]]
            # for c in range(1, len(columns)):
                # ws.cell(row = next_row, column = columns[c], value = values[c-1])
            # next_row = next_row + 1

            
            
            

            

##############################################################################
##Métodos relacionados con cambiar empleados manualmente post-planificación #
##############################################################################

##método que revisa si las asignaciones de empleados que hizo el usuario entregan una planificación factible
# def planningChangesPlausible(db):
    # wb = load_workbook('ReportePlanificacion.xlsx')
    # ws = wb["Reporte planificación"]
    # if not employeesSkillsPlausible(db, ws):
        # return False, "Uno de los empleados fue asignado a una tarea para la cual no está capacitado."
    # if not employeesActivitiesPlausible(db, ws):
        # return False, "Uno de los empleados fue asignado a una tarea en fecha que coincide con sus vacaciones o alguna licencia."
    # if not employeesTasksPlausible(ws):
        # return False, "Uno de los empleados fue asignado a más de una tarea en la misma fecha."
    # if not employeesRestrictionsPlausible(db, ws)[0]:
        # return False, employeesRestrictionsPlausible(db, ws)[1]
    # return True, "Los cambios hechos a la planificación son válidos, por lo tanto, serán aplicados."

# def employeesSkillsPlausible(db, ws):
    # with db_session:
        # for next_row in range(4, ws.max_row):
            ##revisamos primero el caso de las Skills 1, 2, 3 que es el más sencillo
            # rectifier = ws.cell(row = next_row, column = 4).value
            # designer = ws.cell(row = next_row, column = 7).value
            # fabricator = ws.cell(row = next_row, column = 10).value
            # if db.Employees_Skills[db.Employees[rectifier], db.Skills[1]].performance == 0 or \
                # db.Employees_Skills[db.Employees[designer], db.Skills[2]].performance == 0 or \
                # db.Employees_Skills[db.Employees[fabricator], db.Skills[3]].performance == 0:
                # return False
            
            ##ahora revisamos para el Skill 4
            # installers = str(ws.cell(row = next_row, column = 13).value).split(';')
            # print(installers)
            # for i in installers:
                # if db.Employees_Skills[db.Employees[i], db.Skills[4]].performance == 0:
                    # return False
        # return True
        
# def employeesActivitiesPlausible(db, ws):
    ##with db_session:
        ##def employeesAvailable(db, ids_employees, initial_date, end_date):
    ##comentado momentaneamente
    # with db_session:
        # emp_acts = select(ea for ea in db.Employees_Activities if ea.employee.id in ids_employees)
        # emp_tasks = select(et for et in db.Employees_Tasks if et.employee.id in ids_employees)

        # for ea in emp_acts:
            # if not datesOverlap(initial_date, end_date, ea.initial_date, ea.end_date):
                # return False
        # for et in emp_tasks:
            # if not datesOverlap(initial_date, end_date, et.planned_initial_date, et.planned_end_date):
                # return False
        # return True        
    # return True
    
# def employeesTasksPlausible(ws):
    # return True
    
# def employeesRestrictionsPlausible(db, ws):
    # return True


    
#método auxiliar para ver si un empleado está disponible según sus Activities XOR Tasks (activities = True es Activities, si no, Tasks)
# def employeesAvailable(db, ids_employees, initial_date, end_date, activities):
#     with db_session:
#         employee_acts = select(ea for ea in db.Employees_Activities if ea.employee.id in ids_employees)
#         emp_tasks = select(et for et in db.Employees_Tasks if et.employee.id in ids_employees)
#
#         for ea in employee_acts:
#             if not datesOverlap(initial_date, end_date, ea.initial_date, ea.end_date):
#                 return False
#         for et in emp_tasks:
#             if not datesOverlap(initial_date, end_date, et.planned_initial_date, et.planned_end_date):
#                 return False
#         return True

