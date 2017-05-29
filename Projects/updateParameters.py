from pony.orm import *
from openpyxl import load_workbook

def updateFreightCosts(db, file_name):
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_freight = wb_read["Flete"]
    
    next_row = 5
    comuna_to = ws_read_freight.cell(row = next_row, column = 1).value
    while(comuna_to != None):
        freight_cost = ws_read_freight.cell(row = next_row, column = 2).value
        with db_session:
            fc = db.Freight_Costs.get(comuna_to = comuna_to)
            #revisamos si el codigo leido esta ya en la base de datos. Si esta, actualizamos la informacion, si no esta, creamos el nuevo SKU con la informacion entregada
            if fc != None:
                fc.freight_cost = freight_cost
            else:
                db.Freight_Costs(comuna_to = comuna_to, freight_cost = freight_cost)
        next_row = next_row + 1
        comuna_to = ws_read_freight.cell(row = next_row, column = 1).value


        
def updateOperatingCosts(db, file_name):
    pass


    
def updateViaticCosts(db, file_name):
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_viatic = wb_read["Viaticos"]
    
    next_row = 5
    comuna_from = ws_read_viatic.cell(row = next_row, column = 1).value
    while(comuna_from != None):
        comuna_to = ws_read_viatic.cell(row = next_row, column = 2).value
        viatic_cost = ws_read_viatic.cell(row = next_row, column = 3).value
        with db_session:
            vc = db.Viatic_Costs.get(comuna_from = comuna_from, comuna_to = comuna_to)
            #revisamos si el codigo leido esta ya en la base de datos. Si esta, actualizamos la informacion, si no esta, creamos el nuevo SKU con la informacion entregada
            if vc != None:
                vc.viatic_cost = viatic_cost
            else:
                db.Viatic_Costs(comuna_from = comuna_from, comuna_to = comuna_to, viatic_cost = viatic_cost)
        next_row = next_row + 1
        comuna_from = ws_read_viatic.cell(row = next_row, column = 1).value
        
        
        
def updateMovilizationCosts(db, file_name):
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_movilization = wb_read["Movilizacion"]
    
    next_row = 5
    comuna_from = ws_read_movilization.cell(row = next_row, column = 1).value
    while(comuna_from != None):
        comuna_to = ws_read_movilization.cell(row = next_row, column = 2).value
        movilization_cost = ws_read_movilization.cell(row = next_row, column = 3).value
        with db_session:
            mc = db.Movilization_Costs.get(comuna_from = comuna_from, comuna_to = comuna_to)
            #revisamos si el codigo leido esta ya en la base de datos. Si esta, actualizamos la informacion, si no esta, creamos el nuevo SKU con la informacion entregada
            if mc != None:
                mc.movilization_cost = movilization_cost
            else:
                db.Movilization_Costs(comuna_from = comuna_from, comuna_to = comuna_to, movilization_cost = movilization_cost)
        next_row = next_row + 1
        comuna_from = ws_read_movilization.cell(row = next_row, column = 1).value
        
        

def updateCrystalsParameters(db, file_name):
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_crystals = wb_read["Parametros cristales"]
    
    next_row = 5
    thickness = ws_read_crystals.cell(row = next_row, column = 1).value
    while(thickness != None):
        square_meter_cost = ws_read_crystals.cell(row = next_row, column = 2).value
        waste_factor = ws_read_crystals.cell(row = next_row, column = 3).value
        with db_session:
            cp = db.Crystals_Parameters.get(thickness = thickness)
            #revisamos si el codigo leido esta ya en la base de datos. Si esta, actualizamos la informacion, si no esta, creamos el nuevo SKU con la informacion entregada
            if cp != None:
                cp.square_meter_cost = square_meter_cost
                cp.waste_factor = waste_factor
            else:
                db.Crystals_Parameters(thickness = thickness, square_meter_cost = square_meter_cost, waste_factor = waste_factor)
        next_row = next_row + 1
        thickness = ws_read_crystals.cell(row = next_row, column = 1).value
        
        
        
def updateProfilesParameters(db, file_name):
    file_read = file_name + ".xlsx"
    wb_read = load_workbook(file_read, data_only=True)
    ws_read_profiles = wb_read["Parametros perfiles"]
    
    next_row = 5
    profile = ws_read_profiles.cell(row = next_row, column = 1).value
    while(profile != None):
        waste_factor = ws_read_profiles.cell(row = next_row, column = 2).value
        with db_session:
            pp = db.Profiles_Parameters.get(profile = profile)
            #revisamos si el codigo leido esta ya en la base de datos. Si esta, actualizamos la informacion, si no esta, creamos el nuevo SKU con la informacion entregada
            if pp != None:
                pp.waste_factor = waste_factor
            else:
                db.Profiles_Parameters(profile = profile, waste_factor = waste_factor)
        next_row = next_row + 1
        profile = ws_read_profiles.cell(row = next_row, column = 1).value        