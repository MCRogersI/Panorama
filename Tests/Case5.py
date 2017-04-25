#Caso de prueba 5
#Se inicializan las siguientes entidades (tablas) : projects_delays
#Se prueban la(s) siguiente(s) funcionalidad(es): ingreso de atrasos y doPlanning. Cuando se ingresa un atraso de una tarea anterior a instalación, se atrasan todas las tareas que le siguen, en la misma cantidad de días.
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


Sf.createSku(db, 1,'Telescopic', 2.01, 100,219, waste_factor = 0.02)
Sf.createSku(db, 2,'Glass Pane Knob', 6.43, 200,220, waste_factor = 0.03)
Sf.createSku(db, 3,'Lower chamber-9', 4.77, 150,234, waste_factor = 0.04)
Sf.createSku(db, 4,'Upper chamber-9', 3.07, 150,243, waste_factor = 0.05)
Sf.createSku(db, 5,'Lock for latch', 12.03, 100,251, waste_factor = 0.03)
Sf.createSku(db, 6,'Profile joint unit plastic bag', 4.93, 180,268, waste_factor = 0.03)





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

#################################################
#        Lista de empleados test case 1         #
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
                 '17.094.362-0', 150, 2017, 12, 30, estimated_cost = 200)
Pf.createProject(db, 2, 'Suecia 86', 'Arica', 'Franco Soto',
                 '16.224.112-0', 200, 2017, 6, 30, estimated_cost = 300)
Pf.createProject(db, 3, 'Barros Luco 997', 'Curepto', 'Miguel Acevedo',
                 '15.114.992-0', 450, 2017, 6, 3, estimated_cost = 150)
Pf.createProject(db, 4, 'Miguel Angelo 987', 'San José', 'Miguel Devil', 
                    '14.214.392-K',220, 2017, 8, 30, estimated_cost = 250

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

#################
# Crear atrasos #
#################
Pf.createDelay(db, 2, 4, 8)


