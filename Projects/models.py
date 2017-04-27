from pony.orm import *
from datetime import date

def define_models(db):
    class Projects(db.Entity):
        contract_number = PrimaryKey(int, auto=False)
        client_address = Required(str)
        client_comuna = Required(str)
        client_name = Required(str)
        client_rut = Required(str)
        linear_meters = Required(float)
        deadline = Required(date)
        priority = Optional(int)
        real_linear_meters = Optional(float)
        estimated_cost = Optional(int)
        real_cost = Optional(int)
        sale_price = Optional(int)
        difficulties = Set('Difficulties')
        tasks = Set('Tasks')
        employees = Set('Employees_Restrictions')
        restrictions = Set('Deadlines_Restrictions')
        activities = Set('Projects_Activities')
        fixed_planning = Optional(bool)
        fixed_priority = Optional(bool)
        engagements = Set('Engagements')
        costs = Set('Projects_Costs')
        crystal_leadtime = Optional(int, default = 15)
        sale_date = Optional(date)


        def __repr__(self):
            return str(self.contract_number)

    # dificultades tipo "construcción en altura"
    class Difficulties(db.Entity):
        id = PrimaryKey(int, auto=False)
        description = Required(str)
        projects = Set(Projects)

        def __repr__(self):
            return self.description

    # actividades tipo "licencia", "vacaciones", etc. Una actividad necesariamente implica no trabajar.
    class Activities(db.Entity):
        id = PrimaryKey(int, auto=False)
        description = Required(str)
        projects = Set('Projects_Activities')
        employees = Set('Employees_Activities')

        def __repr__(self):
            return self.description
    
    class Projects_Activities(db.Entity):
        id = PrimaryKey(int, auto=True)
        project = Required(Projects)
        activity = Required(Activities)
        initial_date = Optional(date)
        end_date = Optional(date)
    
    class Projects_Delays(db.Entity):
        id = PrimaryKey(int, auto = True)
        project_id = Required(int)
        skill_id = Required(int)
        delay = Required(int)
    
    class Employees_Activities(db.Entity):
        id = PrimaryKey(int, auto=True)
        employee = Required('Employees')
        activity = Required(Activities)
        initial_date = Optional(date)
        end_date = Optional(date)

    class Tasks(db.Entity):
        id = PrimaryKey(int, auto=True)
        skill = Required('Skills')
        project = Required(Projects)
        original_initial_date = Required(date) #Esto debería ser optional,
        # dejarse vacío y luego ser llenado automáticamente por el programa.
        original_end_date = Required(date)#Esto debería ser optional,
        # dejarse vacío y luego ser llenado automáticamente por el programa.
        effective_initial_date = Optional(date)
        effective_end_date = Optional(date)
        failed = Optional(bool)
        fail_cost = Optional(int)
        employees = Set('Employees_Tasks')

        def __repr__(self):
            return str(self.id)

    class Employees_Tasks(db.Entity):
        task = Required(Tasks)
        employee = Required('Employees')
        PrimaryKey(employee, task)
        planned_initial_date = Optional(date)
        planned_end_date = Optional(date)
        
    class Freight_Costs(db.Entity):#La cantidad costo flete sistema que aparece en el excel Base de Datos             #_sistema Gestion de Operaciones_ACO_04 03 2017_vf.xlsx, en la hoja 'COSTO ESTANDAR INSTALACION',
        #se debería fijar una sola vez el costo para todas las comunas de chile. El nombre de la comuna
        #en name, y la región en region. Se podría también tratar a la región como un int
        # id = PrimaryKey(int, auto = False)
        comuna_to = PrimaryKey(str)
        freight_cost = Required(float)
        
    class Operating_Costs(db.Entity):#Cantidades utilizadas en el cálculo del costo de fabricación del
        #excel Base de Datos _sistema Gestion de Operaciones_ACO_04 03 2017_vf.xlsx, en la hoga 
        #'COSTO ESTANDAR FABRICACION'. Se ingresarán los costos fijos y variables de la fábrica,
        # el arriendo y los gastos de luz, agua, etc, el porcentaje de ventas para los materiales. 
        # La depreciación podría ir aquí o ser ingresada cuando se necesite calcular el costo de fab.
        name = PrimaryKey(str)
        cost = Required(float)
        
    class Viatic_Costs(db.Entity):#
        # viaticos para los trabajadores que deben viajar para hacer la instalacion
        comuna_from = Required(str)
        comuna_to = Required(str)
        PrimaryKey(comuna_from, comuna_to)        
        viatic_cost = Required(float)
        
    class Movilization_Costs(db.Entity):#
        # asignacion de movilizacion para los trabajadores que deben moverse entre comunas cercanas para hacer la instalacion
        comuna_from = Required(str)
        comuna_to = Required(str)
        PrimaryKey(comuna_from, comuna_to)        
        movilization_cost = Required(float)
        
    class Projects_Costs(db.Entity):
        project = PrimaryKey(Projects)
        standard_cost_profiles = Optional(float) # costo estandar perfiles
        standard_cost_fittings = Optional(float) # costo estandar herrajes
        standard_cost_crystals = Optional(float) # costo estandar cristales
        standard_cost_material = Optional(float) # costo estandar materias primas
        standard_cost_fabrication = Optional(float) # costo estandar fabricacion (segun yo debiera ser "manufacturing" pero es para ser consistente por mientras, hemos usado "fabricator" en el resto del codigo
        standard_cost_installation = Optional(float) # costo estandar instalacion
        standard_cost_additionals = Optional(float) # costos estandares adicionales
        standard_cost_total = Optional(float) # costo estandar total
        
        effective_cost_material = Optional(float) # costo efectivo materias primas
        effective_cost_fabrication = Optional(float) # costo efectivo fabricacion
        effective_cost_installation = Optional(float) # costo efectivo instalacion
        effective_cost_complements = Optional(float) # costo efectivo complementos
        
        
