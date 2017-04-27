from datetime import date
from pony.orm import *
from Projects.features import createProject, printProjects, editProject, deleteProject, createTask, editTask, printTasks, failedTask, createProjectActivity, deleteProjectActivity, printProjectsActivities
# from Projects.costs import estimateCost

def projects_console(db, level):
    while True:
        if level == 1:
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea crear un proyecto. \
                                                                  \n - 2: Si desea editar un proyecto. \
                                                                  \n - 3: Eliminar un proyecto. \
                                                                  \n - 4: Si desea manejar datos sobre disponibilidad de un cliente. \
                                                                  \n - 5: Para ver proyectos actuales. \
                                                                  \n - 6: Para estimar costos del proyecto. \
                                                                  \n - 7: Para volver atrás. \
                                                                  \n Ingrese la alternativa elegida: ")
        if level == 2:
            opt = input("\n Marque una de las siguientes opciones: \n - 1: Si desea crear un proyecto.\
                                                                   \n - 2: Si desea editar un proyecto.\
                                                                   \n - 3: Para ver proyectos actuales. \
                                                                   \n - 4 : Para estimar costos del proyecto. \
                                                                   \n - 5: Para volver atrás. \
                                                                   \n Ingrese la alternativa elegida: ")
        if level == 3:
            opt = input("\n Marque una de las siguientes opciones:  \n - 1: Para ver proyectos actuales.\
                                                                    \n - 2: Para volver atrás. \
                                                                    \n Ingrese la alternativa elegida: ")

        if(opt == '1' and (level == 1 or level == 2)):
            try:
                contract_number = input("\n Ingrese el número de contrato: ")
                try:
                    int(contract_number)
                except:
                    raise ValueError('No es un número válido')
                with db_session:
                    if len(select( p for p in db.Projects if p.contract_number == int(contract_number))) > 0:
                        raise ValueError('\n Este número de contrato ya existe \n')
                client_address = input("Ingrese la direccion del cliente: ")
                if client_address == '':
                    raise ValueError('\n Debe ingresar una dirección \n')
                client_comuna = input("Ingrese la comuna del cliente: ")
                if client_comuna == '':
                    raise ValueError('\n Debe ingresar una comuna \n')
                client_name = input("Ingrese el nombre del cliente: ")
                if client_name == '':
                    raise ValueError('\n Debe ingresar un nombre \n')
                client_rut = input("Ingrese el RUT del cliente: ")
                if client_rut == '':
                    raise ValueError('\n Debe ingresar un rut \n')
                linear_meters = input("Ingrese los metros lineales del proyecto: ")
                try:
                    int(linear_meters)
                except:
                    raise ValueError('\n Los metros lineales deben ser un número entero \n')
                if int(linear_meters) <0:
                    raise ValueError('\n Los metros lineales deben ser un número entero positivo \n')
                year = input("ingrese el año de la fecha de entrega pactada del proyecto: ")
                try:
                    int(year)
                except:
                    raise ValueError('\n El año debe ser un número entero \n')
                month = input("ingrese el mes de la fecha de entrega pactada del proyecto: ")
                try:
                    int(month)
                except:
                    raise ValueError('\n ser un número entero \n')
                if int(month) >12 or int(month) < 1:
                    raise ValueError('\n El mes debe ser un número entero entre 1 y 12 \n')
                day = input("ingrese el día de la fecha de entrega pactada del proyecto: ")
                try:
                    int(day)
                except:
                    raise ValueError('\n El día debe ser un número entero \n')
                try:
                    date(int(year),int(month),int(day))
                except:
                    raise ValueError('\n No se ha ingresado una fecha válida \n')
                crystal_leadtime = input(" Ingrese la cantidad de días que demorarán en llegar los cristales (solo presione Enter si el valor es 15): ")
                try:
                    int(crystal_leadtime)
                except:
                    crystal_leadtime = 15
                sale_year = input("ingrese el año de la fecha de venta del proyecto: ")
                try:
                    int(sale_year)
                except:
                    raise ValueError('\n El año debe ser un número entero \n')
                sale_month = input("ingrese el mes de la fecha de venta del proyecto: ")
                try:
                    int(sale_month)
                except:
                    raise ValueError('\n ser un número entero \n')
                if int(sale_month) >12 or int(sale_month) < 1:
                    raise ValueError('\n El mes debe ser un número entero entre 1 y 12 \n')
                sale_day = input("ingrese el día de la fecha de venta del proyecto: ")
                try:
                    int(sale_day)
                except:
                    raise ValueError('\n El día debe ser un número entero \n')
                try:
                    sale_date =date(int(sale_year),int(sale_month),int(sale_day))
                except:
                    raise ValueError('\n No se ha ingresado una fecha válida \n')
                sale_price = input('\n Ingrese el precio de venta del proyecto \n')
                try:
                    if int(sale_price) < 0:
                        raise ValueError('\n El precio de venta debe ser un número posititvo \n')
                except:
                    raise ValueError('\n El precio debe ser un número entero \n')
                createProject(db, contract_number, client_address, client_comuna, client_name, client_rut, linear_meters, year, month, day, crystal_leadtime,sale_date, sale_price)
            except ValueError as ve:
                print(ve)
            except:
                print('\n No se pudo ingresar correctamente el proyecto \n')
        elif(opt == '2' and (level == 1 or level == 2)):
            try:
                contract_number = input("\n Ingrese el número de contrato del proyecto a editar: ")
                with db_session:
                    try:
                        db.Projects[int(contract_number)].contract_number
                    except:
                        raise ValueError('\n No existe ese número de contrato \n')
                new_client_address = input("Ingrese la nueva direccion del cliente, solo presione enter si la mantiene: ")
                new_client_comuna = input("Ingrese la nueva comuna del cliente, solo presione enter si la mantiene: ")
                new_client_name = input("Ingrese el nuevo nombre del cliente, solo presione enter si lo mantiene: ")
                new_client_rut = input("Ingrese el nuevo RUT del cliente, solo presione enter si lo mantiene: ")
                new_linear_meters = input("Ingrese los metros lineales del proyecto, solo presione enter si se mantienen: ")
                new_real_linear_meters = input("Ingrese los metros lineales (reales) del proyecto, solo presione enter si no se conocen: ")
                new_deadline_year = input("Ingrese el nuevo año de entrega pactada del proyecto, solo presione enter si se mantiene: ")
                new_deadline_month = input("Ingrese el nuevo año de entrega pactada del proyecto, solo presione enter si se mantiene: ")
                new_deadline_day = input("Ingrese el nuevo año de entrega pactada del proyecto, solo presione enter si se mantiene: ")
                new_estimated_cost = input("Ingrese el costo estimado del proyecto: ")
                new_real_cost = input("Ingrese el costo real del proyecto, solo presione enter si no se conoce: ")
                new_crystal_leadtime = input("Ingrese la cantidad de días que demorarán en llegar los cristales, solo presione enter si se mantiene: ")
                if new_client_address == '':
                    new_client_address = None
                if new_client_comuna == '':
                    new_client_comuna = None
                if new_client_name == '':
                    new_client_name = None
                if new_client_rut == '':
                    new_client_rut = None
                if new_linear_meters == '':
                    new_linear_meters = None
                if new_real_linear_meters == '':
                    new_real_linear_meters = None
                if new_deadline_day == '':
                    new_deadline_day = None
                    if new_deadline_month == '':
                        new_deadline_month = None
                        if new_deadline_year == '':
                            new_deadline_year = None
                elif new_deadline_month == '':
                    with db_session:
                        new_deadline_month = db.Projects[int(contract_number)].deadline.month
                        if new_deadline_year == '':
                            new_deadline_year = db.Projects[int(contract_number)].deadline.year
                elif new_deadline_year == '':
                    with db_session:
                        new_deadline_year = db.Projects[int(contract_number)].deadline.year
                if new_real_cost == '':
                    new_real_cost = None
                if new_linear_meters != None:
                    try:
                        int(new_linear_meters)
                        if int(new_linear_meters) < 0:
                            raise ValueError('\n Los metros lineales deben ser un número entero positivo \n')
                    except:
                        raise ValueError('\n Los metros lineales deben ser un número entero positivo \n')
                if new_real_linear_meters != None:
                    try:
                        int(new_real_linear_meters)
                        if int(new_real_linear_meters) < 0:
                            raise ValueError('\n Los metros lineales deben ser un número entero positivo \n')
                    except:
                        raise ValueError('\n Los metros lineales deben ser un número entero positivo \n')
                if new_real_cost != None:
                    try:
                        float(new_real_cost)
                        if float(new_real_cost) < 0:
                            raise ValueError('\n Los costos deben ser un número positivo \n')
                    except:
                        raise ValueError('\n Los costos deben ser un número positivo \n')
                if new_deadline_year != None or new_deadline_month != None or new_deadline_day != None:
                    try:
                        new_deadline =date(int(new_deadline_year), int(new_deadline_month), int(new_deadline_day))
                    except:
                        raise ValueError('\n Debe ingresar una fecha válida. \n')
                else:
                    new_deadline = None
                if new_crystal_leadtime != None:
                    try:
                        int(new_crystal_leadtime)
                    except:
                        raise ValueError('\n La cantidad de días debe ser un número entero \n')
                editProject(db, contract_number, new_client_address, new_client_comuna, new_client_name, new_client_rut, new_linear_meters, new_real_linear_meters, new_deadline, new_estimated_cost=None, new_real_cost=new_real_cost, new_crystal_leadtime=new_crystal_leadtime)
            except ValueError as ve:
                print(ve)
                input('Precione cualquier tecla para volver \n')
            except:
                print('\n No se pudo realizar la edición. \n')
                input('Precione cualquier tecla para volver \n')

        elif(opt == '3' and level == 1):
            contract_number = input("\n Ingrese el número de contrato del proyecto a eliminar: ")
            try:
                deleteProject(db, contract_number)
            except:
                print('\n Proyecto inexistente \n')
                input('Precione cualquier tecla para volver \n')

        elif(opt == '4' and level == 1):
            opt_projects_activities = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ingresar datos de disponibilidad de un cliente. \
                                                                                       \n - 2: Si desea eliminar una indisponibilidad. \
                                                                                       \n - 3: Si desea ver la lista actual de indisponibilidades. \
                                                                                       \n Ingrese la alternativa elegida: ")

            if opt_projects_activities == '1':
                try:
                    project = input("\n Ingrese el número de contrato asociado al cliente: ")
                    with db_session:
                        try:
                            db.Projects[int(project)].contract_number
                        except:
                            raise ValueError('\n No existe ese número de contrato \n')
                    initial_year = input(" Ingrese el año en que comienza la actividad: ")
                    initial_month = input(" Ingrese el mes en que comienza la actividad: ")
                    initial_day = input(" Ingrese el día en que comienza la actividad: ")
                    try:
                        date(int(initial_year),int(initial_month),int(initial_day))
                    except:
                        raise ValueError('\n Fecha de inicio inválida \n')
                    end_year = input(" Ingrese el año en que termina la actividad: ")
                    end_month = input(" Ingrese el mes en que termina la actividad: ")
                    end_day = input(" Ingrese el día en que termina la actividad: ")
                    try:
                        date(int(end_year),int(end_month),int(end_day))
                    except:
                        raise ValueError('\n Fecha de término inválida \n')
                    createProjectActivity(db, project, 3, initial_year, initial_month, initial_day, end_year, end_month, end_day)
                    input('\n Indisponibilidad ingresada. Presione una tecla para continuar: ')
                except ValueError as ve:
                    print(ve)
                    input('Precione cualquier tecla para volver \n')
            elif opt_projects_activities == '2':
                id_project_activity = input("\n Ingrese el ID de la indisponibilidad que quiere eliminar: ")
                try:
                    deleteProjectActivity(db, id_project_activity)
                except:
                    print('\n No existe esa indisponibilidad \n')
                    input('Precione cualquier tecla para volver \n')
            elif opt_projects_activities == '3':
                print('\n')
                printProjectsActivities(db)

            
        elif(opt == '5' and level == 1) or (opt == '3' and level == 2) or (opt == '1' and level == 3):
            printProjects(db)
        elif (opt =='6' and level == 1) or (opt== '4' and level == 2):
            print('\n Estamos trabajando para usted. \n')
            input('\n Presione cualquier tecla para continuar. \n')
            # try:
                # contract_number = input('\n Ingrese el número de contrato del cual quiere estimar el costo \n')
                # if int(contract_number)  < 0:
                    # raise ValueError('\n El número de contrato debe ser un número entero positivo. \n')
                # with db_session:
                    # if db.Projects.get(contract_number = contract_number) == None:
                        # raise ValueError('\n Número de contrato no existente. \n')
                # file_name = input('\n Ingrese el nombre del archivo de la hoja de corte \n')
                # file_dir = file_name + ".xls"
                # if os.path.isfile(file_dir):
                    # estimateCost(db, contract_number, file_name)
                    # input('\n Costo estimado exitosamente. Presione una tecla para continuar.\n')
                # else:
                    # raise ValueError('\n Archivo no encontrado. \n')
            # except ValueError as ve:
                # print(ve)
                # input('\n Presione una tecla para continuar. \n')
        elif(opt == '7' and level == 1) or(opt == '5' and level == 2) or (opt == '2' and level == 3):
            break

def tasks_console(db, level):
    while True:
        if level == 1:
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea editar una tarea. \n - 2: Si desea ingresar un fallo en una tarea. \n - 3: Si desea ver las tareas actuales. \n - 4: Para volver atrás. \n")
        if level == 2:
            opt = input("\n Marque una de las siguientes opciones:\n - 1: Si desea editar una tarea. \n - 2: Si desea ingresar un fallo en una tarea. \n - 3: Si desea ver las tareas actuales. \n - 4: Para volver atrás. \n")
        if level == 3:
            opt = input("\n Marque una de las siguientes opciones: \n - 1: Si desea ver las tareas actuales. \n - 2: Para volver atrás. \n")

        if(opt == '1' and (level == 1 or level == 2)):
            #id = input("\n Ingrese el ID de la tarea: ")
            try:
                id_skill = input("\n Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
                try:
                    int(id_skill)
                    if 0 > int(id_skill) or 4 < int(id_skill):
                        raise ValueError('\n Ingreso incorrecto de habilidad \n')
                except:
                    raise ValueError('\n Ingreso incorrecto de habilidad \n')
                contract_number = input("\n Ingrese el número de contrato del proyecto asociado: ")
                original_initial_year = input("\n Ingrese el año estimado de inicio: ")
                original_initial_month = input("\n Ingrese el mes estimado de inicio: ")
                original_initial_day= input("\n Ingrese el dia estimado de inicio: ")
                try:
                    original_initial_date = date(int(original_initial_year),int(original_initial_month),int(original_initial_day))
                except:
                    raise ValueError('\n Fecha de inicio original inválida \n')

                original_end_year = input("\n Ingrese el año estimado de término: ")
                original_end_month = input("\n Ingrese el mes estimado de término: ")
                original_end_day = input("\n Ingrese el dia estimado de término: ")
                try:
                    original_end_date = date(int(original_end_year),int(original_end_month),int(original_end_day))
                except:
                    raise ValueError('\n Fecha de término original inválida \n')
                effective_initial_year = input("\n Ingrese el año efectivo de inicio, solo presione enter si no ha comenzado: ")
                effective_initial_month = input("\n Ingrese el mes efectivo de inicio, solo presione enter si no ha comenzado: ")
                effective_initial_day = input("\n Ingrese el dia efectivo de inicio, solo presione enter si no ha comenzado: ")
                try:
                    if effective_initial_year != '' or effective_initial_month != '' or effective_initial_day != '':
                        effective_initial_date = date(int(effective_initial_year),int(effective_initial_month),int(effective_initial_day))
                    else:
                        effective_initial_date = None
                except:
                    raise ValueError('\n Fecha de inicio efectiva inválida \n')
                effective_end_year = input("\n Ingrese el año efectivo de término, solo presione enter si no ha comenzado: ")
                effective_end_month = input("\n Ingrese el mes efectivo de término, solo presione enter si no ha comenzado: ")
                effective_end_day = input("\n Ingrese el dia efectivo de término, solo presione enter si no ha comenzado: ")
                try:
                    if effective_end_year != '' or effective_end_month != '' or effective_end_day != '':
                        effective_end_date = date(int(effective_end_year),int(effective_end_month),int(effective_end_day))
                    else:
                        effective_end_date = None
                except:
                    raise ValueError('\n Fecha de término efectiva inválida \n')

                createTask(db, id_skill, contract_number, original_initial_date, original_end_date, effective_initial_date, effective_end_date)
            except ValueError as ve:
                print(ve)
        elif(opt == '2' and (level == 1 or level == 2)):
            try:
                id_edit = input("\n Ingrese el ID de la tarea que desea editar: ")
                with db_session:
                    if db.Tasks.get(id = id_edit) == None:
                       raise ValueError('\n No existe esa tarea. \n')
                new_id_skill = input(" Ingrese el ID de la habilidad requerida (1: rect, 2: dis, 3: fab, 4: ins): ")
                if int(new_id_skill) != 1 and int(new_id_skill) != 2 and int(new_id_skill) != 3 and int(new_id_skill) != 4:
                    raise ValueError('\n ID de habilidad no válida. \n')
                new_contract_number = input(" Ingrese el número de contrato del proyecto asociado: ")
                with db_session:
                    if db.Projects.get(contract_number = new_contract_number) != None:
                        raise ValueError('\n Proyecto inexistente. \n')
                new_effective_initial_year = input(" Ingrese el año efectivo de inicio, solo presione enter si no ha comenzado: ")
                if new_effective_initial_year != '':
                    new_effective_initial_month = input(" Ingrese el mes efectivo de inicio: ")
                    new_effective_initial_day = input(" Ingrese el dia efectivo de inicio: ")
                    try:
                        new_effective_initial_date = date(new_effective_initial_year,new_effective_initial_month,new_effective_initial_day)
                    except:
                        raise ValueError('\n No es una fecha válida \n')
                if(new_effective_initial_year != ''):
                    new_effective_end_year = input(" Ingrese el año efectivo de término, solo presione enter si no ha terminado: ")
                    if new_effective_end_year != '':
                        new_effective_end_month = input(" Ingrese el mes efectivo de término, solo presione enter si no ha terminado: ")
                        new_effective_end_day = input(" Ingrese el día efectivo de término, solo presione enter si no ha terminado: ")
                        try:
                            new_effective_end_date = date(new_effective_end_year,new_effective_end_month,new_effective_end_day)
                        except:
                            raise ValueError('\n Fecha de término inválida. \n')
                    else:
                        new_effective_end_date = None

                else:
                    new_effective_initial_date = None
                    new_effective_end_date = None
                # new_original_initial_date = datetime.strptime(new_original_initial_date, '%Y-%m-%d')
                # new_original_end_date = datetime.strptime(new_original_end_date, '%Y-%m-%d')
                editTask(db, id_edit, new_id_skill, new_contract_number, original_initial_date =None, original_end_date = None, efective_initial_date = new_effective_initial_date, efective_end_date = new_effective_end_date)
            except ValueError as ve:
                print(ve)
        elif(opt == '3' and (level == 1 or level == 2)):
            try:
                contract_number_fail = input("\n Ingrese el número de contrato del proyecto en el que ha fallado una tarea: ")
                with db_session:
                    if db.Tasks.get(contract_number = contract_number_fail) != None:
                        raise ValueError('\n Número de contrato inexistente \n')
                id_skill_fail = input("\n Ingrese el ID de la habilidad asociada a la tarea (1: rect, 2: dis, 3: fab, 4: ins): ")
                try:
                    if 0 > int(id_skill_fail) or int(id_skill_fail) > 4:
                        raise ValueError(' \n Ingreso inválido de habilidad \n')
                except:
                    raise ValueError(' \n Ingreso inválido de habilidad \n')
                fail_cost = input("\n Ingrese el costo estimado de la falla: ")
                try:
                    if float(fail_cost) < 0 :
                        raise ValueError(' \n El costo debe ser un número no negativo \n')
                except:
                    raise ValueError(' \n El costo debe ser un número no negativo \n')
                failedTask(db, contract_number_fail, id_skill_fail, fail_cost)
            except ValueError as ve:
                print(ve)
            
        elif(opt == '3' and (level == 1 or level == 2)) or (opt == '1' and level == 3):
            printTasks(db)

        elif(opt == '7' and (level == 1 or level == 2)) or (opt == '2' and level == 3):
            break






















