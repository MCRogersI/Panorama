from pony.orm import *
from math import ceil
from Planning.features import getAveragePerformance

def computation(db, wb_read, project_cost, tarifa_viaticos, tarifa_movilizacion, numero_instaladores, costo_flete, tipo_instalador): #en este caso, 1 significa "interno", 0 significa "externo"
    ws_read_measures = wb_read["Measures"]
    ws_read_manufacturing = wb_read["Manufacturing"]
    
    #parametros fijos, tomados de los parametros guardados en la base de datos
    with db_session:
        rendimiento_diario = getAveragePerformance(db, 4)
        factor_errores_instalacion = db.Operating_Costs.get(name = "Factor de errores de instalacion").value
        tarifa_instalacion_interna = db.Operating_Costs.get(name = "Tarifa instalacion interna").value
        tarifa_instalacion_externa = db.Operating_Costs.get(name = "Tarifa instalacion externa").value
    if tipo_instalador == 1:
        tarifa_instalacion = tarifa_instalacion_interna
    else:
        tarifa_instalacion = tarifa_instalacion_externa
    
    #parametros que deben obtenerse del archivo en cuestion, si el formato es suficientemente estandar
    comuna = ws_read_measures.cell(row = 7, column = 15).value
    metros_lineales = linearMeters(ws_read_manufacturing)
    
    #ahora terminamos de escribir en el archivo
    writeInfo(db, project_cost, comuna, metros_lineales, numero_instaladores, rendimiento_diario, tipo_instalador, factor_errores_instalacion, \
                costo_flete, tarifa_viaticos, tarifa_movilizacion, tarifa_instalacion)
    
    
    
def linearMeters(ws_read_manufacturing):
    metros_lineales = 0
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
        metros_lineales = metros_lineales + width/1000
        width = ws_read_manufacturing.cell(row = next_row, column = 4).value
        next_row = next_row + 1
    return metros_lineales

        
        
def writeInfo(db, project_cost, metros_lineales, numero_instaladores, rendimiento_diario, factor_errores_instalacion, \
                   costo_flete, tarifa_viaticos, tarifa_movilizacion, tarifa_instalacion):

    #seguimos con el numero de dias necesarios para la instalacion
    tiempo_estimado = ceil(metros_lineales/(numero_instaladores * rendimiento_diario))
    
    #seguimos con el costo de viaticos, aca tengo dudas importantes de si se calcula asi o no
    viatico = tarifa_viaticos * numero_instaladores + tarifa_movilizacion * numero_instaladores * tiempo_estimado
    
    #seguimos con el costo de instalacion
    instalacion = tarifa_instalacion * metros_lineales
    
    #seguimos con el costo de instalacion antes de fallas
    instalacion_antes_fallas = costo_flete + viatico + instalacion
    
    #terminamos con instalacion despues de fallas
    instalacion_despues_fallas = instalacion_antes_fallas/(1 - factor_errores_instalacion)
    
    #escribimos efectivamente el costo de instalacion en la base de datos
    with db_session:
        db.project_cost.standard_cost_installation = instalacion_despues_fallas