# 2. Crear hilos en Java

Para crear hilos en Java se usan la clase `Thread` y la interfaz `Runnable`, del paquete `java.lang`: no hay que importar nada.

## 2.1 Tres formas de decir qué hace un hilo

Un hilo necesita saber **qué hacer**. Eso se escribe en un método `run()`. Hay tres formas de dárselo:

```java
public class TresFormas {

    // 1. Heredar de Thread y sobrescribir run()
    static class Cocinero extends Thread {
        @Override
        public void run() {
            System.out.println("Cocinero: " + getName());
        }
    }

    // 2. Implementar la interfaz Runnable
    static class Pinche implements Runnable {
        @Override
        public void run() {
            System.out.println("Pinche: " + Thread.currentThread().getName());
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread a = new Cocinero();
        Thread b = new Thread(new Pinche());
        // 3. Lambda: Runnable tiene un solo método, así que se puede escribir como lambda
        Thread c = new Thread(() -> System.out.println("Lambda: " + Thread.currentThread().getName()));

        a.start();
        b.start();
        c.start();
        a.join();
        b.join();
        c.join();
    }
}
```

| Forma | Ventajas | Inconvenientes |
|---|---|---|
| Heredar de `Thread` | Es la más directa. | Java solo permite heredar de una clase, y la gastas en esto. Mezcla la tarea con el hilo. |
| Implementar `Runnable` | Separa la **tarea** del **hilo** que la ejecuta. La misma tarea puede ejecutarse en varios hilos o pasarse a un ejecutor. | Hay que escribir una clase. |
| **Lambda** | Lo mismo que `Runnable`, en una línea. Es lo más habitual hoy. | Para tareas largas, una clase con nombre se lee mejor. |

En los tres casos el trabajo va en `run()` y el hilo arranca con **`start()`**.

!!! warning "Crear el objeto no lanza nada"
    `new Thread(...)` solo crea el objeto. El hilo **no empieza a ejecutarse** hasta que llamas a `start()`.

Ejecuta `TresFormas` varias veces. El orden en que salen «Cocinero», «Pinche» y «Lambda» **cambia**: lo decide el planificador del sistema operativo, no nosotros. Esto se llama **indeterminismo**, y es normal en programas con hilos.

## 2.2 El patrón básico: crear, arrancar y esperar

```java
public class HolaHilos {
    public static void main(String[] args) throws InterruptedException {
        Runnable saludo = () -> System.out.println("Hola desde " + Thread.currentThread().getName());

        Thread t1 = new Thread(saludo, "T1");   // tarea + nombre del hilo
        Thread t2 = new Thread(saludo, "T2");

        t1.start();                             // ahora hay tres hilos: main, T1 y T2
        t2.start();

        t1.join();                              // main espera a que T1 termine
        t2.join();                              // y a que T2 termine
        System.out.println("Fin del main");
    }
}
```

Una salida posible:

```text
Hola desde T2
Hola desde T1
Fin del main
```

1. **`Runnable saludo`** es la tarea. La misma tarea la ejecutan dos hilos distintos.
2. **`new Thread(saludo, "T1")`**: el segundo parámetro es el **nombre** del hilo. Poner nombres ayuda mucho a depurar. Si no se pone, Java los llama `Thread-0`, `Thread-1`…
3. **`start()`** pide a la JVM, y esta al sistema operativo, una nueva línea de ejecución.
4. **`join()`** hace que el hilo que lo llama, aquí `main`, espere hasta que ese hilo termine. Puede lanzar `InterruptedException`; por eso el `throws` en `main` (lo explicamos en el [apartado 4](04-controlar-hilos.md)).
5. **`Thread.currentThread()`** devuelve el hilo que está ejecutando esa línea. Dentro de la tarea es `T1` o `T2`; en `main` sería `main`.

Si quitas los dos `join()`, «Fin del main» puede salir **antes** que los saludos. Aun así, el programa no termina hasta que acaban T1 y T2: la JVM espera a todos los hilos normales.

## 2.3 El error clásico: `run()` en vez de `start()`

```java
Thread t = new Thread(() -> {
    String quien = Thread.currentThread().getName();
    System.out.println("Me ejecuta: " + quien);
}, "Worker");

t.run();     // NO crea hilo: lo ejecuta main, como un método normal
t.start();   // SÍ crea un hilo nuevo, que ejecuta run()
```

```text
Me ejecuta: main
Me ejecuta: Worker
```

| Método | Qué hace |
|---|---|
| `run()` | Contiene **lo que hace** el hilo. Si lo llamas tú, se ejecuta en el hilo que lo llama, de forma secuencial. **Nunca lo llames directamente.** |
| `start()` | Crea un hilo nuevo, y es ese hilo el que llama a `run()`. Solo se puede llamar **una vez** por objeto `Thread`: la segunda lanza `IllegalThreadStateException`. Para repetir la tarea, crea otro `Thread` con el mismo `Runnable`. |

!!! tip "Cómo detectarlo"
    Si imprimes `Thread.currentThread().getName()` dentro de la tarea y sale `main`, has llamado a `run()`.

## 2.4 Muchos hilos: un bucle para arrancar y otro para esperar

Casi nunca se crean los hilos de uno en uno. El patrón es un bucle que crea y arranca, y **después** otro bucle que espera:

```java
import java.util.ArrayList;
import java.util.List;

public class VariosHilos {
    public static void main(String[] args) throws InterruptedException {
        List<Thread> hilos = new ArrayList<>();

        for (int i = 0; i < 8; i++) {
            int n = i;                          // la lambda necesita una variable que no cambie
            Thread t = new Thread(() -> System.out.println("Hola desde H" + n), "H" + n);
            hilos.add(t);
            t.start();
        }

        for (Thread t : hilos) {
            t.join();                           // esperar a todos, después
        }
        System.out.println("Todos han terminado");
    }
}
```

- La **lista** guarda las referencias a los hilos. Sin ellas no podrías hacer `join()` después. También vale un array `Thread[]`.
- **`int n = i`**: una lambda solo puede usar variables locales que no cambien después (*efectivamente finales*). `i` cambia en cada vuelta, así que el compilador no deja usarla dentro de la lambda. Copiándola en `n`, que es una variable nueva en cada vuelta, se soluciona.
- En el segundo bucle da igual el orden en que se espere: si `H3` termina antes que `H0`, su `join()` vuelve al momento.

!!! warning "Trampa: `join()` dentro del bucle que arranca"
    Si escribes `t.start(); t.join();` en el mismo bucle, `main` arranca `H0`, espera a que termine, arranca `H1`, espera… Funciona, pero has perdido toda la concurrencia: vuelve a ser secuencial.

## Preguntas de repaso

1. ¿Por qué es preferible usar `Runnable` o una lambda en lugar de heredar de `Thread`?
2. Llamas a `t.run()` dentro de un bucle de 10 vueltas. ¿Cuántos hilos se crean?
3. ¿Qué ocurre si llamas dos veces a `start()` sobre el mismo objeto `Thread`?
4. ¿Por qué no se puede usar la variable `i` del bucle dentro de la lambda?
5. Tres hilos duermen 1 segundo cada uno. ¿Cuánto tarda el programa si haces `start(); join();` en el mismo bucle? ¿Y con dos bucles?
