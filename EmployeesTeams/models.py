from pony.orm import *



def define_models(db):
	class Employees(db.Entity):
		id = PrimaryKey(int, auto=False)
		name = Required(str)
		team_id = Optional('Teams')
		skills = Set('Skills')

	class Skills (db.Entity):
		id = PrimaryKey(int, auto=False)
		name = Required(str)
		employees = Set(Employees)
		teams = Set('Teams_Skills')
		tasks =Set('Tasks')

		def __repr__(self):
			return self.name

	class Teams(db.Entity):
		id = PrimaryKey(int, auto=False)
		zone = Required(int)
		skills = Set('Teams_Skills')
		employees = Set(Employees)
		tasks = Set('Tasks_Teams')

		def __repr__(self):
			return str(self.id)

	class Teams_Skills(db.Entity):
		team = Required(Teams)
		skill = Required(Skills)
		PrimaryKey(team, skill)
		performance = Required(float)