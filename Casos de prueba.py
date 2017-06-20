Tests 2017/06/04:

Las lineas comentadas son las que est�n revisadas


1) Revisar que inicializaci�n sea correcta:

# - Partir de base de datos inicializada con lo b�sico: Skills, Activities y usuario administrador.
# - Todo se inicializa desde initialize.py.
# - La inicializaci�n anterior funciona, efectivamente, en la base de datos.

2) Revisar que crear Employees funcione: 

# - Que funcione si se ingresa todo bien.
# - Que reclame al ingresar mal, apropiadamente.
# - Que senior/junior te lo pida solo para instaladores.
# - Que te avise que la creaci�n fue exitosa.
# - Que permita rendimientos racionales, no solo enteros.
# - Que exija rendimiento al menos en alguna Skill.
# - Que pregunte por la comuna de residencia y no por el "c�digo de zona".
# - Que parsee el nombre de la comuna.

3) Revisar que crear Projects funcione: 

# - Que funcione si se ingresa todo bien.
# - Que acepte metros lineales racionales, no solo enteros.
# - Que reclame al ingresar mal, apropiadamente.
# - Que reclame (y no se caiga) si se trata de crear sin Employees inscritos.
# - Que no haya problema (en creaci�n ni en planificaci�n) de proyectos atrasados.
# - Que un proyecto atrasado parta ma�ana, y no en la fecha de venta.
# - Que te avise que la creaci�n fue exitosa.
# - Que parsee el nombre de la comuna.

4) Revisar que eliminar Employees funcione: 

# - Que efectivamente salga de la base de datos.
# - En caso de que el Employee haya estado en la planificaci�n, hacer de nuevo doPlanning().
# - Que no sea considerado en nuevas planificaciones.
# - Que los Employees_X desaparezcan todos con X = Skills, Tasks, Activities, Restrictions.

5) Revisar que eliminar Projects funcione:

# - Que efectvamente salga de la base de datos.
# - Que actualice las prioridades de los Projects restantes.
# - Avisar al usuario que puede convenir re-planificar para tratar de mejorar las fechas de entrega.
# - Que los Projects_X desaparezcan todos con X = Activities, Costs, Delays.
# - Tambi�n que desaparezcan las Tasks, Deadlines_Restrictions, Employees_Restrictions, Employees_Tasks asociadas.

6) Revisar que editar Employees funcione:

# - Que cambiar un rendimiento a cero le quite la skill 
# - Que reclame si un empleado es editado para no tener skill 
# - Que replanifique si se cambia de skill y estaba en la planificaci�n 

7) Revisar que Editar Projects funcione:

# - Que cambie la prioridad de el resto de los proyectos adecuadamente
# - Que meter al agregar restricciones cambie la planificaci�n si corresponde.
    nota: agregar restricciones de asignaci�n funciona bien pero las de tiempo no hacen nada
    
8) Revisar que createSku funcione:
# -Que se agregue efectivamente
# -Que reclame si ya existe
