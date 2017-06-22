from pony.orm import *
#Luego deberíamos cambiar la importación de pony para que no se importen todas las cosas con * (mala práctica).
import os
import hashlib
import pandas
from tabulate import tabulate

def createUser(db,name, level,password):
    ''' Este método crea una nueva entrada en la tabla de Usuarios de la base de datos
    Si es que en el futuro un administrador (usuario con level = 1) desea crear un nuevo usuario,
    este puede crearlo con una contraseña por defecto (0000 por ejemplo como para los codigos PIN de las tarjetas SIM)
    y notificar al usuario respectivo para que él cambie su contraseña'''
    salt,hashed_password = createSaltHash(password)

    with db_session:
        u = db.Users(user_name = name, user_level = level,salt = salt, hashed_password = hashed_password)

#falta un editUser o no?
def editUserLevel(db,name,new_level, password):
    with db_session:
        if checkPassEntry(db,name, password):
            u = db.Users.get(user_name = name)
            u.level = new_level
            print('\n Usuario editado con éxito.')
        else:
            print('\n Usuario o contraseña incorrectos.')
            
def deleteUser(db,name):
    with db_session:
        db.Users.get(user_name = name).delete()
        
def printUsers(db):
    with db_session:
        print('\n')
        Users = db.Users.select()
        data = [u.to_dict() for u in Users]
        df = pandas.DataFrame(data, columns = ['user_name','user_level'])
        df.columns = ['Rut de usuario', 'Nivel de usuario']
        print( tabulate(df, headers='keys', tablefmt='psql'))

def checkPassEntry(db,name_request, password):
    ''' Este método revisa que los datos ingresados para el sign-up sean correctos
    Retorna True si lo son y False en el caso contrario '''
    with db_session:
        user = db.Users.get(user_name = name_request)
        if user == None:
            return False
        else:
            if hashComparison(password,user.salt,user.hashed_password):
                return True
            else:
                return False

def getUserLevel(db,user_name):
    ''' Este método entrega el nivel del usuario correspondiente al nombre de usuario entregado.'''
    with db_session:
        user = db.Users.get(user_name = user_name)
        return user.user_level


def createSaltHash(password):
    ''' Este método produce un salt y luego una 'hashed password' a partir de la contraseña ingresa.
     Retorna ambos valores en una tupla '''
    salt = os.urandom(64)
    #Es muy importante notar que aquí no se verifica si la salt ya fue usada para el hash de otro usuario
    #Lo ideal es que los salt sean únicos, pero dado el tamaño de usuarios de la empresa, la probabilidad de que una salt se repita
    #es muy baja (y aunque se repitiera no debería ser un problema).
    #Decidimos hacerlo así por simplicidad
    encoded_pass = password.encode('utf-8')
    hashed_password = hashlib.sha256(salt + encoded_pass).digest()
    return (salt, hashed_password)

def changePassword(db,user_name, password):
    ''' Este método modifica la contraseña del usuario correspondiente '''
    with db_session:
        user = db.Users.get(user_name = user_name)
        salt, hashed_password = createSaltHash(password)
        user.salt = salt
        user.hashed_password = hashed_password

def hashComparison(password,salt,hashed_password):
    ''' Este método verifica si la contraseña entrega (sometida al algoritmo de hash) produce el valor esperado para el hashed_pass
     Retorna True si el valor coincide y False si no'''
    encoded_pass = password.encode('utf-8')
    auxiliar_hashed_password = hashlib.sha256(salt + encoded_pass).digest()
    if auxiliar_hashed_password == hashed_password:
        return True
    else:
        return False
