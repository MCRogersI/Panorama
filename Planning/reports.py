from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font

##########################################################
# Métodos relacionados a los informes post-planificación #
##########################################################


def createReport(db, Delayed):
    with db_session:
        wb = Workbook()
        createDelayedReport(wb, Delayed)
        createPlanningReport(db, wb)
        wb.save('ReportePlanificacion.xlsx')
        
        #entramos en el siguiente ciclo para ver si el usuario acepta la planificación o quiere cambiar datos de los empleados
        while(True):
            print('\n El reporte de la última planificación se encuentra en el archivo ReportePlanificacion.xlsx.')
            opt = input(" Marque una de las siguientes opciones:\n - 1: si acepta la planificación propuesta. \
                                                                  \n - 2: si desea cambiar la asignación de empleados. \
                                                                  \n Ingrese la alternativa elegida: ")
            if opt == '1':
                break
            elif opt == '2':
                input(" Realice los cambios en el archivo ReportePlanificacion.xlsx, y presione cualquier tecla al terminar.")
                changes_plausible = planningChangesPlausible(db)
                if not changes_plausible[0]:
                    print(changes_plausible[1] + " Los cambios a la planificación no serán aplicados.")
                else:
                    implementChanges(db)


def createDelayedReport(wb, Delayed):
    ws = wb.create_sheet(
        "Reporte atrasos")  # aquí se pueden agregar otras restricciones no cumplidas

    # cambiar ancho de columnas
    widths = {"A": 20, "B": 30, "C": 30}
    columns = ["A", "B", "C"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]

    # escribir texto en algunas celdas, en negrita
    rows = [1, 3, 3, 3]
    columns = [1, 1, 2, 3]
    texts = ["Reporte de atrasos", "Número de contrato", "Fecha de entrega comprometida",
             "Fecha de entrega planificada"]
    for i in range(0, len(rows)):
        cell = ws.cell(row=rows[i], column=columns[i], value=texts[i])
        cell.font = Font(bold=True)

    # llenar con los datos de Delayed
    next_row = 4
    for index, row in Delayed.iterrows():
        ws.cell(row=next_row, column=1, value=row['contract number'])
        ws.cell(row=next_row, column=2, value=row['deadline'])
        ws.cell(row=next_row, column=3, value=row['ending date'])
        next_row = next_row + 1


def createPlanningReport(db, wb):
    ws = wb.create_sheet(
        "Reporte planificación")  # aquí se pueden agregar otras restricciones no cumplidas

    # cambiar ancho de columnas
    widths = {"A": 20, "B": 30, "C": 30, "D": 30, "E": 30, "F": 30, "G": 30, "H": 30, "I": 30,
              "J": 30, "K": 30, "L": 30, "M": 30}
    columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]

    # escribir texto en algunas celdas, en negrita
    rows = [1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    columns = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    texts = ["Reporte de planificación", "Número de contrato",
             "Fecha inicio rectificación", "Fecha término rectificación",
             "Empleado encargado rectificación",
             "Fecha inicio diseño", "Fecha término diseño", "Empleado encargado diseño",
             "Fecha inicio fabricación", "Fecha término fabricación",
             "Empleado encargado fabricación",
             "Fecha inicio instalación", "Fecha término instalación",
             "Empleados encargados instalación"]
    for i in range(0, len(rows)):
        cell = ws.cell(row=rows[i], column=columns[i], value=texts[i])
        cell.font = Font(bold=True)

    # llenar con los datos de Delayed
    next_row = 4
    with db_session:
        projects = select(p for p in db.Projects).order_by(lambda p: p.contract_number)
        for p in projects:
            # primero seleccionamos el Task asociado a este Project y a cada Skill, sabemos que es solo una con failed != True, así que tomamos first():
            task_rect = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[1] and (t.failed == None or t.failed == False)).first()
            task_des = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[2] and (t.failed == None or t.failed == False)).first()
            task_fab = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[3] and (t.failed == None or t.failed == False)).first()
            task_inst = select(t for t in db.Tasks if t.project == p and t.skill == db.Skills[4] and (t.failed == None or t.failed == False)).first()

            # sabemos que para las Skills 1,2,3 solamente puede haber un empleado encargado, así que tomamos el primero. Para la Skill 4 es distinto:
            employees_tasks_rect = select(et for et in db.Employees_Tasks if et.task == task_rect).first()
            employees_tasks_des = select(et for et in db.Employees_Tasks if et.task == task_des).first()
            employees_tasks_fab = select(et for et in db.Employees_Tasks if et.task == task_fab).first()
            employees_tasks_inst = select(et for et in db.Employees_Tasks if et.task == task_inst)

            # para el Skill 4, pueden ser varios empleados:
            instalation_planned_initial_date = employees_tasks_inst.first().planned_initial_date
            instalation_planned_end_date = employees_tasks_inst.first().planned_end_date
            instalation_employees = ""
            for et in employees_tasks_inst:
                instalation_employees = instalation_employees + str(et.employee) + " ;"

            # finalmente, escribimos en el Excel el resumen de la planificación:
            values = [p.contract_number,
                      employees_tasks_rect.planned_initial_date, employees_tasks_rect.planned_end_date, employees_tasks_rect.employee.id,
                      employees_tasks_des.planned_initial_date, employees_tasks_des.planned_end_date, employees_tasks_des.employee.id,
                      employees_tasks_fab.planned_initial_date, employees_tasks_fab.planned_end_date, employees_tasks_fab.employee.id,
                      instalation_planned_initial_date, instalation_planned_end_date, instalation_employees[0:-2]]
            for c in range(1, len(columns)):
                ws.cell(row=next_row, column=columns[c], value=values[c - 1])
            next_row = next_row + 1



#############################################################################
# Métodos relacionados con cambiar empleados manualmente post-planificación #
#############################################################################

#método que revisa si las asignaciones de empleados que hizo el usuario entregan una planificación factible
def planningChangesPlausible(db):
    #primero cargamos la hoja de planificación y calculamos cuál es la máxima fila
    wb = load_workbook('ReportePlanificacion.xlsx')
    ws = wb["Reporte planificación"]
    max_row = 3
    while(True):
        if ws.cell(row = max_row + 1, column = 1).value == None:
            break
        max_row = max_row + 1
    #ahora revisamos que la planificación sea factible en distintos sentidos
    if not employeesSkillsPlausible(db, ws, max_row):
        return False, " Uno de los empleados fue asignado a una tarea para la cual no está capacitado."
    if not employeesActivitiesPlausible(db, ws, max_row):
        return False, " Uno de los empleados fue asignado a una tarea en fecha que coincide con sus vacaciones o alguna licencia."
    if not employeesTasksPlausible(db, ws, max_row):
        return False, " Uno de los empleados fue asignado a más de una tarea en la misma fecha."
    if not employeesRestrictionsPlausible(db, ws, max_row):
        return False, str(employeesRestrictionsPlausible(db, ws, max_row))
    return True, " Los cambios hechos a la planificación son válidos, por lo tanto, serán aplicados."

#revisa factibilidad en cuanto a que a un empleado no se le asigne una tarea que requiera una Skill que no maneje
def employeesSkillsPlausible(db, ws, max_row):
    with db_session:
        for next_row in range(4, max_row + 1):
            #revisamos primero el caso de las Skills 1, 2, 3 que es el más sencillo
            rectifier = ws.cell(row = next_row, column = 4).value
            designer = ws.cell(row = next_row, column = 7).value
            fabricator = ws.cell(row = next_row, column = 10).value
            
            rectifier_skill = db.Employees_Skills.get(employee = db.Employees[rectifier], skill = db.Skills[1])
            designer_skill = db.Employees_Skills.get(employee = db.Employees[designer], skill = db.Skills[2])
            fabricator_skill = db.Employees_Skills.get(employee = db.Employees[fabricator], skill = db.Skills[3])
            if rectifier_skill == None or rectifier_skill.performance == 0 or \
                designer_skill == None or designer_skill.performance == 0 or \
                fabricator_skill == None or fabricator_skill.performance == 0:
                return False
            
            #ahora revisamos para el Skill 4
            installers = str(ws.cell(row = next_row, column = 13).value).split(';')
            for i in installers:
                installer_skill = db.Employees_Skills.get(employee = db.Employees[i], skill = db.Skills[4])
                if installer_skill == None or installer_skill.performance == 0:
                    return False
        return True
        
#revisa factibilidad en cuanto a que una tarea no tope con actividades (licencia/vacaciones)
def employeesActivitiesPlausible(db, ws, max_row):
    with db_session:
        for next_row in range(4, max_row + 1):
            rectifier = ws.cell(row = next_row, column = 4).value
            designer = ws.cell(row = next_row, column = 7).value
            fabricator = ws.cell(row = next_row, column = 10).value
            installers = str(ws.cell(row = next_row, column = 13).value).split(';')
            employees = [[rectifier], [designer], [fabricator], installers]
            for i in range(0, 4):
                initial_date = ws.cell(row = next_row, column = 3*i+2).value.date()
                end_date = ws.cell(row = next_row, column = 3*i+3).value.date()
                if not employeesAvailableActivities(db, employees[i], initial_date, end_date, True):
                    return False
    return True

#revisa factibilidad en cuanto a que dos tareas del mismo empleado no se topen 
def employeesTasksPlausible(db, ws, max_row):
    from Planning.features import datesOverlap
    with db_session:
        #recorremos para cada empleado el reporte de planificación, guardando todas las veces en que aparece asignado para una tarea
        employees = select(e for e in db.Employees)
        for e in employees:
            id = e.id
            initial_date_rows = []
            initial_date_columns = []
            for next_row in range(4, max_row + 1):
                if id == ws.cell(row = next_row, column = 4).value:
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(2)
                if id == ws.cell(row = next_row, column = 7).value:
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(5)
                if id == ws.cell(row = next_row, column = 10).value:
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(8)
                if str(id) in str(ws.cell(row = next_row, column = 13).value).split(';'):
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(11)
            #teniendo esa información guardada, ahora revisamos si calzan entre ellas
            dates = len(initial_date_columns)
            for i in range(0, dates):
                for j in (k for k in range(0, dates) if k != i):
                    initial_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i]).value.date()
                    end_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i] + 1).value.date()
                    initial_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j]).value.date()
                    end_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j] + 1).value.date()
                    if datesOverlap(initial_date_1, end_date_1, initial_date_2, end_date_2):
                        return False
    return True

#revisa factibilidad en cuanto a empleados fijos/baneados de proyectos
def employeesRestrictionsPlausible(db, ws, max_row):
    return True
    
#método auxiliar para ver si un empleado está disponible según sus Activities
def employeesAvailableActivities(db, ids_employees, initial_date, end_date, activities):
    from Planning.features import datesOverlap
    with db_session:
        emp_acts = select(ea for ea in db.Employees_Activities if ea.employee.id in ids_employees)
        for ea in emp_acts:
            if datesOverlap(initial_date, end_date, ea.initial_date, ea.end_date):
                return False
        return True

#método que aplica los cambios si es que son factibles
def implementChanges(db):
    from Planning.features import assignTask
    with db_session:
        #primero cargamos la hoja de planificación y calculamos cuál es la máxima fila
        wb = load_workbook('ReportePlanificacion.xlsx')
        ws = wb["Reporte planificación"]
        max_row = 3
        while(True):
            if ws.cell(row = max_row + 1, column = 1).value == None:
                break
            max_row = max_row + 1
        #implementamos primero el caso de las Skills 1, 2, 3 que es el más sencillo
        columns = [4, 7, 10]
        skills = [1, 2, 3]
        for next_row in range(4, max_row + 1):
            for i in range(0, len(columns)):
                #recuperamos el Task, sabiendo que solo puede haber uno para un par Project, Skill que no tenga failed = True, usamos el .first()
                contract_number = ws.cell(row = next_row, column = 1).value
                skill = skills[i]
                task = select(t for t in db.Tasks if t.project == db.Projects[contract_number] and t.skill == db.Skills[skill] and \
                                    (t.failed == None or t.failed == False)).first()
                #luego recuperamos el Employee_Task, para cambiar el empleado asociado
                c = columns[i]
                initial_date = ws.cell(row = next_row, column = c - 2).value.date()
                end_date = ws.cell(row = next_row, column = c - 1).value.date()
                new_employee = ws.cell(row = next_row, column = c).value
                employee_task = db.Employees_Tasks.get(task = task, planned_initial_date = initial_date, planned_end_date = end_date)
                if employee_task != None:
                    employee_task.delete()
                    #el commit() es clave, si no, el empleado no se considera borrado aún, y la línea de assignTask() tira un error
                    commit()
                    assignTask(db, [new_employee], task.id, initial_date, end_date)
                
            
            
            
###############
# Base report #
###############

def baseCreateReport():
    wb = Workbook()
    wb.save('ReportePlanificacionBásico.xlsx')
    ws = wb.create_sheet(
        "Reporte atrasos")
    widths = {"A": 20, "B": 30, "C": 30}
    columns = ["A", "B", "C"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]

    # escribir texto en algunas celdas, en negrita
    rows = [1, 3, 3, 3]
    columns = [1, 1, 2, 3]
    texts = ["Reporte de atrasos", "Número de contrato", "Fecha de entrega comprometida",
             "Fecha de entrega planificada"]
    for i in range(0, len(rows)):
        cell = ws.cell(row=rows[i], column=columns[i], value=texts[i])
        cell.font = Font(bold=True)

    # llenar con los datos

baseCreateReport()
