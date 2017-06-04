from Employees.features import createEmployee, printEmployees, editEmployee, printEmployeesSkills, printSelectSkill, deleteEmployee
from Projects.features import createEmployeeActivity, deleteEmployeeActivity, printEmployeesActivities
from pony.orm import *
from datetime import date
from Employees.reports import createPersonalEmployeeReport, createWorkersReportWide, createRectificatorsReport, createDesignersReport, createFabricatorsReport, createInstallersReport
import pandas
from tabulate import tabulate
def employees_console(db, level, user):
#Es mejor importar las funciones en lugar de entregarsélas como parámetro a la función. Cambiar más adelante.

    while True:
        if (level in [1,2,3,4,5]):
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
                    id = input("\n Ingrese el rut del empleado sin puntos ni número verificador: ")
                    try:
                        int(id)
                    except:
                        raise ValueError('\n Rut no válido \n')
                    nameEmpleado = input("\n Ingrese el nombre del empleado: ")
                    if len(nameEmpleado) <1:
                        raise ValueError('\n El empleado debe tener un nombre \n')
                    zoneEmpleado = input(" Ingrese el código de la zona del empleado: ")
                    try:
                        int(zoneEmpleado)
                    except:
                        raise ValueError('\n La zona debe ser un numero \n')
                    perf_rect = input(" Ingrese el rendimiento histórico en rectificación del empleado, solo presione enter si no realiza esta labor: ")
                    if(perf_rect == ''):
                        perf_rect=None
                    else:
                        try:
                            if int(perf_rect) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                    perf_des = input(" Ingrese el rendimiento histórico en diseño del empleado, solo presione enter si no realiza esta labor: ")
                    if(perf_des == ''):
                        perf_des=None
                    else:
                        try:
                            if int(perf_des) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')                    
                    perf_fab = input(" Ingrese el rendimiento histórico en fabricación del empleado, solo presione enter si no realiza esta labor: ")
                    if(perf_fab == ''):
                        perf_fab=None
                    else:
                        try:
                            if int(perf_fab) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                    perf_ins = input(" Ingrese el rendimiento histórico en instalación del empleado, solo presione enter si no realiza esta labor: ")
                    if(perf_ins == ''):
                        perf_ins=None
                    else:
                        try:
                            if int(perf_ins) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                    senior = None
                    if(perf_ins != None):
                        senior = input(" Ingrese 1 si el empleado es instalador senior, y 0 si es instalador junior: ")
                        try:
                            senior = bool(senior)
                        except:
                            raise ValueError('\n Se debe ingresar 0 o 1. \n')
                    createEmployee(db,id, nameEmpleado, zoneEmpleado, perf_rect, perf_des, perf_fab, perf_ins, senior)
                    input('\n Empleado creado con éxito. Presione enter para continuar: ')
                except ValueError as ve:
                    print(ve)
                    input('\n Presione cualquier tecla para continuar: \n')
                except:
                    print(' No se pudo crear el empleado \n')
                    input('\n Presione enter para continuar: \n')
            else:
                print('\n Acceso denegado.')
                input('\n Presione enter para continuar: ')
        if(opt == '2'):
            if (level == 1):
                try:
                    id_empleado = input("\n Ingrese el rut del empleado a editar sin puntos ni número identificador: ")
                    try:
                        with db_session:
                            e = db.Employees[int(id_empleado)]
                    except:
                        raise ValueError('\n Empleado inexistente. \n')
                    newName = input(" Ingrese el nuevo nombre del empleado, solo presione enter si lo mantiene: ")
                    newZone = input(" Ingrese el código de la nueva zona del empleado, solo presione enter si la mantiene: ")
                    newPerf_rect = input(" Ingrese el rendimiento histórico en rectificación del empleado, solo presione enter si mantiene la información actual: ")
                    newPerf_des = input(" Ingrese el rendimiento histórico en diseño del empleado, solo presione enter mantiene la información actual: ")
                    newPerf_fab = input(" Ingrese el rendimiento histórico en fabricación del empleado, solo presione enter si mantiene la información actual: ")
                    newPerf_ins = input(" Ingrese el rendimiento histórico en instalación del empleado, solo presione enter si mantiene la información actual: ")
                    if newName == '':
                        newName = None
                    if newZone == '':
                        newZone = None
                    else:
                        try:
                            int(newZone)
                        except:
                            raise ValueError('\n La zona debe ser un numero entero. \n')
                    if newPerf_rect == '':
                        newPerf_rect=None
                    else:
                        try:
                            if int(newPerf_rect) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                    if newPerf_des == '':
                        newPerf_des = None
                    else:
                        try:
                            if int(newPerf_des) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                       
                    if newPerf_fab == '':
                        newPerf_fab = None
                    else:
                        try:
                            if int(newPerf_fab) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                    if newPerf_ins == '':
                        newPerf_ins = None
                    else:
                        try:
                            if int(newPerf_ins) < 0:
                                raise ValueError('\n El rendimiento no puede ser negativo. \n')
                        except:
                            raise ValueError('\n El rendimiento debe ser un numero entero. \n')
                    new_senior = input(" Ingrese 1 si el empleado es instalador senior, y 0 si es instalador junior (si no es instalador, solo presione Enter): ")
                    try:
                        if int(new_senior) == 0:
                            new_senior = False
                        elif int(new_senior) != 1:
                            raise ValueError('\n Debe ingresar 0 ó 1. \n')
                    except:
                        raise ValueError('\n Debe ingresar 0 ó 1. \n')
                    editEmployee(db, id_empleado, newName, newZone, newPerf_rect, newPerf_des, newPerf_fab, newPerf_ins, bool(new_senior))
                    input('\n Empleado editado exitosamente. Presione enter para continuar: ')
                except ValueError as ve:
                    print(ve)
                    input('\n Presione cualquier tecla para continuar \n')
            else:
                print('\n Acceso denegado.')
                input('\n Presione enter para continuar: ')
        if(opt == '3'):
            if (level == 1):
                try:
                    idEmpleado = input("\n Ingrese el rut del empleado que desea eliminar: ")
                    with db_session:
                        try:
                            int(idEmpleado)
                        except:
                            raise ValueError('\n El rut de un empleado debe ser un número entero \n')
                        if db.Employees.get(id = int(idEmpleado)) == None:
                            raise ValueError('\n Empleado inexistente \n')
                    deleteEmployee(db, idEmpleado)
                    input('\n Empleado eliminado. Presione enter para continuar: ')
                except ValueError as ve:
                    print(ve)
                    input('\n Presione cualquier tecla para continuar \n')
            else:
                print('\n Acceso denegado.')
                input('\n Presione enter para continuar: ')
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
                            raise ValueError('\n Debe elegir entre licencia y vacaciones. \n')
                        employee = input(" Ingrese el rut del empleado asociado a la actividad elegida (sin puntos ni número identificador): ")
                        try:
                            with db_session:
                                e =  db.Employees[employee]
                        except:
                            raise ValueError('\n Empleado inexistente \n')
                        initial_year = input(" Ingrese el año en que comienza la actividad: ")
                        initial_month = input(" Ingrese el mes en que comienza la actividad: ")
                        initial_day = input(" Ingrese el día en que comienza la actividad: ")
                        try:
                            date(int(initial_year),int(initial_month),int(initial_day))
                        except:
                            raise ValueError('\n No es una fecha válida \n')
                        end_year = input(" Ingrese el año en que termina la actividad: ")
                        end_month = input(" Ingrese el mes en que termina la actividad: ")
                        end_day = input(" Ingrese el día en que termina la actividad: ")
                        try:
                            date(int(end_year),int(end_month),int(end_day))
                        except:
                            raise ValueError('\n La fecha es inválida. \n')
                        createEmployeeActivity(db, employee, activity, initial_year, initial_month, initial_day, end_year, end_month, end_day)
                        input(' \n Actividad creada. Presione enter para continuar: ')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione cualquier tecla para continuar: ')
                elif opt_employees_activities == '2':
                    try:
                        id_employee_activity = input("\n Ingrese el ID de la actividad que quiere eliminar: ")
                        deleteEmployeeActivity(db, id_employee_activity)
                        input(' \n Actividad eliminada. Presione enter para continuar: ')
                    except:
                        print('\n Actividad inexistente. \n')
                        input('\n Presione cualquier tecla para continuar: ')
                elif opt_employees_activities == '3':
                    print('\n')
                    ea = db.Employees_Activities.select()
                    data = [p.to_dict() for p in ea]
                    df = pandas.DataFrame(data, columns = ['id','employee','activity','initial_ date','end_date'])                    
                    df.columns = ['ID','Empleado','Tipo Actividad', 'Fecha Inicio', 'Fecha Fin']
                    print( tabulate(df, headers='keys', tablefmt='psql'))
                    input(' \n Presione enter para continuar: ')
            else:
                print('\n Acceso denegado.')
                input('\n Presione enter para continuar: ')
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
                                                                                     \n - 2: Si desea ver la lista de instaladores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if (level == 4):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de rectificadores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if (level == 5 ):
                opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                     \n - 2: Si desea ver la lista de diseñadores. \
                                                                                     \n - 3: Si desea ver la lista de instaladores. \
                                                                                     \n Ingrese la alternativa elegida: ")
            if ( level in [6,7,8,9]):
                opt_ver_empleados = '1'
            if(opt_ver_empleados == '1' and level in [1,2]):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver lista de empleados. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 3: Si desea ver el calendario de trabajo de todos los empleados\
                                                                                      \n - 4: Si desea ver el calendario de trabajo de todos los rectificadores\
                                                                                      \n - 5: Si desea ver el calendario de trabajo de todos los diseñadores\
                                                                                      \n - 6: Si desea ver el calendario de trabajo de todos los fabricadores\
                                                                                      \n - 7: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 =='1'):
                    print('\n')
                    e = db.Employees.select()
                    data = [p.to_dict() for p in e]
                    df = pandas.DataFrame(data, columns = ['id','name','zone','senior'])                    
                    df.columns = ['Rut','Nombre','Zona', '¿Es Senior?']
                    print( tabulate(df, headers='keys', tablefmt='psql'))
                    input(' \n Presione enter para continuar: ')
                if (opt_ver_empleados_2 == '2'):
                    try:
                        id_employee = input('\n Ingrese el rut del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El rut debe ser un número entero. \n')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente. \n')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado. Puede revisarlo en la carpeta de reportes. \n')
                        input('\n Presione enter para continuar. \n')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione enter para continuar. \n')
                if (opt_ver_empleados_2 == '3'):
                    createWorkersReportWide(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
                if (opt_ver_empleados_2 == '4'):
                    createRectificatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
                if (opt_ver_empleados_2 == '5'):
                    createDesignersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
                if (opt_ver_empleados_2 == '6'):
                    createFabricatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
                if (opt_ver_empleados_2 == '7'):
                    createInstallersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '1' and level == 3):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el rut del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El rut debe ser un número entero. \n')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente. \n')
                            if db.Employees_Skills.get(employee = db.Employees[id_employee]).skill.id != 4:
                                raise ValueError('\n Empleado no es un instalador. Acceso restringido. \n')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado. Puede revisarlo en la carpeta Reportes. \n')
                        input('\n Presione la tecla Enter para continuar. \n')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione la tecla Enter para continuar. \n')
                if (opt_ver_empleados_2 == '2'):
                    createInstallersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '1' and level == 4):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los rectificadores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el RUT del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El rut debe ser un número entero. \n')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente. \n')
                            if db.Employees[int(id_employee)].skill.id != 1:
                                raise ValueError('\n Empleado no es un rectificador. Acceso restringido. \n')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado. Puede revisarlo en la carpeta de reportes. \n')
                        input('\n Presione enter para continuar. \n')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione enter para continuar. \n')
                if (opt_ver_empleados_2 == '2'):
                    createRectificatorsReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '1' and level == 5):
                opt_ver_empleados_2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver el calendario de trabajo de un empleado. \
                                                                                      \n - 2: Si desea ver el calendario de trabajo de todos los diseñadores\
                                                                                      \n - 3: Si desea ver el calendario de trabajo de todos los instaladores\
                                                                                      \n ingrese la alternativa escogida: ")
                if (opt_ver_empleados_2 == '1'):
                    try:
                        id_employee = input('\n Ingrese el rut del empleado cuyo calendario le interesa (sin puntos ni número identificador): ')
                        try:
                            int(id_employee)
                        except:
                            raise ValueError('\n El rut debe ser un número entero. \n')
                        with db_session:
                            if db.Employees.get( id = int(id_employee)) == None:
                                raise ValueError('\n Empleado inexistente. \n')
                            if db.Employees[int(id_employee)].skill.id not in [2,4]:
                                raise ValueError('\n Empleado no es un instalador o diseñador. Acceso restringido. \n')
                        createPersonalEmployeeReport(db,id_employee)
                        print('\n Reporte creado. Puede revisarlo en la carpeta de reportes. \n')
                        input('\n Presione enter para continuar. \n')
                    except ValueError as ve:
                        print(ve)
                        input('\n Presione enter para continuar. \n')
                if (opt_ver_empleados_2 == '2'):
                    createDesignersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
                if (opt_ver_empleados_2 == '3'):
                    createInstallersReport(db)
                    input('\n Reporte creado con éxito. Puede revisarlo en la carpeta de reportes. \
                            \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '1' and level in [6,7,8,9]):
                try:
                    id_employee = user
                    try:
                        int(id_employee)
                    except:
                        raise ValueError('\n Usuario no es trabajador. \n')
                    with db_session:
                        if db.Employees.get( id = int(id_employee)) == None:
                            raise ValueError('\n Usuario no es trabajador. Acceso denegado. \n')
                    createPersonalEmployeeReport(db,id_employee)
                    print('\n Reporte creado. Puede revisarlo en la carpeta de reportes. \n')
                    input('\n Presione enter para continuar. \n')
                except ValueError as ve:
                    print(ve)
                    input('\n Presione enter para continuar. \n')
                finally:
                    break
                                                                                          
            elif(opt_ver_empleados == '2') and (level in [1,2,4]):
                printSelectSkill(db, 1)
                print('\n')
                input(' \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '3' and level in [1,2]) or (opt_ver_empleados == '2' and level == 5):
                printSelectSkill(db, 2)
                input(' \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '4' and level in [1,2]):
                printSelectSkill(db, 3)
                input(' \n Presione enter para continuar: ')
            elif(opt_ver_empleados == '5' and level in [1,2]) or (opt_ver_empleados =='2' and level ==3) or (opt_ver_empleados =='3' and level ==5):
                printSelectSkill(db, 4)
                input(' \n Presione enter para continuar: ')
            else:
                print('\n No es una opción válida. \n')
                input('\n Presione cualquier tecla para continuar: ')
        if(opt == '6'):
            break
