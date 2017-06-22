from distutils.core import setup
import py2exe
import main
from pony.orm import *
from database import db
from datetime import date
# import initialize.py
# import Employees.features as Ef
import Employees.usuario as Eu   #, Employees.reports as Er
import Projects.usuario as Pu
# import Projects.features as Pf
# import Planning.features as PLf
# import Planning.reports as PLr
import Users.features as Uf
import Stock.usuario as Su
# import Tests.Case9 as case9
import Planning.usuario as PlanU
# import Stock.reports as Sr
# import Stock.features as Sf
import Users.usuario as Uu
import numpy as np
import getpass
import os

setup(console=['main.py'])