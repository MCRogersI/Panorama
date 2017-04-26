from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook, drawing
from openpyxl.styles import Font
import openpyxl
import os

def baseCreateReport():
    wb = Workbook()
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

    #Llenar con los datos

    #Insertar imagen
    # ws = wb.worksheets[0]
    # img = openpyxl.drawing.Image('sku_plot.png')
    # img.anchor(ws.cell('A1'))
    # ws.add_image(img)

    #Guardar el archivo
    module_path = os.path.dirname(__file__)
    panorama_folder_path = os.path.abspath(os.path.join(module_path, os.pardir))
    report_folder_path = os.path.join(panorama_folder_path, "Reportes")
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)
    report_file_name = "Informe Stock.xlsx"
    fn = os.path.join(report_folder_path, report_file_name)
    wb.save(fn)

# baseCreateReport()