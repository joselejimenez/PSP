# Boletín de ejercicios · Tema 1

!!! info "Cómo trabajar este boletín"
    - **Diez ejercicios** ordenados de menor a mayor dificultad: los tres primeros son de teoría y del 4 al 10 se programa en **Java (JDK 21 o superior)**.
    - Cada ejercicio indica los **criterios de evaluación del RA1** que trabaja.
    - Entrega: un proyecto con una clase por programa y un `README.md` con las respuestas de teoría y una captura de cada ejecución.
    - Los ejercicios con varias clases (padre e hijo) se compilan juntos: `javac *.java`.

| Nº | Ejercicio | Nivel | CE |
|---|---|---|---|
| 1 | Receta, cocinero y proceso | ★ | a, c, d |
| 2 | La lavandería y la ley de Amdahl | ★ | a, b |
| 3 | La máquina recreativa: estados y tipos de tarea | ★★ | c |
| 4 | Planificación con llegadas | ★★ | c |
| 5 | Un padre y tres hijos | ★★ | c, e |
| 6 | Lanzador con cronómetro | ★★ | e, g, i |
| 7 | Calculadora en un proceso hijo | ★★★ | e, f, g |
| 8 | Filtro de mayúsculas: tuberías y redirecciones | ★★★ | f |
| 9 | Calcular π con dardos en paralelo | ★★★★ | b, g, h |
| 10 | El vigilante: esperar con límite y terminar | ★★★★ | g, i |

---

## 1. Receta, cocinero y proceso ★


1. Completa la analogía de la cocina: ¿qué es en un ordenador la **receta**, el **cocinero**, los **ingredientes** y **cocinar**?
2. Clasifica cada caso como **programa**, **proceso**, **servicio** o **hilo**, y justifica en una frase:
    1. `idea64.exe` guardado en `C:\Program Files`.
    2. Las dos ventanas de Chrome que tienes abiertas.
    3. El proceso que atiende las impresoras aunque nadie haya iniciado sesión.
    4. El corrector ortográfico que revisa mientras escribes en Word.
    5. El servidor SSH de un Linux (`sshd`).
    6. `HolaMundo.class`.
3. ¿Por qué dos procesos no pueden leer directamente la memoria del otro y dos hilos del mismo proceso sí?
4. Abre el Administrador de tareas (o `ps -ef` en Linux) y anota el **PID** y el **PPID** del proceso de tu IDE. ¿Quién es su padre?

## 2. La lavandería y la ley de Amdahl ★


Te vas de viaje en dos horas y tienes cuatro lavadoras pendientes. Cada lavado dura 30 min y cada secado 45 min.

1. ¿Cuánto tardas con **una lavadora y una secadora**, haciendo cada carga entera antes de empezar la siguiente? ¿Y si mientras se seca una carga ya lavas la siguiente?
2. En la lavandería del barrio hay **cuatro lavadoras y cuatro secadoras**. ¿Cuánto tardas ahora? ¿Qué tipo de programación representa cada caso: secuencial, concurrente o paralela?
3. ¿Por qué este problema es *embarrassingly parallel* (paralelismo trivial)? Pon un ejemplo de informática que también lo sea y otro que **no** lo sea.
4. Un programa tarda 100 s y el **80 %** de su código se puede paralelizar. Con la ley de Amdahl, `S = 1 / ((1 − p) + p / n)`, calcula la aceleración con 2, 4 y 8 núcleos. ¿Cuál es el máximo teórico con infinitos núcleos?
5. ¿Qué diferencia hay entre repartir las cargas entre cuatro lavadoras de **la misma lavandería** (paralela) y mandar cada carga a **la casa de un amigo** (distribuida)? Indica una ventaja y un inconveniente de cada opción.

## 3. La máquina recreativa: estados y tipos de tarea ★★


Una máquina recreativa antigua tiene **un único núcleo** y repite tres tareas: leer el mando, calcular el mundo del juego y dibujar la pantalla.

1. Clasifica cada tarea como **limitada por CPU** (*CPU-bound*) o **limitada por E/S** (*I/O-bound*). Justifica.
2. Mientras la tarea «leer el mando» espera a que el jugador pulse un botón, ¿en qué **estado** está? ¿Qué hace mientras tanto el planificador?
3. Ordena los estados por los que pasa la tarea «dibujar» en esta secuencia y nombra cada transición: se crea → espera su turno → usa la CPU → pide escribir en la tarjeta gráfica → la escritura termina → vuelve a usar la CPU → acaba.
4. Di si son posibles estas transiciones y por qué: Bloqueado → Ejecución · Listo → Bloqueado · Ejecución → Listo.
5. El padre de un proceso termina antes que su hijo. ¿Qué es el hijo? ¿Y si el hijo termina y el padre nunca llama a `waitFor()`?

## 4. Planificación con llegadas ★★

Cuatro procesos llegan a la cola de listos en estos instantes:

| Proceso | Llegada | Ráfaga |
|---|---|---|
| P1 | 0 ms | 6 ms |
| P2 | 1 ms | 3 ms |
| P3 | 2 ms | 1 ms |
| P4 | 3 ms | 4 ms |

1. Dibuja el diagrama de Gantt con **FCFS**, **SJF no expropiativo** y **Round Robin con quantum de 2 ms**. En RR, si un proceso llega en el mismo instante en que otro agota su quantum, el que llega entra antes en la cola.
2. Para cada algoritmo calcula el **tiempo de retorno** (fin − llegada) y el **tiempo de espera** (retorno − ráfaga) de cada proceso, y sus medias.
3. ¿Qué algoritmo da menor espera media? ¿Cuál favorece más a P3? ¿Cuántos cambios de contexto hay en RR?

## 5. Un padre y tres hijos ★★


1. Crea `InfoHijo`: recibe un número por argumento y muestra «Hijo N: mi PID es …» y «el PID de mi padre es …» con `ProcessHandle`. Antes de terminar, duerme 1 segundo.
2. Crea `PadreHijos`: muestra su PID, lanza **tres** `InfoHijo` con `inheritIO()` sin esperar entre uno y otro y, medio segundo después, cuenta sus hijos vivos con `ProcessHandle.current().children()`.
3. Espera a los tres con `waitFor()` antes de terminar.
4. Ejecuta varias veces. ¿Salen siempre los mensajes en el mismo orden? ¿Por qué?
5. Teoría: en Python, `fork` crea un hijo que es **una copia** del padre y continúa desde el mismo punto. ¿Qué hace en cambio `ProcessBuilder`?

## 6. Lanzador con cronómetro ★★

1. Crea `Lanzador`: recibe por argumentos un programa y sus argumentos, por ejemplo `java Lanzador ping -c 2 localhost`, y lo ejecuta con `inheritIO()`.
2. Al terminar, muestra el PID, el código de salida y el tiempo que ha tardado en milisegundos (`System.nanoTime()`).
3. `Lanzador` debe terminar con el **mismo código de salida** que el programa lanzado.
4. Si el programa no existe, muestra un mensaje claro y termina con el código **127**. Si no recibe argumentos, muestra cómo se usa y termina con el **2**.
5. Comprueba el código de salida desde la terminal con `echo $?` (Linux y macOS) o `echo %errorlevel%` (Windows).

## 7. Calculadora en un proceso hijo ★★★

El código de salida solo sirve para números pequeños. Para devolver un resultado de verdad, el hijo lo **escribe** y el padre lo **lee**.

1. Crea `Calculadora`: recibe `num op num`, con `op` igual a `+`, `-`, `x` o `/`, y escribe el resultado en la salida estándar.
2. Si hay un error, escribe el motivo en la **salida de errores** y termina con código 1 (datos no válidos) o 2 (división por cero).
3. Crea `PadreCalculadora`: lanza la calculadora para `7 + 5`, `10 / 4`, `3 x 2.5`, `8 / 0` y `2 % 1`. Lee el resultado con `inputReader()` y el error con `errorReader()`.
4. Muestra cada operación con su resultado o su error, y la **suma** de los resultados válidos (22,0).
5. ¿Por qué hay que leer la salida **antes** de `waitFor()`?

## 8. Filtro de mayúsculas: tuberías y redirecciones ★★★


1. Crea `Mayusculas`: lee líneas de la entrada estándar **hasta que se cierre**, escribe cada una en mayúsculas y, al final, informa por la salida de errores de cuántas ha procesado.
2. Crea `PadreMayusculas` con dos versiones:
    1. **Tuberías**: lee `entrada.txt`, escribe sus líneas en el hijo con `outputWriter()`, cierra el flujo, recoge la salida con `inputReader()` y muéstrala.
    2. **Redirecciones**: lanza el hijo con `redirectInput(entrada.txt)` y `redirectOutput(salida.txt)`, sin que Java toque los datos.
3. ¿Qué pasa si en la versión de tuberías no cierras el flujo de escritura? Pruébalo y explícalo.
4. ¿Qué orden de la terminal hace lo mismo que la segunda versión?

## 9. Calcular π con dardos en paralelo ★★★★


Si lanzas dardos al azar sobre un cuadrado de lado 1, la proporción que cae dentro del cuarto de círculo de radio 1 se acerca a π/4. Cuantos más dardos, mejor es la estimación y más se tarda: el trabajo se puede **repartir** entre varios procesos.

1. Crea `Dardos`, el proceso hijo. Recibe cuántos dardos lanzar, genera puntos `(x, y)` con `ThreadLocalRandom` y **escribe** en su salida cuántos cumplen `x² + y² ≤ 1`.
2. Crea `EstimadorPi`, el padre. Reparte 200 millones de dardos entre N procesos y lánzalos **todos a la vez**.
3. Cuando estén todos en marcha, lee el resultado de cada hijo, súmalos y calcula `π ≈ 4 · dentro / total`. Muestra el valor y el tiempo.
4. Mide con 1, 2 y 4 procesos y completa la tabla. La aceleración es S = T₁ / Tₙ.

    | Procesos | Tiempo (ms) | Aceleración |
    |---|---|---|
    | 1 | | 1 |
    | 2 | | |
    | 4 | | |

5. Identifica la parte **secuencial** y la **paralela** del programa. ¿Por qué con más procesos que núcleos deja de mejorar? Relaciónalo con la ley de Amdahl y con el coste de arrancar cada JVM.

## 10. El vigilante: esperar con límite y terminar ★★★★

1. Crea `Dormilon`: duerme los segundos que recibe por argumento. Registra un **gancho de cierre** (`Runtime.getRuntime().addShutdownHook`) que escriba «cierre ordenado».
2. Crea `Vigilante`: lanza un `Dormilon` y lo espera **como mucho 3 segundos** con `waitFor(3, TimeUnit.SECONDS)`.
    - Si termina a tiempo, muestra su código de salida.
    - Si no, llama a `destroy()`, espera 2 s más y, si sigue vivo, a `destroyForcibly()`.
3. Prueba con 1 y con 10 segundos. ¿Qué código de salida obtienes en cada caso? ¿Se ejecuta el gancho de cierre?
4. Cambia `destroy()` por `destroyForcibly()`. ¿Se ejecuta ahora el gancho? Explica la diferencia entre las señales SIGTERM y SIGKILL.
5. Documenta las dos clases con **Javadoc** y genera la documentación con `javadoc -d doc *.java`.
