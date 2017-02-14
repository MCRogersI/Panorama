from pony.orm import *
from database import db
import Employees.features as Ef, Employees.usuario as Eu
from datetime import date
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf

#POR AHORA EJECUTAR LOS SIGUIENTES COMANDOS EN LA CONSOLA HABIENDO ACCEDIDO
# A LA BASE DE DATOS:
#'drop schema public cascade'
# 'create schema public'


with db_session:
	db.Skills(id=1, name='Rectifier')
	db.Skills(id=2, name='Designer')
	db.Skills(id=3, name='Fabricator')
	db.Skills(id=4, name='Installer')

	db.Difficulties(id=1, description='Construccion en altura')

	db.Activities(id=1, description='Licencia')
	db.Activities(id=2, description='Vacaciones')
	db.Activities(id=3, description='Cliente ocupado')

##############################################
# Lista de prueba de proyectos test case 1 #
##############################################

Pf.CreateProject(db, 1, 'Manuel Montt 1235', 'Providencia', 'Pedro Sánchez',
				 '17.094.362-0', 15, date(2017, 5, 27), estimated_cost = 200)
Pf.CreateProject(db, 2, 'Suecia 86', 'Las Condes', 'Franco Soto',
				 '16.224.112-0', 20, date(2017, 6, 6), estimated_cost = 300)
Pf.CreateProject(db, 3, 'Barros Luco 997', 'Puente Alto', 'Miguel Acevedo',
				 '15.114.992-0',
				 30, date(2017, 6, 2), estimated_cost = 150)

with db_session:
	#Definición de las prioridades de los distintos proyectos
	db.Projects[3].priority = 1
	db.Projects[1].priority = 2
	db.Projects[2].priority = 3
	#Fijación de proyectos
	db.Projects[2].fixed_planning = True



#################################################
#        Lista de empleados test case 1 		#
# ###############################################

Ef.CreateEmployee(db, 1, "Juan", 1, perf_rect = 1)
Ef.CreateEmployee(db, 2, "Pedro", 2, perf_des = 2)
Ef.CreateEmployee(db, 3, "Diego", 2, perf_fab = 3)
Ef.CreateEmployee(db, 4, "Miguel", 1, perf_inst = 4)
Ef.CreateEmployee(db, 5, "Mario", 1, perf_rect = 5)
Ef.CreateEmployee(db, 6, "Felipe", 2, perf_des = 6)
Ef.CreateEmployee(db, 7, "Miguel", 1, perf_fab = 4)
Ef.CreateEmployee(db, 8, "Mario", 1, perf_inst = 5)
Ef.CreateEmployee(db, 9, "Felipe", 2, perf_rect = 6)
Ef.CreateEmployee(db, 10, "Miguel", 1, perf_des = 4)
Ef.CreateEmployee(db, 11, "Mario", 1, perf_fab = 5)
Ef.CreateEmployee(db, 12, "Felipe", 1, perf_inst = 6)


##############################################
# Lista de prueba de tasks test case 1 		 #
##############################################

Pf.CreateTask(db, 1, 1, 1, original_initial_date=date(2017, 4, 8), original_end_date=date(2017,2,28))
Pf.CreateTask(db, 2, 2, 1, original_initial_date=date(2017, 4, 15), original_end_date=date(2017,3,1))
Pf.CreateTask(db, 3, 3, 1, original_initial_date=date(2017, 4, 20), original_end_date=date(2017,3,8))
Pf.CreateTask(db, 4, 4, 1, original_initial_date=date(2017, 4, 28), original_end_date=date(2017,12,14))
Pf.CreateTask(db, 5, 1, 2, original_initial_date=date(2017, 4, 3), original_end_date=date(2017,2,28))
Pf.CreateTask(db, 6, 2, 2, original_initial_date=date(2017, 4, 12), original_end_date=date(2017,3,1))
Pf.CreateTask(db, 7, 3, 2, original_initial_date=date(2017, 4, 16), original_end_date=date(2017,3,8))
Pf.CreateTask(db, 8, 4, 2, original_initial_date=date(2017, 4, 26), original_end_date=date(2017,12,14))
Pf.CreateTask(db, 9, 1, 3, original_initial_date=date(2017, 4, 20), original_end_date=date(2017,2,28))
Pf.CreateTask(db, 10, 2, 3, original_initial_date=date(2017, 5, 10), original_end_date=date(2017,3,1))
Pf.CreateTask(db, 11, 3, 3, original_initial_date=date(2017, 5, 15), original_end_date=date(2017,3,8))
Pf.CreateTask(db, 12, 4, 3, original_initial_date=date(2017, 5, 20), original_end_date=date(2017,12,14))

PLf.AssignTask(db, 1, 1, initial_date=date(2017, 4, 8), end_date=date(2017,2,28))
PLf.AssignTask(db, 5, 5,  initial_date=date(2017, 4, 15), end_date=date(2017,3,1))
PLf.AssignTask(db, 9, 9,  initial_date=date(2017, 4, 20), end_date=date(2017,3,8))
PLf.AssignTask(db, 2, 2,  initial_date=date(2017, 4, 28), end_date=date(2017,12,14))
PLf.AssignTask(db, 6, 6,  initial_date=date(2017, 4, 3), end_date=date(2017,2,28))
PLf.AssignTask(db, 10, 10,  initial_date=date(2017, 4, 12), end_date=date(2017,3,1))
PLf.AssignTask(db, 3, 3,  initial_date=date(2017, 4, 16), end_date=date(2017,3,8))
PLf.AssignTask(db, 7, 7,  initial_date=date(2017, 4, 26), end_date=date(2017,12,14))
PLf.AssignTask(db, 11, 11,  initial_date=date(2017, 4, 20), end_date=date(2017,2,28))
PLf.AssignTask(db, [4,8], 4,  initial_date=date(2017, 5, 10), end_date=date(2017,3,1))
PLf.AssignTask(db, [4,8,12], 8, initial_date=date(2017, 5, 15), end_date=date(2017,3,8))
PLf.AssignTask(db, 12, 12,  initial_date=date(2017, 5, 20), end_date=date(2017,12,14))

with db_session:
	#Definición de fechas de inicio efectivas para algunas tareas
	db.Tasks[1].effective_initial_date = date(2017, 4, 8)
	db.Tasks[5].effective_initial_date = date(2017, 4, 15)
	db.Tasks[9].effective_initial_date = date(2017, 4, 18)

PLf.DoPlanning(db)







