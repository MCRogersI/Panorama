from pony.orm import *

#Definir tablas de empleados y equipos
def define_models(db):
	class Skills(db.Entity):
		id = PrimaryKey(int, auto=False)
		name = Required(str)
		employees = Set('Employees_Skills')
		tasks = Set('Tasks')
		
		def __repr__(self):
			return self.name

	class Employees(db.Entity):
		id = PrimaryKey(int, auto=False)
		name = Required(str)
		zone = Required(int)
		skills = Set('Employees_Skills')
		tasks = Set('Employees_Tasks')
		activities = Set('Employees_Activities')
		restrictions = Set('Employees_Restrictions')

		def __repr__(self):
			return str(self.id)

	class Employees_Skills(db.Entity):
		employee = Required(Employees)
		skill = Required(Skills)
		PrimaryKey(employee, skill)
		performance = Required(float)
