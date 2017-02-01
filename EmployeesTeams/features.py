from pony.orm import *
from models import Employees, Skills, Teams, Teams_Skills

def CreateEmployee(id, name, team_id):
    with db_session:
        Employees(id=id, name=name, team_id=team_id)
