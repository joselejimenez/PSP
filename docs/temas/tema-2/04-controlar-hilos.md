# 4. Controlar hilos

Una vez arrancado un hilo, hay que poder **esperarlo**, **dormirlo**, **pedirle que pare** y decidir si la JVM debe esperarlo al salir.

## 4.1 `sleep` y `join`: dormir y esperar

| Método | Qué hace | Detalles |
|---|---|---|
| `Thread.sleep(ms)` | Duerme al hilo **que lo llama** durante ese tiempo. No gasta CPU. | Es **estático**: no duermes a otro hilo, solo a ti mismo. También existe `Thread.sleep(Duration.ofSeconds(1))`. |
| `t.join()` | El hilo que llama espera hasta que **t termine**. | Si `t` ya terminó, vuelve al instante. Puede esperar para siempre si `t` no termina nunca. |
| `t.join(ms)` | Espera **como mucho** ese tiempo y sigue. | Al volver no sabes si `t` terminó o si se agotó el tiempo: compruébalo con `t.isAlive()`. |

!!! warning "Pregunta trampa"
    `otroHilo.sleep(1000)` compila (con un aviso), pero duerme al hilo **actual**, no a `otroHilo`, porque `sleep` es estático.

Los tres métodos pueden lanzar **`InterruptedException`**: es la forma en que Java avisa de que alguien ha pedido a ese hilo que pare. Por eso en `main` ponemos `throws InterruptedException` y dentro de las lambdas, que no pueden declarar `throws`, usamos `try-catch`.

## 4.2 `interrupt()`: pedir a un hilo que pare

En Java **no se puede matar un hilo desde fuera**. Se le **pide** que pare, y el hilo colabora.

```java
public class Interrumpir {
    public static void main(String[] args) throws InterruptedException {
        Thread reloj = new Thread(() -> {
            int s = 0;
            try {
                while (true) {
                    System.out.println("Tic " + s++);
                    Thread.sleep(1000);
                }
            } catch (InterruptedException e) {
                System.out.println("Me han interrumpido: paro limpio");
            }
        });
        reloj.start();
        Thread.sleep(3500);
        reloj.interrupt();     // pide parar, no mata
        reloj.join();
    }
}
```

```text
Tic 0
Tic 1
Tic 2
Tic 3
Me han interrumpido: paro limpio
```

Cómo funciona `interrupt()`:

1. Pone a `true` una **marca de interrupción** del hilo.
2. Si el hilo está dormido o esperando (`sleep`, `join`, `wait`), se despierta en el acto con **`InterruptedException`**, y la marca **se borra**.
3. Si el hilo está calculando y no llama a ninguno de esos métodos, no pasa nada visible: tiene que comprobar él mismo la marca con `Thread.currentThread().isInterrupted()`.

Es un mecanismo **cooperativo**: el hilo decide cómo y cuándo parar, en un punto seguro, y puede cerrar ficheros y conexiones antes de terminar.

En el ejemplo, el `try` envuelve todo el `while`: al saltar la excepción, se sale del bucle y el hilo termina de forma ordenada.

!!! danger "Error típico: tragarse la excepción"
    ```java
    while (true) {
        try { Thread.sleep(100); } catch (InterruptedException e) { }   // ¡vacío!
    }
    ```
    El hilo captura la petición, la excepción borra la marca y el bucle sigue como si nada: **no para nunca**. Como mínimo, sal del bucle (`return`, `break`) o vuelve a marcar la interrupción con `Thread.currentThread().interrupt()`.

Si el hilo comprueba la marca en su bucle, la forma correcta queda así:

```java
Thread crono = new Thread(() -> {
    long ini = System.currentTimeMillis();
    while (!Thread.currentThread().isInterrupted()) {
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();   // la excepción borró la marca: la volvemos a poner
        }
    }
    System.out.printf("Tiempo: %.1f s%n", (System.currentTimeMillis() - ini) / 1000.0);
}, "Crono");
```

## 4.3 Hilos demonio

La JVM termina cuando acaban **todos los hilos normales**, aunque `main` ya haya terminado. A los hilos **demonio** (*daemon*) no los espera: cuando solo quedan demonios, la JVM sale y los corta en seco.

```java
public class Demonio {
    public static void main(String[] args) throws InterruptedException {
        Thread guardado = new Thread(() -> {
            while (true) {
                System.out.println("Autoguardado...");
                try {
                    Thread.sleep(300);
                } catch (InterruptedException e) {
                    return;
                }
            }
        });
        guardado.setDaemon(true);   // siempre antes de start()
        guardado.start();
        Thread.sleep(1000);
        System.out.println("Fin del main: la JVM no espera al demonio");
    }
}
```

Sin `setDaemon(true)`, este programa **no terminaría nunca**: el bucle infinito mantendría viva la JVM. Prueba a comentar esa línea.

- `setDaemon(true)` se llama **antes** de `start()`. Después lanza `IllegalThreadStateException`.
- Un hilo creado desde un demonio también es demonio.
- Sirven para tareas de fondo: autoguardado, limpieza, el recolector de basura de la propia JVM.
- Como se cortan sin avisar, un demonio **no debe hacer nada que tenga que quedar terminado**, como escribir el final de un fichero. Para eso, hilo normal y `join()`.

## Preguntas de repaso

1. ¿A qué hilo duerme `otroHilo.sleep(1000)`?
2. Llamas a `t.join(2000)` y vuelve. ¿Cómo sabes si `t` terminó o si se agotaron los 2 segundos?
3. Un hilo está en `sleep(5000)` y otro le llama a `interrupt()`. ¿Qué pasa?
4. ¿Por qué un `catch (InterruptedException e) { }` vacío dentro de un bucle impide que el hilo pare?
5. ¿Por qué es peligroso que un hilo demonio escriba en un fichero?
6. ¿Qué pasa si llamas a `setDaemon(true)` después de `start()`?
