from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font,Alignment
import os

def createEmployeeReport(db,id_employee):
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

        r+=1

    module_path = os.path.dirname(__file__)
    panorama_folder_path = os.path.abspath(os.path.join(module_path, os.pardir))
    report_folder_path = os.path.join(panorama_folder_path,"Reportes")
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)
    report_file_name = "Reporte empleado {}.xlsx".format(id_employee)
    fn = os.path.join(report_folder_path,report_file_name)
    wb.save(fn)

# # from pony.orm import *
from database import db
createEmployeeReport(db,1)