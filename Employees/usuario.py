from Employees.features import createEmployee, printEmployees, editEmployee, printEmployeesSkills, printSelectSkill, deleteEmployee
from Projects.features import createEmployeeActivity, deleteEmployeeActivity, printEmployeesActivities

def employees_console(db, level):
#Es mejor importar las funciones en lugar de entregarsélas como parámetro a la función. Cambiar más adelante.

	while True:
		
		if level == 1:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear nuevo empleado. \n - 2: si desea editar datos de empleados. \n - 3: si desea eliminar un empleado. \n - 4: para manejar vacaciones/periodos de licencia de los empleados. \n - 5: para ver empleados actuales. \n - 6: para volver atrás. \n Ingrese la alternativa elegida: ")
		elif level == 2:
			opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear nuevo empleado. \n - 2: si desea editar datos de empleados. \n - 3: para manejar vacaciones/periodos de licencia de los empleados. \n - 4: para ver empleados actuales. \n - 5: para volver atrás. \n Ingrese la alternativa elegida: ")
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
			editEmployee(db, idEmpleado, newName, newZone, newPerf_rect, newPerf_des, newPerf_fab, newPerf_ins)

		if(opt == '3' and level == 1):
			idEmpleado = input("\nIngrese el ID del empleado que desea eliminar: ")
			deleteEmployee(db, idEmpleado)
		
		if(opt == '4' and level == 1) or (opt == '3' and level == 2):
			opt_employees_activities = input("\n Marque una de las siguientes opciones: \n - 1: si desea ingresar datos de una actividad. \n - 2: si desea eliminar una actividad. \n - 3: si desea ver la lista actual de actividades.\n Ingrese la alternativa elegida: ")
			
			if opt_employees_activities == '1':
				activity = input("\n Marque una de las siguientes opciones: \n - 1: si desea ingresar datos de vacaciones. \n - 2: si desea ingresar datos de licencia. \n - 3: si desea ingresar otro tipo de dato.\n Ingrese la alternativa elegida: ")
				employee = input(" Ingrese el ID del empleado asociado a la actividad elegida: ")
				initial_year = input(" Ingrese el año en que comienza la actividad: ")
				initial_month = input(" Ingrese el mes en que comienza la actividad: ")
				initial_day = input(" Ingrese el día en que comienza la actividad: ")
				end_year = input(" Ingrese el año en que termina la actividad: ")
				end_month = input(" Ingrese el mes en que termina la actividad: ")
				end_day = input(" Ingrese el día en que termina la actividad: ")
				createEmployeeActivity(db, employee, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day)
			
			elif opt_employees_activities == '2':
				id = input("\n Ingrese el ID de la actividad que quiere eliminar: ")
				deleteEmployeeActivity(db, id)
				
			elif opt_employees_activities == '3':
				print('\n')
				printEmployeesActivities(db)
			
			
		if(opt == '5' and level == 1) or (opt == '4' and level == 2) or (opt == '1' and level == 3):
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

		if(opt == '6' and level == 1) or (opt == '5' and level == 2) or (opt == '2' and level ==3):
			break
