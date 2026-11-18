# Taller práctico · Soluciones

Soluciones de los seis ejercicios de la [Parte 2 del taller](taller.md#parte-2-por-tu-cuenta). Los programas son completos y están probados con JDK 21, y las salidas son de ejecuciones reales. Tus números serán otros, pero el comportamiento debe ser el mismo.

## C1 · El termostato

1. Cada ejecución da un resultado distinto y casi nunca 20. Por ejemplo: −35226, −5487 y −15569.
2. Así se pierde una subida:

    | t | Calefacción (`++`) | Aire (`--`) | `temperatura` |
    |---|---|---|---|
    | 1 | lee 20 | | 20 |
    | 2 | | lee 20 | 20 |
    | 3 | suma: 21 | | 20 |
    | 4 | | resta: 19 | 20 |
    | 5 | escribe 21 | | 21 |
    | 6 | | escribe 19 | **19**: la subida se ha perdido |

3. El recurso compartido es `temperatura`. La sección crítica es `temperatura++` en un hilo y `temperatura--` en el otro: **las dos** deben protegerse con el mismo cerrojo.
4. Con dos métodos `static synchronized`, los dos usan el cerrojo de la clase:

```java
public class TermostatoSync {
    static int temperatura = 20;

    static synchronized void subir() { temperatura++; }
    static synchronized void bajar() { temperatura--; }

    public static void main(String[] args) throws InterruptedException {
        Thread calefaccion = new Thread(() -> {
            for (int i = 0; i < 100_000; i++) subir();
        });
        Thread aire = new Thread(() -> {
            for (int i = 0; i < 100_000; i++) bajar();
        });
        calefaccion.start();
        aire.start();
        calefaccion.join();
        aire.join();
        System.out.println("Esperado 20, obtenido " + temperatura);
    }
}
```

```text
Esperado 20, obtenido 20
```

!!! warning "Error típico"
    Proteger solo la subida, o usar un cerrojo distinto para cada operación, no sirve: la subida y la bajada tocan la misma variable y deben excluirse entre sí.

## C2 · La última entrada

1. Los dos compran:

    | t | Ana | Luis | `asientos` |
    |---|---|---|---|
    | 1 | línea 1: ve 1 > 0 | | 1 |
    | 2 | | línea 1: ve 1 > 0 | 1 |
    | 3 | línea 2: resta | | 0 |
    | 4 | | línea 2: resta | **−1**: dos entradas vendidas |

2. Todo va bien si Ana hace las líneas 1 y 2 antes de que Luis haga la línea 1: Luis ve `asientos = 0` y recibe «agotado».
3. La sección crítica va desde el `if` (línea 1) hasta la resta (línea 2), las dos incluidas. Si solo se protege la resta, los dos pueden pasar el `if` cuando todavía quedaba una entrada.
4. No falla siempre. En tres ejecuciones, los asientos acabaron en −1, 0 y −1. Depende de si el planificador cambia de hilo entre la comprobación y la resta; el `println` que hay en medio lo hace más probable.

```java
public class Entradas {
    static int asientos = 1;                                  // queda una entrada

    static void comprar(String quien) {
        if (asientos > 0) {                                   // 1
            System.out.println(quien + " ve que queda una entrada");
            asientos--;                                       // 2
            System.out.println(quien + " compra. Quedan " + asientos);
        } else {
            System.out.println(quien + ": agotado");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread ana = new Thread(() -> comprar("Ana"));
        Thread luis = new Thread(() -> comprar("Luis"));
        ana.start();
        luis.start();
        ana.join();
        luis.join();
        System.out.println("Asientos al final: " + asientos);
    }
}
```

Se arregla igual que el aparcamiento: `static synchronized void comprar(String quien)`.

## S1 · La urna de votación

1. No sale 100.000 y A + B no cuadra con el total:

    ```text
    Esperado total=100000 → A=47160 B=47913 total=91255 (NO cuadra)
    ```

2. Hay que proteger `votar()` y `resultados()`:

```java
import java.util.concurrent.ThreadLocalRandom;

public class VotacionSync {

    static class Urna {
        private int votosA = 0;
        private int votosB = 0;
        private int total = 0;

        public synchronized void votar(char candidato) {
            if (candidato == 'A') {
                votosA++;
            } else {
                votosB++;
            }
            total++;
        }

        public synchronized String resultados() {
            return "A=" + votosA + " B=" + votosB + " total=" + total
                    + (votosA + votosB == total ? " (cuadra)" : " (NO cuadra)");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Urna urna = new Urna();                               // una sola urna para todos
        Thread[] mesas = new Thread[4];
        for (int i = 0; i < mesas.length; i++) {
            mesas[i] = new Thread(() -> {
                for (int j = 0; j < 25_000; j++) {
                    urna.votar(ThreadLocalRandom.current().nextBoolean() ? 'A' : 'B');
                }
            });
            mesas[i].start();
        }
        for (Thread m : mesas) {
            m.join();
        }
        System.out.println("Esperado total=100000 → " + urna.resultados());
    }
}
```

```text
Esperado total=100000 → A=49961 B=50039 total=100000 (cuadra)
Esperado total=100000 → A=50231 B=49769 total=100000 (cuadra)
```

- `votar()` toca dos variables que deben cambiar juntas: el contador del candidato y el total.
- `resultados()` también va `synchronized`: si se llamara mientras otra mesa vota, podría leer el contador de A ya sumado y el total todavía sin sumar, y no cuadraría.

3. Los métodos `synchronized` normales usan como cerrojo **`this`**: el propio objeto `urna`. Por eso las cuatro mesas deben compartir la misma urna. Si cada mesa tuviera la suya, cada una tendría su cerrojo, y además contarían en sitios distintos.

## S2 · El marcador que no protege

1. Sale menos de 400.000: por ejemplo, 379582, 388764 y 385449.
2. `sumar()` es `synchronized` sobre **`this`**, pero cada jugador crea **su propio** objeto `Puntos`. Hay cuatro objetos y, por tanto, cuatro cerrojos distintos: nadie espera a nadie. En cambio, `puntos` es `static`, así que los cuatro objetos comparten **la misma** variable. Cerrojos distintos para un dato compartido no protegen nada.
3. Hay dos formas de arreglarlo:
    - **Hacer el método `static synchronized`.** El cerrojo pasa a ser la clase, uno solo para todos. Es la versión de abajo.
    - **Compartir un único objeto.** Se crea un solo `Puntos` antes del bucle y todos los jugadores llaman a `sumar()` sobre él. Así `this` es el mismo para todos.

```java
public class MarcadorSync {

    static class Puntos {
        private static int puntos = 0;                        // static: compartido por TODOS los objetos

        public static synchronized void sumar() {             // cerrojo: la clase, uno para todos
            puntos++;
        }

        public static int getPuntos() {
            return puntos;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] jugadores = new Thread[4];
        for (int i = 0; i < jugadores.length; i++) {
            jugadores[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    Puntos.sumar();
                }
            });
            jugadores[i].start();
        }
        for (Thread j : jugadores) {
            j.join();
        }
        System.out.println("Esperado 400000, obtenido " + Puntos.getPuntos());
    }
}
```

```text
Esperado 400000, obtenido 400000
```

## A1 · Los tickets de la cola

1. Con `AtomicInteger` nunca hay repetidos:

    ```text
    Tickets repartidos: 100000 · distintos: 100000 · repetidos: 0
    ```

2. Con `int` y `siguiente++` aparecen tickets repetidos, y el número cambia en cada ejecución:

    ```text
    Tickets repartidos: 100000 · distintos: 89519 · repetidos: 10481
    Tickets repartidos: 100000 · distintos: 95858 · repetidos: 4142
    ```

    Dos taquillas leen el mismo valor antes de que ninguna lo incremente, y dan el mismo número.

3. `getAndIncrement()` lee el valor y lo incrementa en **un solo paso indivisible**. Ninguna otra taquilla puede leer el mismo valor en medio.
4. `getAndIncrement()` devuelve el valor **antes** de sumar (como `x++`) e `incrementAndGet()` el de **después** (como `++x`). Empezando en 0, `getAndIncrement()` da el 0 como primer ticket; `incrementAndGet()` daría el 1.

## A2 · Estadísticas de descargas

```java
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class Estadisticas {
    static AtomicInteger ficheros = new AtomicInteger();
    static AtomicLong megas = new AtomicLong();

    public static void main(String[] args) throws InterruptedException {
        int hilos = 4;
        long[] comprobacion = new long[hilos];                // lo que suma cada hilo por su cuenta
        Thread[] t = new Thread[hilos];
        for (int i = 0; i < hilos; i++) {
            int id = i;
            t[i] = new Thread(() -> {
                long mios = 0;
                for (int j = 0; j < 250; j++) {
                    int tam = ThreadLocalRandom.current().nextInt(1, 101);   // MB del fichero
                    ficheros.incrementAndGet();
                    megas.addAndGet(tam);
                    mios += tam;
                }
                comprobacion[id] = mios;
            });
            t[i].start();
        }
        for (Thread h : t) {
            h.join();
        }
        long suma = 0;
        for (long c : comprobacion) suma += c;
        System.out.println("Ficheros: " + ficheros.get() + " (esperado 1000)");
        System.out.println("Megas: " + megas.get() + " · suma de cada hilo: " + suma
                + (megas.get() == suma ? " (coincide)" : " (NO coincide)"));
    }
}
```

```text
Ficheros: 1000 (esperado 1000)
Megas: 49920 · suma de cada hilo: 49920 (coincide)
```

- Cada hilo suma sus megas en `mios`, una variable **local**, y la guarda en **su** posición de `comprobacion`. Así se puede comprobar el resultado sin compartir nada.
- **Pregunta 5:** con muchas descargas grandes, el total de megas puede pasar del máximo de un `int` (2.147.483.647). Un `long` llega mucho más lejos.
- **Pregunta 6:** con tres atómicas, cada contador por separado acabaría bien, pero `votar()` dejaría de ser una operación única. Si `resultados()` se llama mientras se vota, puede leer el contador de A ya sumado y el total todavía sin sumar, y no cuadraría. Cuando varias variables deben cambiar juntas, hace falta `synchronized`.
