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
                    int(level)
                except:
                    raise ValueError('\n Nivel inválido \n')
                if level not in [6,7,8,9]:
                    name = input('\n Ingrese el Nombre del usuario: ')
                else:
                    name = input('\n Ingrese el rut del usuario sin puntos ni número verificador: ')
                    try:
                        int(name)
                    except:
                        raise ValueError('\n rut inválido. \n')
                password = getpass.getpass('\n Ingrese contraseña para el usuario: ')
                check_password = getpass.getpass('\n Ingrese nuevamente la contraseña para el usuario: ')
                if password == check_password:
                    createUser(db,name, level,password)
                    print(' Usuario creado con éxito.')
                    input(' Presione Enter para continuar. ')
                else:
                    raise ValueError('Contraseñas no coinciden. ')
            except ValueError as ve:
                print(ve)
                input(' Presione Enter para continuar. ')
                
                
        if (opt == '2'):
            name = input(' Ingrese el rut del usuario: ')
            new_level = input(' Ingrese el nuevo nivel de usuario: ')
            password = getpass.getpass(' Ingrese la contraseña del usuario: ')
            editUserLevel(db,name,new_level, password)
        if (opt == '3'):
            name = input(' Ingrese usuario que desea eliminar: ')
            with db_session:
                user = db.Users.get(user_name = name)
            if user == None:
                print(' El usuario no existe. ')
                input( ' Presione Enter para continuar. ')
            else:
                deleteUser(db,name)
        if (opt =='4'):
            printUsers(db)
        if (opt == '5'):
            break