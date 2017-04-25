#Caso de prueba 8
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
    db.Freight_Costs(name = 'San Jose', region = 'Valdivia', freight_cost = 350000)
    ###########################################
    # Fijacion de algunos costos de operacion #
    ###########################################
    db.Operating_Costs(name = 'Remuneracion fija fabrica', cost = 1800000)
    db.Operating_Costs(name = 'Remuneracion variable fabrica', cost = 122500)
    db.Operating_Costs(name = 'Arriendo fabrica', cost = 1000000)
    db.Operating_Costs(name = 'Costos operacion', cost = 400000)#luz, agua, etc
    db.Operating_Costs(name = 'Porcentaje ventas para materiales', cost = 0.02)#cost del 0 al 1
    db.Operating_Costs(name = 'Costo por metro lineal de instalacion', cost = 1500)#este no es estrictamente de operacion, 
    #pero podria dejarse igual aqui
    db.Operating_Costs(name = 'Viatical per day', cost = 60000)#lo mismo que arriba
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

Ef.createEmployee(db,  "Juan", 1, perf_rect = 10)
Ef.createEmployee(db,  "Pedro", 2, perf_des = 20)
Ef.createEmployee(db,  "Diego", 2, perf_fab = 30)
Ef.createEmployee(db,  "Miguel", 1, perf_inst = 40, senior = True)
Ef.createEmployee(db,  "Mario", 1, perf_rect = 50)
Ef.createEmployee(db,  "Felipe", 2, perf_des = 60)
Ef.createEmployee(db,  "Miguel", 1, perf_fab = 40)
Ef.createEmployee(db,  "Mario", 1, perf_inst = 50, senior = False)
Ef.createEmployee(db,  "Felipe", 2, perf_rect = 60)
Ef.createEmployee(db,  "Miguel", 1, perf_des = 40)
Ef.createEmployee(db,  "Mario", 1, perf_fab = 50)
Ef.createEmployee(db,  "Felipe", 1, perf_inst = 60, senior = True)
Ef.createEmployee(db,  "Iker", 1, perf_inst = 70, senior = False)

##############################################
# Lista de prueba de proyectos test case 1   #
##############################################

Pf.createProject(db, 1, 'Cachagua 102', 'Calera', 'Pedro Sanchez',
                 '17.094.362-0', 150, 2017, 5, 10, estimated_cost = 200)
Pf.createProject(db, 2, 'Suecia 86', 'Arica', 'Franco Soto',
                 '16.224.112-0', 200, 2017, 6, 30, estimated_cost = 300)
Pf.createProject(db, 3, 'Barros Luco 997', 'Curepto', 'Miguel Acevedo',
                 '15.114.992-0', 450, 2017, 6, 3, estimated_cost = 150)
Pf.createProject(db, 4, 'Miguel Angelo 987', 'San Jose', 'Miguel Devil', 
                    '14.214.392-K',220, 2017, 8, 30, estimated_cost = 250)



with db_session:
    #Definicion de las prioridades de los distintos proyectos
    db.Projects[3].priority = 3
    db.Projects[1].priority = 2
    db.Projects[2].priority = 1
    #Fijacion de proyectos
    db.Projects[4].fixed_planning = True
    db.Tasks[1].effective_initial_date = date(2017, 3, 28)


# Pf.getCostProject(db, 1)
# Pf.getProjectFeatures(db,1)
# PLf.doPlanning(db)
# print(Sf.getStockValue(db))
# Sf.printStock(db, 50220020)
# Sf.displayStock(db, 50220020)
