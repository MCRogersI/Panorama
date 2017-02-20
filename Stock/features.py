from pony.orm import *
from datetime import date, timedelta
import matplotlib.pyplot as plt

def createSKU(db, name, price, critical_level, real_quantity = None, estimated_quantity = None):

	''' Este método crea una unidad nueva de stock, asigna automáticamente el ID de la misma.
		La cantidad estimada es la que se ve afectada por una planificación que podría cambiarse 
		en el futuro '''

	with db_session:
		s = db.Stock(name = name, price = price, critical_level = critical_level, real_quantity = real_quantity, estimated_quantity = estimated_quantity)

def editSKU(db, id, name = None, price = None, critical_level = None, real_quantity = None, estimated_quantity = None):
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

def createEngagement(db, id_project, SKUs_list,  withdrawal_date = None):
	''' Este método crea una nueva entrada en la tabla de engagements a partir de los datos ingresados  '''
	# SKUs_list es una lista de tuplas con el id del SKU y la cantidad correspondiente.
	with db_session:
		if len(SKUs_list) > 1: #Caso en el que se ingresa un lista de tuplas.
			for sku_row in SKUs_list:
				try:
					sku = db.Stock[sku_row[0]]
					#IMPORTANTE: En 'project' se podría haber guardado simplemente el id del proyecto (contrac_number),
					# pero de esta forma el proyecto puede ser accedido de forma directa a través del engagement.
					# Deberíamos instaurar una convención al respecto.
					db.Engagements(project = db.Projects[id_project], SKU = sku, quantity = sku_row[1], withdrawal_date = withdrawal_date)
				except ObjectNotFound as e:
					print('Object not found: {}'.format(e))
				except ValueError as e:
					print('Value error: {}'.format(e))
		else:
			try:
				sku = db.Stock[SKUs_list[0]]
				db.Engagements(project=db.Projects[id_project], SKU=sku, quantity=SKUs_list[1],withdrawal_date=withdrawal_date)

			except ObjectNotFound as e:
				print('Object not found: {}'.format(e))
			except ValueError as e:
				print('Value error: {}'.format(e))

def createPurchases(db,SKUs_list,  arrival_date):
	''' Este método crea una nueva entrada en la tabla de purchases a partir de los datos ingresados  '''
	# SKUs_list es una lista de tuplas con el id del SKU y la cantidad correspondiente. Se DEBE ingresar la fecha de entrega.
	with db_session:
		if len(SKUs_list) > 1: #Caso en el que se ingresa un lista de tuplas.
			for sku_row in SKUs_list:
				try:
					sku = db.Stock[sku_row[0]]
					db.Purchases(SKU = sku, quantity = sku_row[1], arrival_date = arrival_date)
				except ObjectNotFound as e:
					print('Object not found: {}'.format(e))
				except ValueError as e:
					print('Value error: {}'.format(e))
		else:
			try:
				sku = db.Stock[SKUs_list[0]]
				db.Engagements(SKU=sku, quantity=SKUs_list[1],arrival_date=arrival_date)

			except ObjectNotFound as e:
				print('Object not found: {}'.format(e))
			except ValueError as e:
				print('Value error: {}'.format(e))

def calculateStock(db,id_SKU):
	''' Este método retorna una tupla con los valores (fecha,cantidad) de stock (considerando las fechas en las que se presentan cambios)'''
	with db_session:
		try:
			engagements = select(en for en in db.Engagements if en.SKU.id == id_SKU).order_by(lambda en: en.withdrawal_date)
			purchases = select(pur for pur in db.Purchases if pur.SKU.id == id_SKU).order_by(lambda pur: pur.arrival_date)
			aux_engagements = []
			aux_purchases = []
			for en in engagements:
				aux_engagements.append((-en.quantity, en.withdrawal_date))
			for pur in purchases:
				aux_purchases.append((pur.quantity, pur.arrival_date))
			fluxes = aux_engagements + aux_purchases
			fluxes = sorted(fluxes, key=lambda date: fluxes[1])
			beginning_date = date.today()
			beginning_quantity = db.Stock[id_SKU].real_quantity
			fluxes = [(0,beginning_date)]+fluxes
			values = [(beginning_quantity,beginning_date)]
			for i in range(1,len(fluxes)):
				values.append((values[i-1][0]+fluxes[i][0],fluxes[i][1]))
			return values

		except ObjectNotFound as e:
			print('Object not found: {}'.format(e))
		except ValueError as e:
			print('Value error: {}'.format(e))


def printStock(db, id_SKU):
	with db_session:
		movements = calculateStock(db, id_SKU)
		quantities = []
		dates = []
		for l in movements:
			quantities.append(l[0])
			dates.append(l[1])
		plt.step(dates, quantities, where = 'post')
		plt.xlim((date.today(), dates[len(dates)-1]+timedelta(1)))
		plt.ylabel('Quantity')
		plt.xlabel('Date')
		plt.suptitle('Inventory prediction of unit '+str(id_SKU))
		plt.show()


