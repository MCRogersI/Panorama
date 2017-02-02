from features import *


opt=input("Marque:\n 1 si desea crear empleados/equipos \n 2 si desea editar empleados/equipos \n 3 para ver empleados/equipos actuales \n ")
if(opt=='1'):
    opt1=input("Marque \n 1 si desea crear empleado \n 2 si desea crear un equipo\n")
    if(opt1=='1'):
#el usuario debe entregar siempre un string con id,nombre,teamid,True,False,True,True (ejemplo)
        emp=input("Ingrese las características del empleado: ")
        CreateEmployee(emp.split(",")[0],emp.split(",")[1],emp.split(",")[2],emp.split(",")[3],emp.split(",")[4],emp.split(",")[5],emp.split(",")[6])
        #print(emp.split(",")[0],emp.split(",")[1],emp.split(",")[2],emp.split(",")[3])
if(opt=='2'):
#de esta forma deberia entregar siempre todas las características del usuario
    opt2=input("Marque \n 1 si desea editar empleado \n 2 si desea editar un equipo")
    if(opt2=='1'):
        emp2=input("Ingrese las características nuevas del empleado")
if(opt=='3'):
    opt3=input("Marque \n 1 si desea ver empleados \n 2 si desea ver equipos")
    if(opt3=='1'):
        PrintEmployees()


