from pony.orm import *

def CreateProject(db, contract_number, client_address, client_name, client_rut, linear_meters, real_linear_meters = None, estimated_cost = None, real_cost = None):
	with db_session:
		p = db.Projects(contract_number = contract_number, client_address = client_address, client_name = client_name, client_rut = client_rut, linear_meters = linear_meters, estimated_cost = estimated_cost)
		if real_linear_meters != None:
			p.real_linear_meters.add(real_linear_meters)
		if real_cost != None:
			p.real_cost.add(real_cost)

def PrintProjects(db):
    with db_session:
        db.Projects.select().show()

def EditProject(db, contract_number, new_client_address = None, new_client_name = None, new_client_rut = None , new_linear_meters = None, new_real_linear_meters = None, new_estimated_cost = None, new_real_cost = None):
	with db_session:
		p = db.Projects[contract_number]
		if new_client_address != None:
			p.client_addres = new_client_address
		if new_client_name != None:
			p.client_name = new_client_name
		if new_client_rut != None:
			p.client_rut = new_client_rut
		if new_linear_meters != None:
			p.linear_meters = new_linear_meters
		if new_real_linear_meters != None:
			p.real_linear_meters = real_linear_meters
		if new_estimated_cost != None:
			p.estimated_cost = new_estimated_cost
		if new_real_cost != None:
			p.real_cost = new_real_cost	


def CreateTask(db, id, id_skill, id_project, original_initial_date, original_end_date, efective_initial_date = None, efective_end_date = None, failed = None, fail_cost = None):
	with db_session:
		t = db.Tasks(id = id, id_skill = id_skill, id_project = id_project, original_initial_date = original_initial_date, original_end_date = original_end_date)

def EditTask(db, id , id_skill = None, id_project = None, original_initial_date = None, original_end_date = None, efective_initial_date = None, efective_end_date = None, failed = None, fail_cost = None):
	with db_session:
		t = db.Tasks[id]
		if id_skill != None:
			t.id_skill = id_skill
		if id_project != None:
			t.id_project = id_project
		if original_initial_date != None:
			t.original_initial_date = original_initial_date
		if original_end_date != None:
			t.original_end_date = original_end_date
		if efective_initial_date != None:
			t.efective_initial_date = efective_initial_date
		if efective_end_date != None:
			t.efective_end_date = efective_end_date
		if failed != None:
			t.failed = failed
		if fail_cost != None:
			t.fail_cost = fail_cost
			
# def DeleteTask(db, id_task):
	

def PrintTasks(db):
	with db_session:
		db.Tasks.select().show()


