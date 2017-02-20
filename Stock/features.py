from pony.orm import *
from datetime import date

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

def calculateStock(db):
	''' Este método retorna una tupla con los flujos (fecha,cantidad) de stock  '''
	engagements = select(en for en in db.Engagements).order_by(lambda en: en.withdrawal_date)
	purchases = select(pur for pur in db.Engagements).order_by(lambda pur: pur.arrival_date)
	for en in engagements:
		en = (en.quantity, en.withdrawal_date)
	for pur in engagements:
		pur = (pur.quantity, pur.withdrawal_date)
	fluxes = engagements + purchases
	fluxes.sort(key=lambda f: f[1])
	beginning_date = date.today()
	days_with_flux = []
	fluxes = [(0,beginning_date)]+fluxes
	for f in fluxes:
		days_with_flux.append(f[1])
	return (days_with_flux,fluxes)




