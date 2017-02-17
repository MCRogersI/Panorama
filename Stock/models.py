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
		def __repr__(self):
			return str(self.id)

	class Engagement(db.Entity):
		id = PrimaryKey(int, auto = True)
		id_project = Required(int)
		id_SKU = Required(int)
		quantity = Required(float)
		withdrawal_date = Required(date)
		def __repr__(self):
			return str(self.id)

	class Purchase(db.Entity):
		id = PrimaryKey(int, auto = True)
		id_SKU = Required(int)
		quantity = Required(float)
		arrival_date = Required(date)	
		def __repr__(self):
			return str(self.id)
