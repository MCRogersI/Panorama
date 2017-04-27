from pony.orm import *



def estimateCost(db, contract_number, file_name):
    # primero, obtenemos la comuna donde se realizara el proyecto
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_measures = wb_read["Measures"]
    comuna_to = ws_read_measures.cell(row = 7, column = 15).value
    
    # luego, obtenemos el freight_cost de la tabla Freight_Costs
    freight_cost = db.Freight_Costs[comuna_to].freight_cost
    
    # segundo, obtenemos la lista de instaladores ligados al proyecto
    tasks = select(t for t in db.Tasks if t.skill == db.Skills[4] and t.project == db.Projects[contract_number] and t.failed != True)
    installers = []
    for t in tasks:
        installers_tasks = select(et for et in db.Employees_Tasks if et.task == t)
        for it in installers_tasks:
            installers.append(it.employee)
    
    # luego, obtenemos los datos viatic_cost y movilization_cost de las tablas comuna-comuna, para cada instalador
    # también contamos la cantidad de instaladores, el tema de si son externos o no queda pendiente
    viatic_cost = 0
    movilization_cost = 0
    num_installers = 0
    for i in installers:
        num_installers = num_installers + 1
        viatic_cost = viatic_cost + db.Viatic_Costs[(i.zone, comuna_to)].viatic_cost
        movilization_cost = movilization_cost + db.Movilization_Costs[(i.zone, comuna_to)].movilization_cost
        
    
    parameters = viatic_cost, movilization_cost, , freight_cost, num_installers, file_name