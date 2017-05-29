#Caso de prueba 9
#Se inicializan las siguientes entidades (tablas) : 
#Se prueban la(s) siguiente(s) funcionalidad(es): ingreso de las caracteristicas de un proyecto desde excel, buscando un funcionamiento
#lo mas parecido al real.
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

# Uf.createUser(db,'Alberto',1,'123')
# Uf.createUser(db,'Juan',2,'456')
# Uf.createUser(db,'Felipe',3,'789')

#Aqui las Skills, las Difficulties y las Activities se crean de forma directa. Esto no se hace a traves de metodos "createSkill",
#createActivity" o "create Difficulty" dado que esas relaciones son
# constantes en las base de datos y no es necesario volver a crearlas en el futuro.
with db_session:
    db.Skills(id=1, name='Rectificación')
    db.Skills(id=2, name='Diseño')
    db.Skills(id=3, name='Fabricación')
    db.Skills(id=4, name='Instalación')

    db.Difficulties(id=1, description='Construccion en altura')

    db.Activities(id=1, description='Licencia')
    db.Activities(id=2, description='Vacaciones')
    db.Activities(id=3, description='Cliente ocupado')
    #Las siguientes tres tablas se inicializan al estilo Skills.
    ############################################
    # Relleno de costos de algunas localidades #
    ############################################
    db.Freight_Costs(comuna_to = 'Calera', freight_cost = 50000)
    db.Freight_Costs(comuna_to = 'Curepto', freight_cost = 100000)
    db.Freight_Costs(comuna_to = 'Arica',  freight_cost = 200000)
    db.Freight_Costs(comuna_to = 'San Jose', freight_cost = 350000)
    ###########################################
    # Fijacion de algunos costos de operacion #
    ###########################################
    # db.Operating_Costs(name = 'Remuneracion fija fabrica', cost = 1800000)
    # db.Operating_Costs(name = 'Remuneracion variable fabrica', cost = 122500)
    # db.Operating_Costs(name = 'Arriendo fabrica', cost = 1000000)
    # db.Operating_Costs(name = 'Costos operacion', cost = 400000)#luz, agua, etc
    # db.Operating_Costs(name = 'Porcentaje ventas para materiales', cost = 0.02)#cost del 0 al 1
    # db.Operating_Costs(name = 'Costo por metro lineal de instalacion', cost = 1500)#este no es estrictamente de operacion, 
    # # pero podria dejarse igual aqui
    # db.Operating_Costs(name = 'Viatical per day', cost = 60000)#lo mismo que arriba
    #########################################################################################################
    # Inicializacion de valores para los factores de perdida segun tipo de componentes y los de instalacion #
    #########################################################################################################
    db.Waste_Factors(id = 1, name = 'Components type 1' , factor = 0.03)
    db.Waste_Factors(id = 2, name = 'Components type 2' , factor = 0.03)
    db.Waste_Factors(id = 3, name = 'Components type 3' , factor = 0.03)#En el excel son todos iguales, podrian diferir, aun asi no se como
    db.Waste_Factors(id = 4, name = 'Components type 4' , factor = 0.03)
    db.Waste_Factors(id = 5, name = 'Installation errors' , factor = 0.035)
    db.Waste_Factors(id = 6, name = 'Profile and glassing loss factor', factor = 0.13)

################################################
# Obtener la lista de productos desde un excel #
################################################
# Pf.getListProducts(db)

#################################################
#        Lista de empleados test case 1         #
# ###############################################

Ef.createEmployee(db,  "Juan", "Vitacura", perf_rect = 2)
Ef.createEmployee(db,  "Pedro", "Vitacura", perf_des = 2)
Ef.createEmployee(db,  "Diego", "Vitacura", perf_fab = 30)
Ef.createEmployee(db,  "Miguel", "Vitacura", perf_inst = 40, senior = True)
Ef.createEmployee(db,  "Mario", "Vitacura", perf_rect = 1)
Ef.createEmployee(db,  "Felipe", "Vitacura", perf_des = 1)
Ef.createEmployee(db,  "Miguel", "Vitacura", perf_fab = 40)
Ef.createEmployee(db,  "Mario", "Vitacura", perf_inst = 50, senior = False)
Ef.createEmployee(db,  "Felipe", "Vitacura", perf_rect = 2)
Ef.createEmployee(db,  "Miguel", "Vitacura", perf_des = 1)
Ef.createEmployee(db,  "Mario", "Vitacura", perf_fab = 50)
Ef.createEmployee(db,  "Felipe", "Vitacura", perf_inst = 60, senior = True)
Ef.createEmployee(db,  "Iker", "Vitacura", perf_inst = 70, senior = False)


##############################################
# Lista de prueba de proyectos test case 1   #
##############################################

Sf.createSku(db, 1,'Telescopic', 2.01, 100,219, waste_factor = 0.02)
Sf.createSku(db, 2,'Glass Pane Knob', 6.43, 200,220, waste_factor = 0.03)
Sf.createSku(db, 3,'Lower chamber-9', 4.77, 150,234, waste_factor = 0.04)
Sf.createSku(db, 4,'Upper chamber-9', 3.07, 150,243, waste_factor = 0.05)
Sf.createSku(db, 5,'Lock for latch', 12.03, 100,251, waste_factor = 0.03)
Sf.createSku(db, 6,'Profile joint unit plastic bag', 4.93, 180,268, waste_factor = 0.03)
Sf.createSku(db, 7, 'Screw M4x14 tx20 A2 DIN965', 0.07, 50,0, waste_factor = 0.03)
Sf.createSku(db, 8, 'Fastening Bead 10mm transparent', 2.51, 50,0, waste_factor = 0.03)
Sf.createSku(db, 9, 'Screws for Water Sill', 0.69, 50,0, waste_factor = 0.03)
Sf.createSku(db, 10, 'Lock Keeper, wall side', 6.52, 50,0, waste_factor = 0.03)
Sf.createSku(db, 11, 'Profile joint unit plastic bag',4.93, 50,0, waste_factor = 0.03)


Pf.createProject(db, 1, 'Cachagua 102', 'Calera', 'Pedro Sanchez',
                 '17.094.362-0', 150, 2017, 5, 10, estimated_cost = 200, sale_date_year=2017,sale_date_month=4,sale_date_day=18,sale_price=300)
Pf.createProject(db, 2, 'Suecia 86', 'Arica', 'Franco Soto',
                 '16.2254.112-0', 200, 2017, 6, 30, estimated_cost = 300, sale_date_year=2017,sale_date_month=4,sale_date_day=18,sale_price=300)
Pf.createProject(db, 3, 'Barros Luco 997', 'Curepto', 'Miguel Acevedo',
                 '15.114.992-0', 450, 2017, 6, 3, estimated_cost = 150, sale_date_year=2017,sale_date_month=4,sale_date_day=18,sale_price=300)
Pf.createProject(db, 4, 'Miguel Angelo 987', 'San Jose', 'Miguel Devil', 
                    '14.214.392-K',220, 2017, 8, 30, estimated_cost = 250, sale_date_year=2017,sale_date_month=4,sale_date_day=18,sale_price=300)



Sf.createEngagement(db, 1, [(1,10),(2,150),(3,15),(4,20),(5,70),(6,300)],date(2017, 6, 1))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 1))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 1))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 2))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 2))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 3))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 4))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 5))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 1))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 1))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 1))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 1))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 2))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 2))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 3))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 4))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 5))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))
Sf.createEngagement(db, 1, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))
Sf.createEngagement(db, 2, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))
Sf.createEngagement(db, 3, [(1,10),(2,10),(3,10),(4,10),(5,10),(6,10)],date(2017, 6, 6))

Sf.createEngagement(db, 3, [(7,400)],date(2017, 7, 6))
Sf.createEngagement(db, 3, [(8,300)],date(2017, 7, 9))
# Sf.createEngagement(db, 3, [(9,10)],date(2017, 5, 6))
Sf.createEngagement(db, 3, [(10,10)],date(2017, 6, 6))
# Sf.createEngagement(db, 3, [(11,10)],date(2017, 5, 6))


Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,50),(5,50),(6,50)],date(2017, 5, 4))
Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,50),(5,50),(6,50)],date(2017, 5, 4))
Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,350),(5,50),(6,50)],date(2017, 6, 5))
Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,50),(5,50),(6,50)],date(2017, 6, 15))
Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,50),(5,50),(6,50)],date(2017, 6, 16))
Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,50),(5,50),(6,50)],date(2017, 6, 20))
Sf.createPurchases(db,[(1,50),(2,50),(3,50),(4,50),(5,50),(6,50)],date(2017, 10, 2))

Sf.createPurchases(db,[(7,450)],date(2017, 5, 4))
Sf.createPurchases(db,[(8,350)],date(2017, 5, 4))
# Sf.createPurchases(db,[(9,50)],date(2017, 4, 4))
Sf.createPurchases(db,[(10,50)],date(2017, 5, 4))
# Sf.createPurchases(db,[(11,50)],date(2017, 4, 4))

# with db_session:
#     #Definicion de las prioridades de los distintos proyectos
#     db.Projects[3].priority = 3
#     db.Projects[1].priority = 2
#     db.Projects[2].priority = 1
#     #Fijacion de proyectos
#     db.Projects[4].fixed_planning = True
#     db.Tasks[1].effective_initial_date = date(2017, 3, 28)


# Pf.getCostProject(db, 1)
# Pf.getProjectFeatures(db,1)
# PLf.doPlanning(db)
# print(Sf.getStockValue(db))
# Sf.printStock(db, 50220020)
# Sf.displayStock(db, 50220020)
