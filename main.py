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
# import Users.features as Uf
import numpy as np
import getpass
import os

# para cambiar el tamaño de la ventana y el buffer de la consola
try:
    from win32console import PyConsoleScreenBufferType, GetStdHandle, STD_OUTPUT_HANDLE, PyCOORDType, PySMALL_RECTType

    # Get the standard output buffers.
    win_out = PyConsoleScreenBufferType(GetStdHandle(STD_OUTPUT_HANDLE))
    # Get largest console window size
    buffer_size = win_out.GetConsoleScreenBufferInfo()['Size']
    PyCOORD = win_out.GetLargestConsoleWindowSize()
    # Set console buffer and console window size
    win_out.SetConsoleScreenBufferSize(PyCOORDType(2*PyCOORD.X, 5*buffer_size.Y))
    Left = 0
    Right = PyCOORD.X - 1
    Top = 0
    Bottom = PyCOORD.Y - 1
    win_out.SetConsoleWindowInfo(True, PySMALL_RECTType(Left, Top, Right, Bottom))
    win_out.Close()
except:
    pass

def console(level, user):
    while True:
        if (level == 1):
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Empleados.\
                                                                  \n - 2: Proyectos. \
                                                                  \n - 3: Tareas. \
                                                                  \n - 4: Stock. \
                                                                  \n - 5: Planificacion. \
                                                                  \n - 6: Usuarios de consola.\
                                                                  \n - 7: Para salir. \
                                                                  \n Ingrese la alternativa elegida: ")
        elif (level in [2,3,4,5,6]):
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Empleados.\
                                                                  \n - 2: Proyectos. \
                                                                  \n - 3: Tareas. \
                                                                  \n - 4: Stock. \
                                                                  \n - 5: Para salir. \
                                                                  \n Ingrese la alternativa elegida: ")
        elif level == 7:
            opt2 = input("\n Marque una de las siguientes opciones:\n - 1: Obtener mi calendario de trabajo.\
                                                                  \n - 2: Ingresar hoja de corte. \
                                                                  \n - 3: Para salir. \
                                                                  \n Ingrese la alternativa elegida: ")
            if(opt2 == '1'):
                opt = '1'
            elif(opt2 == '2'):
                opt = '2'
            elif(opt2 == '3'):
                opt = '7'
            else:
                opt =''
        else:
            opt2 = input("\n Marque una de las siguientes opciones:\n - 1: Obtener mi calendario de trabajo.\
                                                                   \n - 2: Para salir. \
                                                                   \n Ingrese la alternativa elegida: ")
            if(opt2 == '1'):
                opt = '1'
            elif(opt2 == '2'):
                opt = '7'
            else:
                opt =''
            opt = '1'
        if(opt == '1'):
            Eu.employees_console(db, level, user)
        if(opt == '2'):
            Pu.projects_console(db, level)
        if( opt== '3'):
            if (level in [1,2,3,4,5,6]):
                Pu.tasks_console(db, level)
            else:
                print("\n Has salido del programa.")
                break
        if (opt == '4'):
            if (level in [1,2,5]):
                Su.stock_console(db, level)
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        if (opt =='5'):
            if (level == 1):
                PlanU.planning_console(db,level)
            elif level in [2,3,4,5,6]:
                print("\n Has salido del programa.")
                break
        if(opt=='6'):
            if(level == 1):
                Uu.users_console(db)
            else:
                print('\n Ingreso incorrecto.')
                input(' Presione Enter para continuar.')
        if(opt == '7'):
            if (level in [1,7,8]) :
                print("\n Has salido del programa.")
                break
            else:
                print('\n Ingreso incorrecto.')
                input(' Presione Enter para continuar.')
def signIn():
    while True:
        user = input(" Ingrese su usuario: ")
        if user == '':
            print("Debe ingresar un usuario.")
        else:
            # password = getpass.getpass(' Ingrese su contrasena: ')
            password = input(" Ingrese su contrasena: ")
            if Uf.checkPassEntry(db, user, password):
                with db_session:
                    level=Uf.getUserLevel(db, user)
                    console(level, user)
                break
            else:
                print(" Usuario y/o Contrasena incorrecto(s).")


signIn()








