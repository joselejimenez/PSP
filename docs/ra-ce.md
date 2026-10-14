# Resultados de aprendizaje, criterios y temas

Relación entre los **resultados de aprendizaje (RA)** del módulo 0495, sus **criterios de evaluación (CE)** y los temas del curso. Los pesos e instrumentos proceden de la programación didáctica del departamento (apartado 4.5), según el Real Decreto 450/2010, actualizado por el Real Decreto 405/2023.

| RA | Peso | Tema | Trimestre |
|---|---|---|---|
| **RA1.** Desarrolla aplicaciones compuestas por varios procesos reconociendo y aplicando principios de programación paralela. | 10 % | Tema 1. Multiprocesos | 1.º |
| **RA2.** Desarrolla aplicaciones compuestas por varios hilos de ejecución analizando y aplicando librerías específicas del lenguaje de programación. | 35 % | Tema 2. Multihilos | 1.º |
| **RA3.** Programa mecanismos de comunicación en red empleando sockets y analizando el escenario de ejecución. | 20 % | Tema 3. Comunicaciones en red | 1.º |
| **RA4.** Desarrolla aplicaciones que ofrecen servicios en red, utilizando librerías de clases y aplicando criterios de eficiencia y disponibilidad. | 20 % | Tema 4. Generación de servicios en red | 2.º |
| **RA5.** Protege las aplicaciones y los datos definiendo y aplicando criterios de seguridad en el acceso, almacenamiento y transmisión de la información. | 15 % | Tema 5. Técnicas de programación segura | 2.º |

## RA1 · Tema 1. Multiprocesos (10 %)

| CE | Descripción | Peso | Dónde se trabaja en el Tema 1 | Instrumento |
|---|---|---|---|---|
| a | Se han reconocido las características de la programación concurrente y sus ámbitos de aplicación. | 1 % | Bloque 2 · Boletín 1, 2 | Prueba teórica/práctica |
| b | Se han identificado las diferencias entre programación paralela y programación distribuida, sus ventajas e inconvenientes. | 1 % | Bloque 2 · Boletín 2, 9 | Prueba teórica/práctica |
| c | Se han analizado las características de los procesos y de su ejecución por el sistema operativo. | 1 % | Bloques 1, 3 y 4 · Boletín 1, 3, 4, 5 | Prueba teórica/práctica |
| d | Se han caracterizado los hilos de ejecución y descrito su relación con los procesos. | 2 % | Bloque 1 (se amplía en el Tema 2) · Boletín 1 | Prueba teórica/práctica |
| e | Se han utilizado clases para programar aplicaciones que crean subprocesos. | 1 % | Bloque 5 · Boletín 5, 6, 7 | Prueba teórica/práctica y actividades |
| f | Se han utilizado mecanismos para compartir información con los subprocesos iniciados. | 1 % | Bloque 6 · Boletín 7, 8 | Prueba teórica/práctica |
| g | Se han utilizado mecanismos para sincronizar y obtener el valor devuelto por los subprocesos iniciados. | 1 % | Bloques 5 y 6 · Boletín 6, 7, 9, 10 | Prueba teórica/práctica |
| h | Se han desarrollado aplicaciones que gestionen y utilicen procesos para la ejecución de varias tareas en paralelo. | 1 % | Bloque 5 · Boletín 9 | Actividades |
| i | Se han depurado y documentado las aplicaciones desarrolladas. | 1 % | Boletín 6, 10 | Prueba teórica/práctica |

<!-- si-visible: temas/tema-1/practica.md -->
### Criterios del RA1 en la práctica evaluable

| CE | Dónde se evalúa en la práctica | Puntos |
|---|---|---|
| a | README: concurrencia y paralelismo trivial | 0,75 |
| b | README: paralela frente a distribuida y tabla de rendimiento | 0,75 |
| c | Estados de los procesos y opción 4 (listar) | 1 |
| d | README: procesos frente a hilos | 0,5 |
| e | Opciones 1 y 2: `ProcessBuilder` portable y redirección a fichero | 2 |
| f | Opción 3: datos por argumentos y resultado por la salida del hijo | 1,5 |
| g | `waitFor`, códigos de salida, opciones 5 y 0 | 1,5 |
| h | Opción 3: varios procesos en paralelo | 1 |
| i | Javadoc, control de errores y README | 1 |
<!-- fin -->

## RA2 · Tema 2. Multihilos (35 %)

| CE | Descripción | Peso | Instrumento |
|---|---|---|---|
| a | Se han identificado situaciones en las que resulte útil la utilización de varios hilos en un programa. | 3 % | Prueba y actividades |
| b | Se han reconocido los mecanismos para crear, iniciar y finalizar hilos. | 3 % | Prueba y actividades |
| c | Se han programado aplicaciones que implementen varios hilos. | 4 % | Prueba y actividades |
| d | Se han identificado los posibles estados de ejecución de un hilo y programado aplicaciones que los gestionen. | 3 % | Prueba y actividades |
| e | Se han utilizado mecanismos para compartir información entre varios hilos de un mismo proceso. | 3 % | Actividad FFEOE |
| f | Se han desarrollado programas formados por varios hilos sincronizados mediante técnicas específicas. | 3 % | Actividad FFEOE |
| g | Se ha establecido y controlado la prioridad de cada uno de los hilos de ejecución. | 3 % | Prueba y actividades |
| h | Se han depurado y documentado los programas desarrollados. | 3 % | Prueba y actividades |
| i | Se ha analizado el contexto de ejecución de los hilos. | 3 % | Prueba y actividades |
| j | Se han analizado librerías específicas del lenguaje de programación que permiten la programación multihilo. | 3 % | Prueba y actividades |
| k | Se han reconocido los problemas derivados de la compartición de información entre los hilos de un mismo proceso. | 3 % | Prueba y actividades |

## RA3 · Tema 3. Comunicaciones en red (20 %)

| CE | Descripción | Peso | Instrumento |
|---|---|---|---|
| a | Se han identificado escenarios que precisan establecer comunicación en red entre varias aplicaciones. | 2 % | Prueba y actividades |
| b | Se han identificado los roles de cliente y de servidor y sus funciones asociadas. | 2 % | Prueba y actividades |
| c | Se han reconocido librerías y mecanismos del lenguaje de programación que permiten programar aplicaciones en red. | 2 % | Prueba y actividades |
| d | Se ha analizado el concepto de socket, sus tipos y características. | 2 % | Prueba y actividades |
| e | Se han utilizado sockets para programar una aplicación cliente que se comunique con un servidor. | 2 % | Prueba y actividades |
| f | Se ha desarrollado una aplicación servidor en red y verificado su funcionamiento. | 2 % | Actividad FFEOE |
| g | Se han desarrollado aplicaciones que utilizan sockets para intercambiar información. | 2 % | Prueba y actividades |
| h | Se han utilizado hilos para posibilitar la comunicación simultánea de varios clientes con el servidor. | 1 % | Prueba y actividades (requiere el Tema 2) |
| i | Se han caracterizado los modelos de comunicación más usuales en las arquitecturas de aplicaciones distribuidas. | 1 % | Actividad FFEOE |
| j | Se han depurado y documentado las aplicaciones desarrolladas. | 1 % | Actividad FFEOE |

## RA4 · Tema 4 y RA5 · Tema 5 (2.º trimestre)

| RA | CE | Descripción | Peso | Instrumento |
|---|---|---|---|---|
| RA4 | a | Se han identificado diferentes protocolos estándar de comunicación para la implementación de servicios en red. | 2 % | Prueba y actividades |
| RA4 | b | Se han reconocido las ventajas de la utilización de protocolos estándar para la comunicación entre aplicaciones y procesos. | 2 % | Prueba y actividades |
| RA4 | c | Se han analizado librerías que permitan implementar servicios en red utilizando protocolos estándar de comunicación. | 3 % | Prueba y actividades |
| RA4 | d | Se han desarrollado y probado servicios de comunicación en red. | 3 % | Prueba y actividades |
| RA4 | e | Se han utilizado clientes de comunicaciones para verificar el funcionamiento de los servicios. | 3 % | Prueba y actividades |
| RA4 | f | Se han incorporado mecanismos para posibilitar la comunicación simultánea de varios clientes con el servicio. | 3 % | Prueba y actividades |
| RA4 | g | Se ha verificado la disponibilidad del servicio. | 2 % | Prueba y actividades |
| RA4 | h | Se han depurado y documentado las aplicaciones desarrolladas. | 2 % | Prueba y actividades |
| RA5 | a | Se han identificado y aplicado principios y prácticas de programación segura. | 2 % | Actividad FFEOE |
| RA5 | b | Se han analizado las principales técnicas y prácticas criptográficas. | 2 % | Prueba y actividades |
| RA5 | c | Se han definido e implantado políticas de seguridad para limitar y controlar el acceso de los usuarios a las aplicaciones desarrolladas. | 1 % | Prueba y actividades |
| RA5 | d | Se han utilizado esquemas de seguridad basados en roles. | 2 % | Prueba y actividades |
| RA5 | e | Se han empleado algoritmos criptográficos para proteger el acceso a la información almacenada. | 2 % | Actividad FFEOE |
| RA5 | f | Se han identificado métodos para asegurar la información transmitida. | 2 % | Prueba y actividades |
| RA5 | g | Se han desarrollado aplicaciones que utilicen comunicaciones seguras para la transmisión de información. | 3 % | Actividad FFEOE |
| RA5 | h | Se han depurado y documentado las aplicaciones desarrolladas. | 1 % | Actividad FFEOE |
