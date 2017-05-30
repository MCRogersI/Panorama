from pony.orm import *
from database import db
from datetime import date
import Employees.features as Ef, Employees.usuario as Eu   #, Employees.reports as Er
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf
import Planning.reports as PLr
import Users.features as Uf
import Stock.usuario as Su
# import Tests.Case9 as case9
import Planning.usuario as PlanU
import Stock.reports as Sr
import Stock.features as Sf
import Users.usuario as Uu
import numpy as np
import getpass
import os
# Uf.createUser(db,'1', 1,'1')
# Uf.createUser(db,'2', 2,'2')
# Uf.createUser(db,'3', 3,'3')
# Uf.createUser(db,'4', 4,'4')
# Uf.createUser(db,'5', 5,'5')
# Uf.createUser(db,'6', 6,'6')
# Uf.createUser(db,'7', 7,'7')
# Uf.createUser(db,'8', 8,'8')
# Uf.createUser(db,'9', 9,'9')



def console(level, user):
    while True:
        if (level in [1,2,3,4,5]):
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Empleados.\
                                                                  \n - 2: Proyectos. \
                                                                  \n - 3: Tareas. \
                                                                  \n - 4: Stock. \
                                                                  \n - 5: Planificación \
                                                                  \n - 6: Usuarios de consola\
                                                                  \n - 7: Para salir. \
                                                                  \n Ingrese la alternativa elegida: ")
        else:
            opt2 = input("\n Marque una de las siguientes opciones:\n - 1: Obtener mi calendario de trabajo.\
                                                                  \n - 2: Ingresar hoja de corte. \
                                                                  \n - 3: Para salir. \
                                                                  \n Ingrese la alternativa elegida: ")
            if(opt2 == '1'):
                print('holi')
                opt = '1'
            elif(opt2 == '2'):
                opt = '2'
            elif(opt2 == '3'):
                opt = '7'
            else:
                opt =''
        if(opt == '1'):
            Eu.employees_console(db, level, user)
        if(opt == '2'):
            Pu.projects_console(db, level)
        if( opt== '3'):
            if (level in [1,2,3,4,5]):
                Pu.tasks_console(db, level)
            else:
                print('\n Acceso denegado. \n')
                input(' Presione una tecla para continuar: ')
        if (opt == '4'):
            if (level == 1):
                Su.stock_console(db, level)
            else:
                print('\n Acceso denegado. \n')
                input(' Presione una tecla para continuar: ')
        if (opt =='5'):
            if (level == 1):
                PlanU.planning_console(db,level)
            else:
                print('\n Acceso denegado. \n')
                input(' Presione una tecla para continuar: ')
        if(opt=='6'):
            if(level ==1):
                Uu.users_console(db)
            else:
                print('\n Acceso denegado. \n')
                input(' Presione una tecla para continuar: ')
        if(opt == '7'):
            print("\n Has salido del programa.")
            break
def signIn():
    while True:
        user = input(" Ingrese su usuario: ")
        # password = input("Ingrese su contraseña: ")
        password = getpass.getpass(' Ingrese su contraseña: ')
        if Uf.checkPassEntry(db, user, password):
            with db_session:
                level=Uf.getUserLevel(db, user)
                console(level, user)
                
        else:
            print(" Usuario y/o Contraseña incorrecto(s))")
        break
# os.system("mode con cols=100 lines=30")
signIn()
