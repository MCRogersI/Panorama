from pony.orm import *
from datetime import date

def define_models(db):
	class Stock(db.Entity):
		id = PrimaryKey(int, auto = False)
		name = Required(str)
		# type = Optional(str)#crystal, profile, components, etc. Según el formato de los excel, no sería necesario
		price = Required(float)
		critical_level = Required(float)#En el futuro este valor podría calcularse pero inicialmente debe ser fijado
		real_quantity = Required(float)# Required desde el 29/03/2017, no tiene sentido q sea opcional, y es necesario para calcular stock.
		waste_factor = Optional(float)#Required desde el 29/03/2017, todos los materiales tienen factores de pérdida (pensandolo mejor, es Optional desde 18/05/2017, porque algunos waste_factor son bien generales y abarcan hartos SKUs)
		estimated_quantity = Optional(float)
		engagements = Set('Engagements')
		purchases = Set('Purchases')
		
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

