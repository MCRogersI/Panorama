def projects_console(db, CreateProject, PrintProjects, EditProject, DeleteProject):
	while True:
		opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear un proyecto. \n - 2: si desea editar un proyecto. \n - 3: para ver proyectos actuales. \n - 4: eliminar un proyecto. \n - 5: para salir. \n Ingrese la alternativa elegida: ")
		if(opt == '1'):
			contract_number = input("\nIngrese el numero de contrato: ")
			client_address = input("Ingrese la direccion del cliente: ")
			client_name = input("Ingrese el nombre del cliente: ")
			client_rut = input("Ingrese el RUT del cliente: ")
			linear_meters = input("Ingrese los metros lineales del proyecto: ")
			CreateProject(db, contract_number, client_address, client_name, client_rut, linear_meters)
		if(opt == '2'):
			contract_number = input("\nIngrese el numero de contrato del proyecto a editar: ")
			new_client_address = input("Ingrese la direccion del cliente: ")
			new_client_name = input("Ingrese el nombre del cliente: ")
			new_client_rut = input("Ingrese el RUT del cliente: ")
			new_linear_meters = input("Ingrese los metros lineales del proyecto: ")
			new_real_linear_meters = input("Ingrese los metros lineales (reales) del proyecto: ")
			new_real_cost = input("Ingrese el costo real del proyecto: ")
			EditProject(db, contract_number, new_client_address, new_client_name, new_client_rut, new_linear_meters, new_real_linear_meters, new_real_cost=new_real_cost)
		if(opt == '3'):
			contract_number = input("\nIngrese el numero de contrato del proyecto a eliminar: ")
			DeleteProject(db, contract_number)
		if(opt == '4'):
			PrintProjects(db)
		if(opt == '5'):
			break
