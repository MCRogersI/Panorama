from pony.orm import *
from datetime import date, timedelta
import pandas as pd
import numpy as np
from openpyxl import Workbook, load_workbook
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Font,Alignment
import os

#################
# Global report #
#################

newpath = "C:\\Users\\Alonso\\Desktop\\EMPRENDIMIENTO\\Proyectos mubound\\Panorama\\reportes"
if not os.path.exists(newpath):
    os.makedirs(newpath)

def createGlobalReport(db):
    wb = Workbook()
    by_default_sheet = wb.get_sheet_by_name('Sheet')
    by_default_sheet.title = 'Introducción del informe'
    ws = wb.create_sheet(
        "BASE DE DATOS OUTPUT A EXCEL")

    widths = {"A": 5, "B": 35, "C": 5,"D": 35, "E": 35, "F": 35,
              "G": 35, "H": 35, "I": 35,"J": 35, "K": 35, "L": 35,
              "M": 35, "N": 35, "O": 35,"P": 35, "Q": 35, "R": 35,
              "S": 35, "T": 35, "U": 35,"V": 35, "W": 35, "X": 35,
              "Y": 35, "Z": 35, "AA": 35, "AB": 35, "AC": 35, "AD": 35,
              "AE": 35, "AF": 35, "AG": 35, "AH": 35, "AI": 35, "AJ": 35,
              "AK": 35, "AL": 35, "AM": 35, "AN": 35, "AO": 35, "AP": 35,
              "AQ": 35, "AR": 35, "AS": 35, "AT": 35, "AU": 35, "AV": 35,
              "AW": 35, "AX": 35, "AY": 35, "AZ": 35,"BA": 35, "BB": 35,
              "BC": 35, "BD": 35,"BE": 35, "BF": 35, "BG": 35, "BH": 35,
              "BI": 35, "BJ": 35,"BK": 35, "BL": 35, "BM": 35}

    heights = {"A": 10, "B": 10, "C": 10, "D": 10, "E": 10, "F": 10,
              "G": 10, "H": 10, "I": 10, "J": 10, "K": 10, "L": 10,
              "M": 10, "N": 10, "O": 10, "P": 10, "Q": 10, "R": 10,
              "S": 10, "T": 10, "U": 10, "V": 10, "W": 10, "X": 10,
              "Y": 10, "Z": 10, "AA": 10, "AB": 10, "AC": 10, "AD": 10,
              "AE": 10, "AF": 10, "AG": 10, "AH": 10, "AI": 10, "AJ": 10,
              "AK": 10, "AL": 10, "AM": 10, "AN": 10, "AO": 10, "AP": 10,
              "AQ": 10, "AR": 10, "AS": 10, "AT": 10, "AU": 10, "AV": 10,
              "AW": 10, "AX": 10, "AY": 10, "AZ": 10, "BA": 10, "BB": 10,
              "BC": 10, "BD": 10, "BE": 10, "BF": 10, "BG": 10, "BH": 10,
              "BI": 10, "BJ": 10, "BK": 10, "BL": 10, "BM": 10}

    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))


    columns = ["A", "B", "C","D","E","F","G","H","I","J","K","L","M","N",
               "O","P","Q","R","S","T","U","V","W","X","Y","Z","AA","AB",
               "AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN",
               "AO","AP","AQ","AR","AS","AT","AU","AV","AW","AX","AY","AZ",
               "BA","BB","BC","BD","BE","BF","BG","BH","BI","BJ","BK","BL","BM"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]
        ws.column_dimensions[c].height = heights[c]


    num_columns, letter_columns = zip(*list(enumerate(columns)))
    num_columns = list(num_columns)
    num_columns = [x + 1 for x in num_columns] #Desplazamos los valores en 1 porque Excel está indexado desde el 1 y no desde el 0
    letter_columns = list(letter_columns)

    # escribir los títulos de las columnas, en negrita

    texts = ["","","","NRO CONTRATO", "FECHA VENTA CONTRATO", "MES_AÑO VENTA CONTRATO", "PRECIO VENTA CTTO",
             "MTS LINEALES CTTO", "MTS 2 CTTO", "STATUS INICIAL_CTTO", "STATUS FINAL_CTTO",
             "UNIDAD ORIGEN FALLA CALIDAD", "COSTO ESTANDAR PERFILES", "COSTO ESTANDAR HERRAJES",
             "COSTO ESTANDAR CRISTALES", "COSTO ESTANDAR M PRIMAS", "COSTO ESTANDAR FABRICACION",
             "COSTO ESTANDAR INSTALACION", "COSTO ESTANDAR ADICIONALES", "COSTO ESTANDAR TOTAL",
             "COSTO EFECTIVO M PRIMAS", "COSTO EFECTIVO FABRICACION", "COSTO EFECTIVO INSTALACION",
             "COSTO EFECTIVO COMPLEMENTOS", "FECHA LIMITE ENTREGA_CTTO",
             "FECHA EFECTIVA ENTREGA_CTTO",
             "MAYOR PLAZO ENTREGA_CTTO", "MES_AÑO RECTIFIC CONTRATO", "FECHA PLANIF ENTREGA_RECTIF",
             "FECHA EFECTIVA ENTREGA_RECTIF", "MAYOR PLAZO RECTIFICACION", "ID RECTIFICADOR",
             "MES_AÑO ENTREGA HOJA CORTE CTTO", "FECHA PLANIF ENTREGA_HC",
             "FECHA EFECTIVA ENTREGA_HC",
             "MAYOR PLAZO ENTREGA_HC", "ID DISEÑADOR_HC",
             "FECHA PLANIFICACION EMISION O.C. CRISTALES",
             "FECHA EFECTIVA EMISION O.C. CRISTALES", "MAYOR PLAZO EMISION O.C. CRISTALES",
             "MES_AÑO EMISION O.C. CRISTALES", "ID EMISOR_OC CRISTALES",
             "FECHA PLANIF RECEPCION CRISTALES",
             "FEHCA EFECTIVA RECEPCION CRISTALES", "MAYOR PLAZO RECEPCION CRISTALES",
             "MES_AÑO RECEP CRISTALES",
             "ID PROVEEDOR CRISTALES", "FECHA PLANIF INICIO FABRICACION",
             "FECHA EFECTIVA INICIO FABRICACION",
             "MAYOR PLAZO INICIO FABRICACION", "MES_AÑO INICIO FABRICACION", "ID RESPONS FABRICAC",
             "FECHA PLANIFIC FINALIZAC FABRICAC", "FECHA EFECTIVA FINALIZAC FABRICAC",
             "MAYOR PLAZO FINALIZ FABRICACION", "MEZ_AÑO FINALIZ FABRICACION", "I.D FABRICACION",
             "FECHA INICIO PLANIF INSTALACION", "FECHA INICIO EFECTIVA INSTALACION",
             "MAYOR PLAZO INICIO INSTALACION", "ID INSTALADOR",
             "FECHA PLANIFICADA FINALIZ INSTALACION",
             "FECHA EFECTIVA FINALIZ INSTALACION", "MAYOR PLAZO INSTALACION", "ID INSTALADOR"]

    for i in range(4,len(num_columns)+1):
        cell = ws.cell(row=3, column=i, value=texts[i-1])
        cell.font = Font(bold=True,)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')

    # Escribir título general
    cell = ws.cell(row=1, column=2, value="PLANNER OPERATION SYSTEM")
    cell.font = Font(bold=True,underline="single")
    cell.alignment = Alignment(horizontal='center')


    # Escribir título general
    cell = ws.cell(row=4, column=2, value="RESPONSABLE DIGITAC INFORMAC")
    # cell.font = Font(bold=True)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')

    # Escribir título general
    cell = ws.cell(row=6, column=2, value="UNIDAD DE MEDIDA")
    # cell.font = Font(bold=True)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')

    # Escribir título general
    cell = ws.cell(row=8, column=2, value="STATUS POSIBLES")
    # cell.font = Font(bold=True)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')

    # Escribir título general
    cell = ws.cell(row=10, column=2, value="OBSERVACIONES")
    # cell.font = Font(bold=True)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')

    # Escribir título general
    cell = ws.cell(row=16, column=2, value="COSTOS ESTANDARES")
    # cell.font = Font(bold=True)
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center')




    # llenar con los datos


    with db_session:
        projects = select(p for p in db.Projects).order_by(lambda p: p.contract_number)
        r=4
        for p in projects:
            #Escribe el número de contrato
            cell = ws.cell(row=4, column=4, value=p.contract_number)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

            #Escribe la fecha de venta del contrato
            cell = ws.cell(row=4, column=5, value=p.sale_date)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

            # Escribe el mes y año de venta del contrato
            sale_year = p.sale_date.year
            sale_month = p.sale_dale.month
            months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto",
                      "Septiembre","Octubre","Noviembre","Diciembre"]
            sale_month = months[sale_month-1]
            cell = ws.cell(row=4, column=6, value="{0}_{1}".format(sale_month,sale_year))
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

            # # Escribe el precio de venta del contrato
            # cell = ws.cell(row=4, column=7, value=p.sale_cost)
            # cell.font = Font(bold=True)
            # cell.border = thin_border
            # cell.alignment = Alignment(horizontal='center')
            #
            # # Escribe la cantidad de metros lineales del proyecto (contrato)
            # cell = ws.cell(row=4, column=8, value=p.linear_meters)
            # cell.font = Font(bold=True)
            # cell.border = thin_border
            # cell.alignment = Alignment(horizontal='center')
            #
            # # Escribe la cantidad de metros lineales del proyecto (contrato)
            # cell = ws.cell(row=4, column=8, value=p.linear_meters)
            # cell.font = Font(bold=True)
            # cell.border = thin_border
            # cell.alignment = Alignment(horizontal='center')

            r+=1

    wb.save("C:\\Users\\Alonso\\Desktop\\EMPRENDIMIENTO\\Proyectos mubound\\Panorama\\reportes\\Global Report.xlsx")



# # from pony.orm import *
# from database import db
# createGlobalReport(db)

def createGlobalReportCompact(db):
    wb = Workbook()
    by_default_sheet = wb.get_sheet_by_name('Sheet')
    by_default_sheet.title = 'Introducción del informe'
    ws = wb.create_sheet(
        "Informe BD compacto")

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


    columns = ["A", "B", "C","D","E","F","G","H","I","J","K","L","M","N"]
    for c in columns:
        ws.column_dimensions[c].width = widths[c]
        ws.column_dimensions[c].height = heights[c]


    num_columns, letter_columns = zip(*list(enumerate(columns)))
    num_columns = list(num_columns)
    num_columns = [x + 1 for x in num_columns] #Desplazamos los valores en 1 porque Excel está indexado desde el 1 y no desde el 0
    letter_columns = list(letter_columns)

    # escribir los títulos de las columnas, en negrita

    texts = ["","","","NUMERO DE CONTRATO", "NOMBRE CLIENTE", "PRIORIDAD", "METROS LINEALES",
             "FECHA LÍMITE","COMUNA CLIENTE", "DIRECCIÓN CLIENTE", "METROS LINEALES REALES", "COSTO ESTIMADO",
             "PRECIO DE VENTA", "FECHA DE VENTA"]

    for i in range(4,len(num_columns)+1):
        cell = ws.cell(row=3, column=i, value=texts[i-1])
        cell.font = Font(bold=True,)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center')

    # llenar con los datos


    with db_session:
        projects = select(p for p in db.Projects).order_by(lambda p: p.contract_number)
        r=4
        for p in projects:
            #Escribe el número de contrato
            cell = ws.cell(row=4, column=4, value=p.contract_number)
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')

            r+=1

    wb.save("C:\\Users\\Alonso\\Desktop\\EMPRENDIMIENTO\\Proyectos mubound\\Panorama\\reportes\\Global Report Compact.xlsx")

# # from pony.orm import *
from database import db
createGlobalReportCompact(db)
















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
    from Planning.features import datesOverlap, fillCommitments
    with db_session:
        #recorremos para cada empleado el reporte de planificación, guardando todas las veces en que aparece asignado para una tarea
        employees = select(e for e in db.Employees)
        for e in employees:
            id = e.id
            initial_date_rows = []
            initial_date_columns = []
            skills = []
            for next_row in range(4, max_row + 1):
                if id == ws.cell(row = next_row, column = 4).value:
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(2)
                    skills.append(1)
                if id == ws.cell(row = next_row, column = 7).value:
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(5)
                    skills.append(2)
                if id == ws.cell(row = next_row, column = 10).value:
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(8)
                    skills.append(3)
                if str(id) in str(ws.cell(row = next_row, column = 13).value).split(';'):
                    initial_date_rows.append(next_row)
                    initial_date_columns.append(11)
                    skills.append(4)
            #teniendo esa información guardada, ahora revisamos si calzan entre ellas
            dates = len(initial_date_columns)
            for i in range(0, dates):
                #si el Skill es 3 o 4, entonces su fecha no puede calzar con ninguna otra
                if skills[i] == 3 or skills[i] == 4:
                    for j in (k for k in range(0, dates) if k != i):
                        initial_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i]).value.date()
                        end_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i] + 1).value.date()
                        initial_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j]).value.date()
                        end_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j] + 1).value.date()
                        if datesOverlap(initial_date_1, end_date_1, initial_date_2, end_date_2):
                            return False
                #si el Skill es 1 o 2, nos fijamos solamente en las otras fechas con Skill 1 o 2, los otros Skills estan cubiertos por el IF de arriba
                else:
                    initial_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i]).value.date()
                    end_date_1 = ws.cell(row = initial_date_rows[i], column = initial_date_columns[i] + 1).value.date()
                    # creamos un arreglo de puros 0's de largo el lapso de tiempo entre initial_date y end_date, y lo vamos llenando con las tareas que tienen
                    commitments_skill_1 = np.zeros( abs((end_date - initial_date).days) + 1 )
                    commitments_skill_2 = np.zeros( abs((end_date - initial_date).days) + 1 )
                    for j in (k for k in range(0, dates) if k != i and skills[k] == 1):
                        initial_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j]).value.date()
                        end_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j] + 1).value.date()
                        commitments_skill_1 = fillCommitments(commitments_skill_1, initial_date_1, end_date_1, et.planned_initial_date_2, et.planned_end_date_2)
                    for j in (k for k in range(0, dates) if k != i and skills[k] == 2):
                        initial_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j]).value.date()
                        end_date_2 = ws.cell(row = initial_date_rows[j], column = initial_date_columns[j] + 1).value.date()
                        commitments_skill_2 = fillCommitments(commitments_skill_2, initial_date_1, end_date_1, et.planned_initial_date_2, et.planned_end_date_2)    
                    # vemos cuánto es lo máximo que puede hacer por día, entre ambos Skills (si alguno es 0, solo entre un Skill)
                    es_skill_1 = db.Employees_Skills.get(employee = db.Employees[id], skill = db.Skills[1])
                    limit_skill_1 = np.floor(es_skill_1.performance)
                    es_skill_2 = db.Employees_Skills.get(employee = db.Employees[id], skill = db.Skills[2])
                    limit_skill_2 = np.floor(es_skill_2.performance)
                    # en este caso nos fijamos solo en los Tasks del Skill 2
                    if limit_skill_1 == 0:
                        for c in commitments_skill_2:
                            if c > limit_skill_2:
                                return False
                    # en este caso nos fijamos solo en los Tasks del Skill 1
                    elif limit_skill_2 == 0:
                        for c in commitments_skill_1:
                            if c > limit_skill_1:
                                return False
                    # en este caso nos fijamos en los Tasks del Skill 1 y tambien del Skill 2
                    else:
                        for i in range(0, len(commitments_skill_1)):
                            proportion = commitments_skill_1[i]/limit_skill_1 + commitments_skill_2[i]/limit_skill_2
                            if proportion > 1:
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
