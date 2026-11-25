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

### Esperar como mucho un tiempo

`tryLock` también admite un tiempo máximo de espera. Aquí un hilo tiene el cerrojo 3 segundos y el `main` solo está dispuesto a esperar 2:

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class Espera {
    static final ReentrantLock cerrojo = new ReentrantLock(true);   // true: respeta el orden de llegada

    public static void main(String[] args) throws InterruptedException {
        Thread ocupa = new Thread(() -> {
            cerrojo.lock();
            try {
                Thread.sleep(3000);                 // tiene el cerrojo 3 segundos
            } catch (InterruptedException e) {
                return;
            } finally {
                cerrojo.unlock();
            }
        });
        ocupa.start();
        Thread.sleep(100);
        if (cerrojo.tryLock(2, TimeUnit.SECONDS)) { // espera como mucho 2 segundos
            try {
                System.out.println("Conseguido");
            } finally {
                cerrojo.unlock();
            }
        } else {
            System.out.println("Ocupado más de 2 segundos: inténtalo más tarde");
        }
        ocupa.join();
    }
}
```

```text
Ocupado más de 2 segundos: inténtalo más tarde
```

`tryLock(2, TimeUnit.SECONDS)` espera hasta 2 segundos: si en ese tiempo consigue el cerrojo, devuelve `true`; si no, devuelve `false`. Como puede esperar, lanza `InterruptedException`, igual que `sleep`.

El `true` de `new ReentrantLock(true)` hace que el cerrojo respete el **orden de llegada**: cuando se suelta, se lo da al hilo que lleva más tiempo esperando. Así ningún hilo se queda siempre sin turno, que es la **inanición** que verás en el [apartado 11](11-interbloqueo.md#114-inanicion). Por defecto no se respeta el orden, porque así va algo más rápido.

## 9.4 ¿`synchronized` o `Lock`?

Para todo lo que hemos hecho hasta ahora (el contador, el cajero, el aparcamiento, la hucha), **`synchronized` es mejor**: hace lo mismo, es más corto y no se te puede olvidar soltar el cerrojo.

`Lock` solo merece la pena cuando necesitas algo que `synchronized` no sabe hacer. Con `synchronized`, si el cerrojo está ocupado, el hilo **espera sin límite** y no puede rendirse.

| Necesitas… | Con `Lock` | Ejemplo |
|---|---|---|
| No esperar si está ocupado | `tryLock()` | La taquilla: si está ocupada, el cliente se va |
| Esperar como mucho un tiempo | `tryLock(2, TimeUnit.SECONDS)` | Un servidor que, si no consigue un recurso, responde «inténtalo más tarde» en vez de quedarse colgado |
| Respetar el orden de llegada | `new ReentrantLock(true)` | Que ningún hilo se quede siempre sin turno |
| Escapar de un interbloqueo | `tryLock()` sobre el segundo cerrojo | Si no consigo el segundo cerrojo, suelto el primero y lo vuelvo a intentar |

!!! tip "Regla"
    Si con `synchronized` te vale, usa `synchronized`. Usa `Lock` cuando necesites **no esperar**, **esperar con un límite** o **respetar el orden de llegada**.

## Preguntas de repaso

1. ¿Qué diferencia hay entre `lock()` y `tryLock()`?
2. ¿Por qué el `unlock()` va siempre en un `finally`?
3. ¿Qué pasa si un hilo hace `lock()` y nunca hace `unlock()`?
4. En la taquilla, ¿por qué quedan entradas sin vender aunque hay cuatro clientes?
5. Si `synchronized` hace lo mismo y es más seguro, ¿cuándo usarías un `ReentrantLock`? Pon un ejemplo.
6. ¿Qué hace el `true` de `new ReentrantLock(true)`? ¿Con qué problema del apartado 11 tiene que ver?

## Ejercicio autoguiado: el cajero con `Lock`

Vas a construir el programa en cuatro pasos. En cada paso tienes **qué hacer**, **qué debería salir** y, plegada, la **solución**. Intenta cada paso antes de abrirla.

Ana y Luis comparten una cuenta con 100 €. Los dos van a la vez a un cajero y cada uno intenta sacar 80 €.

### Paso 1 · Sin proteger

Escribe la clase `CajeroPaso1` con:

- un `static int saldo = 100;`
- un método `static void retirar(String quien, int cantidad)` que, **si hay saldo suficiente**, espere 10 ms (el cajero cuenta los billetes), reste la cantidad e imprima el saldo. Si no hay saldo, imprime «saldo insuficiente».
- un `main` que lance dos hilos, `retirar("Ana", 80)` y `retirar("Luis", 80)`, espere a los dos con `join()` e imprima el saldo final.

Salida que verás (casi siempre):

```text
Ana retira 80. Saldo: -60
Luis retira 80. Saldo: -60
Saldo final: -60
```

**Piensa:** ¿por qué los dos pasan el `if`? (Los dos comprueban el saldo antes de que el otro lo reste: es una condición de carrera.)

??? success "Solución del paso 1"
    ```java
    public class CajeroPaso1 {
        static int saldo = 100;

        static void retirar(String quien, int cantidad) {
            if (saldo >= cantidad) {
                pausa(10);                                   // el cajero cuenta los billetes
                saldo -= cantidad;
                System.out.println(quien + " retira " + cantidad + ". Saldo: " + saldo);
            } else {
                System.out.println(quien + ": saldo insuficiente");
            }
        }

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread ana = new Thread(() -> retirar("Ana", 80));
            Thread luis = new Thread(() -> retirar("Luis", 80));
            ana.start();
            luis.start();
            ana.join();
            luis.join();
            System.out.println("Saldo final: " + saldo);
        }
    }
    ```

### Paso 2 · Protegerlo con `ReentrantLock`

Copia la clase como `CajeroPaso2` y protege **todo** el método `retirar` (la comprobación y la resta) con un `ReentrantLock` compartido. Recuerda el patrón: `lock()`, `try`, y `unlock()` en el `finally`.

Salida esperada, siempre:

```text
Ana retira 80. Saldo: 20
Luis: saldo insuficiente
Saldo final: 20
```

(Puede ser Luis quien retire y Ana quien se quede sin saldo.)

??? success "Solución del paso 2"
    ```java
    import java.util.concurrent.locks.ReentrantLock;

    public class CajeroPaso2 {
        static int saldo = 100;
        static final ReentrantLock cerrojo = new ReentrantLock();

        static void retirar(String quien, int cantidad) {
            cerrojo.lock();
            try {
                if (saldo >= cantidad) {
                    pausa(10);
                    saldo -= cantidad;
                    System.out.println(quien + " retira " + cantidad + ". Saldo: " + saldo);
                } else {
                    System.out.println(quien + ": saldo insuficiente");
                }
            } finally {
                cerrojo.unlock();
            }
        }

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread ana = new Thread(() -> retirar("Ana", 80));
            Thread luis = new Thread(() -> retirar("Luis", 80));
            ana.start();
            luis.start();
            ana.join();
            luis.join();
            System.out.println("Saldo final: " + saldo);
        }
    }
    ```

### Paso 3 · Si el cajero está ocupado, me voy

Copia la clase como `CajeroPaso3`. Cambia `lock()` por `tryLock()`: si el cajero está ocupado, el cliente imprime «cajero ocupado, vuelve más tarde» y **no espera**.

Ojo: el `unlock()` solo se hace si `tryLock()` devolvió `true`.

Salida esperada:

```text
Luis: cajero ocupado, vuelve más tarde
Ana retira 80. Saldo: 20
Saldo final: 20
```

**Piensa:** ahora el que llega segundo ni siquiera ve «saldo insuficiente». ¿Por qué?

??? success "Solución del paso 3"
    ```java
    import java.util.concurrent.locks.ReentrantLock;

    public class CajeroPaso3 {
        static int saldo = 100;
        static final ReentrantLock cerrojo = new ReentrantLock();

        static void retirar(String quien, int cantidad) {
            if (cerrojo.tryLock()) {                         // si está ocupado, no espero
                try {
                    if (saldo >= cantidad) {
                        pausa(10);
                        saldo -= cantidad;
                        System.out.println(quien + " retira " + cantidad + ". Saldo: " + saldo);
                    } else {
                        System.out.println(quien + ": saldo insuficiente");
                    }
                } finally {
                    cerrojo.unlock();
                }
            } else {
                System.out.println(quien + ": cajero ocupado, vuelve más tarde");
            }
        }

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread ana = new Thread(() -> retirar("Ana", 80));
            Thread luis = new Thread(() -> retirar("Luis", 80));
            ana.start();
            luis.start();
            ana.join();
            luis.join();
            System.out.println("Saldo final: " + saldo);
        }
    }
    ```

### Paso 4 · Esperar como mucho 1 segundo

Copia la clase como `CajeroPaso4` y usa `tryLock(1, TimeUnit.SECONDS)`. Como puede esperar, lanza `InterruptedException`: rodéalo con un `try-catch`.

Salida esperada:

```text
Ana retira 80. Saldo: 20
Luis: saldo insuficiente
Saldo final: 20
```

**Piensa:** ¿por qué vuelve a salir lo mismo que en el paso 2? (El primero solo tarda 10 ms, mucho menos de 1 segundo, así que el segundo espera y entra.) Cambia la pausa de 10 a 1500 ms y vuelve a ejecutar: ¿qué ves ahora?

??? success "Solución del paso 4"
    ```java
    import java.util.concurrent.TimeUnit;
    import java.util.concurrent.locks.ReentrantLock;

    public class CajeroPaso4 {
        static int saldo = 100;
        static final ReentrantLock cerrojo = new ReentrantLock();

        static void retirar(String quien, int cantidad) {
            try {
                if (cerrojo.tryLock(1, TimeUnit.SECONDS)) {  // espero como mucho 1 segundo
                    try {
                        if (saldo >= cantidad) {
                            pausa(10);
                            saldo -= cantidad;
                            System.out.println(quien + " retira " + cantidad + ". Saldo: " + saldo);
                        } else {
                            System.out.println(quien + ": saldo insuficiente");
                        }
                    } finally {
                        cerrojo.unlock();
                    }
                } else {
                    System.out.println(quien + ": cajero ocupado más de 1 segundo, vuelve más tarde");
                }
            } catch (InterruptedException e) {
                System.out.println(quien + ": interrumpido mientras esperaba");
            }
        }

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread ana = new Thread(() -> retirar("Ana", 80));
            Thread luis = new Thread(() -> retirar("Luis", 80));
            ana.start();
            luis.start();
            ana.join();
            luis.join();
            System.out.println("Saldo final: " + saldo);
        }
    }
    ```

    Con una pausa de 1500 ms, el segundo cliente espera 1 segundo, no consigue el cerrojo e imprime «cajero ocupado más de 1 segundo, vuelve más tarde».
