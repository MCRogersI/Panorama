from pony.orm import *
from models import Employees, Teams, Skills, Teams_Skills

def CreateEmpoyee(id, name, team_id, rect, des, fab, inst):
	with db_session:
		e = Employees(id = id, name = name, team_id = team_id)
		if rect == 1:
			e.Skills.add(Skills[1])
		if des == 1:
			e.Skills.add(Skills[2])
		if fab == 1:
			e.Skills.add(Skills[3])
		if inst == 1:
			e.Skills.add(Skills[4])
