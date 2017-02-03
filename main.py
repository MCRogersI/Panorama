from pony.orm import *
from database import db
import EmployeesTeams.features as ETf


ETf.CreateTeam(db,1 , 1, perf_rect= 1.2)
# Etf.CreateEmployee(id, name, team_id, rect, des, fab, inst):
