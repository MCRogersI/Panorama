Cambios en funciones

# 1) edit project tiene que revisar la ultima versión

# 2) DeleteProject borra la ultima versión o borra todas las versiones??

# 3) finishProject debe revisar la ultima versión

# 4) Ahora al terminar una versión del proyecto por fallo la prioridad no cambia. La versión nueva hereda la prioridad del anterior. No se puede usar la función finnishProject para esto

# 5) getNumberConcurrentProjects debe revisar la última versión
    nota: no sabemos que es ni la usamos

# 6) getCostRM debe revisar la última versión? o es que debe sumar los de todas las versiones? idem para getCostInstallation, getCostProject y getCostFabrication
    nota: no sabemos que es ni la usamos

# 7) createTask debe revisar la versión del proyecto. Edit task tambien para la query de proyecto
    nota: EditTask no se usa

8) las tablas de printTasks no van a mostrar versiones del proyecto

9) failedTask necesita cambios mayores