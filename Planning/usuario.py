from datetime import date
from pony.orm import *
from Planning.features import changePriority, addDelayed, doPlanning, checkVeto
from Planning.reports import createGlobalReportCompact

def planning_console(db,level):
    if level==1:
        while True:
            opt = input( "\n Marque una de las siguientes opciones:\n - 1: Generar planificación.  \n - 2: Cambiar la prioridad de un proyecto. \n - 3: Para ver restricciones. \n - 4: Para generar informe. \n - 5: Para volver atrás. \n Ingrese la alternativa elegida: ")
            if opt == '1':
                doPlanning(db)
            if opt == '2':
                try:
                    contract_number = input('ingrese el numero de contrato del proyecto que desea cambiar ')
                    with db_session:
                        try:
                            db.Projects[int(contract_number)].contract_number
                        except:
                            raise ValueError('\n No existe ese número de contrato \n')
                            
                    with db_session:
                        current_projects = len(select(p for p in db.Projects))
                        old_priority = db.Projects[int(contract_number)].priority
                    print('la prioridad actual de este proyecto es de ' + str(old_priority) + ' de ' + str(current_projects))
                    new_priority = input('ingrese la nueva prioridad que desea asignarle al proyecto. Presione enter si no quiere cambiar la prioridad ')
                    if new_priority != None:
                        try:
                            changePriority(db, int(contract_number), int(new_priority))
                        except:
                            
                            print('Ingreso de variables inválidas')
                except ValueError as ve:
                    print(ve)
                    input('Precione cualquier tecla para volver \n')
            if opt == '3':
                opt2 = input('\n Marque una de las siguientes opciones: \n - 1: Agregar una restricción de asignación. \n - 2: Eliminar una restricción de asignación. \n - 3: Agregar una restricción de tiempo. \n - 4: Eliminar una restricción de tiempo. \n - 5: Ver restricciones actuales. \n Ingrese la alternativa elegida: ')
                if opt2 == '1':
                    try:
                        contract_number = input('\n Ingrese el número de contrato del proyecto que desea seleccionar: ')
                        with db_session:
                            if db.Projects.get(contract_number = contract_number) != None:
                                raise ValueError('\n El proyecto no existe \n')
                        employee_id = input(' Ingrese el ID del empleado que desea asociar o vetar del proyecto: ')
                        with db_session:
                            if db.Employees.get(employee_id = id) != None:
                                raise ValueError('\n El empleado no existe \n')
                        like = input(' Marque una de las siguientes opciones: \n - 1: Si quiere asociar al empleado con el proyecto. \n - 0: Si quiere vetar a este empleado del proyecto. \n Ingrese la alternativa elegida: ')
                        with db_session:
                            if like == '1':
                                r = db.Employees_Restrictions(employee = db.Employees[int(employee_id)], project = db.Projects[int(contract_number)], fixed = True)
                            if like == '0':
                                r = db.Employees_Restrictions(employee = db.Employees[int(employee_id)], project = db.Projects[int(contract_number)], fixed = False)
                                print (str(checkVeto(db, int(contract_number),4)) +' ,'+ str(checkVeto(db, int(contract_number),1)))
                                if checkVeto(db, int(contract_number),4) or checkVeto(db, int(contract_number),1):
                                    db.Employees_Restrictions[db.Employees[int(employee_id)],db.Projects[int(contract_number)]].delete()
                                    print('\n La planificación se hace infactible al vetar a todos los empleados \n')
                            else:
                                print('\n debe elegir entre 1 ó 0 \n')
                    except ValueError as ve:
                        print(ve)
                            
                if opt2 == '2':
                    contract_number = input('\n Ingrese el número de contrato del proyecto que desea seleccionar: ')
                    employee_id = input(' Ingrese el ID del empleado que desea liberar: ')
                    with db_session:
                        db.Employees_Restrictions[db.Employees[int(employee_id)],db.Projects[int(contract_number)]].delete()
                if opt2 == '3':
                    contract_number = input('\n Ingrese el número de contrato del proyecto elegido: ')
                    skill_id = input(' Marque la tarea que se quiere restringir: \n - 1: Rectificación . \n - 2: Diseño. \n - 3: Fabricación. \n - 4: Instalación. \n Ingrese la alternativa elegida: ')
                    year = input(' Ingrese el año de la fecha límite: ')
                    month = input(' Ingrese el mes de la fecha límite: ')
                    day = input(' Ingrese el dia de la fecha límite: ')
                    with db_session:
                        r = db.Deadlines_Restrictions( project = db.Projects[int(contract_number)], skill = db.Skills[int(skill_id)], deadline = date(int(year),int(month),int(day)))
                if opt2 == '4':
                    id = input('\n Ingrese el ID de la restricción a eliminar: ')
                    with db_session:
                        db.Deadlines_Restrictions[int(id)].delete()
                if opt2 == '5':
                    with db_session:
                        print('\n Restricciones de asignación: \n')
                        db.Employees_Restrictions.select().show()
                        print('\n Restricciones de tiempo \n')
                        db.Deadlines_Restrictions.select().show()
                if opt2 == '4':
                    continue
            if opt == '4':
                try:
                    createGlobalReportCompact(db)
                except:
                    print(' Estamos trabajando para usted.')
            if opt == '5':
                break