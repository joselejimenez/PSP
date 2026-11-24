# 9. Lock: un cerrojo que se coge y se suelta a mano

`synchronized` coge y suelta el cerrojo **solo**: al entrar en el bloque o en el método, y al salir. Java tiene otra forma de hacer lo mismo en la que **tú** decides cuándo coger el cerrojo y cuándo soltarlo: la clase `ReentrantLock`, del paquete `java.util.concurrent.locks`.

## 9.1 El contador con `ReentrantLock`

```java
import java.util.concurrent.locks.ReentrantLock;

public class ContadorLock {
    static int cuenta = 0;
    static final ReentrantLock cerrojo = new ReentrantLock();   // un cerrojo para todos

    public static void main(String[] args) throws InterruptedException {
        Thread[] hilos = new Thread[4];
        for (int i = 0; i < 4; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    cerrojo.lock();             // coger el cerrojo
                    try {
                        cuenta++;               // sección crítica
                    } finally {
                        cerrojo.unlock();       // soltarlo SIEMPRE, aunque haya un error
                    }
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Esperado 400000, obtenido " + cuenta);
    }
}
```

```text
Esperado 400000, obtenido 400000
```

| Método | Qué hace |
|---|---|
| `cerrojo.lock()` | Coge el cerrojo. Si lo tiene otro hilo, **espera** hasta que lo suelte. |
| `cerrojo.unlock()` | Suelta el cerrojo y deja pasar al siguiente. |
| `cerrojo.tryLock()` | Intenta cogerlo. Si está libre, lo coge y devuelve `true`; si está ocupado, **no espera** y devuelve `false`. |

## 9.2 La regla de oro: `unlock()` siempre en un `finally`

Con `synchronized`, Java suelta el cerrojo él solo, aunque salte una excepción. Con `Lock`, **eres tú quien tiene que soltarlo**. Si una excepción salta entre `lock()` y `unlock()` y no lo has previsto, el cerrojo se queda cogido para siempre y todos los demás hilos se quedan esperando.

Por eso se escribe siempre así:

```java
cerrojo.lock();
try {
    // sección crítica
} finally {
    cerrojo.unlock();      // se ejecuta siempre: si todo va bien, si hay return y si salta una excepción
}
```

!!! warning "Errores típicos"
    - Olvidar el `unlock()`: el siguiente hilo se queda bloqueado para siempre.
    - Poner el `unlock()` al final del `try` en vez de en el `finally`: si salta una excepción, no se ejecuta.
    - Crear un `ReentrantLock` nuevo dentro de cada hilo: igual que con `synchronized`, todos tienen que usar **el mismo cerrojo**.

## 9.3 `tryLock()`: no esperar si está ocupado

Lo que `Lock` permite y `synchronized` no es **probar sin esperar**. En esta taquilla, si un cliente la ve ocupada, se va en lugar de hacer cola:

```java
import java.util.concurrent.locks.ReentrantLock;

public class Taquilla {
    static int entradas = 2;
    static final ReentrantLock cerrojo = new ReentrantLock();

    static void comprar(String quien) {
        if (cerrojo.tryLock()) {                // ¿está libre? si no, no espero
            try {
                if (entradas > 0) {
                    try {
                        Thread.sleep(200);      // la venta tarda un poco
                    } catch (InterruptedException e) {
                        return;
                    }
                    entradas--;
                    System.out.println(quien + " compra. Quedan " + entradas);
                } else {
                    System.out.println(quien + ": agotado");
                }
            } finally {
                cerrojo.unlock();
            }
        } else {
            System.out.println(quien + " ve la taquilla ocupada y se va");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        String[] clientes = {"Ana", "Luis", "Marta", "Pepe"};
        Thread[] hilos = new Thread[clientes.length];
        for (int i = 0; i < clientes.length; i++) {
            String nombre = clientes[i];
            hilos[i] = new Thread(() -> comprar(nombre));
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Entradas al final: " + entradas);
    }
}
```

```text
Pepe ve la taquilla ocupada y se va
Marta ve la taquilla ocupada y se va
Luis ve la taquilla ocupada y se va
Ana compra. Quedan 1
Entradas al final: 1
```

El primero que llega coge el cerrojo y tarda 200 ms en comprar. Los otros tres prueban con `tryLock()`, ven que está ocupado y se van sin esperar. Quién llega primero cambia en cada ejecución.

## 9.4 ¿`synchronized` o `Lock`?

| | `synchronized` | `ReentrantLock` |
|---|---|---|
| Coger y soltar | Automático | A mano: `lock()` y `unlock()` en un `finally` |
| Si salta una excepción | Se suelta solo | Se suelta si está en el `finally` |
| Probar sin esperar | No se puede | `tryLock()` |
| Cuándo usarlo | Casi siempre: es más corto y no se te puede olvidar soltarlo | Cuando necesitas `tryLock()` u otras opciones avanzadas |

## Preguntas de repaso

1. ¿Qué diferencia hay entre `lock()` y `tryLock()`?
2. ¿Por qué el `unlock()` va siempre en un `finally`?
3. ¿Qué pasa si un hilo hace `lock()` y nunca hace `unlock()`?
4. En la taquilla, ¿por qué quedan entradas sin vender aunque hay cuatro clientes?
5. Si `synchronized` hace lo mismo, ¿cuándo usarías un `ReentrantLock`?
