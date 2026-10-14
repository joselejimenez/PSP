# 3. Estados de un proceso

Desde que se crea hasta que termina, un proceso pasa por distintos **estados**. El sistema operativo apunta el estado actual en el PCB y lo usa para decidir qué hacer con cada proceso.

## 3.1 Los cinco estados

<svg class="diagrama" viewBox="0 0 760 300" role="img" aria-label="Diagrama de los cinco estados de un proceso y sus transiciones">
<defs><marker id="punta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>
<rect class="caja" x="10" y="40" width="110" height="46" rx="10"/><text class="txt" x="65" y="63">Nuevo</text>
<rect class="caja" x="200" y="40" width="110" height="46" rx="10"/><text class="txt" x="255" y="63">Listo</text>
<rect class="caja activa" x="430" y="40" width="130" height="46" rx="10"/><text class="txt" x="495" y="63">Ejecución</text>
<rect class="caja" x="640" y="40" width="110" height="46" rx="10"/><text class="txt" x="695" y="63">Terminado</text>
<rect class="caja" x="305" y="220" width="130" height="46" rx="10"/><text class="txt" x="370" y="243">Bloqueado</text>
<path class="flecha" d="M120,63 L198,63"/><text class="etq" x="159" y="52">admitir</text>
<path class="flecha" d="M310,55 L428,55"/><text class="etq" x="369" y="22">el planificador</text><text class="etq" x="369" y="37">lo elige</text>
<path class="flecha" d="M430,74 L312,74"/><text class="etq" x="371" y="96">fin del quantum</text>
<path class="flecha" d="M560,63 L638,63"/><text class="etq" x="599" y="52">termina</text>
<path class="flecha" d="M495,86 L495,243 L437,243"/><text class="etq" x="560" y="170">pide E/S o</text><text class="etq" x="560" y="185">espera un suceso</text>
<path class="flecha" d="M305,243 L255,243 L255,88"/><text class="etq" x="190" y="170">llega lo que</text><text class="etq" x="190" y="185">esperaba</text>
</svg>

| Estado | Qué significa | Ejemplo |
|---|---|---|
| **Nuevo** | El SO está creando el proceso: reserva memoria y crea su PCB. | Acabas de hacer doble clic en el icono. |
| **Listo** | Está preparado para ejecutarse; solo le falta que le den la CPU. Espera en la **cola de listos**. | Hay 200 procesos y solo 8 núcleos: la mayoría están listos, esperando turno. |
| **En ejecución** | Está usando un núcleo de la CPU. | El navegador está procesando una página. |
| **Bloqueado** (o en espera) | No puede continuar hasta que ocurra algo: que termine una lectura de disco, que llegue un dato por la red o que el usuario pulse una tecla. | Un programa espera en `Scanner.nextLine()` a que escribas. |
| **Terminado** | Ha acabado (bien o con error). El SO libera sus recursos y guarda su código de salida hasta que el padre lo recoja. | El `main` de Java ha llegado al final. |

## 3.2 Las transiciones

1. **Nuevo → Listo (admitir).** El SO termina de crear el proceso y lo pone en la cola de listos.
2. **Listo → Ejecución.** El **planificador** elige ese proceso y le asigna un núcleo.
3. **Ejecución → Listo.** Se le acaba su turno (su **quantum**) o llega un proceso más prioritario. Vuelve a la cola de listos aunque no haya terminado.
4. **Ejecución → Bloqueado.** El proceso pide algo lento mediante una **llamada al sistema**: leer un fichero, recibir datos de la red, esperar una tecla. Como no puede seguir, deja la CPU libre para otro.
5. **Bloqueado → Listo.** Llega lo que esperaba. El hardware avisa al SO con una **interrupción** y el proceso vuelve a la cola de listos.
6. **Ejecución → Terminado.** El proceso acaba o se produce un error grave.

!!! warning "Dos transiciones que NO existen"
    - **Bloqueado → Ejecución.** Un proceso bloqueado que recibe lo que esperaba pasa primero a **Listo** y espera su turno como los demás.
    - **Listo → Bloqueado.** Solo puede bloquearse un proceso que se está ejecutando, porque bloquearse es consecuencia de pedir algo.

!!! note "¿Cuántos procesos puede haber en cada estado?"
    En un ordenador con 8 núcleos, como máximo **8 procesos** pueden estar en ejecución a la vez. En Listo y en Bloqueado puede haber todos los que quepan en memoria.

## 3.3 Las colas del sistema operativo

El sistema operativo organiza los procesos en **colas**:

| Cola | Qué procesos contiene |
|---|---|
| **Cola de procesos** | Todos los procesos del sistema. |
| **Cola de listos** | Los procesos en estado Listo, esperando CPU. El planificador elige de aquí. |
| **Colas de dispositivo** | Una por dispositivo (disco, red, teclado…), con los procesos bloqueados esperando ese dispositivo. |

## 3.4 Procesos limitados por CPU y por E/S

Según en qué pasen la mayor parte del tiempo, los procesos se clasifican en:

- **Limitados por CPU** (*CPU-bound*): pasan casi todo el tiempo calculando. Ejemplos: comprimir un vídeo, entrenar un modelo, calcular números primos. Van más rápido con un procesador más rápido o repartiendo el trabajo entre varios núcleos.
- **Limitados por E/S** (*I/O-bound*): pasan casi todo el tiempo **bloqueados**, esperando al disco, a la red o al usuario. Ejemplos: un editor de texto, un navegador descargando una página, un servidor esperando peticiones. Van más rápido con un disco o una red más rápidos.

!!! example "Una máquina recreativa con un solo núcleo"
    Un videojuego antiguo repite tres tareas: **leer el mando** (E/S), **calcular el mundo del juego** (CPU) y **dibujar la pantalla** (E/S). Mientras el juego espera a que el jugador pulse un botón, la tarea de leer el mando está bloqueada y el núcleo puede dedicarse a calcular. Mezclar tareas de CPU y de E/S aprovecha mucho mejor el procesador.

## 3.5 ¿Y si se acaba la memoria RAM?

Si hay más procesos de los que caben en la RAM, el sistema operativo usa la **memoria virtual**: mueve al disco las partes de la memoria de los procesos que se usan poco (zona de **intercambio** o *swap*; en Windows, el archivo de paginación) y las vuelve a traer cuando hacen falta.

- **Ventaja:** se pueden ejecutar más programas de los que caben en la RAM.
- **Inconveniente:** el disco es miles de veces más lento que la RAM. Si se abusa, el sistema se pasa el tiempo moviendo datos y todo va muy lento. Esta situación se llama **hiperpaginación** (*thrashing*).

## 3.6 Ver el estado de un proceso

En Linux, la columna `STAT` de `ps` muestra el estado con una letra:

```bash
ps -eo pid,ppid,stat,cmd | head
```

| Letra | Estado |
|---|---|
| `R` | En ejecución o listo (*running/runnable*) |
| `S` | Bloqueado, esperando un suceso (*sleeping*) |
| `D` | Bloqueado esperando E/S, no se puede interrumpir |
| `T` | Detenido |
| `Z` | Zombi |

En Java, `Process.isAlive()` indica si el proceso hijo sigue vivo (en cualquier estado salvo terminado).

## Preguntas de repaso

1. ¿Qué diferencia hay entre un proceso **listo** y uno **bloqueado**? ¿Cuál de los dos podría usar la CPU si se la dieran?
2. ¿Por qué un proceso bloqueado no pasa directamente a ejecución cuando llega lo que esperaba?
3. Un programa Java está parado en `Scanner.nextLine()`. ¿En qué estado está? ¿Qué transición se produce cuando pulsas Intro?
4. Clasifica como limitado por CPU o por E/S: un compresor ZIP, un cliente de correo, un servidor de bases de datos, un programa que calcula decimales de π.
5. ¿Qué es la hiperpaginación y por qué ralentiza el sistema?
