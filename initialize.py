from pony.orm import *
from database import db
import Employees.features as Ef, Employees.usuario as Eu
from datetime import date
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf
import Users.features as Uf
import Stock.features as Sf

#POR AHORA EJECUTAR LOS SIGUIENTES COMANDOS EN LA CONSOLA HABIENDO ACCEDIDO
# A LA BASE DE DATOS:
#'drop schema public cascade'
# 'create schema public'

Uf.createUser(db,'Alberto',1,'123')
Uf.createUser(db,'Juan',2,'456')
Uf.createUser(db,'Felipe',3,'789')


Sf.createSKU(db, 'Telescopic', 2.01, 100)
Sf.createSKU(db, 'Glass Pane Knob', 6.43, 200)
Sf.createSKU(db, 'Lower chamber-9', 4.77, 150)
Sf.createSKU(db, 'Upper chamber-9', 3.07, 150)
Sf.createSKU(db, 'Lock for latch', 12.03, 1000)
Sf.createSKU(db, 'Profile joint unit plastic bag', 4.93, 180)



#Aquí las Skills, las Difficulties y las Activities se crean de forma directa. Esto no se hace a través de métodos "createSkill",
#createActivity" o "create Difficulty" dado que esas relaciones son
# constantes en las base de datos y no es necesario volver a crearlas en el futuro.
with db_session:
	db.Skills(id=1, name='Rectification')
	db.Skills(id=2, name='Design')
	db.Skills(id=3, name='Fabrication')
	db.Skills(id=4, name='Installation')

	db.Difficulties(id=1, description='Construccion en altura')

	db.Activities(id=1, description='Licencia')
	db.Activities(id=2, description='Vacaciones')
	db.Activities(id=3, description='Cliente ocupado')

##############################################
# Lista de prueba de proyectos test case 1 #
##############################################

Pf.CreateProject(db, 1, 'Manuel Montt 1235', 'Providencia', 'Pedro Sánchez',
				 '17.094.362-0', 150, date(2017, 12, 30), estimated_cost = 200)
Pf.CreateProject(db, 2, 'Suecia 86', 'Las Condes', 'Franco Soto',
				 '16.224.112-0', 200, date(2017, 6, 30), estimated_cost = 300)
Pf.CreateProject(db, 3, 'Barros Luco 997', 'Puente Alto', 'Miguel Acevedo',
				 '15.114.992-0',
 320, date(2017, 6, 30), estimated_cost = 150)

Sf.createEngagement(db,2,[(1,10),(5,2),(3,20),(5,16),(6,38)])

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

Ef.CreateEmployee(db,  "Juan", 1, perf_rect = 10)
Ef.CreateEmployee(db,  "Pedro", 2, perf_des = 20)
Ef.CreateEmployee(db,  "Diego", 2, perf_fab = 30)
Ef.CreateEmployee(db,  "Miguel", 1, perf_inst = 40)
Ef.CreateEmployee(db,  "Mario", 1, perf_rect = 50)
Ef.CreateEmployee(db,  "Felipe", 2, perf_des = 60)
Ef.CreateEmployee(db,  "Miguel", 1, perf_fab = 40)
Ef.CreateEmployee(db,  "Mario", 1, perf_inst = 50)
Ef.CreateEmployee(db,  "Felipe", 2, perf_rect = 60)
Ef.CreateEmployee(db,  "Miguel", 1, perf_des = 40)
Ef.CreateEmployee(db,  "Mario", 1, perf_fab = 50)
Ef.CreateEmployee(db,  "Felipe", 1, perf_inst = 60)
#Ef.CreateEmployee(db,  "Iker", 1, perf_inst = 70)


##############################################
# Lista de prueba de tasks test case 1 		 #
##############################################

Pf.CreateTask(db, 1, 1, original_initial_date=date(2017, 4, 8), original_end_date=date(2017,4,28))
Pf.CreateTask(db, 2, 1, original_initial_date=date(2017, 4, 29), original_end_date=date(2017,5,10))
Pf.CreateTask(db, 3, 1, original_initial_date=date(2017, 5, 11), original_end_date=date(2017,5,30))
Pf.CreateTask(db, 4, 1, original_initial_date=date(2017, 6, 2), original_end_date=date(2017,6,14))
Pf.CreateTask(db, 1, 2, original_initial_date=date(2017, 4, 3), original_end_date=date(2017,5,18))
Pf.CreateTask(db, 2, 2, original_initial_date=date(2017, 5, 19), original_end_date=date(2017,5,29))
Pf.CreateTask(db, 3, 2, original_initial_date=date(2017, 5, 30), original_end_date=date(2017,6,1))
Pf.CreateTask(db, 4, 2, original_initial_date=date(2017, 6, 2), original_end_date=date(2017,6,15))
Pf.CreateTask(db, 1, 3, original_initial_date=date(2017, 6, 3), original_end_date=date(2017,6,10))
Pf.CreateTask(db, 2, 3, original_initial_date=date(2017, 6, 11), original_end_date=date(2017,6,20))
Pf.CreateTask(db, 3, 3, original_initial_date=date(2017, 6, 21), original_end_date=date(2017,7,8))
Pf.CreateTask(db, 4, 3, original_initial_date=date(2017, 7, 9), original_end_date=date(2017,7,19))

PLf.AssignTask(db, 1, 1, initial_date=date(2017, 4, 8), end_date=date(2017,4,28))
PLf.AssignTask(db, 5, 5,  initial_date=date(2017, 4, 15), end_date=date(2017,4,25))
PLf.AssignTask(db, 9, 9,  initial_date=date(2017, 6, 1), end_date=date(2017,6,12))
#PLf.AssignTask(db, 2, 2,  initial_date=date(2017, 4, 28), end_date=date(2017,5,20))
#PLf.AssignTask(db, 6, 6,  initial_date=date(2017, 4, 3), end_date=date(2017,4,18))
#PLf.AssignTask(db, 10, 10,  initial_date=date(2017, 4, 12), end_date=date(2017,5,1))
#PLf.AssignTask(db, 3, 3,  initial_date=date(2017, 4, 16), end_date=date(2017,5,7))
#PLf.AssignTask(db, 7, 7,  initial_date=date(2017, 4, 26), end_date=date(2017,6,1))
#PLf.AssignTask(db, 11, 11,  initial_date=date(2017, 4, 20), end_date=date(2017,4,30))
#PLf.AssignTask(db, [4,8], 4,  initial_date=date(2017, 5, 10), end_date=date(2017,5,20))
#PLf.AssignTask(db, [4,8,12], 8, initial_date=date(2017, 5, 15), end_date=date(2017,6,8))
#PLf.AssignTask(db, 12, 12,  initial_date=date(2017, 5, 20), end_date=date(2017,7,3))

with db_session:
	#Definición de fechas de inicio efectivas para algunas tareas
	db.Tasks[1].effective_initial_date = date(2017, 4, 8)
	db.Tasks[5].effective_initial_date = date(2017, 4, 15)
	db.Tasks[9].effective_initial_date = date(2017, 4, 18)
# recordar que una vez corrimos el mismo método croque y mai y nos daban resultados distintos
PLf.DoPlanning(db, Pf.CreateTask)







