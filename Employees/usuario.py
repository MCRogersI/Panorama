from Employees.features import createEmployee, printEmployees, editEmployee, printEmployeesSkills, printSelectSkill, deleteEmployee
from Projects.features import createEmployeeActivity, deleteEmployeeActivity, printEmployeesActivities
from pony.orm import *
from datetime import date
from Employees.reports import createPersonalEmployeeReport, createWorkersReportWide, createRectificatorsReport, createDesignersReport, createFabricatorsReport, createInstallersReport
import pandas
from tabulate import tabulate
import convert


def employees_console(db, level, user):
#Es mejor importar las funciones en lugar de entregarsélas como parámetro a la función. Cambiar más adelante.

    while True:
        if (level in [1,2,3,4,5,6]):
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea crear nuevo empleado. \
                                                                      \n - 2: Si desea editar datos de empleados. \
                                                                      \n - 3: Si desea eliminar un empleado. \
                                                                      \n - 4: Para manejar vacaciones/periodos de licencia de los empleados. \
                                                                      \n - 5: Para ver empleados actuales. \
                                                                      \n - 6: Para volver atrás. \
                                                                      \n Ingrese la alternativa elegida: ")
        else:
            opt = '5'
        if(opt == '1'):
            if (level == 1):
                try:
                    id = input("\n Ingrese el RUT del empleado sin puntos ni número verificador: ")
                    try:
                        int(id)
                    except:
                        raise ValueError('\n RUT no válido.')
                    name_empleado = input(" Ingrese el nombre del empleado: ")
                    if len(name_empleado.replace(' ','')) <1:
                        raise ValueError('\n El empleado debe tener un nombre.')
                    zone_empleado = input(" Ingrese la comuna de residencia del empleado: ")
                    if len( zone_empleado.replace(' ',''))<1:
                        raise ValueError('\n La comuna no puede estar vacía.')
                    try:
                        zone_empleado_parsed = convert.get_fuzzy(zone_empleado)
                    except:
                        raise ValueError('\n La comuna ingresada es inválida.')
                    perf_rect = input(" Ingrese el rendimiento histórico en rectificación del empleado, solo presione Enter si no realiza esta labor: ")
                    if(perf_rect == ''):
                        perf_rect=None
                    else:
                        try:
                            if float(perf_rect) <= 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                    perf_des = input(" Ingrese el rendimiento histórico en diseño del empleado, solo presione Enter si no realiza esta labor: ")
                    if(perf_des == ''):
                        perf_des=None
                    else:
                        try:
                            if float(perf_des) <= 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')                    
                    perf_fab = input(" Ingrese el rendimiento histórico en fabricación del empleado, solo presione Enter si no realiza esta labor: ")
                    if(perf_fab == ''):
                        perf_fab=None
                    else:
                        try:
                            if float(perf_fab) <= 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                    perf_ins = input(" Ingrese el rendimiento histórico en instalación del empleado, solo presione Enter si no realiza esta labor: ")
                    if(perf_ins == ''):
                        perf_ins=None
                    else:
                        try:
                            if float(perf_ins) <= 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                    senior = None
                    if(perf_ins != None):
                        senior = input(" Ingrese 1 si el empleado es instalador senior, y 0 si es instalador junior: ")
                        if senior == '1':
                            senior = True
                        elif senior == '0':
                            senior = False
                        else:
                            raise ValueError('\n Se debe ingresar 0 o 1.')
                    if perf_rect == None and perf_des ==None and perf_fab == None and perf_ins == None:
                        raise ValueError('\n El empleado debe ejercer alguna función.')
                    createEmployee(db,id, name_empleado, zone_empleado_parsed, perf_rect, perf_des, perf_fab, perf_ins, senior)
                    input('\n Empleado creado con éxito. Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
                except:
                    print('\n No se pudo crear el empleado.')
                    input(' Presione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        if(opt == '2'):
            if (level == 1):
                try:
                    skills = [1,2,3,4]
                    skill_added = False
                    id_empleado = input("\n Ingrese el RUT del empleado a editar sin puntos ni número identificador: ")
                    try:
                        id_empleado = int(id_empleado)
                        with db_session:
                            e = db.Employees[id_empleado]
                    except:
                        raise ValueError('\n Empleado inexistente.')
                    new_name = input(" Ingrese el nuevo nombre del empleado, solo presione Enter si lo mantiene: ")
                    new_zone = input(" Ingrese el código de la nueva zona del empleado, solo presione Enter si la mantiene: ")
                    new_perf_rect = input(" Ingrese el rendimiento histórico en rectificación del empleado, solo presione Enter si mantiene la información actual: ")
                    new_perf_des = input(" Ingrese el rendimiento histórico en diseño del empleado, solo presione Enter mantiene la información actual: ")
                    new_perf_fab = input(" Ingrese el rendimiento histórico en fabricación del empleado, solo presione Enter si mantiene la información actual: ")
                    new_perf_ins = input(" Ingrese el rendimiento histórico en instalación del empleado, solo presione Enter si mantiene la información actual: ")
                    new_senior = None
                    if new_name == '':
                        new_name = None
                    if len(new_zone.replace(' ',''))<1:
                        new_zone_parsed = None
                    else:
                        try:
                            new_zone_parsed = convert.get_fuzzy(new_zone)
                        except:
                            raise ValueError('\n La comuna ingresada es inválida.')
                    if new_perf_rect == '':
                        new_perf_rect=None
                    else:
                        try:
                            new_perf_rect = float(new_perf_rect)
                            if new_perf_rect < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                            elif new_perf_rect == 0:
                                skills.remove(1)
                            else:
                                skill_added = True
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                    if new_perf_des == '':
                        new_perf_des = None
                    else:
                        try:
                            new_perf_des = float(new_perf_des)
                            if new_perf_des < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                            elif new_perf_des == 0:
                                skills.remove(2)
                            else:
                                skill_added = True
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                       
                    if new_perf_fab == '':
                        new_perf_fab = None
                    else:
                        try:
                            new_perf_fab = float(new_perf_fab)
                            if new_perf_fab < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                            elif new_perf_fab == 0:
                                skills.remove(3)
                            else:
                                skill_added = True
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                    if new_perf_ins == '':
                        new_perf_ins = None
                    else:
                        try:
                            new_perf_ins = float(new_perf_ins)
                            if new_perf_ins < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo.')
                            elif new_perf_ins == 0:
                                skills.remove(4)
                            else:
                                skill_added = True
                        except:
                            raise ValueError('\n El rendimiento debe ser un número.')
                        new_senior = input(" Ingrese 1 si el empleado es instalador senior, y 0 si es instalador junior: ")
                        try:
                            if int(new_senior) == 0:
                                new_senior = False
                            elif int(new_senior) == 1:
                                new_senior = True
                            else:
                                raise ValueError('\n Debe ingresar 0 ó 1.')
                        except:
                            raise ValueError('\n Debe ingresar 0 ó 1.')
                    with db_session:
                        es = select(es for es in db.Employees_Skills if es.employee == db.Employees[id_empleado] and es.skill.id in skills)
                        if len(es) == 0 and not skill_added:
                            raise ValueError ('\n No puede dejar a un empleado sin habilidad.')
                    editEmployee(db, id_empleado, new_name, new_zone_parsed, new_perf_rect, new_perf_des, new_perf_fab, new_perf_ins, new_senior)
                    input('\n Empleado editado exitosamente. Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        if(opt == '3'):
            if (level == 1):
                try:
                    idEmpleado = input("\n Ingrese el RUT del empleado que desea eliminar: ")
                    with db_session:
                        try:
                            int(idEmpleado)
                        except:
                            raise ValueError('\n El RUT de un empleado debe ser un número entero.')
                        if db.Employees.get(id = int(idEmpleado)) == None:
                            raise ValueError('\n Empleado inexistente')
                    deleteEmployee(db, idEmpleado)
                    input('\n Empleado eliminado. Presione Enter para continuar. ')
                except ValueError as ve:
                    print(ve)
                    input('\n Presione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar. ')
        if(opt == '4'):
            if(level == 1):
                opt_employees_activities = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ingresar datos de una actividad. \
                                                                                            \n - 2: Si desea eliminar una actividad. \
                                                                                            \n - 3: Si desea ver la lista actual de actividades. \
                                                                                            \n Ingrese la alternativa elegida: ")
                
                if opt_employees_activities == '1':
                    activity = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ingresar datos de licencia. \
                                                                                \n - 2: Si desea ingresar datos de vacaciones. \
                                                                                \n Ingrese la alternativa elegida: ")
                    try:
                        if int(activity) != 1 and int(activity)!=2:
                            raise ValueError('\n Debe elegir entre licencia y vacaciones.')
                        employee = input("\n Ingrese el RUT del empleado asociado a la actividad elegida (sin puntos ni número identificador): ")
                        try:
                            with db_session:
                                e =  db.Employees[employee]
                        except:
                            raise ValueError('\n Empleado inexistente.')
                        initial_year = input(" Ingrese el año en que comienza la actividad: ")
                        initial_month = input(" Ingrese el mes en que comienza la actividad: ")
                        initial_day = input(" Ingrese el día en que comienza la actividad: ")
                        try:
                            date(int(initial_year),int(initial_month),int(initial_day))
                        except:
                            raise ValueError('\n No es una fecha válida.')
                        end_year = input(" Ingrese el año en que termina la actividad: ")
                        end_month = input(" Ingrese el mes en que termina la actividad: ")
                        end_day = input(" Ingrese el día en que termina la actividad: ")
                        try:
                            date(int(end_year),int(end_month),int(end_day))
                        except:
                            raise ValueError('\n No es una fecha válida.')
                        createEmployeeActivity(db, employee, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day)
                        input('\n Actividad creada. Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
                elif opt_employees_activities == '2':
                    try:
                        id_employee_activity = input("\n Ingrese el ID de la actividad que quiere eliminar: ")
                        deleteEmployeeActivity(db, id_employee_activity)
                        input('\n Actividad eliminada. Presione Enter para continuar.')
                    except:
                        print('\n Actividad inexistente.')
                        input(' Presione Enter para continuar.')
                elif opt_employees_activities == '3':
                    printEmployeesActivities(db)
                    input(' Presione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        if(opt == '5'):
            if (level in [1,2]):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de rectificadores. \
                                                                                     \n - 3: Si desea ver la lista de diseñadores. \
                                                                                     \n - 4: Si desea ver la lista de fabricadores. \
                                                                                     \n - 5: Si desea ver la lista de instaladores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if (level == 3):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de rectificadores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if (level == 4):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de diseñadores. \
                                                                                     \n - 3: Si desea ver la lista de instaladores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if (level == 5 ):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de fabricadores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if (level == 6 ):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de instaladores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if ( level in [7,8]):
                opt_ver_empleados = '1'
            if(opt_ver_empleados == '1' and level in [1,2]):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver lista de empleados. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 3: Si desea ver el calendario de trabajo de todos los empleados\
                                                                                      \n - 4: Si desea ver el calendario de trabajo de todos los rectificadores\
                                                                                      \n - 5: Si desea ver el calendario de trabajo de todos los diseñadores\
                                                                                      \n - 6: Si desea ver el calendario de trabajo de todos los fabricadores\
                                                                                      \n - 7: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n Ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 =='1'):
                    printEmployees(db)
                if (opt_ver_empleados_2 == '2'):
                    try:
                        id_employee = input('\n Ingrese el RUT del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El RUT debe ser un número entero.')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente.')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes.')
                        input(' Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '3'):
                    createWorkersReportWide(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '4'):
                    createRectificatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '5'):
                    createDesignersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '6'):
                    createFabricatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '7'):
                    createInstallersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
            elif(opt_ver_empleados == '1' and level == 3):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el RUT del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El RUT debe ser un número entero.')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente. \n')
                            if db.Employees_Skills.get(employee = db.Employees[id_employee]).skill.id != 1:
                                raise ValueError('\n Empleado no es un rectificador. Acceso restringido.')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes.')
                        input(' Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '2'):
                    createRectificatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
            elif(opt_ver_empleados == '1' and level == 4):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los diseñadores\
                                                                                      \n - 3: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el RUT del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El RUT debe ser un número entero.')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente.')
                            if db.Employees[int(id_employee)].skill.id not in [2,4]:
                                raise ValueError('\n Empleado no es un diseñador ni intalador. Acceso restringido.')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes.')
                        input(' Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '2'):
                    createDesignersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '3'):
                    createInstallersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                            \n Presione Enter para continuar.')
            elif(opt_ver_empleados == '1' and level == 5):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los fabricadores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el RUT del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El RUT debe ser un número entero.')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente.')
                            if db.Employees[int(id_employee)].skill.id != 3:
                                raise ValueError('\n Empleado no es un fabricador. Acceso restringido.')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes.')
                        input(' Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '2'):
                    createFabricatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                           \n Presione Enter para continuar.')
            elif(opt_ver_empleados == '1' and level == 6):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el RUT del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El RUT debe ser un número entero.')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente.')
                            if db.Employees[int(id_employee)].skill.id != 4:
                                raise ValueError('\n Empleado no es un instalador. Acceso restringido.')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes.')
                        input(' Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione Enter para continuar.')
                if (opt_ver_empleados_2 == '2'):
                    createInstallersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes. \
                           \n Presione Enter para continuar.')
            elif(opt_ver_empleados == '1' and level in [7,8]):
                try:
                    id_employee = user
                    try:
                        int(id_employee)
                    except:
                        raise ValueError('\n Usuario no es trabajador.')
                    with db_session:
                        if db.Employees.get( id = int(id_employee)) == None:
                            raise ValueError('\n Usuario no es trabajador. Acceso denegado.')
                    createPersonalEmployeeReport(db,id_employee)
                    print('\n Reporte creado con éxito. Puede revisarlo en la carpeta Reportes.')
                    input(' Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
                finally:
                    break
                                                                                          
            elif(opt_ver_empleados == '2') and (level in [1,2,3]):
                print('')
                printSelectSkill(db, 1)
                input(' Presione Enter para continuar.')
            elif(opt_ver_empleados == '3' and level in [1,2]) or (opt_ver_empleados == '2' and level == 4):
                print('')
                printSelectSkill(db, 2)
                input(' Presione Enter para continuar.')
            elif(opt_ver_empleados == '4' and level in [1,2]) or (opt_ver_empleados == '2' and level == 5):
                print('')
                printSelectSkill(db, 3)
                input(' Presione Enter para continuar.')
            elif(opt_ver_empleados == '5' and level in [1,2]) or (opt_ver_empleados =='2' and level ==6) or (opt_ver_empleados =='3' and level ==4):
                print('')
                printSelectSkill(db, 4)
                input(' Presione Enter para continuar.')
            else:
                print('\n No es una opción válida.')
                input(' Presione Enter para continuar.')
        if(opt == '6'):
            break
