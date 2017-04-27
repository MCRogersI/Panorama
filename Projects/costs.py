from pony.orm import *
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from . import materialCost, instalationCost, fabricationCost

def estimateCost(db, contract_number, file_name):
    # primero, obtenemos la comuna donde se realizara el proyecto
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_measures = wb_read["Measures"]
    comuna_to = ws_read_measures.cell(row = 7, column = 15).value
    
    # luego, obtenemos el freight_cost de la tabla Freight_Costs
    freight_cost = db.Freight_Costs[comuna_to].freight_cost
    
    # segundo, obtenemos la lista de instaladores ligados al proyecto
    tasks = select(t for t in db.Tasks if t.skill == db.Skills[4] and t.project == db.Projects[contract_number])
    installers = []
    for t in tasks:
        if t.failed != True:
            installers_tasks = select(et for et in db.Employees_Tasks if et.task == t)
            for it in installers_tasks:
                installers.append(it.employee)
    
    # luego, obtenemos los datos viatic_cost y movilization_cost de las tablas comuna-comuna, para cada instalador
    # tambien contamos la cantidad de instaladores, el tema de si son externos o no queda pendiente
    viatic_cost = 0
    movilization_cost = 0
    num_installers = 0
    for i in installers:
        num_installers = num_installers + 1
        viatic_cost = viatic_cost + db.Viatic_Costs[(i.zone, comuna_to)].viatic_cost
        movilization_cost = movilization_cost + db.Movilization_Costs[(i.zone, comuna_to)].movilization_cost
    
    # creamos tambien el Projects_Costs que usaremos en adelante
    project_cost = db.Projects_Costs(project = db.Projects[contract_number])
    
    parameters = viatic_cost, movilization_cost, num_installers, freight_cost, 1, file_name
    standardCostCalculation(db, project_cost, parameters)
    
###################################################################
# Desde aqui los metodos auxiliares que calculan todos los costos #
###################################################################

def standardCostCalculation(db, project_cost, parameters):
    file_read = parameters[5] + ".xlsx"
    file_written = "Costo Estandar " + file_read

    wb_read = load_workbook(file_read, data_only=True)
    wb_written = Workbook()

    #tercero, calculamos y escribimos los costos de instalacion
    instalationCost.computation(wb_read, wb_written, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])

    #cuarto, calculamos y escribimos los costos de fabricacion
    fabricationCost.computation(wb_read, wb_written)

    #segundo, calculamos los costos por materia prima
    materialCost.computation(wb_read, wb_written)

    #quinto, calculamos y escribimos los costos adicionales
    
    #guardamos el archivo de output
    wb_written.save(file_written)
    
    #por ultimo, pasamos los datos a la tabla Projects_Costs
    wb_written = load_workbook(file_written, data_only=True)
    ws_summary = wb_written["Resumen"]
    with db_session:
        profiles_cost = ws_summary.cell(row = 2, column = 5).value
        fittings_cost = ws_summary.cell(row = 2, column = 6).value
        crystals_cost = ws_summary.cell(row = 2, column = 4).value
        
        project_cost.standard_cost_profiles = profiles_cost
        project_cost.standard_cost_fittings = fittings_cost
        project_cost.standard_cost_crystals = crystals_cost
        project_cost.standard_cost_material = profiles_cost + fittings_cost + crystals_cost
        project_cost.standard_cost_fabrication = ws_summary.cell(row = 2, column = 7).value
        project_cost.standard_cost_installation = ws_summary.cell(row = 2, column = 8).value
        project_cost.standard_cost_additionals = 0
        project_cost.standard_cost_total = ws_summary.cell(row = 2, column = 9).value
        
        commit()
    
