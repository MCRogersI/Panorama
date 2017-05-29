from pony.orm import *
from openpyxl import load_workbook
from math import ceil
from copy import copy


######################################################################################
# Muy simple, se encarga de llamar a todas las funciones que hacen de verdad la pega #
######################################################################################

def computation(db, wb_read, project_cost):
    ws_read_manufacturing = wb_read["Manufacturing"]
    
    #necesitamos algunos parametros basicos para costear
    with db_session:
        royalty_porcentaje = db.Operating_Costs.get(name = "Royalty").value
        seguros_porcentaje = db.Operating_Costs.get(name = "Seguros, Transporte, Aduana, Flete").value
        euro = db.Operating_Costs.get(name = "Valor del euro").value
    
    #ahora seguimos escribiendo en el archivo, donde llamamos varias funciones mas
    writeInfoGlass(db, project_cost, ws_read_manufacturing)
    writeInfoProfile(db, project_cost, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro)
    components_cost = writeInfoComponents(db, project_cost, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro)
    sealings_cost = writeInfoSealings(db, project_cost, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro)

    #terminamos con la escritura del archivo Resumen
    project_cost.standard_cost_fittings = components_cost + sealings_cost
    
    
    
##############################################################################
# Aca empezamos a escribir la informacion relacionada al proyecto especifico #
##############################################################################

# Partimos por los Glass
def writeInfoGlass(db, project_cost, ws_read_manufacturing):
    #necesitamos algunos parametros, en este caso, los tomamos de la base de datos
    with db_session:
        thickness = str(ws_read_manufacturing.cell(row = 7, column = 2).value)
        cristal = db.Crystals_Parameters.get(name = thickness)
        costo_cristal_por_m2 = cristal.square_meter_cost
        factor_perdida = cristal.waste_factor
        #lo pasamos de porcentaje a fraccion
        factor_perdida = porcentaje_venta/100.0

    #primero, calculamos los metros lineales
    metros_lineales = 0
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
        metros_lineales = metros_lineales + width/1000
        width = ws_read_manufacturing.cell(row = next_row, column = 4).value
        next_row = next_row + 1
    
    #segundo, calculamos los metros cuadrados
    metros_cuadrados = 0
    height = ws_read_manufacturing.cell(row = 7, column = 3).value
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
        metros_cuadrados = metros_cuadrados + (height*width)/1000000
        height = ws_read_manufacturing.cell(row = next_row, column = 3).value
        width = ws_read_manufacturing.cell(row = next_row, column = 4).value
        next_row = next_row + 1
        
    #calculamos el ultimo dato necesario
    costo_estandar_cristales = metros_cuadrados*costo_cristal_por_m2/(1 - factor_perdida)
    
    #escribimos efectivamente el costo estandar de cristales en la base de datos
    with db_session:
        db.project_cost.standard_cost_crystals = costo_estandar_cristales
    
 
# Pasamos a los Profiles
def writeInfoProfile(db, project_cost, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro):
    #primero, para el Perfil Superior
    with db_session:
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Upper").waste_factor
        length_coords = [48, 2]
        code_coords = [46, 2]
        profile1 = writeProfile(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, factor_perdida, length_coords, code_coords)
    
    #ahora, el Perfil Inferior
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Lower").waste_factor
        length_coords = [60, 2]
        code_coords = [58, 2]
        profile2 = writeProfile(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, factor_perdida, length_coords, code_coords)
    
    #por ultimo, el Perfil Telescopico
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Teleskopic").waste_factor
        length_coords = [72, 2]
        code_coords = [70, 2]
        profile3 = writeProfile(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, factor_perdida, length_coords, code_coords)
    
    #ahora, los Glassing Beads
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Glassing beads").waste_factor
        length_coords = [47, 13]
        code_coords = [78, 14]
        profile4 = writeProfile(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                            factor_perdida, length_coords, code_coords, True)
 
    #ahora, los Glassing Beads Covers
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Glassing bead cover").waste_factor
        length_coords = [47, 13]
        code_coords = [79, 14]
        profile5 = writeProfile(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                            factor_perdida, length_coords, code_coords, True)
                            
        project_cost.standard_cost_profiles = profile1 + profile2 + profile3 + profile4 + profile5
  
 
def writeProfile(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                    factor_perdida, length_coords, code_coords, bead = False):
    #primero, calculamos los metros lineales
    metros_lineales = 0
    length = ws_read_manufacturing.cell(row = length_coords[0], column = length_coords[1]).value
    next_row = length_coords[0] + 1
    while(length > 0): #float(length.replace(',', '.')) en caso que length sea leido como string
        metros_lineales = metros_lineales + length/1000
        length = ws_read_manufacturing.cell(row = next_row, column = length_coords[1]).value
        next_row = next_row + 1
    if bead:
        metros_lineales = 2*metros_lineales
    metros_lineales_totales = metros_lineales/(1 - factor_perdida)
    
    #segundo, calculamos el costo unitario (pre royalty/seguros/flete)
    code = ws_read_manufacturing.cell(row = code_coords[0], column = code_coords[1]).value
    precio, quantity = getByCode(db, code)
    if quantity == 0 and bead:
        precio, quantity = getByCode(db, 54220002)
    
    #ahora, el precio con el royalty y todo
    precio_royalty = precio * (1 + royalty_porcentaje) * (1 + seguros_porcentaje)
    
    #calculamos el ultimo dato necesario
    costo_estandar = metros_lineales_totales*precio_royalty*euro
    
    #escribimos finalmente la informacion obtenida
    return costo_estandar
        
        
# Ahora a los Components
def writeInfoComponents(ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro):
    with db_session:
        #partimos por Components to Glass Panes
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Components to glass panes").waste_factor
        rows_read = [126, 134]
        columns_read = [1, 6]
        rows = [22, 30]
        column = 2
        component1 = writeComponent(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                            factor_perdida, rows_read, columns_read, rows, column)
        
        #seguimos con Components to component box or profiles
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Components to component box or profiles").waste_factor
        rows_read = [140, 150]
        columns_read = [1, 6]
        rows = [36, 45]
        column = 2
        component2 = writeComponent(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                            factor_perdida, rows_read, columns_read, rows, column)
        
        # partimos por Components to Glass Panes
        factor_perdida = db.Profiles__Fittings_Parameters.get(name = "Components to component box").waste_factor
        rows_read = [126, 148]
        columns_read = [8, 15]
        rows = [51, 73]
        column = 2
        component3 = writeComponent(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                            factor_perdida, rows_read, columns_read, rows, column)
                            
        return component1 + component2 + component3


def writeComponent(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro, \
                        factor_perdida, rows_read, columns_read, rows, column):
    for i in range(0, rows_read[1] - rows_read[0] + 1):
        #vemos primero unidades totales requeridas del producto
        units = ws_read_manufacturing.cell(column = columns_read[1], row = rows_read[0] + i).value
        if units == None:
            units = 0
        if units > 500:
            units = units/1000
        units_total = units/(1 - factor_perdida)
        
        #ahora recuperamos el codigo y precio del producto
        code = ws_read_manufacturing.cell(column = columns_read[0], row = rows_read[0] + i).value
        if i > 19:
            code = 51220110
        precio, quantity = getByCode(db, code)
        if quantity == 0 and code == 54220001:
            precio, quantity = 1.19, 1
        precio_royalty = precio * (1 + royalty_porcentaje) * (1 + seguros_porcentaje)
        precio_total = units_total * precio_royalty * euro #parece faltar algo como units_total/quantity
        
        return precio_total

        
# Ahora a los Sealings
def writeInfoSealings(db, ws_read_manufacturing, royalty_porcentaje, seguros_porcentaje, euro):
    #primero, calculamos la cantidad de hojas
    hojas = 0
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
        hojas = hojas + 1
        width = ws_read_manufacturing.cell(row = next_row, column = 4).value
        next_row = next_row + 1
        
    #ahora recuperamos el codigo y precio del producto
    for code in [54043034, 54043044, 54043064, 54043014, 54043024, 54043054, 54042014, 54042024, 54200204, 54200104, 11116200, 11116201]:
        if code in [54043034, 54043044, 54043064]:
            precio, quantity = getByCode(db, code)
            precio_royalty = precio * (1 + royalty_porcentaje) * (1 + seguros_porcentaje)
            precio_total = hojas * precio_royalty * euro /(1 - 0.03)#parece faltar algo como units_total/quantity
        
            #ahora escribimos los datos que necesitamos
            return precio_total
        

    
# Funcion auxiliar muy usada, bastante self-descriptive, auto-descriptiva        
def getByCode(db, code):
    with db_session:
        sku = db.Stock.get(id = code)
        if(sku != None):
            return sku.price
        return 0, 0