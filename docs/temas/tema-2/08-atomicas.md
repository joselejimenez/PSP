# 8. Clases atómicas

Si el problema era que `cuenta++` son tres pasos, la otra solución es usar una operación que los haga **de una sola vez**, sin que ningún otro hilo pueda colarse en medio. Eso son las **clases atómicas** del paquete `java.util.concurrent.atomic`.

## 8.1 `AtomicInteger`

```java
import java.util.concurrent.atomic.AtomicInteger;

public class ContadorAtomico {
    static AtomicInteger cuenta = new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        Thread[] hilos = new Thread[4];
        for (int i = 0; i < 4; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    cuenta.incrementAndGet();            // en vez de cuenta++
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Esperado 400000, obtenido " + cuenta.get());   // siempre 400000
    }
}
```

Una operación **atómica** es indivisible: ningún otro hilo puede verla a medias. `incrementAndGet()` lee, suma y escribe como un único paso, así que el intercalado que perdía incrementos ya no puede ocurrir.

- `AtomicInteger` es un objeto que guarda un `int`. No se usa con `++`, sino con sus métodos.
- **No usa cerrojos**: el procesador tiene instrucciones especiales que hacen la operación de golpe. Ningún hilo se queda BLOCKED.

| Método | Qué hace |
|---|---|
| `get()` / `set(v)` | Leer / escribir el valor |
| `incrementAndGet()` | Suma 1 y devuelve el valor **nuevo** (como `++x`) |
| `getAndIncrement()` | Devuelve el valor **antiguo** y luego suma 1 (como `x++`) |
| `decrementAndGet()` | Resta 1 y devuelve el nuevo |
| `addAndGet(n)` | Suma `n` y devuelve el nuevo |

Si no usas el valor devuelto, da igual `incrementAndGet()` que `getAndIncrement()`. Hay también `AtomicLong`, `AtomicBoolean` y `AtomicReference`.

## 8.2 Ejemplo: contar las descargas

En el gestor de la [práctica guiada](practica-guiada.md), con el límite de 3 segundos, se pueden contar las descargas completadas y canceladas con dos contadores atómicos compartidos:

```java
static final AtomicInteger completadas = new AtomicInteger();
static final AtomicInteger canceladas = new AtomicInteger();

static void descargar(String nombre, int seg) {
    String hilo = Thread.currentThread().getName();
    try {
        Thread.sleep(seg * 1000L);
        System.out.printf("[%s] terminado %s%n", hilo, nombre);
        completadas.incrementAndGet();
    } catch (InterruptedException e) {
        System.out.printf("[%s] CANCELADO %s%n", hilo, nombre);
        canceladas.incrementAndGet();
    }
}

// en el main, después del último bucle de join():
System.out.println("Completadas: " + completadas.get() + " · Canceladas: " + canceladas.get());
```

```text
Completadas: 4 · Canceladas: 1
```

- Los contadores son `static`: uno de cada para todo el programa. Si fueran variables locales de `descargar()`, cada llamada tendría el suyo y siempre valdrían 1.
- Se imprimen **después** del último `join()`, cuando ya no queda ningún hilo trabajando.
- Con solo cinco descargas, un `int` normal casi seguro no habría fallado, porque los incrementos están muy separados en el tiempo. Pero **no está garantizado**, y con miles de descargas fallaría.

## 8.3 ¿`synchronized` o clase atómica?

| Situación | Usa | Por qué |
|---|---|---|
| Un contador | `AtomicInteger` | Una sola variable y una sola operación. Más corto y no bloquea. |
| El cajero (comprobar y actuar) | `synchronized` | Comprobar el saldo y restar son dos pasos que deben ir juntos. |
| Varias variables que cambian a la vez | `synchronized` | Por ejemplo, mover dinero entre dos cuentas: nadie debe ver el dinero restado de una y todavía sin sumar en la otra. |
| Varios hilos que solo leen | Nada | Leer a la vez es seguro. |
| Cada hilo con sus propios datos | Nada | No hay nada compartido. |

Las clases atómicas protegen **una operación sobre una variable**. En cuanto la sección crítica tiene varios pasos o varias variables, hace falta un cerrojo.

!!! tip "La mejor sincronización es no necesitarla"
    Si puedes evitar compartir el dato, evítalo. Por ejemplo, que cada hilo cuente en una variable local y, al final, se sumen los resultados de todos. No hace falta ninguna sincronización mientras trabajan, y suele ser lo más rápido.

## Preguntas de repaso

1. ¿Qué significa que una operación sea atómica?
2. ¿Qué diferencia hay entre `incrementAndGet()` y `getAndIncrement()`?
3. ¿Por qué un hilo nunca queda en estado BLOCKED al usar `AtomicInteger`?
4. ¿Podrías arreglar el cajero haciendo que `saldo` sea un `AtomicInteger` y usando `addAndGet(-cantidad)`? ¿Por qué?
5. Tienes que contar cuántos clientes ha atendido un servidor con muchos hilos. ¿Qué usarías?
