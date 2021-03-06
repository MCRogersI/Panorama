from pony.orm import *
from datetime import date


def define_models(db):

    class Users(db.Entity):
        user_name = PrimaryKey(str, auto = False)
        user_level=Required(int)#'1' = 'Administrador', '2' = 'Usuario Normal', '3' = 'Invitado', '4' = ...
        salt = Required(bytes, auto = False)
        hashed_password = Required(bytes, auto=False)

        def __repr__(self):
            return str(self.user_name)


