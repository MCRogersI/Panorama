from datetime import datetime
from Projects.features import createProject, printProjects, editProject, deleteProject ,createTask, editTask, printTasks, failedTask


def projects_console(db, level):
	while True:
		if level == 1:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear un proyecto. \n - 2: si desea editar un proyecto.  \n - 3: eliminar un proyecto. \n - 4: para ver proyectos actuales. \n - 5: para volver atrás. \n Ingrese la alternativa elegida: ")
		if level == 2:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear un proyecto. \n - 2: si desea editar un proyecto. \n - 3: para ver proyectos actuales. \n - 4: para volver atrás. \n Ingrese la alternativa elegida: ")
		if level == 3:
			opt = input("\n Marque una de las siguientes opciones: \n - 1: para ver proyectos actuales. \n - 2: para volver atrás. \n Ingrese la alternativa elegida: ")

		if(opt == '1' and (level == 1 or level == 2)):
			contract_number = input("\nIngrese el numero de contrato: ")
			client_address = input("Ingrese la direccion del cliente: ")
			client_comuna = input("Ingrese la comuna del cliente: ")
			client_name = input("Ingrese el nombre del cliente: ")
			client_rut = input("Ingrese el RUT del cliente: ")
			linear_meters = input("Ingrese los metros lineales del proyecto: ")
			deadline = input("ingrese la fecha de entrega pactada del proyecto: ")
			createProject(db, contract_number, client_address, client_comuna, client_name, client_rut, linear_meters, deadline)
		if(opt == '2' and (level == 1 or level == 2)):
			contract_number = input("\nIngrese el numero de contrato del proyecto a editar: ")
			new_client_address = input("Ingrese la nueva direccion del cliente, solo presione enter si la mantiene: ")
			if new_client_address == '':
				new_client_address = None
			new_client_comuna = input("Ingrese la nueva comuna del cliente, solo presione enter si la mantiene: ")
			if new_client_comuna == '':
				new_client_comuna = None
			new_client_name = input("Ingrese el nuevo nombre del cliente, solo presione enter si lo mantiene: ")
			if new_client_name == '':
				new_client_name = None
			new_client_rut = input("Ingrese el nuevo RUT del cliente, solo presione enter si lo mantiene: ")
			if new_client_rut == '':
				new_client_rut = None
			new_linear_meters = input("Ingrese los metros lineales del proyecto, solo presione enter si se mantienen: ")
			if new_linear_meters == '':
				new_linear_meters = None
			new_real_linear_meters = input("Ingrese los metros lineales (reales) del proyecto, solo presione enter si no se conocen: ")
			if new_real_linear_meters == '':
				new_real_linear_meters = None
			new_deadline = input("Ingrese la nueva feche de entrega pactada del proyecto, solo presione enter si se mantiene: ")
			if new_deadline == '':
				new_deadline = None
			new_estimated_cost = input("Ingrese el costo estimado del proyecto: ")
			new_real_cost = input("Ingrese el costo real del proyecto, solo presione enter si no se conoce: ")
			if new_real_cost == '':
				new_real_cost = None
			editProject(db, contract_number, new_client_address, new_client_comuna, new_client_name, new_client_rut, new_linear_meters, new_real_linear_meters, new_deadline, new_estimated_cost=None, new_real_cost=new_real_cost)
		if(opt == '3' and level == 1):
			contract_number = input("\nIngrese el numero de contrato del proyecto a eliminar: ")
			deleteProject(db, contract_number)		

		if(opt == '4' and level == 1) or (opt == '3' and level == 2) or (opt == '1' and level == 3):
			printProjects(db)
		
		if(opt == '5' and level == 1) or (opt == '4' and level == 2) or (opt == '2' and level == 3):
			break
def tasks_console(db, level):
	while True:
		if level == 1:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear una tarea. \n - 2: si desea editar una tarea. \n - 3: si desea ingresar un fallo en una tarea. \n - 4: si desea ver las tareas actuales. \n - 5: para volver atrás. \n")
		if level == 2:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear una tarea. \n - 2: si desea editar una tarea. \n - 3: si desea ingresar un fallo en una tarea. \n - 4: si desea ver las tareas actuales. \n - 5: para volver atrás. \n")
		if level == 3:
			opt = input("\n Marque una de las siguientes opciones: \n - 1: si desea ver las tareas actuales. \n - 2: para volver atrás. \n")
		if(opt == '1' and (level == 1 or level == 2)):
			#id = input("\n Ingrese el ID de la tarea: ")
			id_skill = input("\n Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
			contract_number = input("\n Ingrese el número de contrato del proyecto asociado: ")
			original_initial_date = input("\n Ingrese la fecha estimada de inicio: ")
			original_end_date = input("\n Ingrese la fecha estimada de término: ")
			effective_initial_date = input("\n Ingrese la fecha efectiva de inicio, solo presione enter si no ha comenzado: ")
			if(effective_initial_date != ''):
				effective_end_date = input("\n Ingrese la fecha efectiva de término, solo presione enter si no ha terminado: ")
			else: 
				effective_initial_date=None
				effective_end_date=None
			original_initial_date=datetime.strptime(original_initial_date, '%Y-%m-%d')
			original_end_date=datetime.strptime(original_end_date, '%Y-%m-%d')
			createTask(db, id_skill, contract_number, original_initial_date, original_end_date, effective_initial_date, effective_end_date)
		if(opt == '2' and (level == 1 or level == 2)):
			id_edit = input("\n Ingrese el ID de la tarea que desea editar: ")
			new_id_skill = input("\n Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
			new_contract_number = input("\n Ingrese el número de contrato del proyecto asociado: ")
			new_original_initial_date = input("\n Ingrese la fecha estimada de inicio: ")
			new_original_end_date = input("\n Ingrese la fecha estimada de término: ")
			new_effective_initial_date= input("\n Ingrese la fecha efectiva de inicio, solo presione enter si no ha comenzado: ")
			if(new_effective_initial_date != ''):
				new_effective_end_date = input("\n Ingrese la fecha efectiva de término, solo presione enter si no ha terminado: ")
			else: 
				new_effective_initial_date=None
				new_effective_end_date=None
			new_original_initial_date=datetime.strptime(new_original_initial_date, '%Y-%m-%d')
			new_original_end_date=datetime.strptime(new_original_end_date, '%Y-%m-%d')
			editTask(db, id_edit, new_id_skill, new_contract_number, new_original_initial_date, new_original_end_date, new_effective_initial_date, new_effective_end_date)
		if(opt == '3' and (level == 1 or level == 2)):
			contract_number_fail = input("\n Ingrese el número de contrato del proyecto en el que ha fallado una tarea: ")
			id_skill_fail = input("\n Ingrese el ID de la habilidad asociada a la tarea (1: rect, 2: dis, 3: fab, 4: ins): ")
			fail_cost = input("\n Ingrese el costo estimado de la falla: ")
			failedTask(db, contract_number_fail, id_skill_fail, fail_cost)
		if(opt == '4' and (level == 1 or level == 2)) or (opt == '1' and level == 3):
			printTasks(db)
		if(opt == '5' and (level == 1 or level == 2)) or (opt == '2' and level == 3):
			break






















