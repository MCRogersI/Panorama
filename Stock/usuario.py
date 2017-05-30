from Stock.features import createSku, editSku, deleteSku, printStockConsole , makePurchases, editAllSkus
from Stock.reports import createStockReport
import os
from pony.orm import *


#Entiéndase SKU como el producto en si mismo (aunque en realidad significa el código del producto)
def stock_console(db, level):
    while True:
        opt = input("\n Marque una de las siguientes opciones:\n - 1: Agregar un SKU. \
                                                              \n - 2: Editar la información de SKU. \
                                                              \n - 3: Eliminar un SKU.\
                                                              \n - 4: Ver el Inventario. \
                                                              \n - 5: Para agregar ordenes de compra. \
                                                              \n - 6: Generar reporte global de stock. \
                                                              \n - 7: Para volver atrás.\
                                                              \n Ingrese la alternativa elegida: ")
        if (opt == '1'):
            try:
                id = input("\n Ingrese el ID del producto: ")
                try:
                    if int(id) < 0:
                        raise ValueError('\n El ID del producto debe ser un número entero positivo \n')
                except:
                    raise ValueError('\n El ID del producto debe ser un número entero positivo \n')
                name = input(" Ingrese el nombre del producto: ")
                if name == '':
                    raise ValueError('\n Debe ingresar un nombre para el producto \n')
                price = input(" Ingrese el precio unitario del producto: ")
                try:
                    if float(price) < 0:
                        raise ValueError('\n El precio unitario del producto debe ser un número positivo \n')
                except:
                    raise ValueError('\n El precio unitario del producto debe ser un número positivo \n')
                critical_level = input(" Ingrese el nivel crítico del producto: ")
                try:
                    if float(critical_level) < 0:
                        raise ValueError('\n El nivel crítico del producto debe ser un número positivo \n')
                except:
                    raise ValueError('\n El nivel crítico del producto debe ser un número positivo \n')
                real_quantity = input(" Ingrese la cantidad en bodega del producto: ")
                try:
                    if float(real_quantity) < 0:
                        raise ValueError('\n La cantidad en bodega debe ser un número positivo \n')
                except:
                    raise ValueError('\n La cantidad en bodega debe ser un número positivo \n')
                waste_factor = input(' Ingrese el factor de pérdida del SKU: ')
                if waste_factor !='':
                    try:
                        if float(waste_factor) <0:
                            raise ValueError('\n El factor de pérdida debe ser un número positivo \n')
                    except:
                        raise ValueError('\n El factor de pérdida debe ser un número positivo \n')
                createSku(db,id, name, price, critical_level, real_quantity , waste_factor)
                input('\n SKU creado con éxito. Presione una tecla para continuar. \n')
            except ValueError as ve:
                print(ve)
                input('\n Presione una tecla para continuar \n')
        if (opt == '2'):
            opt2 = input('\n Marque una de las siguientes opciones:\n - 1: Edición manual de un SKU. \
                                                                   \n - 2: Cargar adiciones de un archivo. \
                                                                   \n Ingrese la alternativa elegida: ')
            if(opt2 == '1'):
                try:
                    id = input("\n Ingrese el id del producto: ")
                    name = input("\n Ingrese el nuevo nombre del producto, solo presione enter si lo mantiene: ")
                    if name == '':
                        name = None
                    price = input(" Ingrese el nuevo precio unitario del producto, solo presione enter si lo mantiene: ")
                    if price == '':
                        price = None
                    else:
                        try:
                            if float(price) < 0:
                                raise ValueError('\n El precio unitario del producto debe ser un número positivo \n')
                        except:
                            raise ValueError('\n El precio unitario del producto debe ser un número positivo \n')
                    critical_level = input(" Ingrese el nuevo nivel crítico del producto, solo presione enter si lo mantiene: ")
                    if critical_level == '':
                        critical_level = None
                    else:
                        try:
                            if float(critical_level) < 0:
                                raise ValueError('\n El nivel crítico del producto debe ser un número positivo \n')
                        except:
                            raise ValueError('\n El nivel crítico del producto debe ser un número positivo \n')
                    real_quantity = input(" Ingrese la nueva cantidad en bodega del producto, solo presione enter si es que desea ingresar este valor en el futuro: ")
                    if real_quantity == '':
                        real_quantity = None
                    else:
                        try:
                            if float(real_quantity) < 0:
                                raise ValueError('\n La cantidad en bodega debe ser un número positivo \n')
                        except:
                            raise ValueError('\n La cantidad en bodega debe ser un número positivo \n')
                    if waste_factor == '':
                        waste_factor = None
                    else:
                        try:
                            if float(waste_factor) < 0:
                                raise ValueError('\n El factor de pérdida debe ser un número positivo \n')
                        except:
                            raise ValueError('\n El factor de pérdida debe ser un número positivo \n')
                    editSku(db,id = id, name=name, price=price, critical_level=critical_level, real_quantity=real_quantity, waste_factor = waste_factor)
                except ValueError as ve:
                    print(ve)
                    input('\n Presione una tecla para continuar \n')
            if (opt2 == '2'):
                try:
                    file_name = input('\n Ingrese el nombre del archivo con los datos: ')
                    file_dir = file_name + ".xlsx"
                    if os.path.isfile(file_dir):
                        editAllSkus(db, file_name)
                        input('\n Datos cargados exitosamente. Presione una tecla para continuar. ')
                    else:
                        raise ValueError('\n Archivo no encontrado.')
                except ValueError as ve:
                    print(ve)
        if (opt == '3'):
            try:
                id = input("\n Ingrese el ID del producto que desea eliminar: ")
                try:
                    int(id)
                except:
                    raise ValueError('\n No es un ID válido. \n')
                with db_session:
                    if db.Stock.get(id = id) == None:
                        raise ValueError('\n Producto inexistente. \n')
                deleteSku(db, id)
            except ValueError as ve:
                print(ve)
                input('\n Presione una tecla para continuar \n')
        if (opt == '4'):
            printStockConsole(db)
            input('\n Presione una tecla para continuar \n')
        if (opt =='5') :
            try:
                file_name = input(' Ingrese el nombre del archivo de la orden de compra: ')
                file_dir = file_name + ".xlsx"
                if os.path.isfile(file_dir):
                    makePurchases(db, file_name)
                    input('\n Orden de compra ingresada exitosamente. Presione una tecla para continuar.')
                else:
                    raise ValueError('\n Archivo no encontrado.')
            except ValueError as ve:
                print(ve)
                input(' Presione una tecla para continuar.')
        if opt =='6' and level ==1:
            createStockReport(db)
            input('\n Informe creado con éxito. Presione cualquier tecla para continuar. \n')
        if (opt == '7'):
            break