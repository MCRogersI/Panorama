from pony.orm import *
from database import db
import datetime as d
import EmployeesTeams.features as ETf, EmployeesTeams.usuario as ETu
import Projects.features as Pf

# ETf.CreateTeam(db,1 , 1, perf_rect= 1.2)
# Pf.CreateProject(db, 1, 'El retiro 851', 'No mas clavos', '30.173.254-0', 20, estimated_cost = 400,)
#Pf.CreateTask(db, 3, 1, 3, d.datetime(2014, 12, 1), d.datetime(2014,12,15))
Pf.CreateTask(db, 4, 2, 1, d.datetime(2014, 12, 16), d.datetime(2014,12,17))
Pf.CreateTask(db, 5, 3, 1, d.datetime(2014, 12, 18), d.datetime(2014,12,25))
Pf.CreateTask(db, 6, 4, 1, d.datetime(2014, 12, 26), d.datetime(2014,12,31))
# ETu.employees_teams_console(db, ETf.CreateEmployee, ETf.PrintEmployees, ETf.EditEmployee, ETf.CreateTeam, ETf.PrintTeams, ETf.PrintTeamsSkills, ETf.EditTeam, ETf.PrintSkills)

