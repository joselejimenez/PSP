# Tema 1. Multiprocesos

!!! abstract "Resultado de aprendizaje"
    **RA1.** Desarrolla aplicaciones compuestas por varios procesos reconociendo y aplicando principios de programación paralela.

## ¿De qué trata este tema?

Cada vez que abres el navegador, el IDE o un videojuego, el sistema operativo crea uno o varios **procesos** y reparte entre ellos la memoria y el tiempo de CPU. En este tema aprenderás:

- **Qué es un proceso** y en qué se diferencia de un programa, de un servicio y de un hilo.
- **Cómo hace el sistema operativo** para que parezca que todo se ejecuta a la vez, aunque haya un solo núcleo.
- **Cómo programar en Java** aplicaciones que lanzan otros procesos, les pasan datos, leen sus resultados, los esperan y los terminan.

## Apartados

| Apartado | Qué aprenderás |
|---|---|
| [1. Programa, proceso, servicio e hilo](01-conceptos.md) | Los cuatro conceptos básicos del módulo, el PCB, el PID y la jerarquía de procesos. |
| [2. Programación concurrente, paralela y distribuida](02-tipos-programacion.md) | Tres formas de hacer varias cosas a la vez y cuánto se puede ganar con cada una. |
| [3. Estados de un proceso](03-estados.md) | El ciclo de vida de un proceso, desde que se crea hasta que termina. |
| [4. Planificación de la CPU](04-planificacion.md) | Cómo decide el sistema operativo qué proceso usa la CPU en cada momento. |
| [5. Crear procesos en Java](05-crear-procesos.md) | `ProcessBuilder` y `Process`: lanzar programas, otras clases Java y páginas web. |
| [6. Comunicar y controlar procesos](06-comunicar-controlar.md) | Leer la salida de un hijo, enviarle datos, esperarlo con límite, terminarlo y observar procesos. |

## Cómo estudiar este tema

1. Lee cada apartado **después** de la explicación en clase. El texto amplía lo que se ve en las diapositivas.
2. Copia y ejecuta los ejemplos de código. Todos funcionan con **JDK 21 o superior** en Windows, Linux y macOS (cuando hay diferencias entre sistemas, se indica).
3. Al final de cada apartado tienes unas **preguntas de repaso**. Si no sabes responder alguna, vuelve a leer la sección.
4. Practica con el [boletín de ejercicios](boletin.md).

!!! tip "Antes de empezar"
    Comprueba tu versión de Java con `java -version`. Debe ser la 21 o superior. Para compilar y ejecutar los ejemplos desde la terminal:

    ```bash
    javac *.java
    java NombreDeLaClase
    ```
