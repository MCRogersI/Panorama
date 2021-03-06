import getpass
from Users.features import createUser, deleteUser, editUserLevel, printUsers
from pony.orm import *
def users_console(db):
    while True:
        opt = input( "\n Marque una de las siguientes opciones:\n - 1: Crear usuario.\
                                                               \n - 2: Editar nivel de usuario.\
                                                               \n - 3: Eliminar usuario.\
                                                               \n - 4: Ver usuarios actuales.\
                                                               \n - 5: Para volver atrás. \
                                                               \n Ingrese la alternativa elegida: ")
        if (opt == '1') :
            try:
                level = input('\n Ingrese el nivel del usuario que quiere crear: ')
                try:
                    level = int(level)
                except:
                    raise ValueError('\n Nivel inválido.')
                if level not in range(1,10):
                    raise ValueError('\n Nivel inválido. ')
                elif level not in [6,7,8,9]:
                    name = input(' Ingrese el nombre de usuario: ')
                    if name == '':
                        raise ValueError('\n El usuario debe tener un nombre.')
                else:
                    name = input(' Ingrese el RUT del usuario sin puntos ni número verificador: ')
                    try:
                        int(name)
                    except:
                        raise ValueError('\n RUT inválido. ')
                with db_session:
                    u = db.Users.get(user_name = name)
                    if u != None:
                        raise ValueError('\n Usuario ya existente.')
                password = getpass.getpass(' Ingrese contraseña para el usuario: ')
                check_password = getpass.getpass(' Ingrese nuevamente la contraseña para el usuario: ')
                if password == check_password:
                    createUser(db,name, level,password)
                    print('\n Usuario creado con éxito.')
                    input(' Presione Enter para continuar. ')
                else:
                    raise ValueError('\n Contraseñas no coinciden.')
            except ValueError as ve:
                print(ve)
                input(' Presione Enter para continuar.')
        if (opt == '2'):
            try:
                name = input('\n Ingrese el nombre de usuario: ')
                new_level = input(' Ingrese el nuevo nivel de usuario: ')
                try:
                    new_level = int(new_level)
                except:
                    raise ValueError('\n El nivel debe ser un número entero.')
                with db_session:
                    u = db.Employees.get(id = name)
                if u == None and new_level in [7,8]:
                    print('\n Usuario no existe como trabajador. Cambio de nivel anulado.')
                else:
                    password = getpass.getpass(' Ingrese la contraseña del usuario: ')
                    editUserLevel(db, name, new_level, password)
            except ValueError as ve:
                print(ve)
            input(' Presione Enter para continuar.')
        if (opt == '3'):
            name = input('\n Ingrese nombre de usuario que desea eliminar: ')
            with db_session:
                user = db.Users.get(user_name = name)
            if user == None:
                print('\n El usuario no existe.')
                input(' Presione Enter para continuar.')
            else:
                deleteUser(db,name)
                print('\n Usuario eliminado con éxito.')
                input( ' Presione Enter para continuar.')
        if (opt =='4'):
            printUsers(db)
            input(' Presione Enter para continuar.')
        if (opt == '5'):
            break