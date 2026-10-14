# 2. Programación concurrente, paralela y distribuida

Hay tres formas de conseguir que un sistema haga varias cosas «a la vez». Se diferencian en **cuántos procesadores** hay y **dónde están**.

## 2.1 Punto de partida: la ejecución secuencial

Un programa **secuencial** ejecuta las instrucciones una detrás de otra: no empieza un paso hasta que termina el anterior. Es la forma más sencilla de programar, y la que habéis usado hasta ahora.

- **Ventaja:** es fácil de escribir, de entender y de depurar. El resultado siempre es el mismo.
- **Inconveniente:** no aprovecha el hardware. Si el ordenador tiene 8 núcleos, el programa usa uno y los otros siete se quedan parados. Mientras espera al disco o a la red, la CPU tampoco hace nada.

## 2.2 Programación concurrente

Hay **concurrencia** cuando varias tareas están **en curso** durante el mismo periodo de tiempo, aunque no se ejecuten exactamente en el mismo instante.

Imagina **un solo cocinero** que prepara una ensalada y una sopa. Pica un poco de lechuga, se acerca a remover la sopa, vuelve a picar… Los dos platos avanzan, pero en cada instante el cocinero solo hace una cosa. Sin concurrencia, tendría que esperar a que la sopa estuviera hecha para empezar la ensalada.

En un ordenador con **un solo núcleo**, el sistema operativo hace lo mismo: ejecuta un trozo de un proceso, lo para, ejecuta un trozo de otro, y así continuamente. Los cambios son tan rápidos (milisegundos) que parece que todo se ejecuta a la vez. A esto se le llama **multiprogramación**.

<div class="gantt">
<div class="g-titulo">Un núcleo: los procesos se turnan</div>
<div class="g-fila"><span class="g-etq">Núcleo 1</span><div class="g-pista">
<div class="g-barra c1" style="left:0.000%;width:16.667%">A</div>
<div class="g-barra c2" style="left:16.667%;width:16.667%">B</div>
<div class="g-barra c3" style="left:33.333%;width:16.667%">C</div>
<div class="g-barra c1" style="left:50.000%;width:16.667%">A</div>
<div class="g-barra c2" style="left:66.667%;width:16.667%">B</div>
<div class="g-barra c3" style="left:83.333%;width:16.667%">C</div>
</div></div>
<div class="g-eje"><span style="left:0.000%">0</span><span style="left:16.667%">2</span><span style="left:33.333%">4</span><span style="left:50.000%">6</span><span style="left:66.667%">8</span><span style="left:83.333%">10</span><span style="left:100.000%">12</span></div>
</div>

**¿Para qué sirve si no se gana tiempo de CPU?** Para no desperdiciarla mientras se espera. Cuando un proceso pide leer un fichero o espera una respuesta de la red, se queda parado varios milisegundos. En ese tiempo, la CPU puede atender a otro proceso. Además, la concurrencia permite que un programa siga **respondiendo** al usuario mientras hace un trabajo largo.

**Dónde se usa:** sistemas operativos multitarea, servidores que atienden a muchos clientes, interfaces gráficas que no se congelan, videojuegos.

## 2.3 Programación paralela

Hay **paralelismo** cuando varias tareas se ejecutan **en el mismo instante** en procesadores o núcleos distintos. Volviendo a la cocina: ahora hay **dos cocineros**, uno pica y otro remueve. Ya no hay que alternar.

<div class="gantt">
<div class="g-titulo">Tres núcleos: los procesos avanzan a la vez</div>
<div class="g-fila"><span class="g-etq">Núcleo 1</span><div class="g-pista">
<div class="g-barra c1" style="left:0.000%;width:50.000%">A</div>
</div></div>
<div class="g-fila"><span class="g-etq">Núcleo 2</span><div class="g-pista">
<div class="g-barra c2" style="left:0.000%;width:50.000%">B</div>
</div></div>
<div class="g-fila"><span class="g-etq">Núcleo 3</span><div class="g-pista">
<div class="g-barra c3" style="left:0.000%;width:50.000%">C</div>
</div></div>
<div class="g-eje"><span style="left:0.000%">0</span><span style="left:16.667%">2</span><span style="left:33.333%">4</span><span style="left:50.000%">6</span><span style="left:66.667%">8</span><span style="left:83.333%">10</span><span style="left:100.000%">12</span></div>
</div>

- Requiere **hardware** con varios núcleos o procesadores (**multiprocesamiento**). Hoy casi todos los ordenadores y móviles lo tienen.
- La programación paralela consiste en **dividir un problema** en partes que se puedan calcular a la vez y **combinar** después los resultados.
- Todo programa paralelo es concurrente, pero no al revés: la concurrencia es organizar varias tareas; el paralelismo es tener más manos para hacerlas.

!!! warning "Multitarea no es lo mismo que multinúcleo"
    **Multitarea** es la capacidad del sistema operativo de tener varias tareas en curso. Existía mucho antes de los procesadores multinúcleo: Windows 95 era multitarea con un solo núcleo. Tener varios núcleos o procesadores se llama **multiprocesamiento**.

### Tareas independientes y tareas dependientes

No todo problema se puede paralelizar igual de bien.

- **Tareas independientes:** cada parte se puede calcular sin saber nada de las demás. Por ejemplo, aplicar un filtro a 1000 fotos, contar los números primos de un rango o lavar cuatro cargas de ropa en cuatro lavadoras. Se dice que son problemas de **paralelismo trivial**: basta con repartir el trabajo.
- **Tareas dependientes:** un paso necesita el resultado del anterior. Por ejemplo, calcular la sucesión de Fibonacci o hacer los pasos de una receta en orden. Aquí hay que **sincronizar**: hacer esperar a unas tareas hasta que otras terminen. Eso limita mucho lo que se gana.

### La ley de Amdahl: cuánto se puede ganar

Casi todos los programas tienen una parte que se puede paralelizar y otra que es **secuencial** por naturaleza: preparar los datos, repartirlos, juntar los resultados. Por mucho que añadamos núcleos, la parte secuencial tarda lo mismo.

La **ley de Amdahl** calcula la aceleración máxima (*speedup*) con **n** núcleos si una fracción **p** del programa es paralelizable:

```
S(n) = 1 / ( (1 − p) + p / n )
```

!!! example "Ejemplo"
    Un programa tarda 100 s y el 80 % se puede paralelizar (p = 0,8).

    | Núcleos | Aceleración | Tiempo |
    |---|---|---|
    | 1 | 1 | 100 s |
    | 2 | 1 / (0,2 + 0,4) = 1,67 | 60 s |
    | 4 | 1 / (0,2 + 0,2) = 2,5 | 40 s |
    | 8 | 1 / (0,2 + 0,1) = 3,33 | 30 s |
    | ∞ | 1 / 0,2 = **5** | 20 s |

    Aunque tuviéramos infinitos núcleos, el programa nunca bajaría de 20 s: es lo que tarda su parte secuencial. **Un programa paralelo va tan rápido como su parte secuencial más lenta.** Es lo que pasa en un supermercado: cientos de personas compran a la vez, pero al pagar se forman colas porque hay pocas cajas.

Además, repartir el trabajo tiene un **coste**: crear procesos, enviarles datos y recoger los resultados. Si las tareas son muy pequeñas, ese coste puede ser mayor que lo que se gana.

## 2.4 Programación distribuida

En la **programación distribuida**, el trabajo se reparte entre **varios ordenadores independientes**, conectados por una red, que colaboran como si fueran un único sistema. Cada ordenador tiene su propia memoria y su propio reloj, y solo se comunican **enviándose mensajes**.

Ejemplos: una aplicación web con el servidor en la nube y el cliente en el móvil, un videojuego en línea, el sistema de pagos de un banco, el entrenamiento de un modelo de inteligencia artificial en cientos de servidores.

| | Ventajas | Inconvenientes |
|---|---|---|
| **Paralela** (un equipo, varios núcleos) | Comunicación muy rápida a través de la memoria; más sencilla de programar | Limitada a los núcleos de una máquina; si el equipo falla, falla todo |
| **Distribuida** (varios equipos) | Escala añadiendo máquinas; tolera fallos (si cae un servidor, otro lo sustituye); los recursos pueden estar en lugares distintos | La red es lenta y puede fallar; hay que tratar mensajes perdidos o duplicados; es más difícil de programar y depurar |

En la práctica, los sistemas reales **combinan** las tres formas: un servidor web atiende a muchos clientes de forma concurrente, usa varios núcleos en paralelo y forma parte de un sistema distribuido.

## 2.5 Resumen

| | Secuencial | Concurrente | Paralela | Distribuida |
|---|---|---|---|---|
| Procesadores | 1 | 1 o más | Varios en un equipo | Varios equipos |
| Tareas a la vez | Una | Varias en curso, alternándose | Varias en el mismo instante | Varias en distintas máquinas |
| Comunicación | — | Memoria compartida o SO | Memoria compartida o SO | Mensajes por la red |
| Ejemplo | Un script que procesa un fichero | Un SO con un núcleo | Renderizar un vídeo con 8 núcleos | Una aplicación en la nube |

## Preguntas de repaso

1. Explica con tus palabras la diferencia entre concurrencia y paralelismo. Usa un ejemplo de la vida diaria.
2. Si un ordenador tiene un solo núcleo, ¿puede ejecutar programas concurrentes? ¿Y paralelos?
3. ¿Por qué la concurrencia mejora el rendimiento aunque haya un solo núcleo, si los procesos esperan al disco o a la red?
4. Un programa tiene un 50 % de código paralelizable. ¿Cuál es la aceleración máxima que puede conseguir con infinitos núcleos?
5. Indica una ventaja y un inconveniente de la programación distribuida frente a la paralela.
6. ¿Es lo mismo multitarea que multiprocesamiento? Justifica tu respuesta.
