def employees_console(db, CreateEmployee, PrintEmployees, EditEmployee, PrintEmployeesSkills, PrintSelectSkill, DeleteEmployee, level):
#Es mejor importar las funciones en lugar de entregarsélas como parámetro a la función. Cambiar más adelante.

	while True:
		if level == 1:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear empleados. \n - 2: si desea editar empleados. \n - 3: si desea eliminar empleados \n - 4: para ver empleados actuales. \n - 5: para volver atrás. \n Ingrese la alternativa elegida: ")
		if level == 2:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear empleados. \n - 2: si desea editar empleados.  \n - 3: para ver empleados actuales. \n - 4: para volver atrás. \n Ingrese la alternativa elegida: ")
		if level == 3:
			opt = input("\n Marque una de las siguientes opciones: \n - 1: para ver empleados actuales. \n - 2: para volver atrás. \n Ingrese la alternativa elegida: ")
		if(opt == '1' and (level == 1 or level == 2)):
			idEmpleado = input("\nIngrese el ID del empleado: ")
			nameEmpleado = input("Ingrese el nombre del empleado: ")
			zoneEmpleado = input("Ingrese el código de la zona del empleado: ")
			perf_rect = input("Ingrese el rendimiento histórico en rectificación del empleado, ingrese 0 si no realiza esta labor: ")
			if(perf_rect == '0'):
				perf_rect=None
			perf_des = input("Ingrese el rendimiento histórico en diseño del empleado, ingrese 0 si no realiza esta labor: ")
			if(perf_des == '0'):
				perf_des=None
			perf_fab = input("Ingrese el rendimiento histórico en fabricación del empleado, ingrese 0 si no realiza esta labor: ")
			if(perf_fab == '0'):
				perf_fab=None
			perf_ins = input("Ingrese el rendimiento histórico en instalación del empleado, ingrese 0 si no realiza esta labor: ")
			if(perf_ins == '0'):
				perf_ins=None	
			CreateEmployee(db, idEmpleado, nameEmpleado, zoneEmpleado, perf_rect, perf_des, perf_fab, perf_ins)						
		if(opt == '2' and (level == 1 or level == 2)):
			idEmpleado2 = input("\nIngrese el ID del empleado a editar: ")
			newName = input("\nIngrese el nuevo nombre del empleado, ingrese 0 si lo mantiene: ")
			newZone = input("\nIngrese el código de la nueva zona del empleado, ingrese 0 si la mantiene : ")
			newPerf_rect = input("\nIngrese el rendimiento histórico en rectificación del empleado, ingrese 0 si mantiene la información actual: ")
			newPerf_des = input("\nIngrese el rendimiento histórico en diseño del empleado, ingrese 0 mantiene la información actual: ")   
			newPerf_fab = input("\nIngrese el rendimiento histórico en fabricación del empleado, ingrese 0 si mantiene la información actual: ")
			newPerf_ins = input("\nIngrese el rendimiento histórico en instalación del empleado, ingrese 0 si mantiene la información actual: ")
			if newName == '0':
				newName = None
			if newZone == '0':
				newZone = None
			if newPerf_rect == '0':
				newPerf_rect=None
			if newPerf_des == '0':
				newPerf_des = None
			if newPerf_fab == '0':
				newPerf_fab = None
			if newPerf_ins == '0':
				newPerf_ins = None
			EditEmployee(db, idEmpleado2,newName,newZone,newPerf_rect,newPerf_des,newPerf_fab,newPerf_ins)
		if(opt == '3' and level == 1):
			idEmpleado3 = input("\nIngrese el ID del empleado que desea eliminar: ")
			DeleteEmployee(db, idEmpleado3)		
		if(opt == '4' and level == 1) or (opt == '3' and level == 2) or (opt == '1' and level == 3):
			opt3 = input("\n Marque una de las siguientes opciones: \n - 1: si desea ver empleados.  \n - 2: si desea ver la lista de rectificadores. \n - 3: si desea ver la lista de disenadores. \n - 4: si desea ver la lista de fabricadores. \n - 5: si desea ver la lista de instaladores. \n Ingrese la alternativa elegida: ")
			print('\n')
			if(opt3 == '1'):
				PrintEmployees(db)
			if(opt3 == '2'):
				PrintSelectSkill(db, 1)
			if(opt3 == '3'):
				PrintSelectSkill(db, 2)
			if(opt3 == '4'):
				PrintSelectSkill(db, 3)
			if(opt3 == '5'):
				PrintSelectSkill(db, 4)
		if(opt == '5' and level == 1) or (opt == '4' and level == 2) or (opt == '2' and level ==3):
			break
