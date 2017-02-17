from pony.orm import *
from datetime import date

def define_models(db):
	class Stock(db.Entity):
		id = PrimaryKey(int, auto = True)
		name = Required(str)
		price = Required(float)
		critical_level = Required(float)#En el futuro este valor podría calcularse pero inicialmente debe ser fijado
		real_quantity = Optional(float)
		estimated_quantity = Optional(float)
		engagements = Set('Engagements')
		def __repr__(self):
			return str(self.name)

	class Engagements(db.Entity):
		id = PrimaryKey(int, auto = True)
		project = Required(Projects)
		SKU = Required(Stock)
		quantity = Required(float)
		withdrawal_date = Optional(date)
		def __repr__(self):
			return str(self.id)

	class Purchases(db.Entity):
		id = PrimaryKey(int, auto = True)
		id_SKU = Required(int)
		quantity = Required(float)
		arrival_date = Required(date)	
		def __repr__(self):
			return str(self.id)
