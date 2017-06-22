from pony.orm import *
from math import ceil
from Planning.features import getAveragePerformance

def computation(db, wb_read, project_cost, tarifa_viaticos, tarifa_movilizacion, numero_instaladores, costo_flete, tipo_instalador): #en este caso, 1 significa "interno", 0 significa "externo"
    ws_read_measures = wb_read["Measures"]
    ws_read_manufacturing = wb_read["Manufacturing"]
    
    #parametros fijos, tomados de los parametros guardados en la base de datos
    with db_session:
        from Projects.costs import getParameter
        rendimiento_diario = getAveragePerformance(db, 4)
        warning = ' Aviso: el factor de errores de instalacion no se encuentra registrada en la base de datos. Se considerara como 0.'
        factor_errores_instalacion = getParameter(db.Operating_Parameters, "Factor de errores de instalacion", pony.orm.core.ObjectNotFound, warning)
        
        warning = ' Aviso: la tarifa de instalacion de empleados internos no se encuentra registrado en la base de datos. Se considerara como 0.'
        tarifa_instalacion_interna = getParameter(db.Operating_Parameters, "Tarifa instalacion interna", pony.orm.core.ObjectNotFound, warning)
        
        warning = ' Aviso: la tarifa de instalacion de empleados externos no se encuentra registrada en la base de datos. Se considerara como 0.'
        tarifa_instalacion_externa = getParameter(db.Operating_Parameters, "Tarifa instalacion externa", pony.orm.core.ObjectNotFound, warning)
    if tipo_instalador == 1:
        tarifa_instalacion = tarifa_instalacion_interna
    else:
        tarifa_instalacion = tarifa_instalacion_externa
    
    #parametros que deben obtenerse del archivo en cuestion, si el formato es suficientemente estandar
    comuna = ws_read_measures.cell(row = 7, column = 15).value
    metros_lineales = linearMeters(ws_read_manufacturing)
    
    #ahora terminamos de escribir en el archivo
    writeInfo(db, project_cost, metros_lineales, numero_instaladores, rendimiento_diario, factor_errores_instalacion, \
                costo_flete, tarifa_viaticos, tarifa_movilizacion, tarifa_instalacion)
    
    
    
def linearMeters(ws_read_manufacturing):
    metros_lineales = 0
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    
    #si el formato está mal (por ejemplo un width es una palabra) entonces retornamos 0, y avisamos de un posible error
    try:
        while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
            metros_lineales = metros_lineales + width/1000
            width = ws_read_manufacturing.cell(row = next_row, column = 4).value
            next_row = next_row + 1
    except TypeError:
        print(' Error: hay un problema de formato con la hoja de corte. El calculo de costos continuara, pero se consideraran los metros lineales como 0.')
        return 0
        
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
        project_cost.standard_cost_installation = instalacion_despues_fallas