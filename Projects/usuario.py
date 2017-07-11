from datetime import date
from pony.orm import *
from Projects.features import createProject, printProjects, printFinishedProjects, printCurrentProjects, editProject, deleteProject, finishProject, createTask, editTask, printTasks, failedTask, createProjectActivity, deleteProjectActivity, printProjectsActivities, createDelay
from Projects.costs import estimateCost
from Projects.updateParameters import   updateFreightCosts, updateOperatingCosts,  updateViaticCosts,  updateMovilizationCosts, updateCrystalsParameters, updateProfilesParameters
from Planning.features import sumDays, editCrystalSalesOrder, editCrystalArrival
from Projects.engagements import createEngagements
import os
import pandas
from tabulate import tabulate
import convert
# from Projects.costs import estimateCost

def projects_console(db, level):
    while True:
        if (level in [1,2,3,4,5]):
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea crear un proyecto. \
                                                                  \n - 2: Si desea editar un proyecto. \
                                                                  \n - 3: Eliminar un proyecto. \
                                                                  \n - 4: Si desea manejar datos sobre disponibilidad de un cliente. \
                                                                  \n - 5: Para ver proyectos. \
                                                                  \n - 6: Para estimar costos del proyecto. \
                                                                  \n - 7: Para volver atrás. \
                                                                  \n Ingrese la alternativa elegida: ")
        else:
            opt = '6'
        if(opt == '1'):
            if(level == 1):
                try:
                    contract_number = input("\n Ingrese el número de contrato: ")
                    try:
                        int(contract_number)
                    except:
                        raise ValueError('No es un número válido')
                    with db_session:
                        if len(select( p for p in db.Projects if p.contract_number == int(contract_number))) > 0:
                            raise ValueError('\n Este número de contrato ya existe.')
                    client_address = input(" Ingrese la direccion del cliente: ")
                    if len(client_address.replace(' ','')) < 1:
                        raise ValueError('\n Debe ingresar una dirección.')
                    client_comuna = input(" Ingrese la comuna del cliente: ")
                    if len(client_comuna.replace(' ','')) < 1:
                        raise ValueError('\n Debe ingresar una comuna.')
                    try:
                        client_comuna_parsed = convert.get_fuzzy(client_comuna)
                    except:
                        raise ValueError('\n La comuna ingresada es inválida.')
                    client_name = input(" Ingrese el nombre del cliente: ")
                    if len(client_name.replace(' ','')) < 1:
                        raise ValueError('\n Debe ingresar un nombre.')
                    client_rut = input(" Ingrese el RUT del cliente: ")
                    if len(client_rut.replace(' ','')) < 1:
                        raise ValueError('\n Debe ingresar un RUT.')
                    linear_meters = input(" Ingrese los metros lineales del proyecto: ")
                    try:
                        linear_meters = float(linear_meters)
                    except:
                        raise ValueError('\n Los metros lineales deben ser un número.')
                    if float(linear_meters) <0:
                        raise ValueError('\n Los metros lineales deben ser un número positivo.')
                    square_meters = input(" Ingrese los metros cuadrados del proyecto: ")
                    try:
                        square_meters = float(square_meters)
                    except:
                        raise ValueError('\n Los metros cuadrados deben ser un número.')
                    if float(linear_meters) <0:
                        raise ValueError('\n Los metros cuadrados deben ser un número positivo.')
                    year = input(" Ingrese el año de la fecha de entrega pactada del proyecto: ")
                    try:
                        int(year)
                    except:
                        raise ValueError('\n El año debe ser un número entero.')
                    month = input(" Ingrese el mes de la fecha de entrega pactada del proyecto: ")
                    try:
                        int(month)
                    except:
                        raise ValueError('\n El mes debe ser un número entero.')
                    if int(month) > 12 or int(month) < 1:
                        raise ValueError('\n El mes debe ser un número entero entre 1 y 12.')
                    day = input(" Ingrese el día de la fecha de entrega pactada del proyecto: ")
                    try:
                        int(day)
                    except:
                        raise ValueError('\n El día debe ser un número entero.')
                    try:
                        date(int(year),int(month),int(day))
                    except:
                        raise ValueError('\n No se ha ingresado una fecha válida.')
                    crystal_leadtime = input(" Ingrese la cantidad de días que demorarán en llegar los cristales (solo presione Enter si el valor es 15): ")
                    if crystal_leadtime != '':
                        try:
                            int(crystal_leadtime)
                        except:
                            raise ValueError('\n Debe ingresar un número entero.')
                    else:
                        crystal_leadtime = 15
                    sale_year = input(" Ingrese el año de la fecha de venta del proyecto: ")
                    try:
                        int(sale_year)
                    except:
                        raise ValueError('\n El año debe ser un número entero.')
                    sale_month = input(" Ingrese el mes de la fecha de venta del proyecto: ")
                    try:
                        int(sale_month)
                    except:
                        raise ValueError('\n El mes debe ser un número entero. ')
                    if int(sale_month) >12 or int(sale_month) < 1:
                        raise ValueError('\n El mes debe ser un número entero entre 1 y 12.')
                    sale_day = input(" Ingrese el día de la fecha de venta del proyecto: ")
                    try:
                        int(sale_day)
                    except:
                        raise ValueError('\n El día debe ser un número entero.')
                    try:
                        sale_date =date(int(sale_year),int(sale_month),int(sale_day))
                    except:
                        raise ValueError('\n No se ha ingresado una fecha válida.')
                    sale_price = input(' Ingrese el precio de venta del proyecto: ')
                    try:
                        if int(sale_price) < 0:
                            raise ValueError('\n El precio de venta debe ser un número posititvo.')
                    except:
                        raise ValueError('\n El precio debe ser un número entero.')
                    createProject(db, contract_number, client_address, client_comuna_parsed, client_name, client_rut, linear_meters, square_meters, year, month, day, crystal_leadtime, sale_date, sale_price)
                    input('\n Proyecto creado con éxito. Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                # except:
                    # print('\n No se pudo ingresar correctamente el proyecto \n')
            else: 
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif(opt == '2'):
            if(level ==1):
                opt2 = input('\n Seleccione una de las siguientes alternativas: \n - 1: Si desea terminar un proyecto.\
                                                                                \n - 2: Si desea editar un proyecto existente.\
                                                                                \n Ingrese la alternativa elegida: ')
                if (opt2 == '1'):
                    try:
                        contract_number = input(" Ingrese el número de contrato del proyecto a editar: ")
                        try:
                            contract_number = int(contract_number)
                        except:
                            raise ValueError(' El número de contrato debe ser un número entero.')
                        with db_session:
                            p = db.Projects.get(contract_number = contract_number, finished = None)
                            if p == None:
                                raise ValueError(' No existe el número de contrato.')
                        finishProject(db, int(contract_number))
                        print('\n Proyecto terminado con éxito.')
                        input(' Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
                if (opt2 == '2'):
                    try:
                        contract_number = input("\n Ingrese el número de contrato del proyecto a editar: ")
                        with db_session:
                            try:
                                contract_number = int(contract_number)
                            except:
                                raise ValueError(' El número de contrato debe ser un número.' )
                        with db_session:
                            p = db.Projects.get(contract_number = contract_number, finished = None)
                            if p == None:
                                raise ValueError('\n No existe ese número de contrato.')
                        new_client_address = input("Ingrese la nueva direccion del cliente, solo presione Enter si la mantiene: ")
                        if new_client_address.replace(' ','') == '':
                            new_client_address = None
                        new_client_comuna = input("Ingrese la nueva comuna del cliente, solo presione Enter si la mantiene: ")
                        if new_client_comuna.replace(' ','') == '':
                            new_client_comuna_parsed = None
                        else:
                            try:
                                new_client_comuna_parsed = convert.get_fuzzy(new_client_comuna)
                            except:
                                raise ValueError('\n La comuna ingresada es inválida.')
                        new_client_name = input("Ingrese el nuevo nombre del cliente, solo presione Enter si lo mantiene: ")
                        if new_client_name.replace(' ','') == '':
                            new_client_name = None
                        new_client_rut = input("Ingrese el nuevo RUT del cliente, solo presione Enter si lo mantiene: ")
                        if new_client_rut.replace(' ','') == '':
                            new_client_rut = None
                        new_linear_meters = input("Ingrese los metros lineales del proyecto, solo presione Enter si se mantienen: ")
                        if new_linear_meters.replace(' ','') == '':
                            new_linear_meters = None
                        if new_linear_meters != None:
                            try:
                                new_linear_meters = float(new_linear_meters)
                            except:
                                raise ValueError('\n Los metros lineales deben ser un número.')
                            if new_linear_meters < 0:
                                raise ValueError('\n Los metros lineales deben ser un número positivo.')                            
                        new_square_meters = input("Ingrese los metros cuadrados del proyecto, solo presione Enter si se mantienen: ")
                        if new_linear_meters.replace(' ','') == '':
                            new_linear_meters = None
                        if new_linear_meters != None:
                            try:
                                new_linear_meters = float(new_linear_meters)
                            except:
                                raise ValueError('\n Los metros lineales deben ser un número.')
                            if new_linear_meters < 0:
                                raise ValueError('\n Los metros lineales deben ser un número positivo.')                        
                        new_real_linear_meters = input("Ingrese los metros lineales (reales) del proyecto, solo presione Enter si no se conocen: ")
                        if new_real_linear_meters.replace(' ','') == '':
                            new_real_linear_meters = None
                        if new_real_linear_meters != None:
                            try:
                                new_real_linear_meters = float(new_real_linear_meters)
                            except:
                                raise ValueError('\n Los metros lineales deben ser un número positivo.')
                            if new_real_linear_meters < 0:
                                raise ValueError('\n Los metros lineales deben ser un número positivo.')                            
                        new_deadline_year = input("Ingrese el nuevo año de entrega pactada del proyecto, solo presione Enter si se mantiene: ")
                        new_deadline_month = input("Ingrese el nuevo año de entrega pactada del proyecto, solo presione Enter si se mantiene: ")
                        new_deadline_day = input("Ingrese el nuevo año de entrega pactada del proyecto, solo presione Enter si se mantiene: ")
                        if new_deadline_day.replace(' ','') == '':
                            with db_session:
                                new_deadline_day = db.Projects.get(contract_number = contract_number, finished = None).deadline.day
                                if new_deadline_month.replace(' ','') == '':
                                    new_deadline_month = db.Projects.get(contract_number = contract_number, finished = None).deadline.month
                                    if new_deadline_year.replace(' ','') == '':
                                        new_deadline_year = db.Projects.get(contract_number = contract_number, finished = None).deadline.year
                        elif new_deadline_month == '':
                            with db_session:
                                new_deadline_month = db.Projects.get(contract_number = contract_number, finished = None).deadline.month
                                if new_deadline_year == '':
                                    new_deadline_year = db.Projects.get(contract_number = contract_number, finished = None).deadline.year
                        elif new_deadline_year == '':
                            with db_session:
                                new_deadline_year = db.Projects.get(contract_number = contract_number, finished = None).deadline.year
                        try:
                            new_deadline =date(int(new_deadline_year), int(new_deadline_month), int(new_deadline_day))
                        except:
                            raise ValueError('\n Debe ingresar una fecha válida.')
                        new_real_cost = input("Ingrese el costo real del proyecto, solo presione Enter si no se conoce: ")
                        if new_real_cost.replace(' ','') == '':
                            new_real_cost = None
                        if new_real_cost != None:
                            try:
                                new_real_cost = float(new_real_cost)
                                if float(new_real_cost) < 0:
                                    raise ValueError('\n Los costos deben ser un número positivo.')
                            except:
                                raise ValueError('\n Los costos deben ser un número positivo.')

                        new_crystal_leadtime = input("Ingrese la cantidad de días que demorarán en llegar los cristales, solo presione Enter si se mantiene: ")
                        if new_crystal_leadtime != None:
                            try:
                                new_crystal_leadtime = int(new_crystal_leadtime)
                            except:
                                raise ValueError('\n La cantidad de días debe ser un número entero.')
                        editProject(db, contract_number, new_client_address, new_client_comuna_parsed, new_client_name, new_client_rut, new_linear_meters, new_square_meters, new_real_linear_meters, new_deadline, new_estimated_cost=None, new_real_cost=new_real_cost, new_crystal_leadtime=new_crystal_leadtime)
                        print(' Edición realizada con éxito. ')
                        input(' Presione Enter para continuar: ')
                    except ValueError as ve:
                        print(ve)
                        input('Presione Enter para continuar: ')
                    except:
                        print('\n No se pudo realizar la edición.')
                        input('Presione Enter para continuar: ')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar: ')                
        elif(opt == '3'):
            if(level == 1):
                contract_number = input("\n Ingrese el número de contrato del proyecto a eliminar: ")
                try:
                    deleteProject(db, contract_number)
                    print('\n Proyecto eliminado exitosamente. Es altamente recomendable realizar una nueva planificación para mejorar las fechas de entrega.')
                    input(' Presione Enter para continuar: ')
                except:
                    print('\n Proyecto inexistente.')
                    input('Precione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif(opt == '4'):
            if(level == 1):
                opt_projects_activities = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ingresar datos de disponibilidad de un cliente. \
                                                                                           \n - 2: Si desea eliminar una indisponibilidad. \
                                                                                           \n - 3: Si desea ver la lista actual de indisponibilidades. \
                                                                                           \n Ingrese la alternativa elegida: ")

                if opt_projects_activities == '1':
                    try:
                        contract_number = input("\n Ingrese el número de contrato asociado al cliente: ")
                        with db_session:
                            try:
                                contract_number = int(contract_number)
                            except:
                                raise ValueError(' El número de contrato debe ser un número entero.')
                            p = db.Projects.get(contract_number = contract_number, finished = None)
                            if p == None:
                                raise ValueError(' Proyecto no encontrado.')
                        initial_year = input(" Ingrese el año en que comienza la actividad: ")
                        initial_month = input(" Ingrese el mes en que comienza la actividad: ")
                        initial_day = input(" Ingrese el día en que comienza la actividad: ")
                        try:
                            date(int(initial_year),int(initial_month),int(initial_day))
                        except:
                            raise ValueError('\n Fecha de inicio inválida.')
                        end_year = input(" Ingrese el año en que termina la actividad: ")
                        end_month = input(" Ingrese el mes en que termina la actividad: ")
                        end_day = input(" Ingrese el día en que termina la actividad: ")
                        try:
                            date(int(end_year),int(end_month),int(end_day))
                        except:
                            raise ValueError('\n Fecha de término inválida.')
                        createProjectActivity(db, project, 3, initial_year, initial_month, initial_day, end_year, end_month, end_day)
                        input('\n Indisponibilidad ingresada. Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input('Precione Enter para continuar.')
                elif opt_projects_activities == '2':
                    id_project_activity = input("\n Ingrese el ID de la indisponibilidad que quiere eliminar: ")
                    try:
                        deleteProjectActivity(db, id_project_activity)
                    except:
                        print('\n No existe esa indisponibilidad.')
                        input(' Presione Enter para continuar.')
                elif opt_projects_activities == '3':
                    printProjectsActivities(db)
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif(opt == '5'):
            if (level == 1):
                opt2 = input("\n Marque una de las siguientes opciones:\n - 1: Si desea ver proyectos vigentes. \
                                                                      \n - 2: Si desea ver proyectos terminados.\
                                                                      \n - 3: Si desea ver todos los proyectos. \
                                                                      \n - 4: Para volver atrás. \
                                                                      \n Ingrese la alternativa elegida: ")
                if opt2 == '1':
                    printCurrentProjects(db)
                    input(' Presione Enter para continuar.')
                elif opt2 == '2':
                    printFinishedProjects(db)
                    input(' Presione Enter para continuar.')
                elif opt2 == '3':
                    printProjects(db)
                    input(' Presione Enter para continuar.')
                else:
                    print('\n Ingreso inválido.')
                    input(' Presione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif (opt =='6'):
            if (level not in [1,2,3,4,5]) :
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
            else:
                try:
                    contract_number = input('\n Ingrese el número de contrato del cual quiere estimar el costo: ')
                    try:
                        int(contract_number)
                    except:
                        raise ValueError('\n El número de contrato debe ser un número.')
                    if int(contract_number)  < 0:
                        raise ValueError('\n El número de contrato debe ser un número entero positivo.')
                    with db_session:
                        if db.Projects.get(contract_number = contract_number, finished = None) == None:
                            raise ValueError('\n Número de contrato no existente.')
                    file_name = input(' Ingrese el nombre del archivo de la hoja de corte: ')
                    file_dir = file_name + ".xlsx"
                    if os.path.isfile(file_dir):
                        if (estimateCost(db, contract_number, file_name)):
                            createEngagements(db, contract_number, file_name)
                            commit()
                            input('\n Costo estimado exitosamente.')

                    else:
                        raise ValueError('\n Archivo no encontrado.')
                except ValueError as ve:
                    print(ve)                    
                    if (level not in [1,2,3,4,5]) :
                        break
                finally:
                    input(' Presione Enter para continuar.')
        elif(opt == '7'):
            break

def tasks_console(db, level):
    while True:
        opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea editar una tarea.\
                                                              \n - 2: Si desea ver las tareas actuales.\
                                                              \n - 3: Para editar parámetros asociados a costos.\
                                                              \n - 4: Para ingresar atrasos.\
                                                              \n - 5: Para ingresar datos de orden de compra de cristales.\
                                                              \n - 6: Para volver atrás.\
                                                              \n Ingrese la alternativa elegida: ")

        if(opt == '1'):
            if level in  [1,2,3,4,5]:
                opt2 = input("\n Marque una de las siguientes opciones: \n - 1: Ingresar fechas efectivas.\
                                                                        \n - 2: Ingreso de fallos.\
                                                                        \n - 3: Volver.\
                                                                        \n Ingrese la alternativa elegida: ")
                if (opt2 =='1'):
                    try:
                        new_contract_number = input(" Ingrese el número de contrato del proyecto asociado: ")
                        try:
                            new_contract_number = int(new_contract_number)
                        except:
                            raise ValueError(' El número de contrato debe ser un número entero.' )
                        with db_session:
                            p = db.Projects.get(contract_number = new_contract_number, finished = None)
                            if p == None:
                                raise ValueError('\n Proyecto inexistente.')
                        if(level == 1) or (level == 2):
                            new_id_skill = input(" Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
                            if int(new_id_skill) != 1 and int(new_id_skill) != 2 and int(new_id_skill) != 3 and int(new_id_skill) != 4:
                                raise ValueError('\n ID de habilidad no válida.')
                        if(level == 4):
                            new_id_skill = 1  
                        if (level == 3) :   
                            new_id_skill = 4    
                        if (level == 5):
                            new_id_skill = input(" Ingrese el ID de la habilidad requerida (1: dis, 2: ins): ")
                            if new_id_skill == '1':
                                new_id_skill = 2
                            if new_id_skill == '2':
                                new_id_skill = 4
                            else:
                                raise ValueError('\n Error de ingreso.')
                        with db_session:
                            t = db.Tasks.get(skill = db.Skills[new_id_skill], project = p)
                            if t == None:
                                raise ValueError( ' La tarea no existe en esta versión del proyecto.')
                        new_effective_initial_year = input(" Ingrese el año efectivo de inicio, solo presione Enter si mantiene la fecha efectiva actual: ")
                        if new_effective_initial_year != '':
                            new_effective_initial_month = input(" Ingrese el mes efectivo de inicio: ")
                            new_effective_initial_day = input(" Ingrese el dia efectivo de inicio: ")
                            try:
                                new_effective_initial_date = date(int(new_effective_initial_year),int(new_effective_initial_month),int(new_effective_initial_day))
                            except:
                                raise ValueError('\n No es una fecha válida.')
                        else:
                            new_effective_initial_date = None
                        if(new_effective_initial_year != None or t.effective_initial_date != None):
                            new_effective_end_year = input(" Ingrese el año efectivo de término, solo presione Enter si no ha terminado: ")
                            if new_effective_end_year != '':
                                new_effective_end_month = input(" Ingrese el mes efectivo de término, solo presione Enter si no ha terminado: ")
                                new_effective_end_day = input(" Ingrese el día efectivo de término, solo presione Enter si no ha terminado: ")
                                try:
                                    new_effective_end_date = date(int(new_effective_end_year),int(new_effective_end_month),int(new_effective_end_day))
                                except:
                                    raise ValueError('\n Fecha de término inválida.')
                            else:
                                new_effective_end_date = None

                        else:
                            new_effective_end_date = None
                        editTask(db, new_id_skill, new_contract_number, effective_initial_date = new_effective_initial_date, effective_end_date = new_effective_end_date)
                        input('\n Fecha agregada con éxito. Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
                elif(opt2 == '2'):
                    try:
                        contract_number_fail = input("\n Ingrese el número de contrato del proyecto en el que ha fallado una tarea: ")
                        try:
                            contract_number_fail = int(contract_number_fail)
                        except:
                            raise ValueError(' El número de contrato debe ser un número entero.' )
                        with db_session:
                            p = db.Projects.get(contract_number = contract_number_fail, finished = None)
                            if p == None:
                                raise ValueError('\n Número de contrato inexistente.')
                        if(level == 1) or (level == 2):
                            id_skill_fail = input(" Ingrese el ID de la habilidad donde ocurrió el fallo (1: rect, 2: dis, 3: fab, 4: ins): ")
                            try:
                                id_skill_fail = int(id_skill_fail)
                            except:
                                raise ValueError('\n Ingreso de habilidad inválida.')
                            if int(id_skill_fail) not in [1,2,3,4]:
                                raise ValueError('\n ID de habilidad no válida.')
                        if(level == 4) or (level == 6) :
                            id_skill_fail = 1
                        if (level == 7) :   
                            id_skill_fail = 2    
                        if (level == 8) :   
                            id_skill_fail = 3
                        if (level == 9) or (level == 3) :   
                            id_skill_fail = 4    
                        if (level == 5):
                            id_skill_fail = input(" Ingrese el ID de la habilidad requerida (1: dis, 2: ins): ")
                            if id_skill_fail == '1':
                                id_skill_fail = 2
                            if id_skill_fail == '2':
                                id_skill_fail = 4
                            else:
                                raise ValueError(' Error de ingreso. ')
                        with db_session:
                            task = db.Tasks.get( project = p, skill = db.Skills[id_skill_fail])
                            if task != None:
                                if task.effective_initial_date == None :
                                    raise ValueError('\n Esta tarea aun no ha comenzado.')
                        fail_cost = input("\n Ingrese el costo estimado de la falla: ")
                        try:
                            fail_cost = int(fail_cost)
                        except:
                            raise ValueError('\n El costo debe ser un número entero.')
                        if fail_cost < 0 :
                                raise ValueError('\n El costo debe ser un número no negativo.')
                        failedTask(db, contract_number_fail, id_skill_fail, fail_cost)
                        input(' Fallo ingresado con éxito. Presione Enter para continuar.')
                    except ValueError as ve:
                        print(ve)
                        input(' Presione Enter para continuar.')
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif(opt == '2'):
            if (level == 1):
                printTasks(db)
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif(opt == '3'):
            if(level == 1):
                opt2 = input('\n Marque una de las siguientes opciones: \n - 1: Si desea editar costos de flete.\
                                                                        \n - 2: Si desea editar costos de operaciones.\
                                                                        \n - 3: Si desea editar costos de viáticos.\
                                                                        \n - 4: Si desea editar costos de movilización.\
                                                                        \n - 5: Si desea editar parámetros de cristales.\
                                                                        \n - 6: Si desea editar parámetros de perfiles.\
                                                                        \n - 7: Si desea volver atrás.\
                                                                        \n Ingrese la alternativa elegida: ')
                try:
                    try:
                        int(opt2)
                        if int(opt2) not in range(1,8):
                            raise 
                    except:
                        raise ValueError('\n Debe ingresar una alternativa válida.')
                    if(int(opt2) == 7):
                        pass
                    elif( int(opt2) in range(1,7)):
                        file_name = input('\n Ingrese el nombre del archivo: ')
                        file_dir = file_name + ".xlsx"
                        if os.path.isfile(file_dir):
                            if opt2 == '1':
                                if updateFreightCosts(db, file_name):
                                    print('\n Edición realizada exitosamente.')
                            if opt2 == '2':
                                if updateOperatingCosts(db, file_name):
                                    print('\n Edición realizada exitosamente.')
                            if opt2 == '3':
                                if updateViaticCosts(db, file_name):
                                    print('\n Edición realizada exitosamente.')
                            if opt2 == '4':
                                if updateMovilizationCosts(db, file_name):
                                    print('\n Edición realizada exitosamente.')
                            if opt2 == '5':
                                if updateCrystalsParameters(db, file_name):
                                    print('\n Edición realizada exitosamente.')
                            if opt2 == '6':
                                if updateProfilesParameters(db, file_name):
                                    print('\n Edición realizada exitosamente.')
                            input(' Presione Enter para continuar.')
                        else:
                            raise ValueError('\n Archivo no encontrado.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
                
            else:
                print('\n Acceso denegado.')
                input(' Presione Enter para continuar.')
        elif(opt == '4'):
            try:
                contract_number = input(" Ingrese el número de contrato del proyecto asociado: ")
                try:
                    contract_number = int(contract_number)
                except:
                    raise ValueError(' El número de contrato debe ser un número entero.')
                with db_session:
                    if db.Projects.get(contract_number = contract_number, finished = None) == None:
                        raise ValueError(' Número de contrato inexistente.')
                id_skill = input(" Ingrese el ID de la habilidad donde ocurrió el atraso (1: rect, 2: dis, 3: fab, 4: ins): ")
                try:
                    id_skill = int(id_skill)
                except:
                    raise ValueError(' Ingreso de habilidad inválida.')
                if int(id_skill) not in [1,2,3,4]:
                    raise ValueError(' ID de habilidad no válida.')
                with db_session:
                    task = db.Tasks.get( project = db.Projects.get(contract_number = contract_number, finished = None), skill = db.Skills[id_skill], failed = None)
                    if task == None:
                        raise ValueError(' Tarea no encontrada.')
                    if task.effective_initial_date == None :
                        raise ValueError(' Esta tarea aun no ha comenzado.')
                    td = select( td for td in db.Tasks_Delays if td.task == task)
                    if len(td) >0 :
                        largo = str(len(td))
                        data = [d.to_dict() for d in td]
                        df = pandas.DataFrame(data, columns = ['delay']) 
                        df.columns = ['Dias de atraso']
                        print('\n La tarea tiene ingresada ' + largo + ' atrasos. Los atrasos son los siguientes: ')
                        print(tabulate(df, headers='keys', tablefmt='psql'))
                        agree = input(' ¿Desea realizar el ingreso de atrasos de todos modos? : \n - 1: Si \
                                                                                               \n - 0: No \
                                                                                               \n Ingrese la alternativa elegida: ')
                        try:
                            int(agree)
                            if int(agree) not in [0,1]:
                                exception = ' Ingreso incorrecto. Ingreso de atraso cancelado.'
                                raise
                            elif int(agree) == 0:
                                exception = ' Ingreso de atraso cancelado.' 
                                raise 
                        except:
                            if exception:
                                raise ValueError(exception)
                            else:
                                raise ValueError(' Ingreso incorrecto de parámetros. Ingreso de atraso cancelado.')
                    delay = input(' Ingrese el número de días que se atrasó la tarea: ')
                    try:
                        delay = int(delay)
                    except:
                        raise ValueError('\n ID de habilidad no válida.')
                    if delay < 0 :
                        planned_end_date = select( et for et in db.Employees_Tasks if et.task == task).first().planned_end_date
                        if sumDays(date.today(),-1*delay) > planned_end_date: 
                            raise ValueError('\n Según este ingreso la tarea ya terminó. Ingrese una fecha efectiva de término y no un atraso negativo.')
                createDelay(db,task,delay)
                print('\n Atraso ingresado exitosamente.')
            except ValueError as ve:
                print(ve)
            finally:
                input(' Presione Enter para continuar.')
        elif(opt == '5'):
            opt2 = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ingresar/editar la orden de compra.\
                                                                    \n - 2: Si desea ingresar/editar la fecha efectiva de llegada de los cristales.\
                                                                    \n Ingrese la alternativa elegida: ")
            if opt2 == '1':
                try:
                    id_issuer_order = input('\n Ingrese su ID: ')
                    if len(id_issuer_order.replace(' ','')) < 1:
                        raise ValueError(' Debe ingresar su ID. ')
                    contract_number = input(' Ingrese el número de contrato del proyecto asociado a la orden de compra de cristales: ')
                    try:
                        contract_number = int(contract_number)
                    except:
                        raise ValueError(' El número de contrato debe ser un número positivo.')
                    with db_session:
                        project = db.Projects.get(contract_number = contract_number, finished = None)
                        if project == None:
                            raise ValueError(' No existe ese número de contrato. ')
                    id_crystal_provider = input(' Ingrese el ID del proveedor de cristales: ')
                    if len(id_crystal_provider.replace(' ','')) < 1:
                        raise ValueError(' Debe ingresar el ID del proveedor. ')
                    effective_issuing_date_year = input(' Ingrese el año en que se envío la orden de compra al proveedor (solo presione Enter si la fecha es hoy): ')
                    if effective_issuing_date_year == '':
                        effective_issuing_date = date.today()
                    else:
                        effective_issuing_date_month = input(' Ingrese el mes en que se envío la orden de compra al proveedor: ')
                        effective_issuing_date_day = input(' Ingrese el día en que se envío la orden de compra al proveedor: ')
                        try:
                            effective_issuing_date = date(int(effective_issuing_date_year),int(effective_issuing_date_month),int(effective_issuing_date_day))
                        except:
                            raise ValueError('\n No se ha ingresado una fecha válida.')
                    original_arrival_date_year = input(' Ingrese el año en que llegarán los cristales: ')
                    original_arrival_date_month = input(' Ingrese el mes en que llegarán los cristales: ')
                    original_arrival_date_day = input(' Ingrese el día en que llegarán los cristales: ')
                    try:
                        original_arrival_date = date(int(original_arrival_date_year),int(original_arrival_date_month),int(original_arrival_date_day))
                    except:
                        raise ValueError('\n No se ha ingresado una fecha válida.')
                    editCrystalSalesOrder(db, project, original_arrival_date, effective_issuing_date, id_issuer_order, id_crystal_provider)
                    print(' Edición realizada exitosamente.')
                    input(' Presione Enter para continuar.')
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
                
            elif opt2 == '2':
                try:
                    contract_number = input('\n Ingrese el número de contrato del proyecto asociado a la orden de compra de cristales: ')
                    try:
                        contract_number = int(contract_number)
                    except:
                        raise ValueError(' El número de contrato debe ser un número entero.')
                    with db_session:
                        project = db.Projects.get(contract_number = contract_number, finished = None)
                        if project == None:
                            raise ValueError(' No existe ese número de contrato. ')
                    effective_arrival_date_year = input(' Ingrese el año de llegada de los cristales (solo presione Enter si la fecha es hoy): ')
                    if effective_arrival_date_year == '':
                        effective_arrival_date = date.today()
                    else:
                        effective_arrival_date_month = input(' Ingrese el mes de llegada de los cristales: ')
                        effective_arrival_date_day = input(' Ingrese el día de llegada de los cristales: ')
                        try:
                            effective_arrival_date = date(int(effective_arrival_date_year), int(effective_arrival_date_month), int(effective_arrival_date_day))
                        except:
                            raise ValueError('\n No se ha ingresado una fecha válida.')
                    editCrystalArrival(db, project, effective_arrival_date)
                    print(' Edición realizada exitosamente.')
                    input(' Presione Enter para continuar.')
                    
                except ValueError as ve:
                    print(ve)
                    input(' Presione Enter para continuar.')
                
        elif(opt == '6'):
            break






















