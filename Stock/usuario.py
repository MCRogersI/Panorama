from Stock.features import createSku, editSku, deleteSku, printStockConsole , makePurchases, editAllSkus, registerSKUFlux
from Stock.reports import createStockReport
from Projects.features import createStockShortage, deleteStockShortage, printStockShortages
import os
from pony.orm import *
from datetime import date


#Entiéndase SKU como el producto en si mismo (aunque en realidad significa el código del producto)
def stock_console(db, level):
    while True:
        opt = input("\n Marque una de las siguientes opciones:\n - 1: Agregar un SKU. \
                                                              \n - 2: Editar la información de SKU. \
                                                              \n - 3: Eliminar un SKU.\
                                                              \n - 4: Ver el Inventario. \
                                                              \n - 5: Para agregar ordenes de compra. \
                                                              \n - 6: Generar reporte global de stock. \
                                                              \n - 7: Manejar fechas de quiebre de stock. \
                                                              \n - 8: Para volver atrás.\
                                                              \n Ingrese la alternativa elegida: ")
        if (opt == '1'):
            try:
                id = input("\n Ingrese el ID del producto: ")
                try:
                    id = int(id)
                except:
                    raise ValueError('\n El ID del producto debe ser un número entero positivo.')
                with db_session:
                    if db.Stock.get(id = id) != None:
                        raise ValueError('\n El ID del producto ya existe.')

                name = input(" Ingrese el nombre del producto: ")
                if name == '':
                    raise ValueError('\n Debe ingresar un nombre para el producto.')
                price = input(" Ingrese el precio unitario del producto: ")
                try:
                    if float(price) < 0:
                        raise ValueError('\n El precio unitario del producto debe ser un número positivo.')
                except:
                    raise ValueError('\n El precio unitario del producto debe ser un número positivo.')
                critical_level = input(" Ingrese el nivel crítico del producto: ")
                try:
                    if float(critical_level) < 0:
                        raise ValueError('\n El nivel crítico del producto debe ser un número positivo.')
                except:
                    raise ValueError('\n El nivel crítico del producto debe ser un número positivo.')
                real_quantity = input(" Ingrese la cantidad en bodega del producto: ")
                try:
                    if float(real_quantity) < 0:
                        raise ValueError('\n La cantidad en bodega debe ser un número positivo.')
                except:
                    raise ValueError('\n La cantidad en bodega debe ser un número positivo \n')
                # waste_factor = input(' Ingrese el factor de pérdida del SKU: ')
                # if waste_factor !='':
                    # try:
                        # if float(waste_factor) <0:
                            # raise ValueError('\n El factor de pérdida debe ser un número positivo.')
                    # except:
                        # raise ValueError('\n El factor de pérdida debe ser un número positivo.')
                createSku(db,id, name, price, critical_level, real_quantity)
                input('\n SKU creado con éxito. Presione una tecla para continuar.')
            except ValueError as ve:
                print(ve)
                input(' Presione Enter para continuar.')
        if (opt == '2'):
            opt2 = input('\n Marque una de las siguientes opciones:\n - 1: Edición manual de un SKU. \
                                                                   \n - 2: Cargar adiciones de un archivo. \
                                                                   \n - 3: Ingresar flujo de SKU. \
                                                                   \n Ingrese la alternativa elegida: ')
            if(opt2 == '1'):
                try:
                    id = input("\n Ingrese el ID del producto: ")
                    try:
                        id = int(id)
                    except:
                        raise ValueError('\n El ID del producto debe ser un número entero positivo.')
                    with db_session:
                        if db.Stock.get(id = id) == None:
                            raise ValueError('\n El ID del producto ya existe.')
                    name = input(" Ingrese el nuevo nombre del producto, solo presione Enter si lo mantiene: ")
                    if name == '':
                        name = None
                    price = input(" Ingrese el nuevo precio unitario del producto, solo presione Enter si lo mantiene: ")
                    if price == '':
                        price = None
                    else:
                        try:
                            if float(price) < 0:
                                raise ValueError('\n El precio unitario del producto debe ser un número positivo.')
                        except:
                            raise ValueError('\n El precio unitario del producto debe ser un número positivo.')
                    critical_level = input(" Ingrese el nuevo nivel crítico del producto, solo presione Enter si lo mantiene: ")
                    if critical_level == '':
                        critical_level = None
                    else:
                        try:
                            if float(critical_level) < 0:
                                raise ValueError('\n El nivel crítico del producto debe ser un número positivo.')
                        except:
                            raise ValueError('\n El nivel crítico del producto debe ser un número positivo.')
                    real_quantity = input(" Ingrese la nueva cantidad en bodega del producto, solo presione Enter si es que desea ingresar este valor en el futuro: ")
                    if real_quantity == '':
                        real_quantity = None
                    else:
                        try:
                            if float(real_quantity) < 0:
                                raise ValueError('\n La cantidad en bodega debe ser un número positivo.')
                        except:
                            raise ValueError('\n La cantidad en bodega debe ser un número positivo.')
                    waste_factor = input(' Ingrese el nuevo factor de pérdida del producto, solo presione Enter si lo mantiene: ')
                    if waste_factor == '':
                        waste_factor = None
                    else:
                        try:
                            if float(waste_factor) < 0:
                                raise ValueError('\n El factor de pérdida debe ser un número positivo.')
                        except:
                            raise ValueError('\n El factor de pérdida debe ser un número positivo.')
                    editSku(db,id = id, name=name, price=price, critical_level=critical_level, real_quantity=real_quantity, waste_factor = waste_factor)
                    input(' Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
            if (opt2 == '2'):
                try:
                    file_name = input('\n Ingrese el nombre del archivo con los datos: ')
                    file_dir = file_name + ".xlsx"
                    if os.path.isfile(file_dir):
                        editAllSkus(db, file_name)
                        print('\n Datos cargados exitosamente. ')
                        input(' Presione Enter para continuar. ')
                    else:
                        raise ValueError('\n Archivo no encontrado.')
                except ValueError as ve:
                    print(ve)
            if (opt2 == '3'):
                try:
                    id = input(' Ingrese el ID del SKU que desea registrar: ')
                    try:
                        id = int(id)
                    except:
                        raise ValueError(' El id debe ser un número entero. ')
                    with db_session:
                        sku = db.Stock.get(id = id)
                        if sku == None:
                            raise ValueError( ' SKU no encontrado. ')
                    quantity = input( ' Ingrese la cantidad que entra al stock (si sale ingrese un número negativo): ')
                    try:
                        quantity = int(quantity)
                    except:
                        raise ValueError(' La cantidad de flujo debe ser un número entero. ')
                    if sku.real_quantity + quantity < 0:
                        raise ValueError(' El flujo saliente es mayor a la cantidad registrada actualmente. ingreso de flujo abortado. ' )
                    registerSKUFlux(db, id, quantity)
                    print(' Flujo registrado con éxito.')
                    input(' Presione Enter para continuar.')
                except ValueError as ve :
                    print(ve)
                    input(' Presione Enter para continuar. ')
        if (opt == '3'):
            try:
                id = input("\n Ingrese el ID del producto que desea eliminar: ")
                try:
                    int(id)
                except:
                    raise ValueError('\n No es un ID válido.')
                with db_session:
                    if db.Stock.get(id = id) == None:
                        raise ValueError('\n Producto inexistente.')
                deleteSku(db, id)
                print(' Producto eliminado con éxito. ')
                input( ' Presione Enter para continuar. ')
            except ValueError as ve:
                print(ve)
                input(' Presione Enter para continuar.')
        if (opt == '4'):
            printStockConsole(db)
            input(' Presione Enter para continuar.')
        if (opt =='5') :
            try:
                file_name = input(' Ingrese el nombre del archivo de la orden de compra: ')
                file_dir = file_name + ".xlsx"
                if os.path.isfile(file_dir):
                    makePurchases(db, file_name)
                    print('\n Orden de compra ingresada exitosamente. ')
                    input(' Presione Enter para continuar: ')
                else:
                    raise ValueError('\n Archivo no encontrado.')
            except ValueError as ve:
                print(ve)
                input(' Presione Enter para continuar: ')
        if opt =='6' and level ==1:
            createStockReport(db)
            input('\n Informe creado con éxito. Presione Enter para continuar.')
        
        if(opt == '7'):
            if(level == 1):
                opt_stock_shortages = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ingresar fechas de quiebre de stock. \
                                                                                           \n - 2: Si desea eliminar fechas de quiebre de stock. \
                                                                                           \n - 3: Si desea ver la lista actual de fechas de quiebre de stock. \
                                                                                           \n Ingrese la alternativa elegida: ")

                if opt_stock_shortages == '1':
                    try:
                        initial_year = input("\n Ingrese el año en que comienza el quiebre de stock: ")
                        initial_month = input(" Ingrese el mes en que comienza el quiebre de stock: ")
                        initial_day = input(" Ingrese el día en que comienza el quiebre de stock: ")
                        try:
                            date(int(initial_year),int(initial_month),int(initial_day))
                        except:
                            raise ValueError('\n Fecha de inicio inválida.')
                        end_year = input(" Ingrese el año en que termina el quiebre de stock: ")
                        end_month = input(" Ingrese el mes en que termina el quiebre de stock: ")
                        end_day = input(" Ingrese el día en que termina el quiebre de stock: ")
                        try:
                            date(int(end_year),int(end_month),int(end_day))
                        except:
                            raise ValueError('\n Fecha de término inválida.')
                        createStockShortage(db, 4, initial_year, initial_month, initial_day, end_year, end_month, end_day)
                        input('\n Fechas de quiebre de stock ingresadas. Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Precione Enter para continuar.')
                elif opt_stock_shortages == '2':
                    id_stock_shortage = input("\n Ingrese el ID del quiebre de stock que quiere eliminar: ")
                    try:
                        deleteStockShortage(db, id_stock_shortage)
                    except:
                        print('\n No existe ese quiebre de stock.')
                        input(' Presione Enter para continuar.')
                elif opt_stock_shortages == '3':
                    printStockShortages(db)
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        
        if (opt == '8'):
            break