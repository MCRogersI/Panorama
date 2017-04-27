from Employees.features import createEmployee, printEmployees, editEmployee, printEmployeesSkills, printSelectSkill, deleteEmployee
from Projects.features import createEmployeeActivity, deleteEmployeeActivity, printEmployeesActivities
from pony.orm import *
from datetime import date

def employees_console(db, level):
#Es mejor importar las funciones en lugar de entregarsélas como parámetro a la función. Cambiar más adelante.

    while True:
        
        if level == 1:
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea crear nuevo empleado. \
                                                                  \n - 2: Si desea editar datos de empleados. \
                                                                  \n - 3: Si desea eliminar un empleado. \
                                                                  \n - 4: Para manejar vacaciones/periodos de licencia de los empleados. \
                                                                  \n - 5: Para ver empleados actuales. \
                                                                  \n - 6: Para volver atrás. \
                                                                  \n Ingrese la alternativa elegida: ")
        elif level == 2:
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea crear nuevo empleado. \
                                                                  \n - 2: Si desea editar datos de empleados. \
                                                                  \n - 3: Para manejar vacaciones/periodos de licencia de los empleados. \
                                                                  \n - 4: Para ver empleados actuales. \
                                                                  \n - 5: Para volver atrás. \
                                                                  \n Ingrese la alternativa elegida: ")
        elif level == 3:
            opt = input("\n Marque una de las siguientes opciones: \n - 1: Para ver empleados actuales. \
                                                                   \n - 2: Para volver atrás. \
                                                                   \n Ingrese la alternativa elegida: ")

        if(opt == '1' and (level == 1 or level == 2)):
            try:
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
                createEmployee(db, nameEmpleado, zoneEmpleado, perf_rect, perf_des, perf_fab, perf_ins, senior)
                input('\n Empleado creado con éxito. Presione una tecla para continuar: ')
            except ValueError as ve:
                print(ve)
                input('\n Presione cualquier tecla para continuar: \n')
            except:
                print(' No se pudo crear el empleado \n')
                input('\n Presione cualquier tecla para continuar: \n')

        if(opt == '2' and (level == 1 or level == 2)):
            try:
                id_empleado = input("\n Ingrese el ID del empleado a editar: ")
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
                        raise ValueError('\n Debe ingresar 0 0 1. \n')
                except:
                    raise ValueError('\n Debe ingresar 0 0 1. \n')
                editEmployee(db, id_empleado, newName, newZone, newPerf_rect, newPerf_des, newPerf_fab, newPerf_ins, bool(new_senior))
                input('\n Empleado editado exitosamente. Presione una tecla para continuar: ')
            except ValueError as ve:
                print(ve)
                input('\n Presione cualquier tecla para continuar \n')

        if(opt == '3' and level == 1):
            try:
                idEmpleado = input("\n Ingrese el ID del empleado que desea eliminar: ")
                with db_session:
                    try:
                        int(idEmpleado)
                    except:
                        raise ValueError('\n El ID de un empleado debe ser un número entero \n')
                    if db.Employees.get(id = int(idEmpleado)) == None:
                        raise ValueError('\n Empleado inexistente \n')
                deleteEmployee(db, idEmpleado)
                input(' \n Empleado eliminado. Presione una tecla para continuar: ')
            except ValueError as ve:
                print(ve)
                input('\n Presione cualquier tecla para continuar \n')

        
        if(opt == '4' and level == 1) or (opt == '3' and level == 2):
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
                    employee = input(" Ingrese el ID del empleado asociado a la actividad elegida: ")
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
                    input(' \n Actividad creada. Presione una tecla para continuar: ')
                except ValueError as ve:
                    print(ve)
                    input('\n Presione cualquier tecla para continuar: ')
            elif opt_employees_activities == '2':
                try:
                    id_employee_activity = input("\n Ingrese el ID de la actividad que quiere eliminar: ")
                    deleteEmployeeActivity(db, id_employee_activity)
                    input(' \n Actividad eliminada. Presione una tecla para continuar: ')
                except:
                    print('\n Actividad inexistente. \n')
                    input('\n Presione cualquier tecla para continuar: ')
            elif opt_employees_activities == '3':
                print('\n')
                printEmployeesActivities(db)
                input(' \n Presione una tecla para continuar: ')
            
            
        if(opt == '5' and level == 1) or (opt == '4' and level == 2) or (opt == '1' and level == 3):
            opt_ver_empleados = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver empleados. \
                                                                                 \n - 2: Si desea ver la lista de rectificadores. \
                                                                                 \n - 3: Si desea ver la lista de diseñadores. \
                                                                                 \n - 4: Si desea ver la lista de fabricadores. \
                                                                                 \n - 5: Si desea ver la lista de instaladores. \
                                                                                 \n Ingrese la alternativa elegida: ")
            print('\n')
            if(opt_ver_empleados == '1'):
                printEmployees(db)
                input(' \n Presione una tecla para continuar: ')
            elif(opt_ver_empleados == '2'):
                printSelectSkill(db, 1)
                input(' \n Presione una tecla para continuar: ')
            elif(opt_ver_empleados == '3'):
                printSelectSkill(db, 2)
                input(' \n Presione una tecla para continuar: ')
            elif(opt_ver_empleados == '4'):
                printSelectSkill(db, 3)
                input(' \n Presione una tecla para continuar: ')
            elif(opt_ver_empleados == '5'):
                printSelectSkill(db, 4)
                input(' \n Presione una tecla para continuar: ')
            else:
                print('\n No es una opción válida. \n')
                input('\n Presione cualquier tecla para continuar: ')
        if(opt == '6' and level == 1) or (opt == '5' and level == 2) or (opt == '2' and level ==3):
            break
