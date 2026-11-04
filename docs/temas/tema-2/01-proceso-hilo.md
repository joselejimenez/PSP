# 1. Proceso frente a hilo

Un **proceso** es el contenedor de los recursos de un programa en ejecución: su memoria, sus ficheros abiertos, sus conexiones. Un **hilo** (*thread*) es quien ejecuta las instrucciones. Todo proceso tiene al menos un hilo, y puede tener muchos.

## 1.1 Qué es un hilo

Un hilo es una **línea de ejecución dentro de un proceso**. Cuando lanzas un programa Java, la JVM crea un proceso con un hilo principal, el que ejecuta el método `main`. Desde ese hilo puedes crear otros que avancen a la vez.

- Si el ordenador tiene **varios núcleos**, cada hilo puede ejecutarse en uno distinto, de verdad al mismo tiempo (**paralelismo**).
- Si solo hay **un núcleo**, los hilos se turnan: el planificador del sistema operativo los va alternando tan rápido que parece que avanzan a la vez (**concurrencia**).

En un sistema hay dos tipos de hilos:

- **Hilos del sistema operativo**: los que usa el propio sistema para hacer varias cosas a la vez, como escuchar la red, atender el teclado y el ratón o refrescar la pantalla.
- **Hilos de usuario**: los que crean los programadores en sus aplicaciones. Son los que vamos a programar.

!!! example "La cocina"
    En el Tema 1, crear un proceso hijo era como montar **otra cocina** para el pinche, con su nevera y sus fogones: todo duplicado, caro, pero aislado. Crear un hilo es meter **otro cocinero en la misma cocina**. Sale barato y pueden pasarse los ingredientes al momento, pero si dos cogen el mismo cuchillo a la vez, hay problemas. Cada cocinero lleva **su propia libreta** con el paso de la receta en el que va.

!!! tip "Compruébalo en tu ordenador"
    En el Administrador de tareas de Windows, pestaña **Detalles**, añade la columna **Subprocesos**: casi ningún programa tiene un solo hilo, y el navegador suele tener decenas. En Linux, `ps -eLf | wc -l` cuenta todos los hilos del sistema.

## 1.2 Qué comparten los hilos y qué no

Los hilos de un mismo proceso pueden acceder a **todos los recursos del proceso**, excepto a las pilas de los otros hilos.

| Compartido por todos los hilos del proceso | Propio de cada hilo |
|---|---|
| El **heap**: todos los objetos creados con `new` | Su **pila**: las variables locales y los parámetros de los métodos que está ejecutando |
| Los campos `static` | Su **contador de programa**: por qué instrucción va |
| Los ficheros abiertos y las conexiones de red | Su nombre, su prioridad y su estado |

Traducido a Java:

- Una **variable local** dentro de un método vive en la pila: cada hilo tiene su copia y no hay problema.
- Un **objeto** al que dos hilos tienen referencia, o un **campo `static`**, es el mismo para los dos. Si los dos lo modifican a la vez, el resultado puede salir mal. Ese problema se llama **condición de carrera** y lo estudiaremos en el [apartado 6](06-condicion-carrera.md).

| | Proceso | Hilo |
|---|---|---|
| **Memoria** | Propia y aislada | Compartida con los demás hilos del proceso |
| **Crear uno** | Costoso: memoria propia y estructuras del SO | Barato: solo necesita su pila |
| **Comunicarse** | Mecanismos del SO: tuberías, ficheros, sockets | Basta con compartir un objeto |
| **Si falla** | Cae él solo | Puede tumbar todo el proceso |

## 1.3 Para qué queremos hilos

1. **Que el programa no se congele.** Si una aplicación descarga un fichero en el hilo principal, la interfaz deja de responder hasta que acaba. Con la descarga en otro hilo, la interfaz sigue viva. En Android es obligatorio: si bloqueas el hilo principal unos segundos, el sistema muestra «La aplicación no responde».
2. **Atender a muchos a la vez.** Un servidor dedica un hilo a cada cliente, y así ninguno tiene que esperar a que acaben los demás. Lo programarás en el Tema 3 con sockets.
3. **Usar todos los núcleos.** Un cálculo grande se puede partir en trozos, uno por núcleo. Con 8 núcleos, puede ir casi 8 veces más rápido.

Normalmente no trabajarás con hilos «a pelo». Pero todo lo asíncrono que usarás en otros módulos, como las `Promise` de JavaScript, las corrutinas de Kotlin o `async/await`, funciona por debajo **sobre hilos**.

## 1.4 CPU-bound o IO-bound: qué frena tu programa

Antes de meter hilos hay que preguntarse **en qué pasa el tiempo** el programa. Es la misma clasificación que viste con los procesos en el Tema 1.

| | Limitado por CPU (*CPU-bound*) | Limitado por E/S (*IO-bound*) |
|---|---|---|
| **Pasa el tiempo…** | Calculando | Esperando: a la red, al disco, al usuario |
| **Ejemplos** | Comprimir, cifrar, renderizar | Descargar, consultar una base de datos |
| **Los hilos ganan…** | Solo si hay núcleos libres | Casi siempre: mientras uno espera, otro trabaja |
| **Cuántos hilos** | Más o menos, tantos como núcleos | Muchos más que núcleos |

- **CPU-bound:** con 8 núcleos y 8 hilos, cada hilo ocupa un núcleo. Con 100 hilos no ganas nada: se turnan, y encima pierdes tiempo en los cambios de contexto.
- **IO-bound:** un hilo que espera no gasta CPU, así que puedes tener muchos más hilos que núcleos. Es el caso de los servidores.

Para saber cuántos núcleos ve la JVM:

```java
int nucleos = Runtime.getRuntime().availableProcessors();
System.out.println("Núcleos disponibles: " + nucleos);
```

## 1.5 ¿Proceso o hilo?

| Caso | Mejor opción | Por qué |
|---|---|---|
| Un editor revisa la ortografía mientras escribes | Hilo | Necesita leer el mismo documento que estás editando. |
| Chrome aísla cada pestaña | Proceso | Si una página falla o es maliciosa, no debe afectar a las demás. |
| Un servidor atiende a 200 clientes que consultan el mismo catálogo en memoria | Hilo | Comparten el catálogo y cada cliente pasa casi todo el tiempo esperando a la red. |
| El IDE compila tu proyecto con Gradle | Proceso | Gradle es otro programa, como los que lanzabas con `ProcessBuilder`. |
| Un videojuego calcula la física de 500 objetos | Hilo | Necesita los objetos del juego en memoria; se reparte el cálculo entre los núcleos. |

!!! note "Regla práctica"
    Si necesitas **compartir memoria**, usa hilos. Si necesitas **aislamiento**, o lo que vas a ejecutar es **otro programa**, usa procesos.

## Preguntas de repaso

1. ¿Qué tiene cada hilo que no comparte con los demás hilos de su proceso?
2. Un hilo hace `int x = 5;` dentro de su tarea. ¿Puede verlo otro hilo? ¿Y si hace `contador++` sobre un `static int contador`?
3. ¿Por qué un fallo en un hilo puede tumbar todo el proceso y un fallo en un proceso hijo no tumba al padre?
4. ¿Qué gana un programa CPU-bound con 100 hilos en un ordenador de 8 núcleos? ¿Y uno IO-bound?
5. Clasifica como CPU-bound o IO-bound: redimensionar 1000 fotos que ya están en disco; descargar 1000 fotos de Internet.
