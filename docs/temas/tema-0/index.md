# Tema 0. Repaso de Java

!!! abstract "Por qué este tema"
    En PSP todo se programa en **Java**: lanzar procesos, crear hilos, abrir sockets o cifrar datos. Este tema repasa el Java de 1.º DAM que vas a necesitar, desde los tipos básicos hasta las colecciones, la herencia, las lambdas y los ficheros. No es un tema evaluable por sí mismo, pero **sin esta base el resto del módulo se hace cuesta arriba**.

## Apartados

| Apartado | Qué repasarás | Ejercicios |
|---|---|---|
| [1. Fundamentos](01-fundamentos.md) | Estructura de un programa, tipos, variables, operadores, `Scanner`, condicionales y bucles. | 1 – 3 |
| [2. Métodos y arrays](02-metodos-arrays.md) | Métodos `static`, paso de parámetros, sobrecarga, recursividad, arrays de una y dos dimensiones. | 4 – 6 |
| [3. Cadenas de texto](03-cadenas.md) | `String`, comparación, `StringBuilder`, formato de texto y conversión entre texto y números. | 7 – 9 |
| [4. Excepciones](04-excepciones.md) | `try`/`catch`/`finally`, excepciones comprobadas y no comprobadas, `throw`, `throws` y excepciones propias. | 10 |
| [5. Programación orientada a objetos](05-poo.md) | Clases, encapsulación, `static`, herencia, polimorfismo, clases abstractas e interfaces. | 11 – 14 |
| [6. Colecciones](06-colecciones.md) | `List`, `Set` y `Map`, genéricos, recorridos y ordenación con `Comparator`. | 15 – 16 |
| [7. Java moderno](07-java-moderno.md) | Lambdas, interfaces funcionales, `Runnable`, streams, `Optional`, `enum` y `record`. | 17 – 18 |
| [8. Ficheros y entrada/salida estándar](08-ficheros-es.md) | `Path` y `Files`, lectura y escritura con *buffers*, `System.in`, `System.out`, `System.err` y el código de salida. | 19 – 20 |
| [Boletín de repaso](boletin.md) | Veinte ejercicios graduados de ★ a ★★★★★. | |

## Antes de empezar

Comprueba que tienes instalado el **JDK 21 o superior**:

```bash
java -version
javac -version
```

Puedes trabajar con el IDE que prefieras (IntelliJ IDEA, VS Code, NetBeans o Eclipse), pero conviene que sepas compilar y ejecutar desde la terminal, porque en el Tema 1 lanzaremos programas Java desde otros programas Java:

```bash
javac HolaMundo.java     # compila: genera HolaMundo.class
java HolaMundo           # ejecuta la clase
java HolaMundo.java      # desde Java 11: compila y ejecuta un único fichero
```

## Cómo estudiar este tema

1. Lee cada apartado y **ejecuta los ejemplos**: copia el código, cámbialo y observa qué pasa.
2. Al final de cada apartado tienes **preguntas de repaso** y los ejercicios del boletín que le corresponden.
3. Si un apartado ya lo dominas, ve directamente a sus ejercicios. Si no sabes resolverlos, vuelve a la teoría.

!!! tip "Lo que más se usa en el resto del módulo"
    Si vas justo de tiempo, prioriza: **excepciones** (apartado 4), **interfaces y clases** (apartado 5), **colecciones** (apartado 6), **lambdas y `Runnable`** (apartado 7) y **entrada/salida estándar** (apartado 8). Son las piezas que aparecen en los Temas 1, 2 y 3.
