from pony.orm import *
from database import db
import EmployeesTeams.features as ETf
import Projects.features as Pf


# ETf.CreateTeam(db,1 , 1, perf_rect= 1.2)
Pf.PrintProjects(db)
