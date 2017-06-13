Tests 2017/06/04:

1) Creación de proyectos y empleados (VERIFICAR EN LA BASE DE DATOS ADEMÁS DE LA CONSOLA):

- Partir de base de datos inicializada con lo básico: Skills, Activities y usuario administrador.
- Inicializar todo con initialize.py.
- Revisar que crear Employees funcione: que funcione si se ingresa todo bien (con Floats, con Strings, con etc.?).
                                        que reclame al ingresar mal, apropiadamente.
                                        que senior/junior te lo pida solo para instaladores.
                                        que te avise que la creación fue exitosa.
                                        que permita rendimientos racionales, no solo enteros.
                                        que exija rendimiento al menos en alguna Skill.
                                        que parsee el nombre de la comuna.
                                        que revise si se quiere duplicar información (ingresar dos veces lo mismo)
- Revisar que crear Projects funcione: que funcione si se ingresa todo bien (con Floats, con Strings, con etc.).
                                       que acepte metros lineales racionales, no solo enteros.
                                       que reclame al ingresar mal, apropiadamente.
                                       que reclame (y no se caiga) si se trata de crear sin
                                        que revise si se quiere duplicar información (ingresar dos veces lo mismo)
Employees inscritos.
                                       que no haya problema (en creación ni en planificación) de proyectos atrasados.
                                       que un proyecto atrasado parta mañana, y no en la fecha de venta.
                                       que te avise que la creación fue exitosa.
                                       que parsee el nombre de la comuna.
2) Creación y manejo de usuarios:
- Revisar que la creación de Usuarios funcione correctamente.
- Revisar que el chequeo de entrada (sign-in) funcione correctamente (verifique la contraseña y abra la consola correspondiente a los privilegios del usuario respectivo).
3) Stock
- Revisar que al crearse un proyecto se creen correctamente los Engagements correspondientes en la base de Datos.
- Revisar que la lectura de la hoja de corte se haga de forma correcta.
- Revisar que el mecanismo de lectura de la orden de compra (Purchase) funcione correctamente.
4) Visualización de los reportes:
- Revisar que las cantidades mostradas en los reportes de Stock sean las correctas (revisar con un caso de prueba tipo).
- Revisar que el "display" mostrado en los reportes de calendario de los trabajadores estén correctos (revisar con un caso de prueba tipo).
5) Revisar caso excepcionales (casos de prueba):
- Trabajadores con el mismo nombre
- Demasiados proyectos
- Muy pocos proyectos
- Muchos proyectos en una misma fecha
- Cliente muy ocupado
- Trabajadores con licencias largas (o vacaciones).
- Múltiples ordenes de compra para una misma fecha
- EVENTOS EN FECHAS ANTERIORES A LA FECHA ACTUAL
- 
-
                                                                             