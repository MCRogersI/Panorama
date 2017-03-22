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
