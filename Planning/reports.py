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
        print(
            '\n El reporte de la última planificación se encuentra en el archivo ReportePlanificacion.xlsx.')


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
            task_rect = select(t for t in db.Tasks if
                               t.project == p and t.skill == db.Skills[1] and (
                               t.failed == None or t.failed == False)).first()
            task_des = select(t for t in db.Tasks if
                              t.project == p and t.skill == db.Skills[2] and (
                              t.failed == None or t.failed == False)).first()
            task_fab = select(t for t in db.Tasks if
                              t.project == p and t.skill == db.Skills[3] and (
                              t.failed == None or t.failed == False)).first()
            task_inst = select(t for t in db.Tasks if
                               t.project == p and t.skill == db.Skills[4] and (
                               t.failed == None or t.failed == False)).first()

            # sabemos que para las Skills 1,2,3 solamente puede haber un empleado encargado, así que tomamos el primero. Para la Skill 4 es distinto:
            employees_tasks_rect = select(
                et for et in db.Employees_Tasks if et.task == task_rect).first()
            employees_tasks_des = select(
                et for et in db.Employees_Tasks if et.task == task_des).first()
            employees_tasks_fab = select(
                et for et in db.Employees_Tasks if et.task == task_fab).first()
            employees_tasks_inst = select(et for et in db.Employees_Tasks if et.task == task_inst)

            # para el Skill 4, pueden ser varios empleados:
            instalation_planned_initial_date = employees_tasks_inst.first().planned_initial_date
            instalation_planned_end_date = employees_tasks_inst.first().planned_end_date
            instalation_employees = ""
            for et in employees_tasks_inst:
                instalation_employees = instalation_employees + str(et.employee) + " ;"

            # finalmente, escribimos en el Excel el resumen de la planificación:
            values = [p.contract_number,
                      employees_tasks_rect.planned_initial_date,
                      employees_tasks_rect.planned_end_date, employees_tasks_rect.employee.id,
                      employees_tasks_des.planned_initial_date,
                      employees_tasks_des.planned_end_date, employees_tasks_des.employee.id,
                      employees_tasks_fab.planned_initial_date,
                      employees_tasks_fab.planned_end_date, employees_tasks_fab.employee.id,
                      instalation_planned_initial_date, instalation_planned_end_date,
                      instalation_employees[0:-2]]
            for c in range(1, len(columns)):
                ws.cell(row=next_row, column=columns[c], value=values[c - 1])
            next_row = next_row + 1


			
			

#############################################################################
# Métodos relacionados con cambiar empleados manualmente post-planificación #
#############################################################################

#método que revisa si las asignaciones de empleados que hizo el usuario entregan una planificación factible
def planningChangesPlausible(db):
	wb = load_workbook('ReportePlanificacion.xlsx')
	ws = wb["Reporte planificación"]
	if not employeesSkillsPlausible(db, ws):
		return False, "Uno de los empleados fue asignado a una tarea para la cual no está capacitado."
	if not employeesActivitiesPlausible(db, ws):
		return False, "Uno de los empleados fue asignado a una tarea en fecha que coincide con sus vacaciones o alguna licencia."
	if not employeesTasksPlausible(db, ws):
		return False, "Uno de los empleados fue asignado a más de una tarea en la misma fecha."
	if not employeesRestrictionsPlausible(db, ws):
		return False, str(employeesRestrictionsPlausible(db, ws))
	return True, "Los cambios hechos a la planificación son válidos, por lo tanto, serán aplicados."

def employeesSkillsPlausible(db, ws):
	with db_session:
		for next_row in range(4, ws.max_row + 1):
			#revisamos primero el caso de las Skills 1, 2, 3 que es el más sencillo
			rectifier = ws.cell(row = next_row, column = 4).value
			designer = ws.cell(row = next_row, column = 7).value
			fabricator = ws.cell(row = next_row, column = 10).value
			if db.Employees_Skills[db.Employees[rectifier], db.Skills[1]].performance == 0 or \
				db.Employees_Skills[db.Employees[designer], db.Skills[2]].performance == 0 or \
				db.Employees_Skills[db.Employees[fabricator], db.Skills[3]].performance == 0:
				return False
			
			#ahora revisamos para el Skill 4
			installers = str(ws.cell(row = next_row, column = 13).value).split(';')
			print(installers)
			for i in installers:
				if db.Employees_Skills[db.Employees[i], db.Skills[4]].performance == 0:
					return False
		return True
		

def employeesActivitiesPlausible(db, ws):
	with db_session:
		for next_row in range(4, ws.max_row + 1):
			rectifier = ws.cell(row = next_row, column = 4).value
			designer = ws.cell(row = next_row, column = 7).value
			fabricator = ws.cell(row = next_row, column = 10).value
			installers = str(ws.cell(row = next_row, column = 13).value).split(';')
			employees = [[rectifier], [designer], [fabricator], installers]
			for i in range(0, 4):
				initial_date = ws.cell(row = next_row, column = 3*i+2).value.date()
				end_date = ws.cell(row = next_row, column = 3*i+3).value.date()
				if not employeesAvailableBool(db, employees[i], initial_date, end_date, True):
					return False
	return True

	
def employeesTasksPlausible(db, ws):
	with db_session:
		#recorremos para cada empleado el reporte de planificación, guardando todas las veces en que aparece asignado para una tarea
		employees = select(e for e in db.Employees)
		for e in employees:
			id = e.id
			initial_date_rows = []
			initial_date_columns = []
			for next_row in range(4, ws.max_row + 1):
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
					end_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i+1]).value.date()
					initial_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j]).value.date()
					end_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j+1]).value.date()
					if datesOverlap(initial_date_1, end_date_1, initial_date_2, end_date_2):
						return False
	return True
	
def employeesRestrictionsPlausible(db, ws):
	return True
	
#método auxiliar para ver si un empleado está disponible según sus Activities XOR Tasks (activities = True es Activities, si no, Tasks)
def employeesAvailableBool(db, ids_employees, initial_date, end_date, activities):
	with db_session:
		if activities:
			emp_acts = select(ea for ea in db.Employees_Activities if ea.employee.id in ids_employees)
			for ea in emp_acts:
				if datesOverlap(initial_date, end_date, ea.initial_date, ea.end_date):
					return False
		else:
			emp_tasks = select(et for et in db.Employees_Tasks if et.employee.id in ids_employees)
			for et in emp_tasks:
				if datesOverlap(initial_date, end_date, et.planned_initial_date, et.planned_end_date):
					return False
		return True

			
			
			
			
###############
# Base report #
###############

def createGlobalReport():
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

createGlobalReport()
