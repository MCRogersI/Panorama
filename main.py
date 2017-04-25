from pony.orm import *
from database import db
from datetime import date
import Employees.features as Ef, Employees.usuario as Eu
import Projects.usuario as Pu
import Projects.features as Pf
import Planning.features as PLf
import Planning.reports as PLr
import Users.features as Uf
import Stock.usuario as Sf
import Tests.Case8 as case8
import Planning.usuario as PlanU
import Stock.reports as Sr
import numpy as np

# Uf.createUser(db,'1', 1,'1')
# Uf.createUser(db,'Admin', 1,'Armin')
# Uf.createUser(db,'Piola', 2,'Cuatro')
# Uf.createUser(db,'Pleb', 3,'00000')

def console(level):
    while True:
        opt = input("\n Marque una de las siguientes opciones:\n - 1: Empleados. \n - 2: Proyectos. \n - 3: Tareas. \n - 4: Stock. \n - 5: Planificación \n - 6: Para salir. \n Ingrese la alternativa elegida: ")
        if(opt == '1'):
            # Los ids deberían ser creados automáticamente y no ingresados (para asegurarse de que sean únicos).
            # Para el caso particular de los proyectos el contract_number puede ser ingresado porque tiene la propiedad de ser único.
            Eu.employees_console(db, level)
        if(opt == '2'):
            Pu.projects_console(db, level)
        if( opt== '3'):
            Pu.tasks_console(db, level)
        if (opt == '4'):
            Sf.stock_console(db, level)
        if (opt =='5'):
            PlanU.planning_console(db,level)
        if(opt == '6'):
            print("\n Has salido del programa.")
            break
def signIn():
    while True:
        user = input("Ingrese su usuario: ")
        password = input("Ingrese su contraseña: ")
        if Uf.checkPassEntry(db, user, password):
            with db_session:
                level=Uf.getUserLevel(db, user)
                console(level)
                
        else:
            print("Usuario y/o Contraseña incorrecto(s))")
        break
# signIn()
# Uf.createUser(db, "1", 1, "1")
# Uf.createUser(db, "2", 2, "2")
# Uf.createUser(db, "3", 3, "3")
# print(PLf.GetDays(db, 1, 1, 3))
# print(PLf.SumDays(date(2015,1,1), 1.1))
# Pf.failedTask(db, 1, 1, 2300)
# Sr.baseCreateReport()
# PLr.createGlobalReport(db)

# PLf.DoPlanning(db)
# PLf.addDelayed(db, 1,1,1,1,1)
# PLf.addDelayed(db, 10, 2, 2017-2-12, 2017-3-1, 2017-2-28)
# print(PLf.addDelayed(db, 5, 3 , '2017-3-1', '2017-3-10', '2017-3-30'))





###############################################
# Tests de los features de Employees.features #
###############################################
# Ef.CreateEmployee(db, 1, "Juan", 1, perf_rect = 1)
# Ef.CreateEmployee(db, 2, "Pedro", 1, perf_rect = 2)
# Ef.CreateEmployee(db, 3, "Diego", 1, perf_rect = 3)
# Ef.CreateEmployee(db, 4, "Lalo", 1, perf_rect = 4)
# Ef.CreateEmployee(db, 5, "Mario", 1, perf_rect = 5)
# Ef.CreateEmployee(db, 6, "Hector", 1, perf_rect = 6)
# Ef.PrintEmployees(db)
# Ef.DeleteEmployee(db, 4)
# Ef.PrintEmployeesSkills(db)
# Ef.PrintSkills(db)
# Ef.PrintSelectSkill(db, 1)
# Ef.PrintSelectSkill(db, 2)
# Ef.PrintSelectSkill(db, 3)
# Ef.PrintSelectSkill(db, 4)
# Ef.EditEmployee(db, 1, new_zone = 2, perf_rect = 12)





###########################################################
# Tests de la parte de buscar fechas de Planning.features #
###########################################################

# dt = date(2017, 9, 11)
# print(PLf.SumDays(dt, 10))

# print(PLf.GetAveragePerformance(db, 1))
# print(PLf.GetAveragePerformance(db, 2))
# print(PLf.GetAveragePerformance(db, 3))
# print(PLf.GetAveragePerformance(db, 4))

# print(PLf.GetDays(db, 1, 2, 4))
# print(date(2010,2,4) <= date(2010,2,4))

# print(PLf.ClientAvailable(db, 1, date(2017, 2, 2), date(2017, 3, 9)))
# print(PLf.EmployeesAvailable(db, [1, 2], date(2017, 3, 26), date(2017, 3, 31)))

# with db_session:
    # print(PLf.FindEmployees(db, 1, 1, 1, date(2017, 2, 2), date(2017, 2, 15)).show())

# print(PLf.FindEmployees(db, 1, 1, 1, date(2017, 2, 2), date(2017, 2, 15)))



# def foo():
    # return 1, True, "lalala"
# a, b, c = foo()
# print(a)
# print(b)
# print(c)

#with db_session:
#    print(PLf.FindEmployees(db, 3, date(2010,1,1), date(2010,1,1)).show())

# print(PLf.EmployeesBySkill(db, 4))
# print(PLf.EmployeesByStatus(db, 2, False, False))
# with db_session:
    # print(PLf.FindEmployees(db, 3, date(2010,1,1), date(2010,1,1)).show())

# print(PLf.HasNOnes('0001111111', 7))
# print(PLf.Successor([1,1,1,1,0,0,0,0,0,0], 4))
# print([1,8] + [0,4,5])
# print(PLf.GetChosenIds([12, 13, 14], [0, 1, 1]))

# print(PLf.FindEmployees(db, 1, 1, 1, date(2017,3,13), date(2010,3,17)))    
# print(PLf.FindEmployees(db, 1, 1, 2, date(2010,1,1), date(2010,1,1)))
# print(PLf.FindEmployees(db, 1, 1, 3, date(2010,1,1), date(2010,1,1)))
# print(PLf.FindEmployees(db, 1, 1, 4, date(2010,1,1), date(2010,1,1)))
# print(PLf.FindEmployees(db, 1, 1, 5, date(2010,1,1), date(2010,1,1)))
# print(PLf.FindEmployees(db, 1, 1, 6, date(2010,1,1), date(2010,1,1)))
# print(PLf.FindEmployees(db, 1, 1, 7, date(2010,1,1), date(2010,1,1)))

# print(PLf.FindEmployees(db, 1, 2, 1, date(2017,3,7), date(2017,3,15)))
# print(PLf.FindEmployees(db, 1, 2, 2, date(2017,3,7), date(2017,3,15)))
# print(PLf.FindEmployees(db, 1, 2, 3, date(2017,3,7), date(2017,3,15)))
# print(PLf.FindEmployees(db, 1, 2, 4, date(2017,3,7), date(2017,3,15)))
# print(PLf.FindEmployees(db, 1, 2, 5, date(2017,3,7), date(2017,3,15)))
# print(PLf.FindEmployees(db, 1, 2, 6, date(2017,3,7), date(2017,3,15)))

# print(PLf.FindEmployees(db, 1, 2, 3, date(2017,3,7), date(2017,3,17)))
# print(PLf.Successor([0,1,0,1], 2))



# print(PLf.FindDatesEmployees(db, 1, 1, 1, date(2017, 2, 13)))
# print(PLf.FindDatesEmployees(db, 1, 1, 2, date(2017, 2, 13)))
# print(PLf.FindDatesEmployees(db, 1, 1, 3, date(2017, 2, 13)))
# print(PLf.FindDatesEmployees(db, 1, 1, 4, date(2017, 2, 13)))
# print(PLf.FindDatesEmployees(db, 1, 1, 5, date(2017, 2, 13)))

# print(PLf.FindDatesEmployees(db, 1, 2, 1, date(2017, 3, 9)))
# print(PLf.FindDatesEmployees(db, 1, 2, 2, date(2017, 3, 9)))
# print(PLf.FindDatesEmployees(db, 1, 2, 3, date(2017, 3, 9)))
# print(PLf.FindDatesEmployees(db, 1, 2, 4, date(2017, 3, 9)))
# print(PLf.FindDatesEmployees(db, 1, 2, 5, date(2017, 3, 9)))
# print(PLf.FindDatesEmployees(db, 1, 2, 6, date(2017, 3, 9)))

# Pf.createTask(db, 1, 1, date(2017, 3, 9), date(2017, 3, 9))
# print(Pf.printTasks(db))


##############################################
# Tests de los features de Projects.features #
##############################################
# Pf.createProject(db, contract_number, client_address, client_comuna, client_name, client_rut, linear_meters, deadline, real_linear_meters = None, estimated_cost = None, real_cost = None)
# Pf.createProject(db, 1, 'frutillita', 'Las Condes', 'frambuesita', '20.024.322-0', 15, date(2017, 3, 14), estimated_cost = 200,)
# Pf.createProject(db, 2, 'cebollita', 'Las Condes', 'sub-campeon', '21.024.322-0', 20, date(2017, 3, 15), estimated_cost = 300,)
# Pf.createProject(db, 3, 'lalala', 'Las Condes', 'sisisi', '22.024.322-0', 20, date(2017, 4, 30), estimated_cost = 150,)
# with db_session:
    # db.Projects[1].priority = 1
    # db.Projects[2].priority = 2
    # db.Projects[3].priority = 3
    # db.Projects[4].priority = 4
    # db.Projects[5].priority = 5
    # db.Projects[5].fixed_priority = False

# db.Projects[5].fixed_priority = True
# Pf.printProjects(db)
# Pf.editProject(db, 1, new_linear_meters = 12, new_deadline = date(2017, 3, 18), new_real_cost = 315,)
# Pf.deleteProject(db, 2)


# Pf.createTask(db, 1, 1, 1, date(2014, 12, 1), date(2017,2,28))
# Pf.createTask(db, 2, 2, 2, date(2014, 12, 16), date(2017,3,1))
# Pf.createTask(db, 3, 3, 2, date(2014, 12, 18), date(2017,3,8))
# Pf.createTask(db, 4, 4, 2, date(2014, 12, 26), date(2017,12,14))

# Pf.editTask(db, 1, effective_initial_date = d.datetime(2014, 1, 1), effective_end_date = d.datetime(2014, 1, 10))
# Pf.editTask(db, 2, effective_initial_date = d.datetime(2014, 1, 11), effective_end_date = d.datetime(2014, 1, 15))
# Pf.editTask(db, 3, effective_initial_date = d.datetime(2014, 1, 16))

# Eu.employees_teams_console(db, Ef.CreateEmployee, Ef.PrintEmployees, Ef.EditEmployee, Ef.CreateTeam, Ef.PrintTeams, Ef.PrintTeamsSkills, Ef.EditTeam, Ef.PrintSkills)
# Pf.AssignTask(db, 1, 1)
# Pf.deleteTask(db,1)
# Pf.editProject(db, 2 ,new_real_linear_meters = 400, new_real_cost = 8000)
# Pf.deleteProject(db, 1)


#Pf.failedTask(db, 2, 1, 1000)

#####################################
# Probanfo el metodo fillCOmmitment #
#####################################

# with db_session:
    # initial_date = date(2017, 1, 3)
    # end_date = date(2017, 1, 9)
    
    # commitments = np.zeros( abs((end_date - initial_date).days) + 1 )
    # print(commitments)
    
    # initial_date_1 = date(2017, 1, 4)
    # end_date_1 = date(2017, 1, 6)
    # et = db.Employees_Tasks.get(employee = 1, task = 1)
    # et.planned_initial_date = initial_date_1
    # et.planned_end_date = end_date_1
    # commitments = PLf.fillCommitments(db, commitments, initial_date, end_date, et)
    # print(commitments)
    
    # initial_date_1 = date(2017, 1, 5)
    # end_date_1 = date(2017, 1, 11)
    # et = db.Employees_Tasks.get(employee = 1, task = 1)
    # et.planned_initial_date = initial_date_1
    # et.planned_end_date = end_date_1
    # commitments = PLf.fillCommitments(db, commitments, initial_date, end_date, et)
    # print(commitments)

#########################################################################################
# Tests de los features de Planning.features relacionados al reporte post-planificación #
#########################################################################################

# print(PLr.planningChangesPlausible(db))