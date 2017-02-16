from pony.orm import *
from datetime import date

def define_models(db):
    class Users(db.Entity):
        user_id = PrimaryKey(int, auto=True)
        user_name = Required(str)
        # En el caso de haber solo dos tipos de usuario (por ejemplo 'Administrador' y 'Usuario Normal')
        # el valor de user level podría ser Booleano.
        user_level=Required(int)#'1' = 'Administrador', '2' = 'Usuario Normal', '3' = 'Invitado', '4' = ...
        # user_rut = Optional(str)
        salt = Required(bytes, auto = False)
        hashed_pass = Required(bytes, auto=False)

        def __repr__(self):
            return str(self.user_name)


