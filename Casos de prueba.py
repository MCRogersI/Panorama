Tests 2017/06/04:

Las lineas comentadas son las que están revisadas


1) Revisar que inicialización sea correcta:

# - Partir de base de datos inicializada con lo básico: Skills, Activities y usuario administrador.
# - Todo se inicializa desde initialize.py.
# - La inicialización anterior funciona, efectivamente, en la base de datos.

2) Revisar que crear Employees funcione: 

# - Que funcione si se ingresa todo bien.
# - Que reclame al ingresar mal, apropiadamente.
# - Que senior/junior te lo pida solo para instaladores.
# - Que te avise que la creación fue exitosa.
# - Que permita rendimientos racionales, no solo enteros.
# - Que exija rendimiento al menos en alguna Skill.
# - Que pregunte por la comuna de residencia y no por el "código de zona".
# - Que parsee el nombre de la comuna.

3) Revisar que editar Employees funcione:

# - Que cambiar un rendimiento a cero le quite la skill 
# - Que reclame si un empleado es editado para no tener skill 
# - Que replanifique si se cambia de skill y estaba en la planificación 

4) Revisar que eliminar Employees funcione: 

# - Que efectivamente salga de la base de datos.
# - En caso de que el Employee haya estado en la planificación, hacer de nuevo doPlanning().
# - Que no sea considerado en nuevas planificaciones.
# - Que los Employees_X desaparezcan todos con X = Skills, Tasks, Activities, Restrictions.

5) Revisar que Manejar vacaciones/periodos de licencia funcione:

# - Que te permita ver la lista (y que la actualice altiro, sin tener que cerrar el programa).
# - Que permita ingresar la actividad, reclamando si los datos se meten mal.
# - Que al ingresar replanifique si topa con un trabajo.
    nota: por alguna razón a Rogers le hacía el doPlanning en casos en que no era necesario
# - Que elimine efectivamente la actividad.
# - Que imprima todo correctamente

6) Revisar que imprimir Employees funcione:

# - Que al pedir la lista de cada trabajo específicio, entregue los empleados solo de esa tarea.
# - Que genere los calendarios de trabajo pedidos de manera correcta.
# - Que tire mensajes de éxito al crear los calendarios de trabajo.
# - Que reclame si se mete mal el ID del empleado al pedir un calendario de trabajo.

3) Revisar que crear Projects funcione: 

# - Que funcione si se ingresa todo bien.
# - Que acepte metros lineales racionales, no solo enteros.
# - Que reclame al ingresar mal, apropiadamente.
# - Que reclame (y no se caiga) si se trata de crear sin Employees inscritos.
# - Que no haya problema (en creación ni en planificación) de proyectos atrasados.
# - Que un proyecto atrasado parta mañana, y no en la fecha de venta.
# - Que te avise que la creación fue exitosa.
# - Que parsee el nombre de la comuna.

7) Revisar que Editar Projects funcione:

# - Que cambie la prioridad de el resto de los proyectos adecuadamente
# - Que meter al agregar restricciones cambie la planificación si corresponde.
    nota: agregar restricciones de asignación funciona bien pero las de tiempo no hacen nada
  - Que te reclame si metes mal los datos y tire mensaje de éxito.

8) Revisar que eliminar Projects funcione:

# - Que efectvamente salga de la base de datos.
# - Que actualice las prioridades de los Projects restantes.
# - Avisar al usuario que puede convenir re-planificar para tratar de mejorar las fechas de entrega.
# - Que los Projects_X desaparezcan todos con X = Activities, Costs, Delays.
# - También que desaparezcan las Tasks, Deadlines_Restrictions, Employees_Restrictions, Employees_Tasks asociadas.

9) Revisar que Terminar Projects funcione:

# - Que te reclame si el proyecto no existe, y que entregue mensaje de éxito.
# - Que cambie finished a True.
# - Que se reajusten las prioridades.
# - Borrar todos los Employees_Tasks.

10) Revisar que Manejar disponibilidad del cliente funcione:

# - Que te permita ver la lista (y que la actualice altiro, sin tener que cerrar el programa).
# - Que permita ingresar la actividad, reclamando si los datos se meten mal.
- Que al ingresar replanifique si topa con un trabajo.
# - Que elimine efectivamente la actividad.
# - Que imprima todo correctamente

12) Revisar que imprimir Projects funcione:

- Que ofrezca opciones de imprimir proyectos vigentes/terminados/todos, y que lo haga bien.
# - Que muestre todo actualziado, incluidos proyectos recientemente agregados/eliminados (que no haya que cerrar el programa para actualizar).

13) Revisar que estimar costos del Project funcione:

- Que el programa no se caiga si el proyecto aún no ha sido planificado (revisar eso en consola).
- No poder hacerlo si el proyecto ya está terminado (revisar eso en consola).
# - Que el cálculo de costos no se caiga si hay parámetros faltantes en la base de datos.
# - Que el cálculo de costos no se caiga si el archivo viene en formato erróneo.
# - Que la creación de los Engagements no se caiga si hay parámetros faltantes en la base de datos.
# - Que la creación de los Engagements no se caiga si el archivo viene en formato erróneo.
# - Que se pueda ingresar una nueva hoja de corte para el mismo proyecto, y que el programa actualice los costos y los engagements.

14) Revisar que createSku funcione:

# - Que se agregue efectivamente
# - Que reclame si ya existe

15) Revisar que Eliminar SKU funcione:

- Que reclame si se meten mal los datos, y tire mensaje de éxito si se hace bien.
# - Que efectivamente elimine el producto, y que lo muestre altiro.

