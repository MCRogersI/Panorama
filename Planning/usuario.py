from datetime import date
from pony.orm import *
from Planning.features import changePriority, addDelayed, doPlanning, checkVeto, createEmployeesRestrictions
from Planning.reports import createGlobalReportModified
import pandas
from tabulate import tabulate
def planning_console(db,level):
    while True:
        opt = input( "\n Marque una de las siguientes opciones:\n - 1: Generar planificación.\
                                                               \n - 2: Cambiar la prioridad de un proyecto.\
                                                               \n - 3: Para manejar restricciones.\
                                                               \n - 4: Para generar informe.\
                                                               \n - 5: Para volver atrás. \
                                                               \n Ingrese la alternativa elegida: ")
        if opt == '1':
            doPlanning(db)
        if opt == '2':
            try:
                contract_number = input('\n Ingrese el numero de contrato del proyecto que desea cambiar: ')
                with db_session:
                    try:
                        db.Projects.get(contract_number = int(contract_number), finished = None).contract_number
                    except:
                        raise ValueError('\n No existe ese número de contrato.')
                        
                with db_session:
                    current_projects = len(select(p for p in db.Projects if p.finished == None))
                    old_priority = db.Projects.get(contract_number = int(contract_number), finished = None).priority
                print(' La prioridad actual de este proyecto es de ' + str(old_priority) + ' de ' + str(current_projects))
                new_priority = input(' Ingrese la nueva prioridad que desea asignarle al proyecto. Presione Enter si no quiere cambiar la prioridad: ')
                if new_priority != '':
                    try:
                        changePriority(db, int(contract_number), int(new_priority))
                        print('\n Cambio de prioridad realizado exitosamente.')
                        input(' Presione Enter para continuar.')
                    except:
                        print('\n Ingreso de variables inválidas.')
                        input(' Presione Enter para continuar.')
                else:
                    print('\n No se realizó ningún cambio.')
                    input(' Presione Enter para continuar.')
            except ValueError as ve:
                print(ve)
                input(' Presione Enter para volver.')
        if opt == '3':
            opt2 = input('\n Marque una de las siguientes opciones: \n - 1: Agregar una restricción de asignación.\
                                                                    \n - 2: Eliminar una restricción de asignación.\
                                                                    \n - 3: Agregar una restricción de tiempo. \
                                                                    \n - 4: Eliminar una restricción de tiempo.\
                                                                    \n - 5: Ver restricciones actuales. \
                                                                    \n Ingrese la alternativa elegida: ')
            if opt2 == '1':
                try:
                    contract_number = input('\n Ingrese el número de contrato del proyecto que desea seleccionar: ')
                    try:
                        contract_number = int(contract_number)
                    except:
                        raise ValueError('\n El número de contrato debe ser un número.')
                    with db_session:
                        if db.Projects.get(contract_number = contract_number, finished = None) == None:
                            raise ValueError('\n El proyecto no existe.')
                        else:
                            p = db.Projects.get(contract_number = contract_number, finished = None)
                    employee_id = input(' Ingrese el ID del empleado que desea asociar o vetar del proyecto: ')
                    try:
                        employee_id = int(employee_id)
                    except:
                        raise ValueError('\n El ID del empleado debe ser un número.')
                    with db_session:
                        if db.Employees.get(id = employee_id) == None:
                            raise ValueError('\n El empleado no existe.')
                        else:
                            e = db.Employees.get(id = employee_id)
                        er = db.Employees_Restrictions.get(employee = db.Employees[employee_id], project = db.Projects.get(contract_number = int(contract_number), finished = None))
                        if er != None:
                            raise ValueError('\n Ya existe una restricción asociada a este empleado con este proyecto.')
                    like = input(' Marque una de las siguientes opciones: \n - 1: Si quiere asociar al empleado con el proyecto. \n - 0: Si quiere vetar a este empleado del proyecto. \n Ingrese la alternativa elegida: ')
                    if like == '1':
                        like = True
                    elif like == '0':
                        like = False
                    else:
                        raise ValueError('\n Debe elegir entre 1 ó 0.')
                    if not like:
                        if checkVeto(db, int(contract_number),4,employee_id) or checkVeto(db, int(contract_number),1,employee_id):
                            raise ValueError('\n La planificación se hace infactible al vetar a todos los empleados con esa habilidad.')
                        else:
                            r = createEmployeesRestrictions(db,e,p,like)
                            print('\n Restricción agregada con éxito.')
                            input(' Presione Enter para continuar: ')
                    else:
                        r = createEmployeesRestrictions(db, e, p, like)
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar: ')
            if opt2 == '2':
                try:
                    contract_number = input('\n Ingrese el número de contrato del proyecto que desea seleccionar: ')
                    try:
                        contract_number = int(contract_number)
                        with db_session:
                            p = db.Projects.get(contract_number = int(contract_number), finished = None)
                    except:
                        raise ValueError('\n Número de contraro no existente.')
                    employee_id = input(' Ingrese el ID del empleado que desea liberar: ')
                    try:
                        employee_id = int(employee_id)
                        with db_session:
                            e = db.Employees[employee_id]
                    except:
                        raise ValueError('\n Número de contrato no existente.')
                    
                    with db_session:
                        if db.Employees_Restrictions.get(employee = e, project = p) == None:
                            raise ValueError('\n La restricción no existe.')
                        # db.Employees_Restrictions[db.Employees[int(employee_id)],db.Projects[int(contract_number)]].delete()
                        db.Employees_Restrictions[e,p].delete()
                        commit()
                    print('\n Restricción eliminada con éxito.')
                    input(' Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
            if opt2 == '3':
                try:
                    contract_number = input('\n Ingrese el número de contrato del proyecto elegido: ')
                    try:
                        contract_number = int(contract_number)
                        with db_session:
                            p = db.Projects.get(contract_number = int(contract_number), finished = None)
                    except:
                        raise ValueError('\n Número de contraro no existente.')
                    skill_id = input(' Marque la tarea que se quiere restringir: \n - 1: Rectificación . \n - 2: Diseño. \n - 3: Fabricación. \n - 4: Instalación. \n Ingrese la alternativa elegida: ')
                    try:
                        skill_id = int(skill_id)
                    except:
                        raise ValueError('\n Ingreso de habilidad inválida. ')
                    if skill_id not in [1,2,3,4]:
                        raise ValueError('\n Ingreso de habilidad inválida. ')
                    year = input(' Ingrese el año de la fecha límite: ')
                    month = input(' Ingrese el mes de la fecha límite: ')
                    day = input(' Ingrese el dia de la fecha límite: ')
                    try:
                        deadline = date(int(year),int(month),int(day))
                    except:
                        raise ValueError('\n No es una fecha válida.')
                    with db_session:
                        r = db.Deadlines_Restrictions( project = p, skill = db.Skills[int(skill_id)], deadline = deadline)
                        commit()
                    print('\n Restricción creada con éxito.')
                    input(' Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
            if opt2 == '4':
                contract_number = input('\n Ingrese el número de contrato del proyecto elegido: ')
                skill_id = input(' Marque la tarea restringida: \n - 1: Rectificación . \n - 2: Diseño. \n - 3: Fabricación. \n - 4: Instalación. \n Ingrese la alternativa elegida: ')
                try:
                    try:
                        project = db.Projects.get(contract_number = int(contract_number), finished = None).contract_number
                    except:
                        raise ValueError('\n No existe ese número de contrato.')
                    try:
                        db.Skills[int(skill_id)].id
                    except:
                        raise ValueError('\n Tarea inválida.')
                    with db_session:
                        select(dr for dr in db.Deadlines_Restrictions if dr.skill.id == int(skill_id) and dr.project == project).delete()
                        commit()
                    print('\n Restricción eliminada con éxito.')
                    input(' Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
            if opt2 == '5':
                with db_session:
                    ra = db.Employees_Restrictions.select()
                    data1 = [p.to_dict() for p in ra]
                    df = pandas.DataFrame(data1, columns = ['employee','fixed','project'])                    
                    df.columns = ['Empleado', 'Fijo', 'Proyecto']
                    print('\n Restricciones de asignación: \n')
                    print( tabulate(df, headers='keys', tablefmt='psql'))
                    rt = db.Deadlines_Restrictions.select()
                    data2 = [p.to_dict() for p in rt]
                    df2 = pandas.DataFrame(data2,columns = ['id', 'project', 'skill', 'deadline'])   
                    df2.columns = ['Id','Proyecto', 'Habilidad', 'Fecha Límite']
                    print('\n Restricciones de tiempo \n')
                    print( tabulate(df2, headers='keys', tablefmt='psql'))
                    input(' Presione Enter para continuar.')
        if opt == '4':
            try:
                createGlobalReportModified(db)
                input('\n Reporte global creado con éxito. Presione Enter para continuar.')
            except IndexError:
                print('\n No se pudo hacer reporte debido a que la planificación no está actualizada.')
                input(' Presione Enter para continuar.')

        if opt == '5':
            break