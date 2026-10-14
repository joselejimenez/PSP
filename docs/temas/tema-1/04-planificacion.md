# 4. Planificación de la CPU

Si hay más procesos listos que núcleos, alguien tiene que decidir **quién usa la CPU en cada momento** y durante cuánto tiempo. Esa parte del sistema operativo es el **planificador** (*scheduler*), y el criterio que sigue es el **algoritmo de planificación**.

## 4.1 Qué busca el planificador

Un buen planificador intenta, a la vez:

- **Aprovechar la CPU**: que no esté parada si hay trabajo.
- **Ser justo**: que ningún proceso se quede esperando para siempre.
- **Responder rápido** a los programas interactivos (el usuario no quiere esperar).
- **Terminar muchos trabajos** por unidad de tiempo.

Estos objetivos se contradicen entre sí, así que cada algoritmo elige un equilibrio distinto.

### Expropiativo o no expropiativo

- **No expropiativo** (*non-preemptive*): un proceso usa la CPU hasta que termina o se bloquea por sí mismo. El SO no se la quita.
- **Expropiativo** (*preemptive*): el SO puede **quitarle la CPU** a un proceso aunque no haya terminado, por ejemplo cuando se le acaba el tiempo o llega uno más prioritario. Todos los sistemas operativos actuales lo son.

### Medidas para comparar algoritmos

| Medida | Cómo se calcula | Qué indica |
|---|---|---|
| **Ráfaga de CPU** | Dato del problema | Tiempo de CPU que necesita el proceso. |
| **Tiempo de retorno** | Instante de fin − instante de llegada | Cuánto tarda en total, desde que llega hasta que termina. |
| **Tiempo de espera** | Tiempo de retorno − ráfaga | Cuánto tiempo pasa en la cola de listos sin usar la CPU. |
| **Tiempo de respuesta** | Primera vez que usa la CPU − llegada | Cuánto tarda en empezar a atenderse (importante en programas interactivos). |

## 4.2 Algoritmos de planificación

En los ejemplos usaremos estos tres procesos, que llegan todos en el instante 0 en el orden P1, P2, P3:

| Proceso | Ráfaga |
|---|---|
| P1 | 8 ms |
| P2 | 4 ms |
| P3 | 1 ms |

### FCFS / FIFO: primero en llegar, primero en ser servido

Los procesos se atienden **en orden de llegada** y cada uno usa la CPU hasta terminar. No es expropiativo.

<div class="gantt">
<div class="g-fila"><span class="g-etq">CPU</span><div class="g-pista">
<div class="g-barra c1" style="left:0.000%;width:61.538%">P1</div>
<div class="g-barra c2" style="left:61.538%;width:30.769%">P2</div>
<div class="g-barra c3" style="left:92.308%;width:7.692%">P3</div>
</div></div>
<div class="g-eje"><span style="left:0.000%">0</span><span style="left:61.538%">8</span><span style="left:92.308%">12</span><span style="left:100.000%">13</span></div>
</div>

| Proceso | Fin | Espera |
|---|---|---|
| P1 | 8 | 0 |
| P2 | 12 | 8 |
| P3 | 13 | 12 |
| **Media** | | **6,67 ms** |

- **Ventaja:** muy sencillo y justo en el orden.
- **Inconveniente:** un proceso largo al principio hace esperar a todos los cortos (**efecto convoy**). P3 necesita 1 ms y espera 12.

### SJF: el trabajo más corto primero

Se elige siempre el proceso con la **ráfaga más corta**. En su versión no expropiativa, el elegido se ejecuta hasta terminar.

<div class="gantt">
<div class="g-fila"><span class="g-etq">CPU</span><div class="g-pista">
<div class="g-barra c3" style="left:0.000%;width:7.692%">P3</div>
<div class="g-barra c2" style="left:7.692%;width:30.769%">P2</div>
<div class="g-barra c1" style="left:38.462%;width:61.538%">P1</div>
</div></div>
<div class="g-eje"><span style="left:0.000%">0</span><span style="left:7.692%">1</span><span style="left:38.462%">5</span><span style="left:100.000%">13</span></div>
</div>

| Proceso | Fin | Espera |
|---|---|---|
| P3 | 1 | 0 |
| P2 | 5 | 1 |
| P1 | 13 | 5 |
| **Media** | | **2 ms** |

- **Ventaja:** consigue el **menor tiempo de espera medio** posible.
- **Inconvenientes:** hay que saber de antemano cuánto va a durar cada proceso (en la realidad se estima), y los procesos largos pueden esperar indefinidamente si siguen llegando cortos: es la **inanición**.

### SRTF: el de menor tiempo restante

Es la versión **expropiativa** de SJF. Cuando llega un proceso nuevo, se compara su ráfaga con lo que le **queda** al que se está ejecutando; si es más corta, se le quita la CPU al actual.

Ejemplo con llegadas en instantes distintos:

| Proceso | Llegada | Ráfaga |
|---|---|---|
| P1 | 0 | 7 ms |
| P2 | 2 | 4 ms |
| P3 | 4 | 2 ms |

- En 0 solo está P1, que empieza.
- En 2 llega P2 (necesita 4). A P1 le quedan 5: P2 es más corto y **expulsa** a P1.
- En 4 llega P3 (necesita 2). A P2 le quedan 2: empate, sigue P2, que termina en 6.
- P3 se ejecuta de 6 a 8 y P1 termina de 8 a 13.

Esperas: P1 = 13 − 0 − 7 = 6, P2 = 6 − 2 − 4 = 0, P3 = 8 − 4 − 2 = 2. Media: **2,67 ms**.

### Prioridades

Cada proceso tiene una **prioridad** y se elige siempre el de prioridad más alta. Puede ser expropiativo o no.

Si en el ejemplo inicial P2 tiene la prioridad más alta, luego P3 y por último P1, el orden es P2 (0-4), P3 (4-5), P1 (5-13). Esperas 5, 0 y 4: media **3 ms**.

- **Ventaja:** permite atender antes lo urgente (por ejemplo, el sonido o el ratón).
- **Inconveniente:** **inanición** de los procesos de baja prioridad. Se soluciona con el **envejecimiento** (*aging*): la prioridad de un proceso sube poco a poco mientras espera.

### Round Robin: turno rotatorio

Cada proceso usa la CPU como mucho durante un tiempo fijo, el **quantum**. Si no ha terminado, vuelve **al final** de la cola de listos. Es expropiativo y es la base de los sistemas operativos actuales.

Con quantum de 2 ms:

<div class="gantt">
<div class="g-fila"><span class="g-etq">CPU</span><div class="g-pista">
<div class="g-barra c1" style="left:0.000%;width:15.385%">P1</div>
<div class="g-barra c2" style="left:15.385%;width:15.385%">P2</div>
<div class="g-barra c3" style="left:30.769%;width:7.692%">P3</div>
<div class="g-barra c1" style="left:38.462%;width:15.385%">P1</div>
<div class="g-barra c2" style="left:53.846%;width:15.385%">P2</div>
<div class="g-barra c1" style="left:69.231%;width:30.769%">P1</div>
</div></div>
<div class="g-eje"><span style="left:0.000%">0</span><span style="left:15.385%">2</span><span style="left:30.769%">4</span><span style="left:38.462%">5</span><span style="left:53.846%">7</span><span style="left:69.231%">9</span><span style="left:100.000%">13</span></div>
</div>

Paso a paso: P1 usa 2 ms (le quedan 6) y va al final. P2 usa 2 (le quedan 2). P3 solo necesita 1 y termina en 5, **sin agotar el quantum**. P1 usa 2 más (le quedan 4), P2 termina en 9, y P1, ya solo, termina en 13.

| Proceso | Fin | Espera |
|---|---|---|
| P1 | 13 | 5 |
| P2 | 9 | 5 |
| P3 | 5 | 4 |
| **Media** | | **4,67 ms** |

- **Ventaja:** es **equitativo** y da buen tiempo de respuesta: P3 termina en 5 ms en lugar de 13 con FCFS.
- **Inconveniente:** hay muchos más **cambios de contexto**.

!!! tip "¿Qué quantum elegir?"
    - Si el quantum es **muy grande**, Round Robin se comporta como FCFS.
    - Si es **muy pequeño**, la CPU pasa más tiempo cambiando de proceso que trabajando.
    - En la práctica se usan quantums de unos pocos milisegundos (entre 1 y 100 ms).

!!! note "Regla para los ejercicios con llegadas"
    Si un proceso llega en el mismo instante en que otro agota su quantum, el que **llega** entra en la cola **antes** que el que sale de la CPU.

### Comparativa

| Algoritmo | Expropiativo | Ventaja | Riesgo |
|---|---|---|---|
| FCFS | No | Sencillo | Efecto convoy |
| SJF | No | Espera media mínima | Hay que conocer las ráfagas; inanición |
| SRTF | Sí | Aún mejor espera media | Inanición; más cambios de contexto |
| Prioridades | Según versión | Atiende lo urgente | Inanición (solución: envejecimiento) |
| Round Robin | Sí | Equitativo e interactivo | Muchos cambios de contexto si el quantum es pequeño |

Los sistemas reales combinan varias ideas. Linux, por ejemplo, reparte la CPU de forma proporcional entre los procesos y da más peso a los interactivos. Windows usa prioridades con turnos rotatorios dentro de cada nivel.

## 4.3 El cambio de contexto

Cada vez que el planificador cambia el proceso que se ejecuta en un núcleo se produce un **cambio de contexto**:

1. El SO **guarda** en el PCB del proceso saliente su estado: contador de programa, registros, puntero de pila…
2. **Carga** desde el PCB del proceso entrante su estado guardado.
3. El proceso entrante continúa justo donde lo dejó.

Durante ese tiempo la CPU **no hace trabajo útil**: es sobrecarga pura. Además, al cambiar de proceso se pierde el contenido útil de las memorias caché del procesador, lo que ralentiza los primeros instantes del proceso entrante.

**¿Cuándo ocurre?** Cuando se acaba el quantum, cuando el proceso se bloquea, cuando llega uno más prioritario o cuando termina.

!!! note "Hilos"
    Cambiar entre dos hilos del **mismo proceso** es más barato, porque comparten la memoria y no hay que cambiar las tablas de memoria. Lo veremos en el Tema 2.

## Preguntas de repaso

1. ¿Qué diferencia hay entre un planificador expropiativo y uno no expropiativo? ¿Cuál usan los sistemas operativos actuales?
2. ¿Qué es el efecto convoy? ¿Con qué algoritmo aparece?
3. ¿Qué es la inanición? ¿En qué algoritmos puede ocurrir y cómo se evita?
4. Repite el ejemplo de Round Robin con quantum de 4 ms. ¿Mejora o empeora la espera media? ¿Cuántos cambios de contexto hay?
5. ¿Por qué no se usa un quantum de 1 microsegundo para que todo parezca más fluido?
6. ¿Qué datos se guardan en un cambio de contexto y dónde?
