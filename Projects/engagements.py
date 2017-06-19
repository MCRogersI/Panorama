from pony.orm import *
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from . import materialCost, instalationCost, fabricationCost
import convert

def createEngagements(db, contract_number, file_name):
    # primero, obtenemos el archivo de la hoja de corte
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only = True)
    #revisamos que el archivo tenga la hoja que necesitamos
    try:
        ws = wb_read["Manufacturing"]
    except KeyError:
        print(' Formato invalido del archivo. El archivo debe tener una hoja llamada Measures.')
        return
    
    createEngagementsProfiles(db, contract_number, ws)
    createEngagementsFittings(db, contract_number, ws)
    
###################################################################
# Desde aqui los metodos auxiliares que calculan todos los costos #
###################################################################

def standardCostCalculation(db, project_cost, parameters):
    file_read = parameters[5] + ".xlsx"

    wb_read = load_workbook(file_read, data_only=True)

    #tercero, calculamos y escribimos los costos de instalacion
    instalationCost.computation(db, wb_read, project_cost, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])

    #cuarto, calculamos y escribimos los costos de fabricacion
    fabricationCost.computation(db, wb_read, project_cost)

    #segundo, calculamos los costos por materia prima
    materialCost.computation(db, wb_read, project_cost)

    #quinto, calculamos y escribimos los costos adicionales
    
    #por ultimo, actualizamos los datos que faltan en la tabla Projects_Costs
    with db_session:
        project_cost.standard_cost_additionals = 0
    
        profiles_cost = project_cost.standard_cost_profiles
        fittings_cost = project_cost.standard_cost_fittings
        crystals_cost = project_cost.standard_cost_crystals
        project_cost.standard_cost_material = profiles_cost + fittings_cost + crystals_cost
        
        additional_costs = project_cost.standard_cost_additionals
        installation_cost = project_cost.standard_cost_installation
        fabrication_cost = project_cost.standard_cost_fabrication
        project_cost.standard_cost_total = profiles_cost + fittings_cost + crystals_cost + additional_costs + installation_cost + fabrication_cost
        
        commit()
    #si el cálculo es exitoso
    return True
    
####################################################################################################
# Método auxiliar para manejar los casos en que alguno de los valores no están en la base de datos #
####################################################################################################

def getParameter(table, key, exception, warning):
    parameter = 0
    try:
        parameter = table[key].value
    except exception:
        print(warning)
        parameter = 0
    return parameter