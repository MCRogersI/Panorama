from pony.orm import *
from datetime import date, timedelta
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib.pyplot import plot, show
from threading import Thread


def createSKU(db, name, price, critical_level, real_quantity=None, estimated_quantity=None):
	''' Este método crea una unidad nueva de stock, asigna automáticamente el ID de la misma.
		La cantidad estimada es la que se ve afectada por una planificación que podría cambiarse 
		en el futuro '''

	with db_session:
		s = db.Stock(name=name, price=price, critical_level=critical_level,
					 real_quantity=real_quantity, estimated_quantity=estimated_quantity)


def editSKU(db, id, name=None, price=None, critical_level=None, real_quantity=None,
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


def deleteSKU(db, id):
	''' Este método elimina una de las entradas de SKU de la tabla de Stock'''
	with db_session:
		db.Stock[id].delete()


def printStock(db):
	''' Este método elimina una de las entradas de SKU de la tabla de Stock '''
	with db_session:
		db.Stock.select().show()


def createEngagement(db, id_project, SKUs_list, withdrawal_date=None):
	''' Este método crea una nueva entrada en la tabla de engagements a partir de los datos ingresados  '''
	# SKUs_list es una lista de tuplas con el id del SKU y la cantidad correspondiente.
	with db_session:
		if type(SKUs_list) == list:  # Caso en el que se ingresa un lista de tuplas.
			for sku_row in SKUs_list:
				try:
					sku = db.Stock[sku_row[0]]
					# IMPORTANTE: En 'project' se podría haber guardado simplemente el id del proyecto (contrac_number),
					# pero de esta forma el proyecto puede ser accedido de forma directa a través del engagement.
					# Deberíamos instaurar una convención al respecto.
					db.Engagements(project=db.Projects[id_project], SKU=sku, quantity=sku_row[1],
								   withdrawal_date=withdrawal_date)
				except ObjectNotFound as e:
					print('Object not found: {}'.format(e))
				except ValueError as e:
					print('Value error: {}'.format(e))
		else:
			try:
				sku = db.Stock[SKUs_list[0]]
				db.Engagements(project=db.Projects[id_project], SKU=sku, quantity=SKUs_list[1],
							   withdrawal_date=withdrawal_date)

			except ObjectNotFound as e:
				print('Object not found: {}'.format(e))
			except ValueError as e:
				print('Value error: {}'.format(e))
			except TypeError as e:
				print('Type error: {}'.format(e))


def createPurchases(db, SKUs_list, arrival_date):
	''' Este método crea una nueva entrada en la tabla de purchases a partir de los datos ingresados  '''
	# SKUs_list es una lista de tuplas con el id del SKU y la cantidad correspondiente. Se DEBE ingresar la fecha de entrega.
	with db_session:
		if type(SKUs_list) == list:  # Caso en el que se ingresa un lista de tuplas.
			for sku_row in SKUs_list:
				try:
					sku = db.Stock[sku_row[0]]
					db.Purchases(SKU=sku, quantity=sku_row[1], arrival_date=arrival_date)
				except ObjectNotFound as e:
					print('Object not found: {}'.format(e))
				except ValueError as e:
					print('Value error: {}'.format(e))
		else:
			try:
				sku = db.Stock[SKUs_list[0]]
				db.Purchases(SKU=sku, quantity=SKUs_list[1], arrival_date=arrival_date)

			except ObjectNotFound as e:
				print('Object not found: {}'.format(e))
			except ValueError as e:
				print('Value error: {}'.format(e))
			except TypeError as e:
				print('Type error: {}'.format(e))


def calculateStock(db, id_SKU):
	''' Este método retorna una tupla con los valores (fecha,cantidad) de stock (considerando las fechas en las que se presentan cambios)'''
	with db_session:
		try:
			engagements = select(en for en in db.Engagements if en.SKU.id == id_SKU).order_by(
				lambda en: en.withdrawal_date)
			purchases = select(pur for pur in db.Purchases if pur.SKU.id == id_SKU).order_by(
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
			beginning_quantity = db.Stock[id_SKU].real_quantity
			fluxes = [(0, beginning_date)] + fluxes
			values = [(beginning_quantity, beginning_date)]
			for i in range(1, len(fluxes)):
				values.append((values[i - 1][0] + fluxes[i][0], fluxes[i][1]))
			return values

		except ObjectNotFound as e:
			print('Object not found: {}'.format(e))
		except ValueError as e:
			print('Value error: {}'.format(e))

def updateEngagements(db, id_SKU):
	'''Este método actualiza los engagements una vez que se ha hecho una planificación, asignando la fecha de inicio
		de la instalación '''
	with db_session:
		# installations = select(t for t in db.Tasks if t.id_skill.id == 4)
		assigned_inst = select(at for at in db.Employees_Tasks if at.task.id_skill.id == 4)
		engagements = select(e for e in db.Engagements if e.SKU == db.Stock[id_SKU])
		for e in engagements:
			for at in assigned_inst:
				if at.task.id_project == e.project:
					e.withdrawal_date = at.planned_initial_date

def printStock(db, id_SKU):
	'''Este método imprime el comportamiento de un SKU hasta el último de los movimientos registrados '''
	with db_session:
		movements = calculateStock(db, id_SKU)
		quantities = []
		dates = []
		for l in movements:
			quantities.append(l[0])
			dates.append(l[1])

		def plot_graph(quantities, dates):
			plt.figure()
			plt.step(dates, quantities, where='post')
			plt.xlim((date.today(), dates[len(dates) - 1] + timedelta(1)))
			plt.xticks(dates, dates, rotation='vertical')
			plt.ylabel('Quantity')
			plt.xlabel('Date')
			plt.suptitle(
				'Inventory prediction of unit ' + str(db.Stock[id_SKU]) + ', code ' + str(id_SKU))
			plt.axhline(y=db.Stock[id_SKU].critical_level, color='r', linestyle='-')
			plt.tight_layout()
			plt.show(block=False) #Esto debería estar definido con el valor de block = True.
			#Es un 'Workaround' para graficar múltiples gráficos.
		p = Thread(target=plot_graph(quantities=quantities, dates=dates))
		p.start()
		p.join()


def displayStock(db, id_SKU):
	'''Este método grafica el comportamiento de un SKU hasta el último de los movimientos registrados '''
	with db_session:
		critical_level = db.Stock.get(id=id_SKU)
		values = calculateStock(db, id_SKU)
		quantities, dates = zip(*values)

		def plot_graph(quantities, dates):
			plt.figure()
			plt.ylabel('Quantity')
			plt.xlabel('Date')
			plt.title('SKU (id = {}) quantities by date'.format(id_SKU))
			min_date = min(dates)
			max_date = max(dates)
			min_quantity = min(quantities)
			max_quantity = max(quantities)
			span_quantities = max_quantity - min_quantity
			delta = max_date - min_date
			delta = delta.days
			aux_quantity = []
			aux_dates = []

			c = 0
			for i in range(0, delta+1):
				if (min_date + timedelta(days=i) > dates[c]):
					c += 1
				aux_quantity.append(quantities[c])
				aux_dates.append(min_date + timedelta(days=i))
			width = 1
			# offset = 0

			# mask1 = aux_quantity <= critical_level
			# mask2 = aux_quantity > critical_level
			# plt.bar(aux_dates[mask1], aux_quantity[mask1], color='red', align='center')
			# plt.bar(aux_dates[mask2], aux_quantity[mask2], color='blue', align='center')

			p1 = plt.bar(aux_dates, aux_quantity, width=width, color='#0000FF', align='center')

			# print(delta)
			# print(aux_dates)
			plt.grid()
			plt.xlim(min_date, max_date + timedelta(days=1))
			# plt.ylim(min_quantity - (span_quantities / 10), max_quantity + (span_quantities / 10))
			plt.ylim(0, max_quantity + (span_quantities / 10))
			plt.tight_layout()
			plt.show(block=True)
		p = Thread(target=plot_graph(quantities=quantities, dates=dates))
		p.start()
		p.join()


def updateEngagements(db, id_SKU):
	'''Este método actualiza los engagements una vez que se ha hecho una planificación, asignando la fecha de inicio
		de la instalación '''
	with db_session:
		# installations = select(t for t in db.Tasks if t.id_skill.id == 4)
		assigned_inst = select(at for at in db.Employees_Tasks if at.task.id_skill.id == 4)
		engagements = select(e for e in db.Engagements if e.SKU == db.Stock[id_SKU])
		for e in engagements:
			for at in assigned_inst:
				if at.task.id_project == e.project:
					e.withdrawal_date = at.planned_initial_date


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
