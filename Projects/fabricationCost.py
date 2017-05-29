from pony.orm import *
from openpyxl.styles import Font, PatternFill, colors
from math import ceil

def computation(db, wb_read, project_cost):
    ws_read_measures = wb_read["Measures"]
    ws_read_manufacturing = wb_read["Manufacturing"]
    
    #parametros fijos, se toman de la base de datos
    with db_session:
        remuneraciones_fijas = db.Operating_Parameters.get(name = "Remuneraciones fijas fabrica").value
        remuneraciones_variables = db.Operating_Parameters.get(name = "Remuneraciones variables fabrica").value
        porcentaje_venta = db.Operating_Parameters.get(name = "Porcentaje de la venta correspondiente a materiales de fabricacion").value
        #lo pasamos de porcentaje a fraccion
        porcentaje_venta = porcentaje_venta/100.0
        
        arriendo_fabrica = db.Operating_Parameters.get(name = "Arriendo de fabrica").value
        depreciacion = db.Operating_Parameters.get(name = "Depreciacion equipos y herramientas").value
        energia_agua_otros = db.Operating_Parameters.get(name = "Energia, luz, agua, otros").value
        metros_lineales_mes = db.Operating_Parameters.get(name = "Metros lineales vendidos en el mes").value
        venta_neta_mensual = db.Operating_Parameters.get(name = "Venta (neta de IVA) mensual").value
    
    #parametros que deben obtenerse del archivo en cuestion, si el formato es suficientemente estandar
    metros_lineales = linearMeters(ws_read_manufacturing)
    
    #ahora terminamos de escribir en el archivo
    writeInfo(db, project_cost, metros_lineales, metros_lineales_mes, remuneraciones_fijas, remuneraciones_variables, \
                porcentaje_venta, venta_neta_mensual, arriendo_fabrica, depreciacion, energia_agua_otros)
    
    
    
def linearMeters(ws_read_manufacturing):
    metros_lineales = 0
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
        metros_lineales = metros_lineales + width/1000
        width = ws_read_manufacturing.cell(row = next_row, column = 4).value
        next_row = next_row + 1
    return metros_lineales
        
        
        
def writeInfo(db, project_cost, metros_lineales, metros_lineales_mes, remuneraciones_fijas, remuneraciones_variables, \
                porcentaje_venta, venta_neta_mensual, arriendo_fabrica, depreciacion, energia_agua_otros):
    
    #conseguimos algunos de los datos necesarios para escribir la informacion, partiendo por el los "materiales de fabricacion"
    materiales_fabricacion = porcentaje_venta * venta_neta_mensual
    
    #seguimos con el total de costos de fabricacion (entre todos los proyectos)
    total_costos_fabricacion = remuneraciones_fijas + remuneraciones_variables + materiales_fabricacion + \
                                    arriendo_fabrica + depreciacion + energia_agua_otros
                                    
    #seguimos con el costo de fabricacion por emtro lineal vendido
    costo_fabricacion_por_ml = total_costos_fabricacion / metros_lineales_mes
    
    #terminamos con el costo estandar de fabricacion
    costo_estandar_fabricacion = costo_fabricacion_por_ml * metros_lineales
    
    #escribimos efectivamente el costo de fabricacion en la base de datos
    with db_session:
        project_cost.standard_cost_fabrication = costo_estandar_fabricacion