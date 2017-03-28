from pony.orm import *
from datetime import date

def define_models(db):
	class Stock(db.Entity):
		id = PrimaryKey(int, auto = False)
		name = Required(str)
		# type = Optional(str)#crystal, profile, components, etc. Según el formato de los excel, no sería necesario
		price = Required(float)
		critical_level = Required(float)#En el futuro este valor podría calcularse pero inicialmente debe ser fijado
		real_quantity = Optional(float)
		estimated_quantity = Optional(float)
		engagements = Set('Engagements')
		purchases = Set('Purchases')
		waste_factor = Optional(float)#para perfiles y cristales, según el Excel, valor entre 0 y 1
		def __repr__(self):
			return str(self.name)

	class Engagements(db.Entity):#si en alguna otra tarea distinta a instalación se usa stock, quizás conviene asociar a 
#cada engagement una task
		id = PrimaryKey(int, auto = True)
		project = Required('Projects')
		sku = Required('Stock')
		quantity = Required(float)#es m² para los cristales, mL para los perfiles y cantidad para los herrajes (componentes)
		withdrawal_date = Optional(date)
		def __repr__(self):
			return str(self.id)
	
	class Purchases(db.Entity):
		id = PrimaryKey(int, auto = True)
		sku = Required('Stock')
		quantity = Required(float)
		arrival_date = Required(date)	
		def __repr__(self):
			return str(self.id)
	class Waste_Factors(db.Entity):#Los 4 tipos de factores de pérdida de los componentes,
	#que se describe en el excel Base de Datos _sistema Gestion de Operaciones_ACO_04 03 2017_vf.xlsx
	#en la hoja 'COSTO ESTANDAR M PRIMAS'
		id = PrimaryKey(int, auto=False)
		name = Required(str)
		factor = Required(float)
		def __repr__(self):
			return self.name

