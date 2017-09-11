from pony.orm import *
import pandas
from tabulate import tabulate
from Planning.features import doPlanning

def createEmployee(db, id, name, zone, perf_rect = None , perf_des = None, perf_fab = None, perf_ins = None, senior = None):
    with db_session:
        e = db.Employees(id = id, name = name, zone = zone)
        if perf_rect != None:
            db.Employees_Skills(employee = e, skill = 1, performance = perf_rect)
        if perf_des != None:
            db.Employees_Skills(employee = e, skill = 2, performance = perf_des)
        if perf_fab != None:
            db.Employees_Skills(employee = e, skill = 3, performance = perf_fab)
        if perf_ins != None:
            db.Employees_Skills(employee = e, skill = 4, performance = perf_ins)
            # solo para el caso de los instaladores, pueden ser senior o junior, por defecto los consideramos como senior:
            if senior != None:
                e.senior = bool(senior)
            else:
                e.senior = True
        commit()

def printEmployees(db):
    with db_session:
        e = db.Employees.select()
        es = db.Employees_Skills.select()
        data1 = [p.to_dict() for p in e]
        data2 = [p.to_dict() for p in es]
        df1 = pandas.DataFrame(data1, columns = ['id','name','zone','senior'])                    
        df1.columns = ['RUT','Nombre','Comuna', '¿Es Senior?']
        df2 = pandas.DataFrame(data2, columns = ['employee','skill','performance'])
        df2.columns = ['RUT','Tipo Empleado', 'Rendimiento']
        df = pandas.merge(df1,df2,on = 'RUT')
        print()
        print(tabulate(df, headers='keys', tablefmt='psql'))
        input(' Presione Enter para continuar. ')

def editEmployee(db, id, new_name = None, new_zone = None, perf_rect = None, perf_des = None, perf_fab = None, perf_ins = None, senior = None):
    replan = False
    with db_session:
        e = db.Employees[id]
        if new_zone != None:
            e.zone = new_zone
        if new_name != None:
            e.name = new_name
        if perf_rect != None: 
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[1]) != None:
                if perf_rect == 0:
                    if len(select(et for et in db.Employees_Tasks if et.employee == db.Employees[id] and et.task.skill == db.Skills[1]))>0:
                        replan = True
                    db.Employees_Skills[(id, 1)].delete()
                else:
                    db.Employees_Skills[(id, 1)].performance = perf_rect
            elif perf_rect != 0:
                db.Employees_Skills(employee = id, skill = 1, performance = perf_rect)
        if perf_des != None:
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[2]) != None:
                if perf_des == 0:
                    if len(select(et for et in db.Employees_Tasks if et.employee == db.Employees[id] and et.task.skill == db.Skills[2]))>0:
                        replan = True
                    db.Employees_Skills[(id, 2)].delete()
                else:
                    db.Employees_Skills[(id, 2)].performance = perf_des
            elif perf_des != 0:
                db.Employees_Skills(employee = id, skill = 2, performance = perf_des)
        if perf_fab != None:
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[3]) != None:
                if perf_fab == 0 :
                    if len(select(et for et in db.Employees_Tasks if et.employee == db.Employees[id] and et.task.skill == db.Skills[3]))>0:
                        replan = True
                    db.Employees_Skills[(id, 3)].delete()
                else:
                    db.Employees_Skills[(id, 3)].performance = perf_fab
            elif perf_fab != 0:
                db.Employees_Skills(employee = id, skill = 3, performance = perf_fab)
        if perf_ins != None:
            if db.Employees_Skills.get(employee=db.Employees[id],skill=db.Skills[4]) != None:
                if perf_ins == 0:
                    if len(select(et for et in db.Employees_Tasks if et.employee == db.Employees[id] and et.task.skill == db.Skills[4]))>0:
                        replan = True
                    db.Employees_Skills[(id, 4)].delete()
                else:
                    db.Employees_Skills[(id, 4)].performance = perf_ins
            elif perf_ins != 0:
                db.Employees_Skills(employee = id, skill = 4, performance = perf_ins)
        # si es que el empleado no es instalador, no se pesca el valor de la variable senior:
        emp_skill = select(es for es in db.Employees_Skills if es.employee == db.Employees[id] and es.skill == db.Skills[4])
        if len(emp_skill) > 0 and senior != None:
            e.senior = senior
        commit()
        if replan:
            input(' Es necesario hacer una replanificación. Presione enter para empezar la replanificación: ')
            doPlanning(db)
            

            
def deleteEmployee(db, id):
    with db_session:
        if len(select(et for et in db.Employees_Tasks if et.employee == db.Employees[id]))>0:
            db.Employees[id].delete()
            commit()
            input(' Es necesario hacer una replanificación. Presione enter para empezar la replanificación: ')
            doPlanning(db)
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
        es = db.Employees_Skills.select()
        data1 = [p.to_dict() for p in e]
        data2 = [p.to_dict() for p in es]
        if id_skill == 4:
            df1 = pandas.DataFrame(data1, columns = ['id','name','zone','senior'])                    
            df1.columns = ['RUT','Nombre','Comuna', '¿Es Senior?']
        else:
            df1 = pandas.DataFrame(data1, columns = ['id','name','zone'])                    
            df1.columns = ['RUT','Nombre','Comuna']
        df2 = pandas.DataFrame(data2, columns = ['employee','performance'])
        df2.columns = ['RUT', 'Rendimiento']
        df = pandas.merge(df1,df2,on = 'RUT')
        print( tabulate(df, headers='keys', tablefmt='psql'))
