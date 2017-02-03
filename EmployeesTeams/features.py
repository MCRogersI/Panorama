from pony.orm import *

def CreateEmployee(id, name, team_id, rect, des, fab, inst):
	with db_session:
		e = Employees(id = id, name = name, team_id = team_id)
		if rect:
			e.skills.add(Skills[1])
		if des:
			e.skills.add(Skills[2])
		if fab:
			e.skills.add(Skills[3])
		if inst:
			e.skills.add(Skills[4])

def PrintEmployees():
    with db_session:
        Employees.select().show()

def EditEmployee(id,new_name = None, new_team_id = None, rect =None, des = None, fab= None, inst = None):
	with db_session:
		e = Employees[id]
		if new_name != None:
			e.name = new_name
		if new_team_id != None:
			e.team_id = new_team_id
		if rect and not Skills[1] in e.skills:
			e.skills.add(Skills[1])
		if rect == False and Skills[1] in e.skills:
			e.skills.remove(Skills[1])
		if des and not Skills[2] in e.skills:
			e.skills.add(Skills[2])
		if des == False and Skills[2] in e.skills:
			e.skills.remove(Skills[2])
		if fab and not Skills[3] in e.skills:
			e.skills.add(Skills[3])
		if fab == False and Skills[3] in e.skills:
			e.skills.remove(Skills[3])
		if inst and not Skills[4] in e.skills:
			e.skills.add(Skills[4])
		if inst == False and Skills[4] in e.skills:
			e.skills.remove(Skills[4])

def CreateTeam(db, id , zone, perf_rect= None , perf_des = None, perf_fab = None, perf_inst = None):
	with db_session:
		t = Teams(id = id, zone = zone)
		if perf_rect != None:
			Teams_Skills (team = id, skill = Skills[1], performance = perf_rect)
		if perf_des != None:
			Teams_Skills(team = id, skill = 2, performance = perf_des)
		if perf_fab != None:
			Teams_Skills(team = id, skill = 3, performance = perf_fab)
		if perf_inst != None:
			Teams_Skills(team = id, skill = 4, performance = perf_inst)

def PrintTeams(db):
	with db_session:
		db.Teams.select().show()

def PrintTeams_Skills(db):
	with db_session:
		db.Teams_Skills.select().show()

def EditTeam(db, id, new_zone = None, perf_rect = None, perf_des = None, perf_fab = None, perf_inst = None):
	with db_session:
		t = db.Teams[id]
		if new_zone != None:
			t.zone = new_zone
		if perf_rect != None:
			db.Teams_Skills(team = id, skill = 1, performance = perf_rect)
		if perf_des != None:
			db.Teams_Skills(team = id, skill = 2, performance = perf_des)
		if perf_fab != None:
			db.Teams_Skills(team = id, skill = 3, performance = perf_fab)
		if perf_inst != None:
			db.Teams_Skills(team = id, skill = 4, performance = perf_inst)

def PrintSkills(db):
	with db_session:
		db.Skills.select().show()

def PrintTeamsSkills(db):
	with db_session:
		db.Teams_Skills.select().show()
