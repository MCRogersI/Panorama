import getpass
from Users.features import createUser, deleteUser, editUserLevel

def users_console(db):
    while True:
        opt = input( "\n Marque una de las siguientes opciones:\n - 1: Crear usuario.\
                                                               \n - 2: Editar nivel de usuario.\
                                                               \n - 3: Eliminar usuario.\
                                                               \n - 4: Para volver atrás. \
                                                               \n Ingrese la alternativa elegida: ")
        if (opt == '1') :
            try:
                level = input('\n Ingrese el nivel de usuario que quiere crear: ')
                try:
                    int(level)
                except:
                    raise ValueError('\n Nivel inválido \n')
                if level not in [6,7,8,9]:
                    name = input('\n Ingrese el nombre del usuario: ')
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
                else:
                    raise ValueError('\n Contraseñas no coinciden! \n')
            except ValueError as ve:
                print(ve)
                input('\n Presione una tecla para continuar: ')
                
                
        if (opt == '2'):
            name = input('\n Ingrese el nombre del usuario: ')
            new_level = input('\n Ingrese el nuevo nivel de usuario: ')
            password = getpass.getpass('\n Ingrese la contraseña del usuario: ')
            editUserLevel(db,name,new_level, password)
        if (opt == '3'):
            name = input('\n Ingrese usuario que desea eliminar: ')
            deleteUser(db,name)
        if (opt == '4'):
            break