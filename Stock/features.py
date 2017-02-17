from pony.orm import *


def createSKU(db, name, price, critical_level, real_quantity = None, estimated_quantity = None):

	''' Este método crea una unidad nueva de stock, asigna automáticamente el ID de la misma.
		La cantidad estimada es la que se ve afectada por una planificación que podría cambiarse 
		en el futuro '''

	with db_session:
		s = db.Stock(name = name, price = price, critical_level = critical_level, real_quantity = real_quantity, estimated_quantity = estimated_quantity)

def editSKU(db, id, name = None, price = None, critical_level = None, real_quantity = None, estimated_quantity = None):
	''' Este método edita la unidad de stock, en cualquiera de sus características '''

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
