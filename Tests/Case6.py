#Caso de prueba 6
#Se inicializan las siguientes entidades (tablas) : Freight_Costs, Operating_Costs (Projects/models),
#Waste_Factors (Stock/models)
#Se prueban la(s) siguiente(s) funcionalidad(es): cálculo real de costos.
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


Sf.createSku(db, 'Telescopic', 'Profile', 2.01, 100,real_quantity=219, waste_factor = 0.02)
Sf.createSku(db, 'Glass Pane Knob', 'Crystal', 6.43, 200,real_quantity=220, waste_factor = 0.03)
Sf.createSku(db, 'Lower chamber-9', 'Profile', 4.77, 150,real_quantity=234, waste_factor = 0.04)
Sf.createSku(db, 'Upper chamber-9', 'Profile', 3.07, 150,real_quantity=243, waste_factor = 0.05)
Sf.createSku(db, 'Lock for latch', 'Component', 12.03, 100,real_quantity=251, waste_factor = 0.03)
Sf.createSku(db, 'Profile joint unit plastic bag','Component', 4.93, 180,real_quantity=268, waste_factor = 0.03)





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
	#Las siguientes tres tablas se inicializan al estilo Skills.
	############################################
	# Relleno de costos de algunas localidades #
	############################################
	db.Freight_Costs(name = 'Calera', region = 'Valparaiso', freight_cost = 50000)
	db.Freight_Costs(name = 'Curepto', region = 'Talca', freight_cost = 100000)
	db.Freight_Costs(name = 'Arica', region = 'Arica', freight_cost = 200000)
	db.Freight_Costs(name = 'San José', region = 'Valdivia', freight_cost = 350000)
	###########################################
	# Fijación de algunos costos de operación #
	###########################################
	db.Operating_Costs(name = 'Remuneracion fija fabrica', cost = 1800000)
	db.Operating_Costs(name = 'Remuneracion variable fabrica', cost = 122500)
	db.Operating_Costs(name = 'Arriendo fabrica', cost = 1000000)
	db.Operating_Costs(name = 'Costos operacion', cost = 400000)#luz, agua, etc
	db.Operating_Costs(name = 'Porcentaje ventas para materiales', cost = 0.02)#cost del 0 al 1
	db.Operating_Costs(name = 'Costo por metro lineal de instalacion', cost = 1500)#este no es estrictamente de operación, 
	#pero podría dejarse igual aquí
	db.Operating_Costs(name = 'Viatical per day', cost = 60000)#lo mismo que arriba
	#########################################################################################################
	# Inicialización de valores para los factores de pérdida según tipo de componentes y los de instalación #
	#########################################################################################################
	db.Waste_Factors(id = 1, name = 'Components type 1' , factor = 0.03)
	db.Waste_Factors(id = 2, name = 'Components type 2' , factor = 0.04)
	db.Waste_Factors(id = 3, name = 'Components type 3' , factor = 0.02)
	db.Waste_Factors(id = 4, name = 'Components type 4' , factor = 0.01)
	db.Waste_Factors(id = 5, name = 'Installation errors' , factor = 0.035)

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
# Lista de prueba de proyectos test case 1   #
##############################################

Pf.createProject(db, 1, 'Manuel Montt 1235', 'Calera', 'Pedro Sánchez',
				 '17.094.362-0', 150, date(2017, 3, 30), estimated_cost = 200)
Pf.createProject(db, 2, 'Suecia 86', 'Curepto', 'Franco Soto',
				 '16.224.112-0', 200, date(2017, 4, 30), estimated_cost = 300)
Pf.createProject(db, 3, 'Barros Luco 997', 'San José', 'Miguel Acevedo',
				 '15.114.992-0',
 450, date(2017, 6, 3), estimated_cost = 150)
Pf.createProject(db, 4, 'Miguel Angelo 987', 'Arica', 'Miguel Devil', '14.214.392-K',
 220, date(2017, 8, 30), estimated_cost = 250)


Sf.createEngagement(db, 1, [(1,10),(2,2),(3,20),(5,16),(6,38)],date(2017, 2, 27))
Sf.createEngagement(db, 1, [(1,99),(4,100),(2,30)],date(2017, 2, 25))
Sf.createEngagement(db, 1, [(1,55),(2,200)],date(2017, 3, 2))
Sf.createEngagement(db, 1, [(1,60),(2,20),(3,40)],date(2017, 3, 3))
Sf.createEngagement(db, 1, [(4,100),(5,25),(6,60)],date(2017, 3, 7))
Sf.createEngagement(db, 1, [(5,55),(6,30)],date(2017, 3, 2))
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
Pf.getCostProject(db, 1)
