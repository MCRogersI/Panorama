from pony.orm import *
from database import db
import Employees.features as Ef, Employees.usuario as Eu
from datetime import date
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf
import Users.features as Uf
import Stock.features as Sf

Uf.createUser(db,'1', 1,'1')

# with db_session:
#     db.Skills(id=1, name='Rectification')
#     db.Skills(id=2, name='Design')
#     db.Skills(id=3, name='Fabrication')
#     db.Skills(id=4, name='Installation')
#
#     db.Difficulties(id=1, description='Construccion en altura')
#
#     db.Activities(id=1, description='Licencia')
#     db.Activities(id=2, description='Vacaciones')
#     db.Activities(id=3, description='Cliente ocupado')
    
# import Stock.reports
import Tests.Case9