from pony.orm import *
import pandas
from IPython.display import display
from tabulate import tabulate

def createEmployee(db, id, name, zone, perf_rect = None , perf_des = None, perf_fab = None, perf_inst = None, senior = None):
    with db_session:
        e = db.Employees(id = id, name = name, zone = zone)
        if perf_rect != None:
            db.Employees_Skills(employee = e, skill = 1, performance = perf_rect)
        if perf_des != None:
            db.Employees_Skills(employee = e, skill = 2, performance = perf_des)
        if perf_fab != None:
            db.Employees_Skills(employee = e, skill = 3, performance = perf_fab)
        if perf_inst != None:
            db.Employees_Skills(employee = e, skill = 4, performance = perf_inst)
            # solo para el caso de los instaladores, pueden ser senior o junior, por defecto los consideramos como senior:
            if senior != None:
                e.senior = bool(senior)
            else:
                e.senior = True
        commit()

def printEmployees(db):
    with db_session:
        print('\n')
        e = db.Employees.select()
        data = [p.to_dict() for p in e]
        df = pandas.DataFrame(data, columns = ['id','name','zone','senior'])                    
        df.columns = ['Rut','Nombre','Zona', '¿Es Senior?']
        print( tabulate(df, headers='keys', tablefmt='psql'))
        input(' \n Presione Enter para continuar. ')

def editEmployee(db, id, new_name = None, new_zone = None, perf_rect = None, perf_des = None, perf_fab = None, perf_inst = None, senior = None):
    with db_session:
        e = db.Employees[id]
        if new_zone != None:
            e.zone = new_zone
        if new_name != None:
            e.name = new_name
        if perf_rect != None: 
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[1]) != None:
                db.Employees_Skills[(id, 1)].performance = perf_rect
            else:
                db.Employees_Skills(employee = id, skill = 1, performance = perf_rect)
        if perf_des != None:
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[2]) != None:
                db.Employees_Skills[(id, 2)].performance = perf_des
            else:
                db.Employees_Skills(employee = id, skill = 2, performance = perf_des)
        if perf_fab != None:
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[3]) != None:
                db.Employees_Skills[(id, 3)].performance = perf_fab
            else:
                db.Employees_Skills(employee = id, skill = 3, performance = perf_fab)
        if perf_inst != None:
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[4]) != None:
                db.Employees_Skills[(id, 4)].performance = perf_inst
            else:
                db.Employees_Skills(employee = id, skill = 4, performance = perf_inst)
        # si es que el empleado no es instalador, no se pesca el valor de la variable senior:
        emp_skill = select(es for es in db.Employees_Skills if es.employee == id and es.skill == 4)
        if len(emp_skill) > 0 and senior != None:
            e.senior = senior

            
def deleteEmployee(db, id):
    import Planning.features as Pf
    with db_session:
        if len(select(et for et in db.Employees_Tasks if et.employee == db.Employees[id]))>0:
            db.Employees[id].delete()
            commit()
            Pf.doPlanning(db)
        else:
            db.Employees[id].delete()
            commit()


def printEmployeesSkills(db):
    with db_session:
        db.Employees_Skills.select().order_by(lambda es: es.employee).show()
        
def printSkills(db):
    with db_session:
        db.Skills.select().order_by(lambda s: s.id).show()
    
def printSelectSkill(db, id_skill):
    with db_session:
        ids = []
        emps = select(e for e in db.Employees )
        for e in emps:
            es = db.Employees_Skills.get(employee = db.Employees[e.id], skill = db.Skills[id_skill])
            if es != None and es.performance > 0:
                ids.append(e.id)
        e = select(e for e in db.Employees if e.id in ids).order_by(lambda e: e.id)
        print('\n')
        data = [p.to_dict() for p in e]
        df = pandas.DataFrame(data, columns = ['id','name','zone','senior'])                    
        df.columns = ['Rut','Nombre','Zona', '¿Es Senior?']
        print( tabulate(df, headers='keys', tablefmt='psql'))
