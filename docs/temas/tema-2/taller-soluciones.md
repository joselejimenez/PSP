# Taller práctico · Soluciones

Soluciones de los ejercicios de la [Parte 2](taller.md#parte-2-por-tu-cuenta) y de la [Parte 3](taller.md#parte-3-desde-cero) del taller. Los programas son completos y están probados con JDK 21, y las salidas son de ejecuciones reales. Tus números serán otros, pero el comportamiento debe ser el mismo.

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
2. Cada jugador crea **su propio** objeto `Puntos`, porque `new Puntos()` está dentro del hilo. Cada objeto tiene su propio vigilante: con cuatro objetos hay cuatro vigilantes, y ninguno hace esperar a los jugadores de los otros. Pero los cuatro suman en el mismo marcador, así que los incrementos se pierden igual que sin `synchronized`.
3. Se crea **un solo objeto `Puntos` antes del bucle** y los cuatro jugadores lo usan. Así hay un único vigilante y los jugadores suman de uno en uno:

```java
public class MarcadorCompartido {

    static class Puntos {
        private static int puntos = 0;

        public synchronized void sumar() {
            puntos++;
        }

        public static int getPuntos() {
            return puntos;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Puntos p = new Puntos();                              // UN solo objeto, creado fuera de los hilos
        Thread[] jugadores = new Thread[4];
        for (int i = 0; i < jugadores.length; i++) {
            jugadores[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    p.sumar();                                // los cuatro usan el mismo objeto
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

!!! note "Para saber más"
    Otra forma de arreglarlo es escribir `public static synchronized void sumar()` y llamar a `Puntos.sumar()`. Con `static`, el vigilante es de la clase y no de cada objeto, así que hay uno solo aunque se creen varios objetos.

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

## R1 · Los tornos del metro

Versión sin protección:

```java
public class Metro {
    static int pasajeros = 0;                           // personas dentro de la estación

    public static void main(String[] args) throws InterruptedException {
        Thread entrada1 = new Thread(() -> {
            for (int i = 0; i < 50_000; i++) pasajeros++;
        });
        Thread entrada2 = new Thread(() -> {
            for (int i = 0; i < 50_000; i++) pasajeros++;
        });
        Thread salida = new Thread(() -> {
            for (int i = 0; i < 30_000; i++) pasajeros--;
        });
        entrada1.start();
        entrada2.start();
        salida.start();
        entrada1.join();
        entrada2.join();
        salida.join();
        System.out.println("Esperado 70000, obtenido " + pasajeros);
    }
}
```

1. El programa es el de arriba: tres hilos que suman o restan sobre `pasajeros` sin ninguna protección.
2. Cada ejecución da un número distinto y casi nunca 70.000. Por ejemplo: 69911, 36888 y 31662.
3. Se pierde una entrada:

    | t | Entrada 1 (`++`) | Entrada 2 (`++`) | `pasajeros` |
    |---|---|---|---|
    | 1 | lee 500 | | 500 |
    | 2 | | lee 500 | 500 |
    | 3 | suma: 501 | | 500 |
    | 4 | | suma: 501 | 500 |
    | 5 | escribe 501 | | 501 |
    | 6 | | escribe 501 | **501**: han entrado dos y solo cuenta una |

4. El recurso compartido es `pasajeros`. La sección crítica es `pasajeros++` en los tornos de entrada y `pasajeros--` en el de salida: las tres deben protegerse con el mismo cerrojo.
5. Con dos métodos `synchronized`, uno para entrar y otro para salir:

```java
public class MetroSync {
    static int pasajeros = 0;

    static synchronized void entra() { pasajeros++; }
    static synchronized void sale() { pasajeros--; }

    public static void main(String[] args) throws InterruptedException {
        Thread entrada1 = new Thread(() -> {
            for (int i = 0; i < 50_000; i++) entra();
        });
        Thread entrada2 = new Thread(() -> {
            for (int i = 0; i < 50_000; i++) entra();
        });
        Thread salida = new Thread(() -> {
            for (int i = 0; i < 30_000; i++) sale();
        });
        entrada1.start();
        entrada2.start();
        salida.start();
        entrada1.join();
        entrada2.join();
        salida.join();
        System.out.println("Esperado 70000, obtenido " + pasajeros);
    }
}
```

```text
Esperado 70000, obtenido 70000
```

Como los dos métodos son `static synchronized`, los tres tornos usan el mismo vigilante. También valdría un `AtomicInteger` con `incrementAndGet()` y `decrementAndGet()`.

## R2 · La hucha de los hermanos

```java
public class Hucha {
    private int dinero = 20_000;

    public synchronized void meter(int cantidad) {
        dinero += cantidad;
    }

    public synchronized boolean sacar(int cantidad) {
        if (dinero < cantidad) {                        // comprobar...
            return false;
        }
        dinero -= cantidad;                             // ...y actuar, sin que nadie se cuele
        return true;
    }

    public synchronized int getDinero() {
        return dinero;
    }

    public static void main(String[] args) throws InterruptedException {
        Hucha hucha = new Hucha();                      // una sola hucha para los cuatro
        Thread[] hermanos = new Thread[4];
        for (int i = 0; i < hermanos.length; i++) {
            boolean mete = i < 2;                       // los dos primeros meten, los otros dos sacan
            hermanos[i] = new Thread(() -> {
                for (int j = 0; j < 10_000; j++) {
                    if (mete) {
                        hucha.meter(1);
                    } else {
                        hucha.sacar(1);
                    }
                }
            });
            hermanos[i].start();
        }
        for (Thread h : hermanos) {
            h.join();
        }
        System.out.println("Esperado 20000, obtenido " + hucha.getDinero());
    }
}
```

3. Sin `synchronized`, cada ejecución da un resultado distinto: 17390, 19571 y 24348 en tres pruebas. A veces hay dinero de menos y a veces de más, porque se pierden tanto ingresos como retiradas.
4. Con `synchronized` en `meter`, `sacar` y `getDinero`, sale siempre 20.000. Los cuatro hermanos usan la misma hucha, así que comparten el mismo vigilante.
5. `sacar` es un **comprobar y actuar**: primero mira si hay dinero y después resta. Si solo se protege la resta, dos hermanos pueden ver a la vez que queda 1 € y sacarlo los dos. La comprobación y la resta tienen que hacerse sin que nadie se cuele en medio.

!!! note
    En este ejercicio la hucha nunca llega a quedarse vacía, porque empieza con 20.000 € y como mucho se sacan 20.000. Aun así, `sacar` debe comprobar el saldo: el código tiene que ser correcto aunque cambien los números.

## R3 · Las visitas de la web

```java
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;

public class Visitas {
    static AtomicInteger inicio = new AtomicInteger();
    static AtomicInteger tienda = new AtomicInteger();
    static AtomicInteger contacto = new AtomicInteger();

    public static void main(String[] args) throws InterruptedException {
        Thread[] usuarios = new Thread[6];
        for (int i = 0; i < usuarios.length; i++) {
            usuarios[i] = new Thread(() -> {
                for (int j = 0; j < 10_000; j++) {
                    int pagina = ThreadLocalRandom.current().nextInt(3);   // 0, 1 o 2
                    if (pagina == 0) {
                        inicio.incrementAndGet();
                    } else if (pagina == 1) {
                        tienda.incrementAndGet();
                    } else {
                        contacto.incrementAndGet();
                    }
                }
            });
            usuarios[i].start();
        }
        for (Thread u : usuarios) {
            u.join();
        }
        int total = inicio.get() + tienda.get() + contacto.get();
        System.out.println("Inicio: " + inicio.get());
        System.out.println("Tienda: " + tienda.get());
        System.out.println("Contacto: " + contacto.get());
        System.out.println("Total: " + total + " (esperado 60000)");
    }
}
```

```text
Inicio: 20051
Tienda: 20071
Contacto: 19878
Total: 60000 (esperado 60000)
```

4. Con `static int` y `++`, el total no llega a 60.000 y cambia en cada ejecución: 55981, 58484 y 58865 en tres pruebas.
5. Cada visita cambia **un solo contador** con **una sola operación**: sumar 1. Eso es justo lo que hace una clase atómica de una vez. Haría falta `synchronized` si una visita tuviera que cambiar varias cosas que deben ir juntas, como en la urna de S1, donde cada voto suma a un candidato y al total.
