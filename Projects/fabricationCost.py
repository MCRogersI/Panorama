from openpyxl.styles import Font, PatternFill, colors
from math import ceil

def computation(wb_read, wb_written):
    ws_written = wb_written.create_sheet("Costo Estandar Fabricacion")
    ws_read_measures = wb_read["Measures"]
    ws_read_manufacturing = wb_read["Manufacturing"]
    
    #parametros fijos, por ahora uso los que venian en el archivo de ejemplo
    remuneraciones_fijas = 2400000
    remuneraciones_variables = 122500
    porcentaje_venta = 0.02
    arriendo_fabrica = 1500000
    depreciacion = 500000
    energia_agua_otros = 400000
    
    #datos que son a nivel empresa, no a nivel proyecto, aca hay que darlos
    metros_lineales_mes = 240
    venta_neta_mensual = 80000000
    
    #parametros que deben obtenerse del archivo en cuestion, si el formato es suficientemente estandar
    metros_lineales = linearMeters(ws_read_manufacturing)
    
    #ahora partimos escribiendo en el archivo
    writeTitles(ws_written)
    
    #ahora terminamos de escribir en el archivo
    writeInfo(ws_written, metros_lineales, metros_lineales_mes, remuneraciones_fijas, remuneraciones_variables, \
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

    
    
def writeTitles(ws_written):
    #aplicamos ciertos cambios al ancho y formato de algunas columnas y celdas
    ws_written.column_dimensions["B"].width = 45
    fondo_verde = PatternFill(start_color = colors.DARKGREEN, end_color = colors.DARKGREEN, fill_type='solid')
    ws_written['B10'].fill = fondo_verde
    ws_written['B14'].fill = fondo_verde
    
    #escribimos efectivamente los titulos de la columna
    rows = [1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14]
    columns = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    texts = ["ML CoNTRATo", "ML VENDIDoS AL MES", "REMUNERACIoNES FIJAS FABRICA", "REMUNERACIoNES VARIABLES FABRICA", \
                "MATERIALES DE FABRICACIoN", "ARRIENDo DE FABRICA", "DEPRECIACIoN EQUIPoS Y HERRAMIENTAS", \
                "ENERGIA, LUZ, AGUA, oTRoS", "ToTAL CoSToS FABRICACIoN MENSUALES", "CoSTo FABRICACIoN/ ML VENDIDo MENSUAL", \
                "CoSTo ESTANDAR FABRICACIoN CoNTRATo"]
    for i in range(0, len(rows)):
        ws_written.cell(row = rows[i], column = columns[i], value = texts[i])
        
        
        
def writeInfo(ws_written, metros_lineales, metros_lineales_mes, remuneraciones_fijas, remuneraciones_variables, \
                porcentaje_venta, venta_neta_mensual, arriendo_fabrica, depreciacion, energia_agua_otros):
    #aplicamos ciertos cambios al ancho y formato de algunas columnas y celdas
    ws_written.column_dimensions["C"].width = 14
    fondo_verde = PatternFill(start_color = colors.DARKGREEN, end_color = colors.DARKGREEN, fill_type='solid')
    ws_written['C10'].fill = fondo_verde
    ws_written['C14'].fill = fondo_verde
    
    #conseguimos algunos de los datos necesarios para escribir la informacion, partiendo por el los "materiales de fabricacion"
    materiales_fabricacion = porcentaje_venta * venta_neta_mensual
    
    #seguimos con el total de costos de fabricacion (entre todos los proyectos)
    total_costos_fabricacion = remuneraciones_fijas + remuneraciones_variables + materiales_fabricacion + \
                                    arriendo_fabrica + depreciacion + energia_agua_otros
                                    
    #seguimos con el costo de fabricacion por emtro lineal vendido
    costo_fabricacion_por_ml = total_costos_fabricacion / metros_lineales_mes
    
    #terminamos con el costo estandar de fabricacion
    costo_estandar_fabricacion = costo_fabricacion_por_ml * metros_lineales
    
    #escribimos efectivamente la informacion de la columna
    rows = [1, 2, 4, 5, 6, 7, 8, 9, 10, 12, 14]
    columns = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    texts = [metros_lineales, metros_lineales_mes, remuneraciones_fijas, remuneraciones_variables, materiales_fabricacion, \
                arriendo_fabrica, depreciacion, energia_agua_otros, total_costos_fabricacion, costo_fabricacion_por_ml, \
                costo_estandar_fabricacion]
    for i in range(0, len(rows)):
        ws_written.cell(row = rows[i], column = columns[i], value = texts[i])