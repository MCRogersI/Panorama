from pony.orm import *


def createSKU(db, name, price, critical_level, real_quantity = None, estimated_quantity = None):
	''' Este método crea una nueva entrada en la tabla de SKU's de la base de datos '''
	with db_session:
		s = db.Stock(name = name, price = price, critical_level = critical_level, real_quantity = real_quantity, estimated_quantity = estimated_quantity)

def editSKU(db, id, name = None, price = None, critical_level = None, real_quantity = None, estimated_quantity = None):
	''' Este método permite editar el contenido de la fila de la tabla de stock (SKU's) correspondiente al id entregado '''
	with db_session:
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

def deleteSKU(db, id):
	with db_session:
		db.Stock[id].delete()

def printStock(db):
    with db_session:
        db.Stock.select().show()
