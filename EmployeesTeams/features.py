from pony.orm import *

def CreateEmployee(db, id, name, team_id, rect, des, fab, inst):
	with db_session:
		e = db.Employees(id = id, name = name, team_id = team_id)
		if rect:
			e.skills.add(db.Skills[1])
		if des:
			e.skills.add(db.Skills[2])
		if fab:
			e.skills.add(db.Skills[3])
		if inst:
			e.skills.add(db.Skills[4])

def PrintEmployees(db):
    with db_session:
        db.Employees.select().show()

def EditEmployee(db, id, new_name = None, new_team_id = None, rect =None, des = None, fab= None, inst = None):
	with db_session:
		e = db.Employees[id]
		if new_name != None:
			e.name = new_name
		if new_team_id != None:
			e.team_id = new_team_id
		if rect and not db.Skills[1] in e.skills:
			e.skills.add(db.Skills[1])
		if rect == False and db.Skills[1] in e.skills:
			e.skills.remove(db.Skills[1])
		if des and not db.Skills[2] in e.skills:
			e.skills.add(db.Skills[2])
		if des == False and db.Skills[2] in e.skills:
			e.skills.remove(db.Skills[2])
		if fab and not db.Skills[3] in e.skills:
			e.skills.add(db.Skills[3])
		if fab == False and db.Skills[3] in e.skills:
			e.skills.remove(db.Skills[3])
		if inst and not db.Skills[4] in e.skills:
			e.skills.add(db.Skills[4])
		if inst == False and db.Skills[4] in e.skills:
			e.skills.remove(db.Skills[4])

def DeleteEmployee(db, id):
	with db_session:
			db.Employees[id].delete()

def CreateTeam(db, id , zone, perf_rect= None , perf_des = None, perf_fab = None, perf_inst = None):
	with db_session:
		t = db.Teams(id = id, zone = zone)
		if perf_rect != None:
			db.Teams_Skills(team = id, skill = 1, performance = perf_rect)
		if perf_des != None:
			db.Teams_Skills(team = id, skill = 2, performance = perf_des)
		if perf_fab != None:
			db.Teams_Skills(team = id, skill = 3, performance = perf_fab)
		if perf_inst != None:
			db.Teams_Skills(team = id, skill = 4, performance = perf_inst)

def PrintTeams(db):
	with db_session:
		db.Teams.select().show()

def PrintTeamsSkills(db):
	with db_session:
		db.Teams_Skills.select().show()

def EditTeam(db, id, new_zone = None, perf_rect = None, perf_des = None, perf_fab = None, perf_inst = None):
	with db_session:
		t = db.Teams[id]
		if new_zone != None:
			t.zone = new_zone
		if perf_rect != None:
			db.Teams_Skills[(id, 1)].performance = perf_rect
		if perf_des != None:
			db.Teams_Skills[(id, 2)].performance = perf_des
		if perf_fab != None:
			db.Teams_Skills[(id, 3)].performance = perf_fab
		if perf_inst != None:
			db.Teams_Skills[(id, 4)].performance = perf_inst
			
def DeleteTeam(db, id):
	with db_session:
			db.Teams[id].delete()

def PrintSkills(db):
	with db_session:
		db.Skills.select().show()

def PrintTeamsSkills(db):
	with db_session:
		db.Teams_Skills.select().show()
	
def PrintSelectSkill(db, skill_id):
	with db_session:
		select(e for e in db.Employees if db.Skills[skill_id] in e.skills).show()

		
		
