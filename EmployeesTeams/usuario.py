def employees_teams_console(db, CreateEmployee, PrintEmployees, EditEmployee, CreateTeam, PrintTeams, PrintTeamsSkills, EditTeam, PrintSelectSkill):
	while True:
		opt = input("\n Marque una de las siguientes opciones:\n - 1: si desea crear empleados/equipos. \n - 2: si desea editar empleados/equipos. \n - 3: para ver empleados/equipos actuales \n - 4: para salir. \n Ingrese la alternativa elegida: ")
		if(opt == '1'):
			opt1 = input("\n Marque una de las siguientes opciones: \n - 1: si desea crear empleado. \n - 2: si desea crear un equipo. \n Ingrese la alternativa elegida: ")
			if(opt1 == '1'):
				idEmpleado = input("\nIngrese el ID del empleado: ")
				nameEmpleado = input("Ingrese el nombre del empleado: ")
				teamEmpleado = input("Ingrese el ID del equipo del empleado: ")
				rect = input("Ingrese 1 si el empleado es un rectificador, 0 si no: ")
				des = input("Ingrese 1 si el empleado es un diseñador, 0 si no: ")
				fab = input("Ingrese 1 si el empleado es un fabricador, 0 si no: ")
				ins = input("Ingrese 1 si el empleado es un instalador, 0 si no: ")
				if(rect == '1'):
					rectB = True
				else: 
					rectB = False
				if(des == '1'):
					desB = True
				else: 
					desB = False
				if(fab == '1'):
					fabB = True
				else: 
					fabB = False
				if(ins == '1'):
					insB = True
				else: 
					insB = False
				CreateEmployee(db, idEmpleado,nameEmpleado,teamEmpleado,rectB,desB,fabB,insB)
			if(opt1 == '2'):
				id_team = input("\nIngrese el ID del equipo: ")
				zone = input("Ingrese la zona del equipo: ")
				perf_rect = input("Ingrese 0 si el equipo no hace rectificación, en otro caso ingrese el rendimiento histórico: ")
				perf_des = input("Ingrese 0 si el equipo no hace diseño, en otro caso ingrese el rendimiento histórico: ")
				perf_fab = input("Ingrese 0 si el equipo no hace fabricación, en otro caso ingrese el rendimiento histórico: ")
				perf_ins = input("Ingrese 0 si el equipo no hace instalación, en otro caso ingrese el rendimiento histórico: ")
				if(perf_rect == '0'):
					perf_rect = None
				if(perf_des == '0'):
					perf_des = None            
				if(perf_fab == '0'):
					perf_fab = None
				if(perf_ins == '0'):
					perf_ins = None
				CreateTeam(db, id_team, zone, perf_rect, perf_des, perf_fab, perf_ins)			
		if(opt == '2'):
			opt2 = input("\n Marque una de las siguientes opciones: \n - 1: si desea editar empleado. \n - 2: si desea editar un equipo. \n Ingrese la alternativa elegida: ")
			if(opt2 == '1'):
				idEmpleado2 = input("\nIngrese el ID del empleado a editar: ")
				newName = input("Ingrese el nuevo nombre del empleado, 0 si lo mantiene: ")
				newTeamId = input("Ingrese el nuevo ID de equipo del empleado, 0 si lo mantiene: ")
				newRect = input("Ingrese 1 si el empleado es rectificador, 0 si no: ")
				newDes = input("Ingrese 1 si el empleado es diseñador, 0 si no: ")    
				newFab = input("Ingrese 1 si el empleado es fabricador, 0 si no: ")
				newIns = input("Ingrese 1 si el empleado es instalador, 0 si no: ")
				if newName == '0':
					newName = None
				if newTeamId == '0':
					newTeamId = None
				if newRect == '0':
					newRect = None
				else:
					newRect = True
				if newDes == '0':
					newDes = None
				else:
					newDes = True
				if newFab == '0':
					newFab = None
				else:
					newFab = True
				if newIns == '0':
					newIns = None
				else:
					newIns = True
				EditEmployee(db, idEmpleado2,newName,newTeamId,newRect,newDes,newFab,newIns)
			if(opt2=='2'):
				idEquipo2 = input("\nIngrese el ID del equipo que desea editar: ")
				newZone = input("Ingrese la nueva zona del equipo, 0 si la mantiene: ")
				newPerfRect = input("Ingrese el rendimiento histórico del equipo en rectificación, 0 si no realiza esta tarea: ")
				newPerfDes = input("Ingrese el rendimiento histórico del equipo en diseño, 0 si no realiza esta tarea: ")
				newPerfFab = input("Ingrese el rendimiento histórico del equipo en fabricación, 0 si no realiza esta tarea: ")
				newPerfIns = input("Ingrese el rendimiento histórico del equipo en instalación, 0 si no realiza esta tarea: ")
				if(newZone == '0'):
					newZone = None
				if(newPerfRect == '0'):
					newPerfRect = None
				if(newPerfDes == '0'):
					newPerfDes = None            
				if(newPerfFab == '0'):
					newPerfFab = None
				if(newPerfIns == '0'):
					newPerfIns = None
				EditTeam(db, idEquipo2,newZone,newPerfRect,newPerfDes,newPerfFab,newPerfIns)
		if(opt == '3'):
			opt3 = input("\n Marque una de las siguientes opciones: \n - 1: si desea ver empleados. \n - 2: si desea ver equipos. \n - 3: si desea ver la lista de rectificadores. \n - 4: si desea ver la lista de disenadores. \n - 5: si desea ver la lista de fabricadores. \n - 6: si desea ver la lista de instaladores. \n Ingrese la alternativa elegida: ")
			print('\n')
			if(opt3 == '1'):
				PrintEmployees(db)
			if(opt3 == '2'):
				PrintTeams(db)
			if(opt3 == '3'):
				PrintSelectSkill(db, 3)
			if(opt3 == '4'):
				PrintSelectSkill(db, 4)
			if(opt3 == '5'):
				PrintSelectSkill(db, 5)
			if(opt3 == '6'):
				PrintSelectSkill(db, 6)
		if(opt == '4'):
			break
