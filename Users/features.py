from pony.orm import * #Luego deberíamos arreglar esto para que no se importe todo (mala práctica)
import os
import hashlib

def createUser(db,name, level,password):
    salt,hashed_pass = createSaltHash(password)

    with db_session:
        u = db.Users(user_name = name, user_level = level,salt = salt, hashed_pass = hashed_pass)



def checkPass(self, name_request, password):
    pass
    # if self.user[name_request] == hashlib.sha256(
    #                 self.clientes_sals[name_request] + contrasena.encode('utf-8')):
    #     return True
    # else:
    #     return False


def createSaltHash(password):
    salt = os.urandom(64)
    encoded_pass = password.encode('utf-8')
    hashed_pass = hashlib.sha256(salt + encoded_pass)
    return (salt, hashed_pass)
