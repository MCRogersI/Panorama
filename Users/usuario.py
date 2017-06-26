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
                level = input('\n Ingrese el nivel de usuario que quiere crear: ')
                try:
                    level = int(level)
                except:
                    raise ValueError(' Nivel inválido.')
                if level not in range(1,10):
                    raise ValueError(' Nivel no válido. ')
                elif level not in [6,7,8,9]:
                    name = input('\n Ingrese el Nombre del usuario: ')
                    if name == '':
                        raise ValueError(' El usuario debe tener un nombre.')
                else:
                    name = input(' Ingrese el rut del usuario sin puntos ni número verificador: ')
                    try:
                        int(name)
                    except:
                        raise ValueError(' rut inválido. ')
                with db_session:
                    u = db.Users.get(user_name = name)
                    if u != None:
                        raise ValueError(' Usuario ya existente. ')
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
            name = input('\n Ingrese el RUT del usuario: ')
            new_level = input(' Ingrese el nuevo nivel de usuario: ')
            password = getpass.getpass(' Ingrese la contraseña del usuario: ')
            editUserLevel(db,name,new_level, password)
            input(' Presione Enter para continuar.')
        if (opt == '3'):
            name = input(' Ingrese usuario que desea eliminar: ')
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
        if (opt == '5'):
            break