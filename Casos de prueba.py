Tests 2017/06/04:

1) Creaci�n de proyectos y empleados:

- Partir de base de datos inicializada con lo b�sico: Skills, Activities y usuario administrador.
- Inicializar todo con initialize.py.
- Revisar que crear Employees funcione: que funcione si se ingresa todo bien.
                                        que reclame al ingresar mal, apropiadamente.
                                        que senior/junior te lo pida solo para instaladores.
                                        que te avise que la creaci�n fue exitosa.
                                        que permita rendimientos racionales, no solo enteros.
                                        que exija rendimiento al menos en alguna Skill.
                                        que parsee el nombre de la comuna.
- Revisar que crear Projects funcione: que funcione si se ingresa todo bien.
                                       que acepte metros lineales racionales, no solo enteros.
                                       que reclame al ingresar mal, apropiadamente.
                                       que reclame (y no se caiga) si se trata de crear sin Employees inscritos.
                                       que no haya problema (en creaci�n ni en planificaci�n) de proyectos atrasados.
                                       que un proyecto atrasado parta ma�ana, y no en la fecha de venta.
                                       que te avise que la creaci�n fue exitosa.
                                       que parsee el nombre de la comuna.
                                                                             