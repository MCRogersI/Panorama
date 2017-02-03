from pony.orm import *
from database import db
import EmployeesTeams.features as ETf, EmployeesTeams.usuario as ETu
import Projects.features as Pf


# ETf.CreateTeam(db,1 , 1, perf_rect= 1.2)
Pf.PrintProjects(db)
#ETu.employees_teams_console(db, ETf.CreateEmployee, ETf.PrintEmployees, ETf.EditEmployee, ETf.CreateTeam, ETf.PrintTeams, ETf.PrintTeamsSkills, ETf.EditTeam, ETf.PrintSkills)
