from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook, drawing
from openpyxl.styles import Font
import openpyxl
from openpyxl import Workbook
from openpyxl.chart import BarChart, Series, Reference
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



def createStockReport(db):
    id_sku = 1
    from Stock.features import displayStock, calculateStockForExcel
    displayStock(db,id_sku)
    base = calculateStockForExcel(db,id_sku)
    dates = base[0]
    values = base[1]

    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    # rows = [
    #     ('Fechas', 'Cantidad', 'Batch 2'),
    #     (2, 10, 30),
    #     (3, 40, 60),
    #     (4, 50, 70),
    #     (5, 20, 10),
    #     (6, 10, 40),
    #     (7, 50, 30),
    # ]
    # vals = [(i,np.sqrt(i)) for i in range(0,20)]
    vals = zip(dates,values)
    rows = [('Fechas', 'Cantidad')]
    rows.extend(vals)

    for row in rows:
        ws.append(row)

    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Status del SKU"
    chart1.y_axis.title = 'Cantidad'
    chart1.x_axis.title = 'Fecha'

    # data = Reference(ws, min_col=2, min_row=1, max_row=7, max_col=3)
    data = Reference(ws, min_col=2, min_row=1, max_row=len(dates)+1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=len(dates)+1)
    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)
    chart1.shape = 4
    chart1.width = 50
    ws.add_chart(chart1, "A10")

    from copy import deepcopy
    chart2 = deepcopy(chart1)

    ws.add_chart(chart2, "A25")
    # ws.insert_chart('C1', chart1) #Alternativa para insertar el gráfico

    # from copy import deepcopy
    #
    # chart2 = deepcopy(chart1)
    # chart2.style = 11
    # chart2.type = "bar"
    # chart2.title = "Horizontal Bar Chart"
    #
    # ws.add_chart(chart2, "G10")
    #
    # chart3 = deepcopy(chart1)
    # chart3.type = "col"
    # chart3.style = 12
    # chart3.grouping = "stacked"
    # chart3.overlap = 100
    # chart3.title = 'Stacked Chart'
    #
    # ws.add_chart(chart3, "A27")
    #
    # chart4 = deepcopy(chart1)
    # chart4.type = "bar"
    # chart4.style = 13
    # chart4.grouping = "percentStacked"
    # chart4.overlap = 100
    # chart4.title = 'Percent Stacked Chart'
    #
    # ws.add_chart(chart4, "G27")

    module_path = os.path.dirname(__file__)
    panorama_folder_path = os.path.abspath(os.path.join(module_path, os.pardir))
    report_folder_path = os.path.join(panorama_folder_path, "Reportes")
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)
    report_file_name = "Informe de Stock.xlsx"
    fn = os.path.join(report_folder_path, report_file_name)
    wb.save(fn)


from database import db
# createStockReport(db)