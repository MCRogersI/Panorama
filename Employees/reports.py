from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font,Alignment
import os

def createEmployeeReportV1(db,id_employee):
    ''' Este método crea un informe en Excel compacto con una proción de la información de la base de datos. '''
    wb = Workbook()
    by_default_sheet = wb.get_sheet_by_name('Sheet')
    by_default_sheet.title = 'Introducción del informe'
    wb.remove_sheet(by_default_sheet)
    ws = wb.create_sheet(
        "Informe trabajador",index=0)

    widths = {"A": 5, "B": 35, "C": 5,"D": 35, "E": 35, "F": 35,
              "G": 35, "H": 35, "I": 35,"J": 35, "K": 35, "L": 35,
              "M": 35, "N": 35}

    heights = {"A": 10, "B": 10, "C": 10, "D": 10, "E": 10, "F": 10,
              "G": 10, "H": 10, "I": 10, "J": 10, "K": 10, "L": 10,
              "M": 10, "N": 10}

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))


    columns = ["A", "B", "C","D","E","F","G","H","I"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]
        ws.column_dimensions[c].height = heights[c]


    num_columns, letter_columns = zip(*list(enumerate(columns)))
    num_columns = list(num_columns)
    num_columns = [x + 1 for x in num_columns] #Desplazamos los valores en 1 porque Excel está indexado desde el 1 y no desde el 0
    letter_columns = list(letter_columns)

    # escribir los títulos de las columnas, en negrita

    texts = ["","","","ID", "NOMBRE", "ZONA", "COMPETENCIA",
             "SENIOR","RENDIMIENTO"]

    for i in range(4,len(num_columns)+1):
        cell = ws.cell(row=3, column=i, value=texts[i-1])
        cell.font = Font(bold=True,)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')


    # A continuación llenamos con los datos


    with db_session:
        e = db.Employees.get(id=id_employee)
        r=4
        #Escribe el ID del empleado
        if e.id != None:
            cell = ws.cell(row=r, column=4, value=e.id)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        else:
            cell = ws.cell(row=r, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

        # Escribe el nombre del empleado
        if e.name != None:
            cell = ws.cell(row=r, column=5, value=e.name)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        else:
            cell = ws.cell(row=r, column=5, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

        # Escribe la zona geográfica del empleado
        if e.zone != None:
            cell = ws.cell(row=r, column=6, value=e.zone)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        else:
            cell = ws.cell(row=r, column=6, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

        # Escribe la competencia del empleado (por el momento se asume que solo es una)
        es = db.Employees_Skills.get(employee = e)
        if es.skill != None:
            skill_name = es.skill.name
            cell = ws.cell(row=r, column=7, value=skill_name)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        else:
            cell = ws.cell(row=r, column=7, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

        # Escribe si el empleado es senior o no (Sí o No)
        if e.senior != None:
            if es.senior:
                value = "Sí"
            else:
                value = "No"
            cell = ws.cell(row=r, column=8, value = value)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        else:
            cell = ws.cell(row=r, column=8, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

        if es.performance != None:
            cell = ws.cell(row=r, column=9, value = es.performance)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        else:
            cell = ws.cell(row=r, column=9, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

        #Imprimir el horario del trabajador
        cell = ws.cell(row=r+9, column=4, value="SEMANA del lunes")
        cell.font = Font(bold=True)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
        aux_c = 1
        for day in ["Lunes","Martes", "Miercoles","Jueves","Viernes"]:
            cell = ws.cell(row=r + 9, column=4 + aux_c, value="{0}".format(day))
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
            aux_c+=1
        span_of_weeks = 14
        dates = []
        today = date.today()
        initial_week_date = today + timedelta(days=-today.weekday())
        calendar_r = r + 10 #Esta variable para la fila podría definirse se otra forma
        for i in range (0,span_of_weeks):
            dates.append(initial_week_date+i*timedelta(days=7))
        for d in dates:
            cell = ws.cell(row=calendar_r, column=4, value=d)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
            calendar_r+=1


    module_path = os.path.dirname(__file__)
    panorama_folder_path = os.path.abspath(os.path.join(module_path, os.pardir))
    report_folder_path = os.path.join(panorama_folder_path,"Reportes")
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)
    report_file_name = "Versión 1 Reporte empleado {}.xlsx".format(id_employee)
    fn = os.path.join(report_folder_path,report_file_name)
    wb.save(fn)

# # from pony.orm import *
from database import db
createEmployeeReportV1(db,3)

def createEmployeeReportV2(db,id_employee):
    ''' Este método crea un informe en Excel compacto con una proción de la información de la base de datos. '''
    wb = Workbook()
    by_default_sheet = wb.get_sheet_by_name('Sheet')
    by_default_sheet.title = 'Introducción del informe'
    wb.remove_sheet(by_default_sheet)
    ws = wb.create_sheet(
        "Informe trabajador",index=0)

    widths = {"A": 20, "B": 20, "C": 20,"D": 20, "E": 20, "F": 20,
              "G": 20, "H": 20, "I": 20,"J": 20, "K": 20, "L": 20,
              "M": 20, "N": 20}

    heights = {"A": 10, "B": 10, "C": 10, "D": 10, "E": 10, "F": 10,
              "G": 10, "H": 10, "I": 10, "J": 10, "K": 10, "L": 10,
              "M": 10, "N": 10}

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))


    columns = ["A", "B", "C","D","E","F","G","H","I"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]
        ws.column_dimensions[c].height = heights[c]


    num_columns, letter_columns = zip(*list(enumerate(columns)))
    num_columns = list(num_columns)
    num_columns = [x + 1 for x in num_columns] #Desplazamos los valores en 1 porque Excel está indexado desde el 1 y no desde el 0
    letter_columns = list(letter_columns)

    # escribir los títulos de las columnas, en negrita

    texts = ["","","","ID", "NOMBRE", "ZONA", "COMPETENCIA",
             "SENIOR","RENDIMIENTO"]

    for i in range(4,len(num_columns)+1):
        cell = ws.cell(row=i, column=3, value=texts[i-1])
        cell.font = Font(bold=True,)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='left')


    # A continuación llenamos con los datos


    with db_session:
        e = db.Employees.get(id=id_employee)
        r=4
        #Escribe el ID del empleado
        if e.id != None:
            cell = ws.cell(row=r, column=4, value=e.id)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')
        else:
            cell = ws.cell(row=r, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')

        # Escribe el nombre del empleado
        if e.name != None:
            cell = ws.cell(row=r+1, column=4, value=e.name)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')
        else:
            cell = ws.cell(row=r+1, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')

        # Escribe la zona geográfica del empleado
        if e.zone != None:
            cell = ws.cell(row=r+2, column=4, value=e.zone)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')
        else:
            cell = ws.cell(row=r+2, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')

        # Escribe la competencia del empleado (por el momento se asume que solo es una)
        es = db.Employees_Skills.get(employee = e)
        if es.skill != None:
            skill_name = es.skill.name
            cell = ws.cell(row=r+3, column=4, value=skill_name)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')
        else:
            cell = ws.cell(row=r+3, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')

        # Escribe si el empleado es senior o no (Sí o No)
        if e.senior != None:
            if es.senior:
                value = "Sí"
            else:
                value = "No"
            cell = ws.cell(row=r+4, column=4, value = value)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')
        else:
            cell = ws.cell(row=r+4, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')

        if es.performance != None:
            cell = ws.cell(row=r+5, column=4, value = es.performance)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')
        else:
            cell = ws.cell(row=r+5, column=4, value="Dato no disponible")
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')

        #Imprimir el horario del trabajador
        cell = ws.cell(row=r+9, column=3, value="SEMANA")
        cell.font = Font(bold=True)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')
        aux_c = 1
        for day in ["Lunes","Martes", "Miercoles","Jueves","Viernes"]:
            cell = ws.cell(row=r + 9, column=3 + aux_c, value="{0}".format(day))
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
            aux_c+=1
        span_of_weeks = 14
        dates = []
        today = date.today()
        initial_week_date = today + timedelta(days=-today.weekday())
        calendar_r = r + 10 #Esta variable para la fila podría definirse se otra forma
        for i in range (0,span_of_weeks):
            dates.append(initial_week_date+i*timedelta(days=7))
        for d in dates:
            cell = ws.cell(row=calendar_r, column=3, value=d)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
            calendar_r+=1

    for r in [i for i in range(14,28)]:
        ws.row_dimensions[r].height = 40


    module_path = os.path.dirname(__file__)
    panorama_folder_path = os.path.abspath(os.path.join(module_path, os.pardir))
    report_folder_path = os.path.join(panorama_folder_path,"Reportes")
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)
    report_file_name = "Versión 2 Reporte empleado {}.xlsx".format(id_employee)
    fn = os.path.join(report_folder_path,report_file_name)
    wb.save(fn)

createEmployeeReportV2(db,3)