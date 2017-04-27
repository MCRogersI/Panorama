from pony.orm import *
from datetime import date, timedelta
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib.pyplot import plot, show
from threading import Thread


def createSku(db,id, name, price, critical_level, real_quantity, waste_factor, estimated_quantity=None):
    ''' Este método crea una unidad nueva de stock, asigna automáticamente el ID de la misma.
        La cantidad estimada es la que se ve afectada por una planificación que podría cambiarse 
        en el futuro '''

    with db_session:
        s = db.Stock(id=id, name=name, price=price, critical_level=critical_level,
                     real_quantity=real_quantity, estimated_quantity=estimated_quantity, waste_factor = waste_factor)


def editSku(db, id, name=None, price=None, critical_level=None, real_quantity=None,
            estimated_quantity=None):
    ''' Este método edita la unidad de stock, en cualquiera de sus características '''

    with db_session:
        try:
            s = db.Stock[id]
            if name != None:
                s.name = name
            if price != None:
                s.price = price
            if critical_level != None:
                s.critical_level = critical_level
            if real_quantity != None:
                s.real_quantity = real_quantity
            if estimated_quantity != None:
                s.estimated_quantity = estimated_quantity

        except ObjectNotFound as e:
            print('Object not found: {}'.format(e))
        except ValueError as e:
            print('Value error: {}'.format(e))


def deleteSku(db, id):
    ''' Este método elimina una de las entradas de SKU de la tabla de Stock'''
    with db_session:
        db.Stock[id].delete()


def printStockConsole(db):
    ''' Este método elimina una de las entradas de SKU de la tabla de Stock '''
    with db_session:
        db.Stock.select().show()


def createEngagement(db, contract_number, skus_list, withdrawal_date=None):
    ''' Este método crea una nueva entrada en la tabla de engagements a partir de los datos ingresados  '''
    # skus_list es una lista de tuplas con el id del SKU y la cantidad correspondiente.
    with db_session:
        if type(skus_list) == list:  # Caso en el que se ingresa un lista de tuplas.
            for sku_row in skus_list:
                try:
                    sku = db.Stock[sku_row[0]]
                    # IMPORTANTE: En 'project' se podría haber guardado simplemente el id del proyecto (contract_number),
                    # pero de esta forma el proyecto puede ser accedido de forma directa a través del engagement.
                    # Deberíamos instaurar una convención al respecto.
                    db.Engagements(project=db.Projects[contract_number], sku=sku, quantity=sku_row[1],
                                   withdrawal_date=withdrawal_date)
                except ObjectNotFound as e:
                    print('Object not found: {}'.format(e))
                except ValueError as e:
                    print('Value error: {}'.format(e))
        else:
            try:
                sku = db.Stock[skus_list[0]]
                db.Engagements(project=db.Projects[contract_number], sku=sku, quantity=skus_list[1],
                               withdrawal_date=withdrawal_date)

            except ObjectNotFound as e:
                print('Object not found: {}'.format(e))
            except ValueError as e:
                print('Value error: {}'.format(e))
            except TypeError as e:
                print('Type error: {}'.format(e))


def createPurchases(db, skus_list, arrival_date):
    ''' Este método crea una nueva entrada en la tabla de purchases a partir de los datos ingresados  '''
    # skus_list es una lista de tuplas con el id del SKU y la cantidad correspondiente. Se DEBE ingresar la fecha de entrega.
    with db_session:
        if type(skus_list) == list:  # Caso en el que se ingresa un lista de tuplas.
            for sku_row in skus_list:
                try:
                    sku = db.Stock[sku_row[0]]
                    db.Purchases(sku=sku, quantity=sku_row[1], arrival_date=arrival_date)
                except ObjectNotFound as e:
                    print('Object not found: {}'.format(e))
                except ValueError as e:
                    print('Value error: {}'.format(e))
        else:
            try:
                sku = db.Stock[skus_list[0]]
                db.Purchases(sku=sku, quantity=skus_list[1], arrival_date=arrival_date)

            except ObjectNotFound as e:
                print('Object not found: {}'.format(e))
            except ValueError as e:
                print('Value error: {}'.format(e))
            except TypeError as e:
                print('Type error: {}'.format(e))


def calculateStock(db, id_sku):
    ''' Este método retorna una tupla con los valores (fecha,cantidad) de stock (considerando las fechas en las que se presentan cambios)'''
    with db_session:
        try:
            engagements = select(en for en in db.Engagements if en.sku.id == id_sku).order_by(
                lambda en: en.withdrawal_date)
            purchases = select(pur for pur in db.Purchases if pur.sku.id == id_sku).order_by(
                lambda pur: pur.arrival_date)
            aux_engagements = []
            aux_purchases = []
            for en in engagements:
                aux_engagements.append((-en.quantity, en.withdrawal_date))
            for pur in purchases:
                aux_purchases.append((pur.quantity, pur.arrival_date))
            fluxes = aux_engagements + aux_purchases
            fluxes = sorted(fluxes, key=itemgetter(1))
            beginning_date = date.today()
            beginning_quantity = db.Stock[id_sku].real_quantity
            fluxes = [(0, beginning_date)] + fluxes
            values = [(beginning_quantity, beginning_date)]
            for i in range(1, len(fluxes)):
                values.append((values[i - 1][0] + fluxes[i][0], fluxes[i][1]))
            return values

        except ObjectNotFound as e:
            print('Object not found: {}'.format(e))
        except ValueError as e:
            print('Value error: {}'.format(e))

def updateEngagements(db, id_sku):
    '''Este método actualiza los engagements una vez que se ha hecho una planificación, asignando la fecha de inicio
        de la instalación '''
    with db_session:
        # installations = select(t for t in db.Tasks if t.skill.id == 4)
        assigned_inst = select(at for at in db.Employees_Tasks if at.task.skill.id == 4)
        engagements = select(e for e in db.Engagements if e.sku == db.Stock[id_sku])
        for e in engagements:
            for at in assigned_inst:
                if at.task.project == e.project:
                    e.withdrawal_date = at.planned_initial_date

def printStock(db, id_sku): #Revisar este método para el caso 3 gráfica una línea al principio que no parece función.
    '''Este método imprime el comportamiento de un SKU hasta el último de los movimientos registrados '''
    with db_session:
        movements = calculateStock(db, id_sku)
        quantities = []
        dates = []
        for l in movements:
            quantities.append(l[0])
            dates.append(l[1])

        #Lo siguiente le agrega 7 días de stock constante después del último movimiento (agrega un fecha 7 días después con el mismo valor)
        dates.append(dates[len(dates)-1]+timedelta(days = 7))
        quantities.append(quantities[len(quantities) - 1])

        def plot_graph(quantities, dates):
            min_quantity = min(quantities)
            max_quantity = max(quantities)
            span_quantities = max_quantity - min_quantity
            plt.figure()
            plt.step(dates, quantities, where='post')
            plt.xlim((date.today(), dates[len(dates) - 1] + timedelta(1)))
            plt.ylim(min_quantity - (span_quantities / 10), max_quantity + (span_quantities / 10))
            plt.xticks(dates, dates, rotation='vertical')
            plt.ylabel('Quantity')
            plt.xlabel('Date')
            plt.title('SKU (id = {}) quantities by date'.format(id_sku))
            plt.title(
                'Inventory prediction of unit ' + str(db.Stock[id_sku]) + ', code: ' + str(id_sku))
            plt.axhline(y=db.Stock[id_sku].critical_level, color='r', linestyle='-')
            plt.tight_layout()
            plt.show(block=False) #Esto debería estar definido con el valor de block = True.
            #Es un 'Workaround' para graficar múltiples gráficos.
        p = Thread(target=plot_graph(quantities=quantities, dates=dates))
        p.start()
        p.join()

def displayStock(db, id_sku):
    '''Este método grafica el comportamiento de un SKU hasta el último de los movimientos registrados '''
    with db_session:
        sku = db.Stock.get(id=id_sku)
        critical_level = sku.critical_level
        values = calculateStock(db, id_sku)
        quantities, dates = zip(*values)#<-- wooowowooo (que bonita función)

        def plot_graph(quantities, dates):
            plt.figure()
            plt.ylabel('Quantity')
            plt.xlabel('Date')
            plt.title(
                'Inventory prediction of unit ' + str(db.Stock[id_sku]) + ', code: ' + str(id_sku))
            min_date = min(dates)
            max_date = max(dates)
            min_quantity = min(quantities)
            max_quantity = max(quantities)
            span_quantities = max_quantity - min_quantity
            delta = max_date - min_date
            delta = delta.days
            aux_quantity = []
            aux_dates = []
            virtual_extra_days = 7

            def get_set_from_dates(quantities,dates): #Método auxiliar para generar un 'set' de los datos en values
                result = []
                for i in range(1,len(dates)):
                    if dates[i-1]!=dates[i]:
                        result.append((quantities[i-1],dates[i-1]))
                    if i == len(dates)-1:
                        result.append((quantities[i], dates[i]))
                return result

            set_of_quantities, set_of_dates = zip(*get_set_from_dates(quantities,dates)) #Revisar que sucede cuando no hay engagements y/o no hay purchases


            for i in range(0,delta + virtual_extra_days):
                aux_dates.append(min_date+timedelta(days=i))
                aux_quantity.append(0)

            d = 0
            for i in range(0,len(aux_dates)):
                if d < len(set_of_dates)-1:
                    if aux_dates[i] < set_of_dates[d+1]:
                        aux_quantity[i] = set_of_quantities[d]

                    elif d<len(set_of_dates)-1:
                        aux_quantity[i] = set_of_quantities[d+1]
                        d += 1

                else:
                    aux_quantity[i] = set_of_quantities[d]

            width = 1
            p1 = plt.bar(aux_dates, aux_quantity, width=width, color='#0000FF', align='center')

            for i in range(0,len(aux_dates)): #Para colorear los días con stock bajo el nivel crítico.
                if aux_quantity[i] <= critical_level:
                    p1[i].set_color('r')
                    # p1[i].set_linewidth(1)
                    # p1[i].set_edgecolor('k')
                p1[i].set_linewidth(1.1)
                p1[i].set_edgecolor('k')

            # plt.xticks(dates, dates, rotation='vertical') #Con esta configuración solo aparecen los labels de las fechas con cambios
            plt.xticks(aux_dates, aux_dates, rotation='vertical')  # Con esta configuración aparecen los labels de todos los días
            plt.grid()
            plt.axhline(y=db.Stock[id_sku].critical_level, color='r', linestyle='dashed',
                        linewidth=2.5)
            plt.axvline(x=max_date, color='k', linestyle='dashed', linewidth=1.5)
            plt.xlim(min_date, max_date + timedelta(
                days=7))  # Se agregan 7 días 'extras/ficticios' para un mejor display
            plt.ylim(min_quantity - (span_quantities / 10), max_quantity + (span_quantities / 10))
            # plt.ylim(0, max_quantity + (span_quantities / 10))
            # plt.savefig("SKU{}.png".format(id_sku))
            plt.tight_layout()
            plt.show(block=True)

        p = Thread(target=plot_graph(quantities=quantities, dates=dates))
        p.start()
        p.join()

def calculateStockForExcel(db, id_sku):
    '''Este método calcula el comportamiento de un SKU hasta el último de los movimientos registrados HECHO PARA EXCEL'''
    with db_session:
        sku = db.Stock.get(id=id_sku)
        critical_level = sku.critical_level
        values = calculateStock(db, id_sku)
        quantities, dates = zip(*values)#<-- wooowowooo (que bonita función)

        def intermediate_calculation(quantities, dates):
            # plt.figure()
            # plt.ylabel('Quantity')
            # plt.xlabel('Date')
            # plt.title(
            #     'Inventory prediction of unit ' + str(db.Stock[id_sku]) + ', code: ' + str(id_sku))
            min_date = min(dates)
            max_date = max(dates)
            min_quantity = min(quantities)
            max_quantity = max(quantities)
            span_quantities = max_quantity - min_quantity
            delta = max_date - min_date
            delta = delta.days
            aux_quantity = []
            aux_dates = []
            virtual_extra_days = 7

            def get_set_from_dates(quantities,dates): #Método auxiliar para generar un 'set' de los datos en values
                result = []
                for i in range(1,len(dates)):
                    if dates[i-1]!=dates[i]:
                        result.append((quantities[i-1],dates[i-1]))
                    if i == len(dates)-1:
                        result.append((quantities[i], dates[i]))
                return result

            set_of_quantities, set_of_dates = zip(*get_set_from_dates(quantities,dates)) #Revisar que sucede cuando no hay engagements y/o no hay purchases


            for i in range(0,delta + virtual_extra_days):
                aux_dates.append(min_date+timedelta(days=i))
                aux_quantity.append(0)

            d = 0
            for i in range(0,len(aux_dates)):
                if d < len(set_of_dates)-1:
                    if aux_dates[i] < set_of_dates[d+1]:
                        aux_quantity[i] = set_of_quantities[d]

                    elif d<len(set_of_dates)-1:
                        aux_quantity[i] = set_of_quantities[d+1]
                        d += 1

                else:
                    aux_quantity[i] = set_of_quantities[d]

            # width = 1
            # p1 = plt.bar(aux_dates, aux_quantity, width=width, color='#0000FF', align='center')

            # for i in range(0,len(aux_dates)): #Para colorear los días con stock bajo el nivel crítico.
            #     if aux_quantity[i] <= critical_level:
            #         p1[i].set_color('r')
                    ##p1[i].set_linewidth(1)
                    ##p1[i].set_edgecolor('k')
                # p1[i].set_linewidth(1.1)
                # p1[i].set_edgecolor('k')

            # plt.xticks(dates, dates, rotation='vertical') #Con esta configuración solo aparecen los labels de las fechas con cambios
            # plt.xticks(aux_dates, aux_dates, rotation='vertical')  # Con esta configuración aparecen los labels de todos los días
            # plt.grid()
            # plt.axhline(y=db.Stock[id_sku].critical_level, color='r', linestyle='dashed',
            #             linewidth=2.5)
            # plt.axvline(x=max_date, color='k', linestyle='dashed', linewidth=1.5)
            # plt.xlim(min_date, max_date + timedelta(
            #     days=7))  # Se agregan 7 días 'extras/ficticios' para un mejor display
            # plt.ylim(min_quantity - (span_quantities / 10), max_quantity + (span_quantities / 10))
            ## plt.ylim(0, max_quantity + (span_quantities / 10))
            ## plt.savefig("SKU{}.png".format(id_sku))
            # plt.tight_layout()
            # plt.show(block=True)

        # p = Thread(target=plot_graph(quantities=quantities, dates=dates))
        # p.start()
        # p.join()
            return (aux_dates, aux_quantity)
        return intermediate_calculation(quantities=quantities,dates=dates)
def displayStockForExcel(db, id_sku):
    '''Este método grafica el comportamiento de un SKU hasta el último de los movimientos registrados HECHO PARA EXCEL'''
    with db_session:
        sku = db.Stock.get(id=id_sku)
        critical_level = sku.critical_level
        values = calculateStock(db, id_sku)
        quantities, dates = zip(*values)  # <-- wooowowooo (que bonita función)

        def plot_graph(quantities, dates):
            plt.figure()
            plt.ylabel('Quantity')
            plt.xlabel('Date')
            plt.title(
                'Inventory prediction of unit ' + str(db.Stock[id_sku]) + ', code: ' + str(
                    id_sku))
            min_date = min(dates)
            max_date = max(dates)
            min_quantity = min(quantities)
            max_quantity = max(quantities)
            span_quantities = max_quantity - min_quantity
            delta = max_date - min_date
            delta = delta.days
            aux_quantity = []
            aux_dates = []
            virtual_extra_days = 7

            def get_set_from_dates(quantities,
                                   dates):  # Método auxiliar para generar un 'set' de los datos en values
                result = []
                for i in range(1, len(dates)):
                    if dates[i - 1] != dates[i]:
                        result.append((quantities[i - 1], dates[i - 1]))
                    if i == len(dates) - 1:
                        result.append((quantities[i], dates[i]))
                return result

            set_of_quantities, set_of_dates = zip(*get_set_from_dates(quantities, dates))

            for i in range(0, delta + virtual_extra_days):
                aux_dates.append(min_date + timedelta(days=i))
                aux_quantity.append(0)

            d = 0
            for i in range(0, len(aux_dates)):
                if d < len(set_of_dates) - 1:
                    if aux_dates[i] < set_of_dates[d + 1]:
                        aux_quantity[i] = set_of_quantities[d]

                    elif d < len(set_of_dates) - 1:
                        aux_quantity[i] = set_of_quantities[d + 1]
                        d += 1

                else:
                    aux_quantity[i] = set_of_quantities[d]

            width = 1
            return  aux_dates,aux_quantity
        plot_graph(quantities,dates)

#FUNCIÓN EN DESARROLLO
# def displayALlSKUs(db):
#     with db_session:
#         skus = select(sku for sku in db.Stock).order_by(lambda s: s.id)
#         for sku in skus:
#             displayStock(db,sku.id)

def checkStockAlarms(db):
    '''Este método revisa los niveles de stock para cada sku en el futuro y verifica si están bajo el nivel crítico.
    Retorna en una lista de tuplas, las cantidades bajo el nivel crítico detectadas y sus respectivas fechas.  '''
    alarms = []
    with db_session:
        skus = select(sku for sku in db.Stock)
        for sku in skus:
            sku_levels = calculateStock(db, sku.id)
            critical_level = sku.critical_level
            for sku_level in sku_levels:
                if sku_level[0] <= critical_level:
                    alarms.append(sku_level)
                    alarms = sorted(alarms, key=itemgetter(1))
                    print(
                        'SKU (id = {0}) quantity below critical level {1}, on the date {2}'.format(
                            sku.id, sku_level[0], sku_level[1]))
    return alarms
def getStockValue(db):
    '''Método que entrega el precio en euros del stock existente el día en que se llama el método '''
    with db_session:
        skus = select(sku for sku in db.Stock)
        total_sum = 0
        for s in skus:
            total_sum += s.price*s.real_quantity
        return total_sum
def updateStock(db):
    ''' Método que realiza los cambios efectivos de stock correspondientes a la fecha en que se llama al método,
    debería llamarse todos los días y/o cada vez que se ingrese algún movimiento efectivo '''
    with db_session:
        engagements = select (e for e in db.Engagements if e.withdrawal_date == date.today())
        purchases = select( pur for pur in db.Purchases if pur.arrival_date == date.today())

