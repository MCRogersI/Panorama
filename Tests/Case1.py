#Caso de prueba 1
#Se inicializan las siguientes entidades (tablas) : XXX, XXX, XXX, ...
#Se prueban la(s) siguiente(s) funcionalidad(es): utilización de prioridades, fijación de proyectos, algoritmo de asignación en general.
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


Sf.createSKU(db, 'Telescopic', 2.01, 100,real_quantity=219)
Sf.createSKU(db, 'Glass Pane Knob', 6.43, 200,real_quantity=220)
Sf.createSKU(db, 'Lower chamber-9', 4.77, 150,real_quantity=234)
Sf.createSKU(db, 'Upper chamber-9', 3.07, 150,real_quantity=243)
Sf.createSKU(db, 'Lock for latch', 12.03, 100,real_quantity=251)
Sf.createSKU(db, 'Profile joint unit plastic bag', 4.93, 180,real_quantity=268)



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
# Lista de prueba de proyectos test case 1   #
##############################################

Pf.createProject(db, 1, 'Manuel Montt 1235', 'Providencia', 'Pedro Sánchez',
				 '17.094.362-0', 150, date(2017, 12, 30), estimated_cost = 200)
Pf.createProject(db, 2, 'Suecia 86', 'Las Condes', 'Franco Soto',
				 '16.224.112-0', 200, date(2017, 6, 30), estimated_cost = 300)
Pf.createProject(db, 3, 'Barros Luco 997', 'Puente Alto', 'Miguel Acevedo',
				 '15.114.992-0',
 450, date(2017, 6, 3), estimated_cost = 150)
Pf.createProject(db, 4, 'Miguel Angelo 987', 'María Pinto', 'Miguel Devil', '14.214.392-K',
 220, date(2017, 8, 30), estimated_cost = 250)


Sf.createEngagement(db, 2, [(1,10),(2,2),(3,20),(5,16),(6,38)],date(2017, 2, 27))
Sf.createEngagement(db, 2, [(1,99),(4,100),(2,30)],date(2017, 2, 25))
Sf.createEngagement(db, 2, [(1,55),(2,200)],date(2017, 3, 2))
Sf.createEngagement(db, 1, [(1,60),(2,20),(3,40)],date(2017, 3, 3))
Sf.createEngagement(db, 1, [(4,100),(5,25),(6,60)],date(2017, 3, 7))
Sf.createEngagement(db, 3, [(5,55),(6,30)],date(2017, 3, 2))
Sf.createPurchases(db,[(3,18),(5,142)],date(2017, 3, 2))
Sf.createPurchases(db,(1,155),date(2017, 3, 4))


aux_check_debug_variable_stock_calculation = Sf.calculateStock(db,1)

#print(aux_check_debug_variable_stock_calculation)


with db_session:
	#Definición de las prioridades de los distintos proyectos
	db.Projects[3].priority = 3
	db.Projects[1].priority = 2
	db.Projects[2].priority = 1
	#Fijación de proyectos
	db.Projects[4].fixed_planning = True



#################################################
#        Lista de empleados test case 1 		#
# ###############################################

Ef.createEmployee(db,  "Juan", 1, perf_rect = 10)
Ef.createEmployee(db,  "Pedro", 2, perf_des = 20)
Ef.createEmployee(db,  "Diego", 2, perf_fab = 30)
Ef.createEmployee(db,  "Miguel", 1, perf_inst = 40)
Ef.createEmployee(db,  "Mario", 1, perf_rect = 50)
Ef.createEmployee(db,  "Felipe", 2, perf_des = 60)
Ef.createEmployee(db,  "Miguel", 1, perf_fab = 40)
Ef.createEmployee(db,  "Mario", 1, perf_inst = 50)
Ef.createEmployee(db,  "Felipe", 2, perf_rect = 60)
Ef.createEmployee(db,  "Miguel", 1, perf_des = 40)
Ef.createEmployee(db,  "Mario", 1, perf_fab = 50)
Ef.createEmployee(db,  "Felipe", 1, perf_inst = 60)
Ef.createEmployee(db,  "Iker", 1, perf_inst = 70)


##############################################
# Lista de prueba de tasks test case 1 		 #
##############################################

Pf.createTask(db, 1, 1, original_initial_date=date(2017, 4, 8), original_end_date=date(2017,4,28))
Pf.createTask(db, 2, 1, original_initial_date=date(2017, 4, 29), original_end_date=date(2017,5,10))
Pf.createTask(db, 3, 1, original_initial_date=date(2017, 5, 11), original_end_date=date(2017,5,30))
Pf.createTask(db, 4, 1, original_initial_date=date(2017, 6, 2), original_end_date=date(2017,6,14))
Pf.createTask(db, 1, 2, original_initial_date=date(2017, 4, 3), original_end_date=date(2017,5,18))
Pf.createTask(db, 2, 2, original_initial_date=date(2017, 5, 19), original_end_date=date(2017,5,29))
Pf.createTask(db, 3, 2, original_initial_date=date(2017, 5, 30), original_end_date=date(2017,6,1))
Pf.createTask(db, 4, 2, original_initial_date=date(2017, 6, 2), original_end_date=date(2017,6,15))
Pf.createTask(db, 1, 3, original_initial_date=date(2017, 6, 3), original_end_date=date(2017,6,10))
Pf.createTask(db, 2, 3, original_initial_date=date(2017, 6, 11), original_end_date=date(2017,6,20))
Pf.createTask(db, 3, 3, original_initial_date=date(2017, 6, 21), original_end_date=date(2017,7,8))
Pf.createTask(db, 4, 3, original_initial_date=date(2017, 7, 9), original_end_date=date(2017,7,19))


PLf.assignTask(db, 1, 1, initial_date=date(2017, 4, 8), end_date=date(2017,4,28))
PLf.assignTask(db, 5, 5,  initial_date=date(2017, 4, 15), end_date=date(2017,4,25))
PLf.assignTask(db, 9, 9,  initial_date=date(2017, 5, 1), end_date=date(2017,5,12))
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
#print(Pf.getCostProject(db, 2, 10, 0.1))


PLf.doPlanning(db, Pf.createTask, Sf.updateEngagements)

# Sf.printStock(db, 2)
#Sf.updateEngagements(db, 2)
print('------')
print(Sf.checkStockAlarms(db))
Sf.printStock(db, 1)
Sf.displayStock(db,1)
