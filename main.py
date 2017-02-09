from pony.orm import *
from database import db
from datetime import date
import Employees.features as Ef, Employees.usuario as Eu
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf

###############################################
# Tests de los features de Employees.features #
###############################################
# Ef.CreateEmployee(db, 1, "Juan", 1, perf_rect = 1)
# Ef.CreateEmployee(db, 2, "Pedro", 1, perf_rect = 2)
# Ef.CreateEmployee(db, 3, "Diego", 1, perf_rect = 3)
# Ef.CreateEmployee(db, 4, "Lalo", 1, perf_rect = 4)
# Ef.CreateEmployee(db, 5, "Mario", 1, perf_rect = 5)
# Ef.CreateEmployee(db, 6, "Hector", 1, perf_rect = 6)
# Ef.PrintEmployees(db)
# Ef.DeleteEmployee(db, 4)
# Ef.PrintEmployeesSkills(db)
# Ef.PrintSkills(db)
# Ef.PrintSelectSkill(db, 1)
# Ef.PrintSelectSkill(db, 2)
# Ef.PrintSelectSkill(db, 3)
# Ef.PrintSelectSkill(db, 4)
# Ef.EditEmployee(db, 1, new_zone = 2, perf_rect = 12)


###########################################################
# Tests de la parte de buscar fechas de Planning.features #
###########################################################

# dt = date(2017, 9, 11)
# print(PLf.SumDays(dt, 10))

print(PLf.GetAveragePerformance(db, 1))
print(PLf.GetAveragePerformance(db, 2))
print(PLf.GetAveragePerformance(db, 3))
print(PLf.GetAveragePerformance(db, 4))








#Pf.CreateProject(db, 1, 'El retiro 851', 'No mas clavos', '30.173.254-0', 20, estimated_cost = 400,)
#Pf.DeleteProject(db, 1)
# Pf.CreateTask(db, 1, 1, 2, d.datetime(2014, 12, 1), d.datetime(2014,12,15))
# Pf.CreateTask(db, 2, 2, 2, d.datetime(2014, 12, 16), d.datetime(2014,12,17))
# Pf.CreateTask(db, 3, 3, 2, d.datetime(2014, 12, 18), d.datetime(2014,12,25))
# Pf.CreateTask(db, 4, 4, 2, d.datetime(2014, 12, 26), d.datetime(2014,12,31))

# Pf.EditTask(db, 1, efective_initial_date = d.datetime(2014, 1, 1), efective_end_date = d.datetime(2014, 1, 10))
# Pf.EditTask(db, 2, efective_initial_date = d.datetime(2014, 1, 11), efective_end_date = d.datetime(2014, 1, 15))
# Pf.EditTask(db, 3, efective_initial_date = d.datetime(2014, 1, 16))

# Eu.employees_teams_console(db, Ef.CreateEmployee, Ef.PrintEmployees, Ef.EditEmployee, Ef.CreateTeam, Ef.PrintTeams, Ef.PrintTeamsSkills, Ef.EditTeam, Ef.PrintSkills)
# Pf.AssignTask(db, 1, 1)
# Pf.DeleteTask(db,1)
# Pf.EditProject(db, 2 ,new_real_linear_meters = 400, new_real_cost = 8000)
# Pf.DeleteProject(db, 1)


#Pf.FailedTask(db, 2, 1, 1000)
# while True:
		# opt = input("\n Marque una de las siguientes opciones:\n - 1: Empleados. \n - 2: Proyectos. \n - 3: Tareas. \n - 4: para salir. \n Ingrese la alternativa elegida: ")
		# if(opt == '1'):
			# Eu.employees_console(db, Ef.CreateEmployee, Ef.PrintEmployees, Ef.EditEmployee, Ef.PrintEmployeesSkills, Ef.PrintSelectSkill, Ef.DeleteEmployee)
		# if(opt == '2'):
			# Pu.projects_console(db, Pf.CreateProject, Pf.PrintProjects, Pf.EditProject, Pf.DeleteProject)
		# if( opt== '3'):
			# Pu.tasks_console(db, Pf.CreateTask, Pf.EditTask, Pf.AssignTask, Pf.PrintTasks, Pf.FailedTask)
		# else:
			# print("Has salido de la consola")
			# break

