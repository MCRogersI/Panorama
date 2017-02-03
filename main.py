from pony.orm import *
from database import db
import EmployeesTeams.features as ETf, EmployeesTeams.usuario as ETu

ETu.employees_teams_console(db, ETf.CreateEmployee, ETf.PrintEmployees, ETf.EditEmployee, ETf.CreateTeam, ETf.PrintTeams, ETf.PrintTeamsSkills, ETf.EditTeam, ETf.PrintSkills)
