from Stock.features import createSku, editSku, deleteSku, printStockConsole


#Entiéndase SKU como el producto en si mismo (aunque en realidad significa el código del producto)
def stock_console(db, level):
    while True:
        if level == 1:
            opt = input(
                "\n Marque una de las siguientes opciones:\n - 1: Agregar un SKU. \n - 2: Editar la información de un SKU.  \n - 3: Eliminar un SKU. \n - 4: Ver el Inventario. \n - 5: Para volver atrás. \n Ingrese la alternativa elegida: ")
        if level == 2:
            opt = input(
                "\n Marque una de las siguientes opciones:\n - 1: Ver SKU. \n - 2: para volver atrás. \n Ingrese la alternativa elegida: ")
        if level == 3:
            opt = input(
                "\n Marque una de las siguientes opciones:\n - 1: Ver SKU. \n - 2: para volver atrás. \n Ingrese la alternativa elegida: ")

        if (opt == '1' and level == 1):
            id = input("\nIngrese el id del producto: ")
            name = input("\nIngrese el nombre del producto: ")
            price = input("Ingrese el precio unitario del producto: ")
            critical_level = input("Ingrese el nivel crítico del producto: ")
            real_quantity = input("Ingrese la cantidad en bodega del producto, solo presione enter si es que desea ingresar este valor en el futuro: ")
            createSku(db, name = name, price = price, critical_level = critical_level, real_quantity = real_quantity)

        if (opt == '2' and level == 1):
            id = input("\nIngrese el id del producto: ")
            name = input("\nIngrese el nuevo nombre del producto, solo presione enter si lo mantiene:")
            if name == '':
                name = None
            price = input(
                "Ingrese el nuevo precio unitario del producto, solo presione enter si lo mantiene: ")
            if price == '':
                price = None
            critical_level = input(
                "Ingrese el nuevo nivel crítico del producto, solo presione enter si lo mantiene: ")
            if critical_level == '':
                critical_level = None
            real_quantity = input(
                "Ingrese la nueva cantidad en bodega del producto, solo presione enter si es que desea ingresar este valor en el futuro: ")
            if real_quantity == '':
                real_quantity = None
            try:
                editSku(db,id = id, name=name, price=price, critical_level=critical_level,
                      real_quantity=real_quantity)
            except ObjectNotFound as e:
                print('Object not found: {}'.format(e))
            except ValueError as e:
                print('Value error: {}'.format(e))
        if (opt == '3' and level == 1):
            id = input("\nIngrese el id del producto que desea eliminar: ")
            # name = input("\nIngrese el nombre del SKU que desea elmininar: ")
            try:
                deleteSku(db, id)
            except ObjectNotFound as e:
                print('Object not found: {}'.format(e))
            except ValueError as e:
                print('Value error: {}'.format(e))

        if (opt == '4' and level == 1) or (opt == '1' and level == 2) or (
                opt == '1' and level == 3):
            printStockConsole(db)

        if (opt == '5' and level == 1) or (opt == '2' and level == 2) or (
                opt == '2' and level == 3):
            break