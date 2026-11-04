# Tema 2. Multihilos

!!! abstract "Resultado de aprendizaje"
    **RA2.** Desarrolla aplicaciones compuestas por varios hilos de ejecución analizando y aplicando librerías específicas del lenguaje de programación.

## ¿De qué trata este tema?

En el Tema 1 aprendiste a lanzar **procesos**: programas completos, cada uno con su propia memoria. En este tema bajamos un nivel. Dentro de un mismo programa puede haber varias líneas de ejecución trabajando a la vez: los **hilos**. Aprenderás:

- **Qué es un hilo**, qué comparte con los demás hilos de su proceso y para qué sirve tener varios.
- **Cómo crear, arrancar, esperar y parar hilos** en Java, y en qué estados puede estar cada uno.
- **Qué pasa cuando varios hilos tocan el mismo dato** y cómo evitar que el resultado salga mal.

## Apartados

| Apartado | Qué aprenderás |
|---|---|
| [1. Proceso frente a hilo](01-proceso-hilo.md) | Qué es un hilo, qué comparte y qué no, para qué sirve y cuándo merece la pena. |
| [2. Crear hilos en Java](02-crear-hilos.md) | `Thread`, `Runnable` y lambdas; `start()` frente a `run()`; lanzar y esperar muchos hilos. |
| [3. Ciclo de vida de un hilo](03-estados.md) | Los seis estados de `Thread.State` y qué provoca cada cambio. |
| [4. Controlar hilos](04-controlar-hilos.md) | `sleep`, `join`, `interrupt` y los hilos demonio. |
<!-- si-visible: temas/tema-2/05-hilos-virtuales.md -->
| [5. Hilos virtuales](05-hilos-virtuales.md) | La novedad de Java 21: hilos ligeros para tareas que pasan mucho tiempo esperando. |
<!-- fin -->
| [Práctica guiada: gestor de descargas](practica-guiada.md) | Un programa que junta todo lo anterior, paso a paso. |
| [Práctica guiada: solución](practica-guiada-solucion.md) | El código completo de cada paso, con su salida y las respuestas. |
| [6. Condición de carrera](06-condicion-carrera.md) | Por qué falla un programa cuando dos hilos escriben en el mismo dato. |
| [7. synchronized](07-synchronized.md) | Exclusión mutua: que solo un hilo a la vez entre en la sección crítica. |
| [8. Clases atómicas](08-atomicas.md) | `AtomicInteger` y cuándo usar cada solución. |

<!-- si-oculto: temas/tema-2/05-hilos-virtuales.md -->
!!! note "Apartado 5"
    El apartado 5, **hilos virtuales**, se publica cuando lo veamos en clase, junto con los ejecutores.
<!-- fin -->

## Cómo estudiar este tema

1. Lee cada apartado **después** de la explicación en clase. El texto amplía lo que se ve en las diapositivas.
2. Copia y ejecuta los ejemplos. Todos funcionan con **JDK 21 o superior**. Ejecútalos **varias veces**: con hilos, el orden de la salida cambia de una ejecución a otra, y verlo es parte de lo que hay que aprender.
3. Al final de cada apartado tienes **preguntas de repaso**. Si no sabes responder alguna, vuelve a leer la sección.
4. Practica con el [boletín de ejercicios](boletin.md).

!!! tip "Antes de empezar"
    Comprueba tu versión de Java con `java -version`: debe ser la **21 o superior**. Algunas partes del tema, como `Thread.ofVirtual()`, no existen en versiones anteriores.

    ```bash
    javac NombreDeLaClase.java
    java NombreDeLaClase
    ```
