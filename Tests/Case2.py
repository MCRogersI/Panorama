#Caso de prueba 2
#Se inicializan las siguientes entidades (tablas) : XXX, XXX, XXX, ...
#Se prueban la(s) siguiente(s) funcionalidad(es): cambios de prioridades explícitos e ingreso de vacaciones y project activities.
from pony.orm import *
from database import db
import Employees.features as Ef, Employees.usuario as Eu
from datetime import date
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf
import Users.features as Uf
import Stock.features as Sf

#Uf.createUser(db,'Alberto',1,'123')
#Uf.createUser(db,'Juan',2,'456')
#Uf.createUser(db,'Felipe',3,'789')

#####################################################################
# Inicialización de skills, dificultades y actividades, test case 2 #
#####################################################################
with db_session:
	db.Skills(id=1, name='Rectification')
	db.Skills(id=2, name='Design')
	db.Skills(id=3, name='Fabrication')
	db.Skills(id=4, name='Installation')

	db.Difficulties(id=1, description='Construccion en altura')

	db.Activities(id=1, description='Licencia')
	db.Activities(id=2, description='Vacaciones')
	db.Activities(id=3, description='Cliente ocupado')

#############################
# Stock inicial test case 2 #
#############################

Sf.createSku(db, 'Telescopic', 'Profile',2.01, 100,real_quantity=219)
Sf.createSku(db, 'Glass Pane Knob','Profile', 6.43, 200,real_quantity=220)
Sf.createSku(db, 'Lower chamber-9','Profile', 4.77, 150,real_quantity=234)
Sf.createSku(db, 'Upper chamber-9', 'Profile',3.07, 150,real_quantity=243)
Sf.createSku(db, 'Lock for latch', 'Profile',12.03, 100,real_quantity=251)
Sf.createSku(db, 'Screw M4x12 tx20 A2 DIN965','Profile', 0.07, 500,real_quantity=1000)
Sf.createSku(db, 'Screw M4x14 tx20 A2 DIN965','Profile', 0.07, 500,real_quantity=1000)
Sf.createSku(db, 'Fastening Bead 10mm transparent','Profile', 2.51, 300,real_quantity=600)
Sf.createSku(db, 'Screws for Water Sill','Profile', 0.69, 200,real_quantity=500)
Sf.createSku(db, 'Lock Keeper, wall side','Profile', 6.52, 200,real_quantity=800)
Sf.createSku(db, 'Profile joint unit plastic bag','Profile', 4.93, 180,real_quantity=268)

#########################
# Proyectos test case 2 #
#########################
Pf.createProject(db, 1, 'Manuel Montt 1235', 'Providencia', 'Pedro Sánchez',
				 '17.094.362-0', 150, 2017, 12, 30, estimated_cost = 200)
Pf.createProject(db, 2, 'Suecia 86', 'Las Condes', 'Franco Soto',
				 '16.224.112-0', 200, 2017, 6, 30, estimated_cost = 300)
Pf.createProject(db, 3, 'Barros Luco 997', 'Puente Alto', 'Miguel Acevedo',
				 '15.114.992-0',
 320, 2017, 6, 3, estimated_cost = 150)
Pf.createProject(db, 4, 'Miguel Angelo 987', 'María Pinto', 'Miguel Devil',
				 '14.214.392-K',
 220, 2017, 8, 30, estimated_cost = 250)

###########################
# Engagements test case 2 #
###########################

Sf.createEngagement(db, 2, [(1,10),(2,2),(3,20),(5,16),(6,38)],date(2017, 2, 27))
Sf.createEngagement(db, 2, [(1,99),(4,100),(2,30)],date(2017, 2, 25))
Sf.createEngagement(db, 2, [(1,55),(2,200)],date(2017, 3, 2))
Sf.createEngagement(db, 1, [(1,60),(2,20),(3,40)],date(2017, 3, 3))
Sf.createEngagement(db, 1, [(4,100),(5,25),(6,60)],date(2017, 3, 7))
Sf.createEngagement(db, 3, [(5,55),(6,30)],date(2017, 3, 2))
Sf.createPurchases(db,[(3,18),(5,142)],date(2017, 3, 2))
Sf.createPurchases(db,(1,155),date(2017, 3, 4))

#################################################
#        Lista de empleados test case 2 		#
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
Ef.CreateEmployee(db,  "Iker", 1, perf_inst = 70)

##############################################
# Lista de prueba de tasks test case 2 		 #
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

######################################################
# Lista de asignación de rectificaciones test case 2 #
######################################################

PLf.AssignTask(db, 1, 1, initial_date=date(2017, 4, 8), end_date=date(2017,4,28))
PLf.AssignTask(db, 5, 5,  initial_date=date(2017, 4, 15), end_date=date(2017,4,25))
PLf.AssignTask(db, 9, 9,  initial_date=date(2017, 5, 1), end_date=date(2017,5,12))

############################################################################################
# Cambios forzosos a prioridades, fijación de proyectos y de inicialización de actividades #
############################################################################################

with db_session:
	#Definición de las prioridades de los distintos proyectos
	db.Projects[3].priority = 3
	db.Projects[1].priority = 2
	db.Projects[2].priority = 1
	#Fijación de proyectos
	db.Projects[4].fixed_planning = True
	#Definición de fechas de inicio efectivas para algunas tareas
	db.Tasks[1].effective_initial_date = date(2017, 4, 8)
	db.Tasks[5].effective_initial_date = date(2017, 4, 15)
	#Ingresar las vacaciones de un empleado
	db.Employees_Activities(employee = db.Employees[13], activity = db.Activities[2], initial_date = date(2017,3,1), end_date = date(2017,4,30))
#	db.Employees_Activities(employee = db.Employees[12], activity = db.Activities[2], initial_date = date(2017,3,1), end_date = date(2017,4,30))
#	db.Employees_Activities(employee = db.Employees[8], activity = db.Activities[2], initial_date = date(2017,3,1), end_date = date(2017,4,30))
	#Considera bien las vacaciones
	#Ingresar la no disponibilidad de un cliente:
	db.Projects_Activities(project = db.Projects[1], activity = db.Activities[3], initial_date = date(2017,4,8), end_date = date(2017,5,10))
	#Cuando una tarea ya fue fijada, no considera que el cliente pase a estar ocupado. ARREGLAR

PLf.changePriority(db, 3, 1)
PLf.DoPlanning(db, Pf.createTask, Sf.updateEngagements)
print('------')
print(Sf.checkStockAlarms(db))
Sf.printStock(db, 1)
Sf.displayStock(db,1)
