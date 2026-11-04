# 5. Hilos virtuales

Desde **Java 21**, además de los hilos de siempre existen los **hilos virtuales**: hilos ligeros que gestiona la propia JVM. Puedes tener cientos de miles, o millones, esperando a la vez.

## 5.1 Hilo de plataforma frente a hilo virtual

Todos los hilos de los apartados anteriores son **hilos de plataforma**: cada objeto `Thread` corresponde a un hilo del sistema operativo. Son caros: el sistema reserva para cada uno una pila de alrededor de 1 MB y los planifica el núcleo. Con unos miles ya se nota.

| | De plataforma | Virtual |
|---|---|---|
| **Lo gestiona** | El sistema operativo | La JVM |
| **Pila** | ≈ 1 MB reservado | Unos pocos KB; crece si hace falta |
| **Cuántos caben** | Miles | Millones |
| **Mientras espera E/S** | Ocupa un hilo del sistema | Se «aparca» y deja libre el hilo real |
| **Ideal para** | Tareas CPU-bound | Muchas tareas IO-bound |

Cómo funcionan:

- Para ejecutarse, la JVM monta el hilo virtual sobre un hilo de plataforma, llamado **portador** (*carrier*). Hay pocos portadores, más o menos uno por núcleo.
- Cuando el hilo virtual hace algo que espera (`sleep`, leer de la red, consultar una base de datos), la JVM lo **desmonta** y el portador queda libre para ejecutar otro hilo virtual. Cuando llega el dato, lo vuelve a montar, quizá en otro portador.

!!! example "Los camareros"
    En un restaurante con un camarero por mesa (hilos de plataforma), los camareros pasan casi todo el tiempo esperando a que los clientes decidan. Con hilos virtuales, unos pocos camareros atienden muchas mesas, porque nunca se quedan parados esperando: atienden otra y vuelven.

!!! warning "No hacen el cálculo más rápido"
    Los hilos virtuales hacen **más barata la espera**, no el cálculo. Si la tarea es CPU-bound, no hay esperas que aprovechar y van igual que los de plataforma.

## 5.2 Crear un hilo virtual

Un hilo virtual **es un `Thread`**: `join`, `sleep`, `interrupt` y `getState` funcionan igual. Solo cambia cómo se crea.

```java
public class CrearVirtual {
    public static void main(String[] args) throws InterruptedException {
        Runnable tarea = () -> System.out.println(Thread.currentThread());

        Thread v = Thread.ofVirtual().name("virtual-1").start(tarea);
        Thread p = Thread.ofPlatform().name("plataforma-1").start(tarea);
        v.join();
        p.join();
        System.out.println("¿v es virtual? " + v.isVirtual());

        // Atajo: Thread.startVirtualThread(tarea);
    }
}
```

```text
VirtualThread[#18,virtual-1]/runnable@ForkJoinPool-1-worker-1
Thread[#20,plataforma-1,5,main]
¿v es virtual? true
```

- `Thread.ofVirtual()` y `Thread.ofPlatform()` devuelven un constructor al que se le da nombre y luego se llama a `start(tarea)`, que **crea y arranca** a la vez.
- Al imprimir un hilo virtual se ve el **portador** que lo ejecuta: `ForkJoinPool-1-worker-1`.
- Los hilos virtuales son **siempre demonios**.

## 5.3 Diez mil tareas que esperan un segundo

```java
import java.time.Duration;
import java.util.concurrent.Executors;

public class Virtuales {
    public static void main(String[] args) {
        long ini = System.currentTimeMillis();
        try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 10_000; i++) {
                exec.submit(() -> {
                    Thread.sleep(Duration.ofSeconds(1));   // simula esperar a la red
                    return null;
                });
            }
        }   // al cerrar el try, espera a que acaben todas
        System.out.println("10.000 tareas en " + (System.currentTimeMillis() - ini) + " ms");
    }
}
```

En una prueba con JDK 21 tardó unos **1100 ms**: las 10.000 esperan a la vez.

- `Executors.newVirtualThreadPerTaskExecutor()` crea un **ejecutor**: un objeto al que se le entregan tareas con `submit()` y que se encarga de los hilos. Este crea un hilo virtual nuevo por cada tarea.
- La tarea devuelve `null` para que pueda lanzar la excepción de `sleep` sin `try-catch`.
- El ejecutor va en un **try-with-resources**: al cerrarse, espera a que terminen todas las tareas. No hacen falta los `join()`.

Si comparas 1000 tareas de 1 segundo con un **pool de 100 hilos de plataforma** (`Executors.newFixedThreadPool(100)`) y con hilos virtuales:

| Versión | Tiempo |
|---|---|
| 100 hilos de plataforma | ≈ 10 s: 1000 tareas ÷ 100 hilos = 10 tandas de 1 s |
| Hilos virtuales | ≈ 1 s: un hilo por tarea, todas esperan a la vez |

## Preguntas de repaso

1. ¿Qué es el hilo portador de un hilo virtual?
2. ¿Qué hace la JVM con un hilo virtual cuando este se queda esperando datos de la red?
3. Una tarea calcula números primos durante 1 segundo. ¿Ganas algo pasándola a hilos virtuales? ¿Por qué?
4. ¿Qué cambia en el código al pasar de un hilo de plataforma a uno virtual? ¿Qué se queda igual?
5. ¿Por qué el ejecutor de hilos virtuales no necesita `join()`?
