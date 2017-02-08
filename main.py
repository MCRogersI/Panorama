from pony.orm import *
from database import db
import datetime as d
import EmployeesTeams.features as ETf, EmployeesTeams.usuario as ETu
import Projects.usuario as Pu
import Projects.features as Pf

# ETf.CreateTeam(db,1 , 1, perf_rect= 1.2)
#Pf.CreateProject(db, 1, 'El retiro 851', 'No mas clavos', '30.173.254-0', 20, estimated_cost = 400,)
#Pf.DeleteProject(db, 1)
# Pf.CreateTask(db, 1, 1, 2, d.datetime(2014, 12, 1), d.datetime(2014,12,15))
# Pf.CreateTask(db, 2, 2, 2, d.datetime(2014, 12, 16), d.datetime(2014,12,17))
# Pf.CreateTask(db, 3, 3, 2, d.datetime(2014, 12, 18), d.datetime(2014,12,25))
# Pf.CreateTask(db, 4, 4, 2, d.datetime(2014, 12, 26), d.datetime(2014,12,31))

# Pf.EditTask(db, 1, efective_initial_date = d.datetime(2014, 1, 1), efective_end_date = d.datetime(2014, 1, 10))
# Pf.EditTask(db, 2, efective_initial_date = d.datetime(2014, 1, 11), efective_end_date = d.datetime(2014, 1, 15))
# Pf.EditTask(db, 3, efective_initial_date = d.datetime(2014, 1, 16))

# ETu.employees_teams_console(db, ETf.CreateEmployee, ETf.PrintEmployees, ETf.EditEmployee, ETf.CreateTeam, ETf.PrintTeams, ETf.PrintTeamsSkills, ETf.EditTeam, ETf.PrintSkills)
# Pf.AssignTask(db, 1, 1)
# Pf.DeleteTask(db,1)
# Pf.EditProject(db, 2 ,new_real_linear_meters = 400, new_real_cost = 8000)
# Pf.DeleteProject(db, 1)


#Pf.FailedTask(db, 2, 1, 1000)
while True:
		opt = input("\n Marque una de las siguientes opciones:\n - 1: Empleados/equipos. \n - 2: Proyectos. \n - 3: para salir. \n Ingrese la alternativa elegida: ")
		if(opt == '1'):
			ETu.employees_teams_console(db, ETf.CreateEmployee, ETf.PrintEmployees, ETf.EditEmployee, ETf.CreateTeam, ETf.PrintTeams, ETf.PrintTeamsSkills, ETf.EditTeam, ETf.PrintSelectSkill)
		if(opt == '2'):
			Pu.projects_console(db, Pf.CreateProject, Pf.PrintProjects, Pf.EditProject, Pf.DeleteProject)
		else:
			print("Has salido de la consola")
			break
			

