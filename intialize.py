from pony.orm import *
from database import db

with db_session:
	db.Skills(id=1, name='Rectifier')
	db.Skills(id=2, name='Designer')
	db.Skills(id=3, name='Fabricator')
	db.Skills(id=4, name='Installer')
