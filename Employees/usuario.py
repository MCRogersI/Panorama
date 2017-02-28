from Employees.features import createEmployee, printEmployees, editEmployee, printEmployeesSkills, printSelectSkill, deleteEmployee

def employees_console(db, level):
#Es mejor importar las funciones en lugar de entregarsélas como parámetro a la función. Cambiar más adelante.

	while True:
		
		if level == 1:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear empleados. \n - 2: si desea editar empleados. \n - 3: si desea eliminar empleados \n - 4: para ver empleados actuales. \n - 5: para volver atrás. \n Ingrese la alternativa elegida: ")
		elif level == 2:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear empleados. \n - 2: si desea editar empleados.  \n - 3: para ver empleados actuales. \n - 4: para volver atrás. \n Ingrese la alternativa elegida: ")
		elif level == 3:
			opt = input("\n Marque una de las siguientes opciones: \n - 1: para ver empleados actuales. \n - 2: para volver atrás. \n Ingrese la alternativa elegida: ")

		if(opt == '1' and (level == 1 or level == 2)):
			#idEmpleado = input("\nIngrese el ID del empleado: ")
			nameEmpleado = input("Ingrese el nombre del empleado: ")
			zoneEmpleado = input("Ingrese el código de la zona del empleado: ")
			perf_rect = input("Ingrese el rendimiento histórico en rectificación del empleado, solo presione enter si no realiza esta labor: ")
			if(perf_rect == ''):
				perf_rect=None
			perf_des = input("Ingrese el rendimiento histórico en diseño del empleado, solo presione enter si no realiza esta labor: ")
			if(perf_des == ''):
				perf_des=None
			perf_fab = input("Ingrese el rendimiento histórico en fabricación del empleado, solo presione enter si no realiza esta labor: ")
			if(perf_fab == ''):
				perf_fab=None
			perf_ins = input("Ingrese el rendimiento histórico en instalación del empleado, solo presione enter si no realiza esta labor: ")
			if(perf_ins == ''):
				perf_ins=None	
			createEmployee(db, nameEmpleado, zoneEmpleado, perf_rect, perf_des, perf_fab, perf_ins)

		if(opt == '2' and (level == 1 or level == 2)):
			idEmpleado = input("\nIngrese el ID del empleado a editar: ")
			newName = input("\nIngrese el nuevo nombre del empleado, solo presione enter si lo mantiene: ")
			newZone = input("\nIngrese el código de la nueva zona del empleado, solo presione enter si la mantiene : ")
			newPerf_rect = input("\nIngrese el rendimiento histórico en rectificación del empleado, solo presione enter si mantiene la información actual: ")
			newPerf_des = input("\nIngrese el rendimiento histórico en diseño del empleado, solo presione enter mantiene la información actual: ")
			newPerf_fab = input("\nIngrese el rendimiento histórico en fabricación del empleado, solo presione enter si mantiene la información actual: ")
			newPerf_ins = input("\nIngrese el rendimiento histórico en instalación del empleado, solo presione enter si mantiene la información actual: ")
			if newName == '':
				newName = None
			if newZone == '':
				newZone = None
			if newPerf_rect == '':
				newPerf_rect=None
			if newPerf_des == '':
				newPerf_des = None
			if newPerf_fab == '':
				newPerf_fab = None
			if newPerf_ins == '':
				newPerf_ins = None
			editEmployee(db, idEmpleado,newName,newZone,newPerf_rect,newPerf_des,newPerf_fab,newPerf_ins)

		if(opt == '3' and level == 1):
			idEmpleado = input("\nIngrese el ID del empleado que desea eliminar: ")
			deleteEmployee(db, idEmpleado)

		if(opt == '4' and level == 1) or (opt == '3' and level == 2) or (opt == '1' and level == 3):
			opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: si desea ver empleados.  \n - 2: si desea ver la lista de rectificadores. \n - 3: si desea ver la lista de disenadores. \n - 4: si desea ver la lista de fabricadores. \n - 5: si desea ver la lista de instaladores. \n Ingrese la alternativa elegida: ")
			print('\n')
			if(opt_ver_empleados == '1'):
				printEmployees(db)
			if(opt_ver_empleados == '2'):
				printSelectSkill(db, 1)
			if(opt_ver_empleados == '3'):
				printSelectSkill(db, 2)
			if(opt_ver_empleados == '4'):
				printSelectSkill(db, 3)
			if(opt_ver_empleados == '5'):
				printSelectSkill(db, 4)

		if(opt == '5' and level == 1) or (opt == '4' and level == 2) or (opt == '2' and level ==3):
			break
