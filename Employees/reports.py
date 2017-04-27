from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font,Alignment
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import Color
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
# createEmployeeReportV1(db,3)

def createEmployeeReportV2(db,id_employee):
    ''' Este método crea un informe en Excel compacto con una proción de la información de la base de datos. '''
    with db_session:
        e = db.Employees.get(id=id_employee)
        es = db.Employees_Skills.get(employee=e)
        # ea = select(ea for ea in db.Employees_Activities if ea.employee == e)
        ea = db.Employees_Activities.get(employee=e)
        # print(ea.id) #Revisar creación de activities en consola
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

        if (es.skill.id == 4):
            # columns = ["A", "B", "C","D","E","F","G","H","I"] #Para un instalador y con el rendimiento
            columns = ["A", "B", "C", "D", "E", "F", "G", "H"]  # Para un instalador sin el rendimiento
            # texts = ["","","","ID", "NOMBRE", "ZONA", "COMPETENCIA",
            #          "SENIOR","RENDIMIENTO"] #Para un instalador y con el rendimiento
            texts = ["","","","ID", "NOMBRE", "ZONA", "COMPETENCIA",
                     "SENIOR"] #Para un instalador sin el rendimiento
        else:
            columns = ["A", "B", "C", "D", "E", "F", "G"]
            texts = ["", "", "", "ID", "NOMBRE", "ZONA", "COMPETENCIA"]

        aux_columns = ["A", "B", "C", "D", "E", "F", "G", "H"] #Solo para mantener el ancho de las celdas en el caso que no sea un instalador

        for c in aux_columns:
            ws.column_dimensions[c].width = widths[c]
            ws.column_dimensions[c].height = heights[c]


        num_columns, letter_columns = zip(*list(enumerate(columns)))
        num_columns = list(num_columns)
        num_columns = [x + 1 for x in num_columns] #Desplazamos los valores en 1 porque Excel está indexado desde el 1 y no desde el 0
        letter_columns = list(letter_columns)

        # escribir los títulos de las columnas, en negrita




        for i in range(4,len(num_columns)+1):
            cell = ws.cell(row=i, column=3, value=texts[i-1])
            cell.font = Font(bold=True,)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='left')


        # A continuación llenamos con los datos


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
        if(es.skill.id == 4):
            if e.senior != None:
                if e.senior:
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

        # # Escribe el rendimiento del trabajador
        # if es.performance != None:
        #     cell = ws.cell(row=r+5, column=4, value = es.performance)
        #     cell.font = Font(bold=True)
        #     cell.border = thin_border
        #     cell.alignment = Alignment(horizontal='left')
        # else:
        #     cell = ws.cell(row=r+5, column=4, value="Dato no disponible")
        #     cell.font = Font(bold=True)
        #     cell.border = thin_border
        #     cell.alignment = Alignment(horizontal='left')

        #Preparar el formato del horario/calendario del trabajador
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

        for f in [i for i in range(14, 14+len(dates))]:#Revisar los limites de indexación
            ws.row_dimensions[f].height = 40
            for c in [i for i in range(4,9)]:
                cell = ws.cell(row=f, column=c)
                cell.font = Font(bold=True)
                cell.border = thin_border
                # cell.alignment = Alignment(horizontal='center')
                wrap_alignment = Alignment(wrap_text=True, horizontal="center",vertical="center")
                cell.alignment = wrap_alignment



        #Imprimir las tareas del trabajador
        from Planning.features import isHoliday,isNotWorkday #Es realmente necesario importar isHoliday

        tareas = select(et for et in db.Employees_Tasks if et.employee == e)
        for tarea in tareas:
            task_initial_d = tarea.planned_initial_date
            task_final_d = tarea.planned_end_date
            task = db.Tasks.get(id=tarea.task.id)
            # Ajustar para que solo tome fechas de trabajo en días hábiles
            working_days = (task_final_d-task_initial_d).days
            working_days_span = working_days
            working_dates = []
            # working_dates = [task_initial_d + i*timedelta(days=1) for i in range(0,working_days)]
            working_days_counter = 0
            while(working_days_counter<working_days_span):
                if(not isNotWorkday(task_initial_d + working_days_counter*timedelta(days=1))):
                    working_dates.append(task_initial_d + working_days_counter*timedelta(days=1))
                else:
                    # working_days_span+=1 #Ya está considerado en el Planning
                    pass
                working_days_counter+=1


            for i in range(0,len(dates)-1):
                # if(dates[i]<=task_initial_d<dates[i+1]):
                #     # cell = ws.cell(row=r +10 + i, column=4+task_initial_d.weekday(), value="{0} \n Proyecto: {1}".format(task_initial_d, task.project))
                #     cell = ws.cell(row=r + 10 + i, column=4 + task_initial_d.weekday(),value="Proyecto {}".format(task.project))
                #     cell.font = Font(bold=True)
                #     cell.border = thin_border
                #     cell.alignment = Alignment(horizontal='center')
                #     # cell.style.alignment.wrap_text = True #Para autoajustar el tamaño de la celca. Revisar su correcto funcionamiento
                #     # create alignment style
                #     wrap_alignment = Alignment(wrap_text=True,horizontal="center",vertical="center")
                #     # assign
                #     cell.alignment = wrap_alignment
                for d in working_dates:
                    if (dates[i] <= d < dates[i + 1]):
                        # cell = ws.cell(row=r +10 + i, column=4+task_initial_d.weekday(), value="{0} \n Proyecto: {1}".format(task_initial_d, task.project))
                        cell = ws.cell(row=r + 10 + i, column=4 + d.weekday(),
                                       value="Proyecto {0}\n{1}".format(task.project,task.project.client_address))
                        cell.font = Font(bold=True)
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='center')
                        # cell.style.alignment.wrap_text = True #Para autoajustar el tamaño de la celca. Revisar su correcto funcionamiento
                        # create alignment style
                        wrap_alignment = Alignment(wrap_text=True, horizontal="center",
                                                   vertical="center")
                        # assign
                        cell.alignment = wrap_alignment
                        cell.fill = PatternFill("solid", fgColor="ffff00")
                    elif (dates[len(dates) - 1] <= d):
                        # cell = ws.cell(row=r +10 + i, column=4+task_initial_d.weekday(), value="{0} \n Proyecto: {1}".format(task_initial_d, task.project))
                        cell = ws.cell(row=r + 10 + i + 1, column=4 + d.weekday(),
                                       value="Proyecto {0}\n{1}".format(task.project,
                                                                        task.project.client_address))
                        cell.font = Font(bold=True)
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='center')
                        # cell.style.alignment.wrap_text = True #Para autoajustar el tamaño de la celca. Revisar su correcto funcionamiento
                        # create alignment style
                        wrap_alignment = Alignment(wrap_text=True, horizontal="center",
                                                   vertical="center")
                        # assign
                        cell.alignment = wrap_alignment
                        cell.fill = PatternFill("solid", fgColor="ffff00")

        # Imprimir los días feriados
        all_the_days_on_display = []
        for i in range(0,span_of_weeks*7):
            all_the_days_on_display.append(initial_week_date+timedelta(days=i))
        for i in range(0, len(dates)-1):
            for d in all_the_days_on_display:
                if (dates[i] <= d < dates[i + 1]):
                    if(isHoliday(d) and d.weekday() < 5):
                        cell = ws.cell(row=r + 10 + i, column=4 + d.weekday(),value="Feriado")
                        cell.font = Font(bold=True)
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='center')
                        wrap_alignment = Alignment(wrap_text=True, horizontal="center",vertical="center")
                        cell.alignment = wrap_alignment
                        cell.fill = PatternFill("solid", fgColor="00ffff")
                    elif(ws.cell(row=r + 10 + i, column=4 + d.weekday()).value==None and d.weekday() < 5):
                        ws.cell(row=r + 10 + i, column=4 + d.weekday()).value = "Disponible"
                        ws.cell(row=r + 10 + i, column=4 + d.weekday()).fill = PatternFill("solid", fgColor="00ff00")
                elif(dates[len(dates)-1] <= d):
                    if (isHoliday(d) and d.weekday() < 5):
                        cell = ws.cell(row=r + 10 + i + 1, column=4 + d.weekday(), value="Feriado")
                        cell.font = Font(bold=True)
                        cell.border = thin_border
                        cell.alignment = Alignment(horizontal='center')
                        wrap_alignment = Alignment(wrap_text=True, horizontal="center",
                                                   vertical="center")
                        cell.alignment = wrap_alignment
                        cell.fill = PatternFill("solid", fgColor="00ffff")
                    elif (ws.cell(row=r + 10 + i + 1, column=4 + d.weekday()).value == None and d.weekday() < 5):
                        ws.cell(row=r + 10 + i + 1, column=4 + d.weekday()).value = "Disponible"
                        ws.cell(row=r + 10 + i + 1, column=4 + d.weekday()).fill = PatternFill("solid", fgColor="00ff00")


        # for f in [i for i in range(14, 14+len(dates))]:
        #     ws.row_dimensions[f].height = 40
        #     for c in [i for i in range(4,9)]:
        #         cell = ws.cell(row=f, column=c)
        #         cell.font = Font(bold=True)
        #         cell.border = thin_border
        #         cell.alignment = Alignment(horizontal='center')









    module_path = os.path.dirname(__file__)
    panorama_folder_path = os.path.abspath(os.path.join(module_path, os.pardir))
    report_folder_path = os.path.join(panorama_folder_path,"Reportes")
    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)
    report_file_name = "Versión 2 Reporte empleado {}.xlsx".format(id_employee)
    fn = os.path.join(report_folder_path,report_file_name)
    wb.save(fn)

createEmployeeReportV2(db,1)
createEmployeeReportV2(db,2)
createEmployeeReportV2(db,3)
createEmployeeReportV2(db,4)
createEmployeeReportV2(db,5)
createEmployeeReportV2(db,6)
createEmployeeReportV2(db,7)
createEmployeeReportV2(db,8)
createEmployeeReportV2(db,9)
createEmployeeReportV2(db,10)
createEmployeeReportV2(db,11)
createEmployeeReportV2(db,12)
createEmployeeReportV2(db,13)
