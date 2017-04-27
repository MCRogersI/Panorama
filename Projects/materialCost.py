from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, colors
from math import ceil
from copy import copy


######################################################################################
# Muy simple, se encarga de llamar a todas las funciones que hacen de verdad la pega #
######################################################################################

def computation(wb_read, wb_written):
    ws_written = wb_written.create_sheet("Costo Estandar Materias Primas")
    ws_read_manufacturing = wb_read["Manufacturing"]
    wb_example = load_workbook("PPta Costa Cachagua Etapa 3_V1_09.03.2017.xlsx", data_only=True)
    
    #necesitamos algunos parametros basicos para costear
    royalty_porcentaje = 0.175
    seguros_porcentaje = 0.06
    euro = 712.9
    
    #primero damos formato a las celdas, por ahora, en particular, sobre todo el color de fondo
    ws_sheet = wb_written["Sheet"]
    formatCells(ws_written, ws_sheet, wb_example)
    
    #ahora partimos escribiendo en el archivo
    ws_summary = wb_written["Resumen"]
    writeTitlesSummary(ws_summary, wb_example)
    writeTitlesGlass(ws_written)
    writeTitlesProfilesComponents(ws_written, wb_example)
    
    #ahora seguimos escribiendo en el archivo, donde llamamos varias funciones mas
    writeInfoGlass(ws_read_manufacturing, ws_written)
    writeInfoProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro)
    writeInfoComponents(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro)
    writeInfoSealings(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro)

    #terminamos con la escritura del archivo Resumen
    writeInfoSummary(ws_summary, ws_written, wb_written["Costo Estandar Fabricacion"], wb_written["Costo Estandar Instalacion"])
    
    
    
    
    
###################################################################################################
# Para dar el formato a las celdas de la parte de Glass, y para cambiar el tamano de las columnas #
###################################################################################################

def formatCells(ws_written, ws_sheet, wb_example):
    #aplicamos ciertos cambios al ancho y formato de algunas columnas y celdas en la Hoja de Costeo de Materias Primas
    ws_read = wb_example["Edif A_Hoja Corte"]
    columns_cachagua = ["B", "C", "D", "E", "F", "G", "H", "I"]
    columns = ["B", "C", "D", "E", "F", "G", "H", "I"]
    for i in range(0, len(columns)):
        new_width = ws_read.column_dimensions[columns_cachagua[i]].width
        if new_width != None:
            ws_written.column_dimensions[columns[i]].width = new_width
            
    #aplicamos ciertos cambios al ancho y formato de algunas columnas y celdas en la Resumen
    ws_sheet.title = "Resumen"
    columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    widths = [10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 22, 25]
    for i in range(0, len(columns)):
        ws_sheet.column_dimensions[columns[i]].width = widths[i]
    
    #definimos los colores de fondo que vamos a usar
    fondo_amarillo = PatternFill(start_color = colors.YELLOW, end_color = colors.YELLOW, fill_type='solid')
    
    #asignamos el formato a las celdas donde va Glass
    rows = [2, 3, 4, 5, 6]
    num_rows = len(rows)
    for i in range(0, num_rows):
        ws_written.cell(row = rows[i], column = 2).fill = fondo_amarillo
        ws_written.cell(row = rows[i], column = 3).fill = fondo_amarillo
    ws_written.cell(row = rows[-1], column = 2).font = Font(bold=True)
    ws_written.cell(row = rows[-1], column = 3).font = Font(bold=True)
    

   

   
##############################################################################################
# Aca empezamos a escribir los titulos que van si o si, no dependen del proyecto en cuestion #
##############################################################################################

# Partimos por las celdas de la hoja Resumen
def writeTitlesSummary(ws_summary, wb_example):
    ws_read = wb_example["Resumen"]
    
    rows_cachagua = [1, 2]
    columns_cachagua = [1, 12]
    writeTitleProfileComponent(ws_summary, ws_read, rows_cachagua, columns_cachagua, rows_cachagua, columns_cachagua)
    formatProfileComponent(ws_summary, ws_read, rows_cachagua, columns_cachagua, rows_cachagua, columns_cachagua)

# Seguimos por los Cristales
def writeTitlesGlass(ws_written):
    #partimos por los titulos correspondientes a Glass
    rows = [2, 3, 4, 5, 6]
    columns = [2, 2, 2, 2, 2]
    texts = ["M2", "ML", "CoSTo CRISTAL ( CLP/M2 )", "FACToR DE PERDIDA", "CoSTo ESTANDAR CRISTALES CTTo"]
    for i in range(0, len(rows)):
        ws_written.cell(row = rows[i], column = columns[i], value = texts[i])
    
# Despues, seguimos con los distintos Profiles y Components, que se leen del archivo de ejemplo
def writeTitlesProfilesComponents(ws_written, wb_example):
    ws_read = wb_example["Edif A_Hoja Corte"]
    
    #partimos con los Perfiles (todos)
    rows_cachagua = [205, 211]
    columns_cachagua = [2, 9]
    rows = [10, 16]
    columns = [2, 9]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    
    #seguimos por Components to Glass Panes
    rows_cachagua = [219, 228]
    columns_cachagua = [2, 9]
    rows = [21, 30]
    columns = [2, 9]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    
    #seguimos con Components to component box or profiles
    rows_cachagua = [232, 242]
    columns_cachagua = [2, 9]
    rows = [35, 45]
    columns = [2, 9]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    #arreglamos un pequeno corrimiento que hay
    ws_written.cell(row = 46, column = 2, value = ws_written.cell(row = 45, column = 2).value)
    ws_written.cell(row = 45, column = 2, value = ws_written.cell(row = 44, column = 2).value)
    ws_written.cell(row = 44, column = 2, value = ' ')
    
    #seguimos con Components to component box
    rows_cachagua = [248, 273]
    columns_cachagua = [2, 9]
    rows = [50, 75]
    columns = [2, 9]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)

    #despues, seguimos con los Sealings
    rows_cachagua = [176, 188]
    columns_cachagua = [1, 6]
    rows = [81, 93]
    columns = [1, 6]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    #hay que usar un truco para que quede bien
    rows_cachagua = [174, 175]
    columns_cachagua = [1, 6]
    rows = [79, 80]
    columns = [1, 6]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    #hay que usar un truco para que quede bien
    rows_cachagua = [177, 188]
    columns_cachagua = [2, 2]
    rows = [82, 93]
    columns = [2, 2]
    writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)
    formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns)

    
# Esta funcion es auxiliar, es para escribir los titulos
def writeTitleProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns):
    for i in range(0, rows_cachagua[1] - rows_cachagua[0] + 1):
        cell = ws_written.cell(column = columns[0], row = rows[0] + i, value = \
                                    ws_read.cell(column = columns_cachagua[0], row = rows_cachagua[0] + i).value)
    for j in range(0, columns_cachagua[1] - columns_cachagua[0] + 1):
        cell_1 = ws_written.cell(column = columns[0] + j, row = rows[0], value = \
                                    ws_read.cell(column = columns_cachagua[0] + j, row = rows_cachagua[0]).value)

# Esta funcion es auxiliar, es para dar el formato a las celdas
def formatProfileComponent(ws_written, ws_read, rows_cachagua, columns_cachagua, rows, columns):
    for i in range(0, rows_cachagua[1] - rows_cachagua[0] + 1):
        for j in range(0, columns_cachagua[1] - columns_cachagua[0] + 1):
            cell = ws_written.cell(column = columns[0] + j, row = rows[0] + i)
            cell_read = ws_read.cell(column = columns_cachagua[0] + j, row = rows_cachagua[0] + i)
            #copiamos el color de fondo de la celda de CostaCachagua a la celda del nuevo archivo
            color_read = cell_read.fill.start_color
            if color_read.rgb != '00000000':
                pattern = PatternFill(start_color = color_read, fill_type = 'solid')
                cell.fill = pattern
            #copiamos tambien el formato y los bordes
            cell.font = copy(cell_read.font)
            cell.border = copy(cell_read.border)
    

    
    
##############################################################################
# Aca empezamos a escribir la informacion relacionada al proyecto especifico #
##############################################################################

# Partimos por los Glass
def writeInfoGlass(ws_read_manufacturing, ws_written):
    #necesitamos algunos parametros, en este caso, los tomamos del archivo de ejemplo y del Pedido de Cristales que mando al mail
    costo_cristal_por_m2 = 30000 #para este tipo de cristales, de espesor 10
    factor_perdida = 0.05

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
    
    #escribimos finalmente la informacion obtenida
    rows = [2, 3, 4, 5, 6]
    columns = [3, 3, 3, 3, 3]
    texts = [metros_cuadrados, metros_lineales, costo_cristal_por_m2, factor_perdida, costo_estandar_cristales]
    for i in range(0, len(rows)):
        ws_written.cell(row = rows[i], column = columns[i], value = texts[i])
    
 
# Pasamos a los Profiles
def writeInfoProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro):
    #primero, para el Perfil Superior
    factor_perdida = 0.14
    length_coords = [48, 2]
    code_coords = [46, 2]
    table_row = 11
    writeProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, factor_perdida, length_coords, code_coords, table_row)
    
    #ahora, el Perfil Inferior
    factor_perdida = 0.14
    length_coords = [60, 2]
    code_coords = [58, 2]
    table_row = 12
    writeProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, factor_perdida, length_coords, code_coords, table_row)
    
    #por ultimo, el Perfil Telescopico
    factor_perdida = 0.14
    length_coords = [72, 2]
    code_coords = [70, 2]
    table_row = 13
    writeProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, factor_perdida, length_coords, code_coords, table_row)
    
    #ahora, los Glassing Beads
    factor_perdida = 0.14
    length_coords = [47, 13]
    code_coords = [78, 14]
    table_row = 14
    writeProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
                        factor_perdida, length_coords, code_coords, table_row, True)
 
    #ahora, los Glassing Beads Covers
    factor_perdida = 0.14
    length_coords = [47, 13]
    code_coords = [79, 14]
    table_row = 15
    writeProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
                        factor_perdida, length_coords, code_coords, table_row, True)
  
 
def writeProfile(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
                    factor_perdida, length_coords, code_coords, table_row, bead = False):
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
    precio, quantity = getByCode(code)
    if quantity == 0 and bead:
        precio, quantity = getByCode(54220002)
    
    #ahora, el precio con el royalty y todo
    precio_royalty = precio * (1 + royalty_porcentaje) * (1 + seguros_porcentaje)
    
    #calculamos el ultimo dato necesario
    costo_estandar = metros_lineales_totales*precio_royalty*euro
    
    #escribimos finalmente la informacion obtenida
    columns = [3, 4, 5, 6, 7, 8, 9]
    texts = [metros_lineales, factor_perdida, metros_lineales_totales, code, precio, \
                precio_royalty, costo_estandar]
    for i in range(0, len(columns)):
        ws_written.cell(row = table_row, column = columns[i], value = texts[i])
        
        
# Ahora a los Components
def writeInfoComponents(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro):
    #se considera perdida constante de 3%, segun archivo de CostaCachagua
    factor_perdida = 0.03

    #partimos por Components to Glass Panes
    rows_read = [126, 134]
    columns_read = [1, 6]
    rows = [22, 30]
    column = 2
    writeComponent(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
                        factor_perdida, rows_read, columns_read, rows, column)
    
    #seguimos con Components to component box or profiles
    rows_read = [140, 150]
    columns_read = [1, 6]
    rows = [36, 45]
    column = 2
    writeComponent(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
                        factor_perdida, rows_read, columns_read, rows, column)
    
    # partimos por Components to Glass Panes
    rows_read = [126, 148]
    columns_read = [8, 15]
    rows = [51, 73]
    column = 2
    writeComponent(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
                        factor_perdida, rows_read, columns_read, rows, column)


def writeComponent(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro, \
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
        precio, quantity = getByCode(code)
        if quantity == 0 and code == 54220001:
            precio, quantity = 1.19, 1
        precio_royalty = precio * (1 + royalty_porcentaje) * (1 + seguros_porcentaje)
        precio_total = units_total * precio_royalty * euro #parece faltar algo como units_total/quantity
        
        #ahora escribimos los datos que necesitamos
        ws_written.cell(row = rows[0] + i, column = column + 1, value = units)
        ws_written.cell(row = rows[0] + i, column = column + 2, value = factor_perdida)
        ws_written.cell(row = rows[0] + i, column = column + 3, value = units_total)
        ws_written.cell(row = rows[0] + i, column = column + 4, value = code)
        #ojo que el siguiente valor puede dar 0 si es que el item no esta en la lista
        ws_written.cell(row = rows[0] + i, column = column + 5, value = precio)
        ws_written.cell(row = rows[0] + i, column = column + 6, value = precio_royalty)
        ws_written.cell(row = rows[0] + i, column = column + 7, value = precio_total)

        
# Ahora a los Sealings
def writeInfoSealings(ws_read_manufacturing, ws_written, royalty_porcentaje, seguros_porcentaje, euro):
    #primero, calculamos la cantidad de hojas
    hojas = 0
    width = ws_read_manufacturing.cell(row = 7, column = 4).value
    next_row = 8
    while(width > 0): #float(width.replace(',', '.')) en caso que width sea leido como string
        hojas = hojas + 1
        width = ws_read_manufacturing.cell(row = next_row, column = 4).value
        next_row = next_row + 1
        
    #ahora recuperamos el codigo y precio del producto
    for r in range(82, 94):
        code = ws_written.cell(column = 1, row = r).value
        if code in [54043034, 54043044, 54043064]:
            precio, quantity = getByCode(code)
            precio_royalty = precio * (1 + royalty_porcentaje) * (1 + seguros_porcentaje)
            precio_total = hojas * precio_royalty * euro /(1 - 0.03)#parece faltar algo como units_total/quantity
        
            #ahora escribimos los datos que necesitamos
            ws_written.cell(row = r, column = 3, value = hojas)
            ws_written.cell(row = r, column = 4, value = precio)
            ws_written.cell(row = r, column = 5, value = precio_royalty)
            ws_written.cell(row = r, column = 6, value = precio_total)
        

# Terminamos con el Resumen
def writeInfoSummary(ws_summary, ws_written, ws_fabrication, ws_instalation):
    #escribimos primero lo relativo a Glass
    ws_summary.cell(row = 2, column = 2, value = ws_written.cell(row = 3, column = 3).value)
    ws_summary.cell(row = 2, column = 3, value = ws_written.cell(row = 2, column = 3).value)
    ws_summary.cell(row = 2, column = 4, value = ws_written.cell(row = 6, column = 3).value)
    
    #ahora, lo relativo a Profiles
    profiles_cost = 0
    for r in range(11, 16):
        profiles_cost = profiles_cost + ws_written.cell(row = r, column = 9).value
    ws_summary.cell(row = 2, column = 5, value = profiles_cost)
    ws_written.cell(row = 16, column = 9, value = profiles_cost)
    
    #ahora, lo relativo a Components 
    components_cost = 0
    for r in range(22, 31):
        components_cost = components_cost + ws_written.cell(row = r, column = 9).value
    ws_summary.cell(row = 2, column = 6, value = components_cost)
    ws_written.cell(row = 31, column = 9, value = components_cost)
    
    components_cost = 0
    for r in range(36, 47):
        components_cost = components_cost + ws_written.cell(row = r, column = 9).value
    ws_summary.cell(row = 2, column = 6).value = ws_summary.cell(row = 2, column = 6).value + components_cost
    ws_written.cell(row = 47, column = 9, value = components_cost)
    
    components_cost = 0
    for r in range(51, 74):
        if ws_written.cell(row = r, column = 9).value != None:
            components_cost = components_cost + ws_written.cell(row = r, column = 9).value
    ws_summary.cell(row = 2, column = 6).value = ws_summary.cell(row = 2, column = 6).value + components_cost
    ws_written.cell(row = 74, column = 9, value = components_cost)
    
    #ahora, lo relativo a Sealings
    sealings_cost = 0
    for r in range(82, 94):
        if ws_written.cell(row = r, column = 6).value != None:
            sealings_cost = sealings_cost + ws_written.cell(row = r, column = 6).value
    ws_summary.cell(row = 2, column = 6).value = ws_summary.cell(row = 2, column = 6).value + sealings_cost
    ws_written.cell(row = 94, column = 6, value = sealings_cost)
    
    #ahora, lo relativo a Fabricacion e Instalacion
    ws_summary.cell(row = 2, column = 7, value = ws_fabrication.cell(row = 14, column = 3).value)
    ws_summary.cell(row = 2, column = 8, value = ws_instalation.cell(row = 17, column = 3).value)
    
    #ahora, el costo total y los asociados
    total_cost = 0
    for c in range(2, 9):
        total_cost = total_cost + ws_summary.cell(row = 2, column = c).value
    ws_summary.cell(row = 2, column = 9, value = total_cost)
    
    price = total_cost/0.45
    ws_summary.cell(row = 2, column = 11, value = price)
    ws_summary.cell(row = 2, column = 12, value = price + price*0.05/0.6)
    
    
    
    
    
# Funcion auxiliar muy usada, bastante self-descriptive, auto-descriptiva        
def getByCode(code):
    wb = load_workbook("PPta Costa Cachagua Etapa 3_V1_09.03.2017.xlsx", data_only=True)
    ws = wb["Hoja2"]
    next_row = 13
    code_read = ws.cell(row = next_row, column = 2).value
    while(code_read != None):
        if str(code_read) == str(code):
            return ws.cell(row = next_row, column = 5).value, ws.cell(row = next_row, column = 7).value
        next_row = next_row + 1
        code_read = ws.cell(row = next_row, column = 2).value
    return 0, 0