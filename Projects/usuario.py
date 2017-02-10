def projects_console(db, CreateProject, PrintProjects, EditProject, DeleteProject):
	while True:
		opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear un proyecto. \n - 2: si desea editar un proyecto. \n - 3: para ver proyectos actuales. \n - 4: eliminar un proyecto. \n - 5: para volver atrás. \n Ingrese la alternativa elegida: ")
		if(opt == '1'):
			contract_number = input("\nIngrese el numero de contrato: ")
			client_address = input("Ingrese la direccion del cliente: ")
			client_comuna = input("Ingrese la comuna del cliente: ")
			client_name = input("Ingrese el nombre del cliente: ")
			client_rut = input("Ingrese el RUT del cliente: ")
			linear_meters = input("Ingrese los metros lineales del proyecto: ")
			deadline = input("ingrese la fecha de entrega pactada del proyecto")
			CreateProject(db, contract_number, client_address, client_comuna, client_name, client_rut, linear_meters, deadline)
		if(opt == '2'):
			contract_number = input("\nIngrese el numero de contrato del proyecto a editar: ")
			new_client_address = input("Ingrese la direccion del cliente: ")
			new_client_comuna = input("Ingrese la comuna del cliente: ")
			new_client_name = input("Ingrese el nombre del cliente: ")
			new_client_rut = input("Ingrese el RUT del cliente: ")
			new_linear_meters = input("Ingrese los metros lineales del proyecto: ")
			new_real_linear_meters = input("Ingrese los metros lineales (reales) del proyecto: ")
			new_real_cost = input("Ingrese el costo real del proyecto: ")
			EditProject(db, contract_number, new_client_address, new_client_comuna, new_client_name, new_client_rut, new_linear_meters, new_real_linear_meters, new_real_cost=new_real_cost)
		if(opt == '3'):
			PrintProjects(db)
		if(opt == '4'):
			contract_number = input("\nIngrese el numero de contrato del proyecto a eliminar: ")
			DeleteProject(db, contract_number)
		if(opt == '5'):
			break
def tasks_console(db, CreateTask, EditTask, PrintTasks, FailedTask):
	while True:
		opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear una tarea. \n - 2: si desea editar una tarea. \n - 3: si desea ingresar un fallo en una tarea. \n - 4: si desea ver las tareas actuales. \n - 5: para volver atrás. \n")
		if(opt == '1'):
			id = input("\n Ingrese el ID de la tarea: ")
			id_skill = input("\n Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
			id_project = input("\n Ingrese el ID del proyecto asociado: ")
			original_initial_date = input("\n Ingrese la fecha estimada de inicio: ")
			original_end_date = input("\n Ingrese la fecha estimada de término: ")
			efective_initial_date = input("\n Ingrese la fecha efectiva de inicio, 0 si no ha comenzado: ")
			if(efective_initial_date != 0):
				efective_end_date = input("\n Ingrese la fecha efectiva de término, 0 si no ha terminado: ")
			else: 
				efective_initial_date=None
				efective_end_date=None
			CreateTask(db, id, id_skill, id_project, original_initial_date, original_end_date, efective_initial_date, efective_end_date)
		if(opt == '2'):
			id_edit = input("\n Ingrese el ID de la tarea que desea editar: ")
			new_id_skill = input("\n Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
			new_id_project = input("\n Ingrese el ID del proyecto asociado: ")
			new_original_initial_date = input("\n Ingrese la fecha estimada de inicio: ")
			new_original_end_date = input("\n Ingrese la fecha estimada de término: ")
			new_efective_initial_date= input("\n Ingrese la fecha efectiva de inicio, 0 si no ha comenzado: ")
			if(new_efective_initial_date != 0):
				new_efective_end_date = input("\n Ingrese la fecha efectiva de término, 0 si no ha terminado: ")
			else: 
				new_efective_initial_date=None
				new_efective_end_date=None
			EditTask(db, id_edit, new_id_skill, new_id_project, new_original_initial_date, new_original_end_date, new_efective_initial_date, new_efective_end_date)
		if(opt == '3'):
			id_project_fail = input("\n Ingrese el ID del proyecto en el que ha fallado una tarea: ")
			id_skill_fail = input("\n Ingrese el ID de la habilidad asociada a la tarea (1: rect, 2: dis, 3: fab, 4: ins): ")
			fail_cost = input("\n Ingrese el costo estimado de la falla: ")
			FailedTask(db, id_project_fail, id_skill_fail, fail_cost)
		if(opt == '4'):
			PrintTasks(db)
		if(opt == '5'):
			break






















