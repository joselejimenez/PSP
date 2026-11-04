# Boletín de ejercicios · Soluciones

Soluciones de los diez ejercicios del [boletín del Tema 2](boletin.md). Todos los programas son **completos**: puedes copiarlos y ejecutarlos con JDK 21 o superior.

!!! tip "Cómo usar esta página"
    - Intenta cada ejercicio antes de mirar la solución. Muchos admiten otras soluciones igual de válidas: lo importante es que la tuya dé el resultado correcto **siempre**, no solo una vez.
    - Los tiempos que aparecen se midieron en un ordenador de **2 núcleos**. En el tuyo saldrán otros números; lo que debe coincidir es la comparación entre versiones.
    - La primera medición de un programa suele ser más lenta, porque la JVM todavía está optimizando el código. Si quieres comparar con más precisión, repite cada medición varias veces.

## 1. ¿Proceso o hilo? ★

1. Clasificación de los cinco casos:

    | Caso | Usaría | Tipo | Por qué |
    |---|---|---|---|
    | Descargar la siguiente canción mientras suena la actual | Hilo | IO-bound | Comparte la lista de reproducción con el reproductor y pasa casi todo el tiempo esperando a la red. |
    | Exportar un vídeo repartiendo fotogramas entre núcleos | Hilo | CPU-bound | Todos los hilos necesitan el mismo proyecto en memoria; tiene sentido un hilo por núcleo. |
    | Ejecutar un script de Python que ya existe | Proceso | — | Es otro programa: se lanza con `ProcessBuilder`, como en el Tema 1. |
    | Servidor de chat con 500 usuarios | Hilo | IO-bound | Comparten la lista de usuarios y los mensajes, y cada conexión pasa casi todo el tiempo esperando. |
    | Extensiones del navegador aisladas | Proceso | — | Lo que importa es el aislamiento: si una falla, no debe tumbar al resto. |

2. Comparten todo lo del proceso: el **heap** (todos los objetos), los campos **`static`**, los ficheros abiertos y las conexiones. Cada hilo tiene su propia **pila** (variables locales y parámetros) y su **contador de programa**.

3. No irá más rápido. Con un trabajo CPU-bound, cada hilo necesita un núcleo para avanzar. Si hay más hilos que núcleos, se turnan, y además se pierde tiempo en los cambios de contexto. Lo razonable es usar tantos hilos como núcleos.

## 2. Tres corredores ★

```java
import java.util.concurrent.ThreadLocalRandom;

public class Carrera {
    public static void main(String[] args) throws InterruptedException {
        Thread[] corredores = new Thread[3];
        for (int i = 0; i < corredores.length; i++) {
            corredores[i] = new Thread(() -> {
                String yo = Thread.currentThread().getName();
                for (int vuelta = 1; vuelta <= 5; vuelta++) {
                    System.out.println(yo + ": vuelta " + vuelta);
                    try {
                        Thread.sleep(ThreadLocalRandom.current().nextInt(100, 501));
                    } catch (InterruptedException e) {
                        return;
                    }
                }
                System.out.println(yo + " llega a meta");
            }, "Corredor-" + (i + 1));
            corredores[i].start();
        }
        for (Thread c : corredores) {
            c.join();
        }
        System.out.println("Carrera terminada");
    }
}
```

Final de una ejecución:

```text
Corredor-2: vuelta 5
Corredor-3 llega a meta
Corredor-1 llega a meta
Corredor-2 llega a meta
Carrera terminada
```

- El nombre se pone al crear el hilo y cada corredor lo recupera con `Thread.currentThread().getName()`.
- Crear y arrancar en un bucle; esperar en otro. Así «Carrera terminada» sale siempre al final.
- **No gana siempre el mismo**: cada vuelta dura un tiempo aleatorio y, además, el orden en que se ejecutan los hilos lo decide el planificador.
- `ThreadLocalRandom` es el generador aleatorio pensado para varios hilos: cada hilo tiene el suyo y no se estorban.

## 3. Predice los estados ★★

1. Predicción, que coincide con la ejecución:

    | Línea | Imprime | Por qué |
    |---|---|---|
    | A | `NEW` | `espera` todavía no ha arrancado. |
    | B | `TIMED_WAITING` | `lento` lleva 0,5 s de sus 2 s de `sleep`. |
    | C | `WAITING` | `espera` está dentro de `lento.join()`, sin límite de tiempo. No es BLOCKED: BLOCKED es solo esperar un cerrojo. |
    | D | `TERMINATED` | El `main` ha esperado a `espera`, que a su vez esperó a `lento`. |
    | E | `false` | Cuando `espera` termina, `lento` ya ha terminado. |

2. Con `lento.join(5000)` cambia la **C**: pasa a `TIMED_WAITING`, porque ahora la espera tiene un límite. Lo demás no cambia, porque `lento` termina antes de los 5 s.
3. Con `Thread.sleep(3000)` en el `main`, cuando se imprimen B y C los dos hilos ya han terminado: **B y C imprimen `TERMINATED`**.
4. Porque Java no distingue entre un hilo que está listo y uno que se está ejecutando: las dos situaciones son `RUNNABLE`. Quién usa la CPU en cada momento lo decide el sistema operativo, y la JVM no lo controla.

## 4. Cuenta atrás cancelable ★★

```java
import java.util.Scanner;

public class CuentaAtras {
    public static void main(String[] args) throws InterruptedException {
        Thread cuenta = new Thread(() -> {
            int s = 10;
            try {
                while (s > 0) {
                    System.out.println(s);
                    Thread.sleep(1000);
                    s--;
                }
                System.out.println("¡Despegue!");
            } catch (InterruptedException e) {
                System.out.println("Despegue abortado en el segundo " + s);
            }
        }, "CuentaAtras");

        Thread teclado = new Thread(() -> {
            Scanner sc = new Scanner(System.in);
            while (sc.hasNextLine()) {
                if (sc.nextLine().trim().equalsIgnoreCase("abortar")) {
                    cuenta.interrupt();
                    return;
                }
            }
        }, "Teclado");
        teclado.setDaemon(true);          // si la cuenta llega a 0, la JVM no espera al teclado

        cuenta.start();
        teclado.start();
        cuenta.join();                    // el main solo espera a la cuenta atrás
    }
}
```

Escribiendo `abortar` a los 3 segundos:

```text
10
9
8
Despegue abortado en el segundo 8
```

Sin escribir nada, la cuenta llega a 0, imprime `¡Despegue!` y el programa termina.

- **El teclado se lee en un hilo demonio.** El `main` solo espera a la cuenta atrás. Si la cuenta llega a 0, el `main` termina y la JVM no espera al hilo del teclado, aunque siga bloqueado en `nextLine()`. Si el `main` leyera el teclado él mismo, se quedaría esperando una línea y el programa no terminaría.
- **`interrupt()`** despierta el `sleep` de la cuenta atrás con `InterruptedException`. El `try` envuelve todo el bucle, así que la excepción saca al hilo del bucle y termina.
- **Pregunta 5:** con un `catch` vacío **dentro** del bucle, la excepción se tragaría la petición de parar y la cuenta seguiría hasta 0 como si nada. En esta solución el `catch` está fuera del bucle, y por eso funciona.

## 5. Copias de seguridad con límite de tiempo ★★

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Copias {
    public static void main(String[] args) throws InterruptedException {
        Map<String, Integer> carpetas = new LinkedHashMap<>();
        carpetas.put("Documentos", 2);
        carpetas.put("Fotos", 6);
        carpetas.put("Proyectos", 3);
        carpetas.put("Música", 5);

        Map<String, Thread> hilos = new LinkedHashMap<>();
        long ini = System.currentTimeMillis();
        for (Map.Entry<String, Integer> c : carpetas.entrySet()) {
            Thread t = new Thread(() -> {
                try {
                    Thread.sleep(c.getValue() * 1000L);   // simula la copia
                } catch (InterruptedException e) {
                    // cancelada: no hace falta hacer nada más, el hilo termina
                }
            }, c.getKey());
            hilos.put(c.getKey(), t);
            t.start();
        }

        long limite = ini + 4000;                             // un único instante límite
        Map<String, String> resultado = new LinkedHashMap<>();
        for (Map.Entry<String, Thread> h : hilos.entrySet()) {
            Thread t = h.getValue();
            long queda = limite - System.currentTimeMillis();
            if (queda > 0) {
                t.join(queda);
            }
            if (t.isAlive()) {
                t.interrupt();
                resultado.put(h.getKey(), "cancelada");
            } else {
                resultado.put(h.getKey(), "completada");
            }
        }
        for (Thread t : hilos.values()) {
            t.join();
        }

        System.out.printf("%-12s %s%n", "Carpeta", "Resultado");
        resultado.forEach((k, v) -> System.out.printf("%-12s %s%n", k, v));
        System.out.printf("Total: %.1f s%n", (System.currentTimeMillis() - ini) / 1000.0);
    }
}
```

```text
Carpeta      Resultado
Documentos   completada
Fotos        cancelada
Proyectos    completada
Música       cancelada
Total: 4,0 s
```

- Se calcula **un único instante límite** (inicio + 4 s) y cada `join()` espera solo lo que queda hasta ese instante.
- Después de cada `join()`, `isAlive()` dice si la copia terminó a tiempo. Si sigue viva, se interrumpe y se anota como cancelada.
- El último bucle de `join()` espera a que las canceladas terminen de verdad.
- **Pregunta 5:** con `join(4000)` uno detrás de otro, cada espera puede durar hasta 4 s. `Fotos` (6 s) haría esperar 4 s y luego `Música` (5 s) otro segundo más: el total pasaría de 4 s. Con más copias lentas, todavía más.
- `LinkedHashMap` mantiene las carpetas en el orden en que se añadieron, para que la tabla salga ordenada.

## 6. Encuentra la condición de carrera ★★

| # | ¿Carrera? | Sección crítica y solución |
|---|---|---|
| 1 | No | Todos leen y nadie escribe. |
| 2 | **Sí** | `total = total + importe;` son tres pasos: leer, sumar y escribir. Se arregla con `synchronized` sobre un cerrojo común o con un método `static synchronized`. |
| 3 | No | Cada hilo tiene su propio `StringBuilder`: no hay nada compartido. |
| 4 | **Sí** | Comprobar y actuar: desde `if (asientosLibres > 0)` hasta `asientosLibres--`, ambos incluidos. Se pueden vender más asientos de los que hay. Se protege el bloque entero con `synchronized`. |
| 5 | **Sí** | `ArrayList` no está preparado para varios hilos: `add()` también son varios pasos. Se protege cada `add()` con `synchronized (lista)` o se usa una lista preparada para hilos. |
| 6 | No | El `main` espera con `join()` a que termine el hilo que rellena la lista. Cuando la recorre, ya nadie escribe en ella. |

Comprobación del caso 2:

```java
public class SumaDouble {
    static double total = 0;

    public static void main(String[] args) throws InterruptedException {
        Thread[] hilos = new Thread[4];
        for (int i = 0; i < 4; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    total = total + 1.0;
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Esperado 400000.0, obtenido " + total);
    }
}
```

```text
Esperado 400000.0, obtenido 384865.0
Esperado 400000.0, obtenido 368289.0
Esperado 400000.0, obtenido 363089.0
```

## 7. Sumar un array en paralelo ★★★

```java
import java.util.concurrent.ThreadLocalRandom;

public class SumaParalela {
    static final int TAM = 100_000_000;

    static long sumarConHilos(int[] datos, int numHilos) throws InterruptedException {
        long[] parciales = new long[numHilos];               // una posición por hilo
        Thread[] hilos = new Thread[numHilos];
        int trozo = datos.length / numHilos;
        for (int k = 0; k < numHilos; k++) {
            int id = k;
            int desde = k * trozo;
            int hasta = (k == numHilos - 1) ? datos.length : desde + trozo;   // el último se lleva el resto
            hilos[k] = new Thread(() -> {
                long suma = 0;                               // variable local: no se comparte
                for (int i = desde; i < hasta; i++) {
                    suma += datos[i];
                }
                parciales[id] = suma;                        // cada hilo escribe solo en SU posición
            });
            hilos[k].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        long total = 0;
        for (long p : parciales) {
            total += p;
        }
        return total;
    }

    public static void main(String[] args) throws InterruptedException {
        int[] datos = new int[TAM];
        for (int i = 0; i < TAM; i++) {
            datos[i] = ThreadLocalRandom.current().nextInt(10);
        }

        long t0 = System.nanoTime();
        long secuencial = 0;
        for (int d : datos) {
            secuencial += d;
        }
        long tSec = (System.nanoTime() - t0) / 1_000_000;
        System.out.println("main: " + secuencial + " en " + tSec + " ms");

        int nucleos = Runtime.getRuntime().availableProcessors();
        long t1 = 0;
        for (int n : new int[]{1, 2, 4, nucleos}) {
            long ini = System.nanoTime();
            long total = sumarConHilos(datos, n);
            long ms = (System.nanoTime() - ini) / 1_000_000;
            if (n == 1) t1 = ms;
            System.out.printf("%2d hilos: %d en %d ms · aceleración %.2f · %s%n",
                    n, total, ms, (double) t1 / ms, total == secuencial ? "correcto" : "¡DISTINTO!");
        }
    }
}
```

Una ejecución en un ordenador de 2 núcleos:

| Hilos | Tiempo (ms) | Aceleración |
|---|---|---|
| 1 | 74 | 1 |
| 2 | 39 | 1,90 |
| 4 | 28 | 2,64 |
| 2 (núcleos) | 34 | 2,18 |

- El array se divide en trozos iguales y **el último hilo se lleva el resto**, por si la división no es exacta.
- Cada hilo suma en una **variable local** y, al final, escribe su resultado en **su propia posición** de `parciales`.
- **Pregunta 5:** no hace falta `synchronized` porque ningún par de hilos escribe en la misma posición. Compartir el array no es el problema: el problema es que dos hilos escriban en el **mismo dato**. Además, el `main` lee `parciales` después de los `join()`, cuando ya nadie escribe.
- **Pregunta 6:** es **CPU-bound**: el array ya está en memoria y el trabajo es sumar. Con el doble de hilos que núcleos no debería mejorar más, porque los hilos se turnan. En la tabla, 4 hilos salen algo mejor que 2 porque las primeras mediciones todavía incluyen la optimización de la JVM; repitiendo varias veces, los tiempos con 2 y 4 hilos se igualan.
- 100 millones de `int` ocupan unos **400 MB**. Si te sale `OutOfMemoryError`, ejecuta con más memoria: `java -Xmx1g SumaParalela`.

## 8. Contador de visitas: tres versiones ★★★

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Visitas {
    static final int HILOS = 10;
    static final int VISITAS = 100_000;

    // Versión 1: sin protección
    static int sinProteccion = 0;

    // Versión 2: clase con métodos synchronized
    static class Contador {
        private int valor = 0;
        public synchronized void incrementar() { valor++; }
        public synchronized int getValor() { return valor; }
    }

    // Lanza HILOS hilos que ejecutan la tarea y espera a todos; devuelve los ms
    static long medir(Runnable tarea) throws InterruptedException {
        long ini = System.nanoTime();
        Thread[] hilos = new Thread[HILOS];
        for (int i = 0; i < HILOS; i++) {
            hilos[i] = new Thread(tarea);
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        return (System.nanoTime() - ini) / 1_000_000;
    }

    public static void main(String[] args) throws InterruptedException {
        int esperado = HILOS * VISITAS;

        long ms1 = medir(() -> { for (int j = 0; j < VISITAS; j++) sinProteccion++; });
        System.out.printf("1. Sin protección:  %7d en %4d ms%n", sinProteccion, ms1);

        Contador c = new Contador();
        long ms2 = medir(() -> { for (int j = 0; j < VISITAS; j++) c.incrementar(); });
        System.out.printf("2. synchronized:    %7d en %4d ms%n", c.getValor(), ms2);

        AtomicInteger a = new AtomicInteger();
        long ms3 = medir(() -> { for (int j = 0; j < VISITAS; j++) a.incrementAndGet(); });
        System.out.printf("3. AtomicInteger:   %7d en %4d ms%n", a.get(), ms3);

        // Versión 4: cada hilo cuenta en su variable y el main suma al final
        int[] parciales = new int[HILOS];
        Thread[] hilos = new Thread[HILOS];
        long ini = System.nanoTime();
        for (int i = 0; i < HILOS; i++) {
            int id = i;
            hilos[i] = new Thread(() -> {
                int mias = 0;                          // local: no se comparte
                for (int j = 0; j < VISITAS; j++) mias++;
                parciales[id] = mias;                  // cada hilo escribe solo en su posición
            });
            hilos[i].start();
        }
        for (Thread h : hilos) h.join();
        int total = 0;
        for (int p : parciales) total += p;
        System.out.printf("4. Sin compartir:   %7d en %4d ms%n", total, (System.nanoTime() - ini) / 1_000_000);

        // Error a propósito: un cerrojo por hilo
        int[] malo = {0};
        medir(() -> {
            Object cerrojo = new Object();             // ¡cada hilo crea el suyo!
            for (int j = 0; j < VISITAS; j++) {
                synchronized (cerrojo) { malo[0]++; }
            }
        });
        System.out.printf("5. Cerrojo por hilo: %7d (esperado %d)%n", malo[0], esperado);
    }
}
```

Dos ejecuciones:

```text
1. Sin protección:   613931 en   10 ms
2. synchronized:    1000000 en  135 ms
3. AtomicInteger:   1000000 en   41 ms
4. Sin compartir:   1000000 en   12 ms
5. Cerrojo por hilo:  727744 (esperado 1000000)

1. Sin protección:   807091 en   18 ms
2. synchronized:    1000000 en  120 ms
3. AtomicInteger:   1000000 en   32 ms
4. Sin compartir:   1000000 en   13 ms
5. Cerrojo por hilo:  879200 (esperado 1000000)
```

| Versión | ¿Resultado correcto? | Tiempo |
|---|---|---|
| Sin protección | No, y cambia en cada ejecución | El más rápido, pero no sirve |
| `synchronized` | Sí, siempre | El más lento: los hilos hacen cola para el cerrojo |
| `AtomicInteger` | Sí, siempre | Bastante más rápido que `synchronized`: no bloquea |
| Sin compartir (versión 4) | Sí, siempre | Tan rápido como sin protección |

- **Versión 4:** cada hilo cuenta en una variable local y guarda su resultado en su posición de `parciales`. Mientras trabajan no comparten nada, así que no hace falta sincronizar.
- **Pregunta 6, un cerrojo por hilo:** el resultado vuelve a ser incorrecto. Cada hilo crea su propio objeto cerrojo, así que nunca tiene que esperar a nadie: es como si no hubiera cerrojo. Todos los hilos que tocan el dato deben sincronizarse sobre **el mismo** objeto.

## 9. El banco: transferencias sin perder dinero ★★★★

```java
import java.util.concurrent.ThreadLocalRandom;

public class Banco {

    static class Cuenta {
        private final int numero;
        private int saldo;

        Cuenta(int numero, int saldo) {
            this.numero = numero;
            this.saldo = saldo;
        }

        void ingresar(int cantidad) {
            saldo += cantidad;
        }

        boolean retirar(int cantidad) {
            if (saldo < cantidad) {
                return false;
            }
            saldo -= cantidad;
            return true;
        }

        int getSaldo() {
            return saldo;
        }
    }

    private final Cuenta[] cuentas = new Cuenta[5];
    private final Object cerrojo = new Object();      // un único cerrojo para todo el banco
    private final boolean protegido;

    Banco(boolean protegido) {
        this.protegido = protegido;
        for (int i = 0; i < cuentas.length; i++) {
            cuentas[i] = new Cuenta(i, 1000);
        }
    }

    void transferir(int origen, int destino, int cantidad) {
        if (protegido) {
            synchronized (cerrojo) {
                mover(origen, destino, cantidad);
            }
        } else {
            mover(origen, destino, cantidad);
        }
    }

    // Comprobar, retirar e ingresar: todo debe ir dentro de la misma sección crítica
    private void mover(int origen, int destino, int cantidad) {
        if (cuentas[origen].retirar(cantidad)) {
            cuentas[destino].ingresar(cantidad);
        }
    }

    int total() {
        synchronized (cerrojo) {
            int t = 0;
            for (Cuenta c : cuentas) t += c.getSaldo();
            return t;
        }
    }

    int negativas() {
        int n = 0;
        for (Cuenta c : cuentas) if (c.getSaldo() < 0) n++;
        return n;
    }

    static void probar(boolean protegido) throws InterruptedException {
        Banco banco = new Banco(protegido);
        Thread[] hilos = new Thread[10];
        for (int i = 0; i < hilos.length; i++) {
            hilos[i] = new Thread(() -> {
                ThreadLocalRandom r = ThreadLocalRandom.current();
                for (int j = 0; j < 10_000; j++) {
                    int origen = r.nextInt(5);
                    int destino = r.nextInt(5);
                    if (origen != destino) {
                        banco.transferir(origen, destino, r.nextInt(1, 101));
                    }
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) h.join();
        System.out.printf("%-14s total = %d € (esperado 5000) · cuentas en negativo: %d%n",
                protegido ? "Con cerrojo:" : "Sin protección:", banco.total(), banco.negativas());
    }

    public static void main(String[] args) throws InterruptedException {
        probar(false);
        probar(true);
    }
}
```

Tres ejecuciones:

```text
Sin protección: total = 5952 € (esperado 5000) · cuentas en negativo: 0
Con cerrojo:   total = 5000 € (esperado 5000) · cuentas en negativo: 0
Sin protección: total = 14104 € (esperado 5000) · cuentas en negativo: 0
Con cerrojo:   total = 5000 € (esperado 5000) · cuentas en negativo: 0
Sin protección: total = 22900 € (esperado 5000) · cuentas en negativo: 0
Con cerrojo:   total = 5000 € (esperado 5000) · cuentas en negativo: 0
```

- **Sin protección, el total no cuadra**: los saldos pierden o ganan incrementos, igual que el contador, y el banco «crea» o «destruye» dinero. También pueden quedar cuentas en negativo, porque `retirar` es un comprobar y actuar.
- **Con un único cerrojo para todo el banco**, cada transferencia completa (comprobar, retirar e ingresar) es una sola sección crítica, y el total es siempre 5000 €.
- **Pregunta 6:** si `ingresar` y `retirar` fueran `synchronized` por separado, cada operación sería segura, pero la transferencia no. Entre retirar de una cuenta e ingresar en otra, otro hilo podría ver el dinero «en el aire» y el total no cuadraría en ese momento. Una transferencia son dos pasos que deben ir juntos.
- **Pregunta 7:** `AtomicInteger` protege una operación sobre **una** variable. Una transferencia cambia **dos** saldos y además tiene que comprobar antes que hay dinero. Para eso hace falta un cerrojo.
- `total()` también usa el cerrojo, para no sumar los saldos a mitad de una transferencia.

## 10. Contar palabras en paralelo ★★★★

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Cuenta cuántas veces aparece cada palabra de un fichero de texto,
 * de forma secuencial y repartiendo las líneas entre varios hilos.
 */
public class ContarPalabras {

    static final String[] PALABRAS = {"hilo", "proceso", "cerrojo", "java", "carrera", "núcleo",
            "pila", "heap", "tarea", "estado", "monitor", "atómico", "servidor", "cliente",
            "socket", "memoria", "cola", "sección", "crítica", "join"};

    /**
     * Genera un fichero con líneas de 10 palabras elegidas al azar.
     *
     * @param ruta   fichero que se crea (o se sobrescribe)
     * @param lineas número de líneas
     * @throws IOException si no se puede escribir el fichero
     */
    static void generar(Path ruta, int lineas) throws IOException {
        ThreadLocalRandom r = ThreadLocalRandom.current();
        List<String> texto = new ArrayList<>(lineas);
        for (int i = 0; i < lineas; i++) {
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < 10; j++) {
                if (j > 0) sb.append(' ');
                sb.append(PALABRAS[r.nextInt(PALABRAS.length)]);
            }
            texto.add(sb.toString());
        }
        Files.write(ruta, texto);
    }

    /**
     * Cuenta las palabras de un trozo de la lista en un mapa propio.
     *
     * @param lineas todas las líneas
     * @param desde  primera línea del trozo (incluida)
     * @param hasta  última línea del trozo (excluida)
     * @return mapa palabra → apariciones en ese trozo
     */
    static Map<String, Integer> contarTrozo(List<String> lineas, int desde, int hasta) {
        Map<String, Integer> cuenta = new HashMap<>();
        for (int i = desde; i < hasta; i++) {
            for (String p : lineas.get(i).split(" ")) {
                cuenta.merge(p, 1, Integer::sum);
            }
        }
        return cuenta;
    }

    /**
     * Versión 1: todos los hilos actualizan el mismo mapa, protegido con synchronized.
     *
     * @param lineas   líneas del texto
     * @param numHilos número de hilos
     * @return mapa palabra → apariciones
     * @throws InterruptedException si se interrumpe la espera a los hilos
     */
    static Map<String, Integer> mapaCompartido(List<String> lineas, int numHilos) throws InterruptedException {
        Map<String, Integer> cuenta = new HashMap<>();
        Thread[] hilos = new Thread[numHilos];
        int trozo = lineas.size() / numHilos;
        for (int k = 0; k < numHilos; k++) {
            int desde = k * trozo;
            int hasta = (k == numHilos - 1) ? lineas.size() : desde + trozo;
            hilos[k] = new Thread(() -> {
                for (int i = desde; i < hasta; i++) {
                    for (String p : lineas.get(i).split(" ")) {
                        synchronized (cuenta) {          // el mapa es el recurso compartido
                            cuenta.merge(p, 1, Integer::sum);
                        }
                    }
                }
            });
            hilos[k].start();
        }
        for (Thread h : hilos) h.join();
        return cuenta;
    }

    /**
     * Versión 2: cada hilo cuenta en su propio mapa y el hilo principal los fusiona al final.
     *
     * @param lineas   líneas del texto
     * @param numHilos número de hilos
     * @return mapa palabra → apariciones
     * @throws InterruptedException si se interrumpe la espera a los hilos
     */
    @SuppressWarnings("unchecked")
    static Map<String, Integer> mapasLocales(List<String> lineas, int numHilos) throws InterruptedException {
        Map<String, Integer>[] parciales = new Map[numHilos];
        Thread[] hilos = new Thread[numHilos];
        int trozo = lineas.size() / numHilos;
        for (int k = 0; k < numHilos; k++) {
            int id = k;
            int desde = k * trozo;
            int hasta = (k == numHilos - 1) ? lineas.size() : desde + trozo;
            hilos[k] = new Thread(() -> parciales[id] = contarTrozo(lineas, desde, hasta));
            hilos[k].start();
        }
        for (Thread h : hilos) h.join();
        Map<String, Integer> total = new HashMap<>();
        for (Map<String, Integer> m : parciales) {
            m.forEach((p, n) -> total.merge(p, n, Integer::sum));
        }
        return total;
    }

    /**
     * Genera el texto, lo cuenta de tres formas y compara resultados y tiempos.
     *
     * @param args no se usan
     * @throws Exception si falla la lectura o escritura del fichero
     */
    public static void main(String[] args) throws Exception {
        Path ruta = Path.of("texto.txt");
        generar(ruta, 200_000);
        List<String> lineas = Files.readAllLines(ruta);

        long ini = System.nanoTime();
        Map<String, Integer> referencia = contarTrozo(lineas, 0, lineas.size());
        System.out.printf("Secuencial:             %4d ms%n", (System.nanoTime() - ini) / 1_000_000);

        for (int n : new int[]{1, 2, 4}) {
            ini = System.nanoTime();
            Map<String, Integer> a = mapaCompartido(lineas, n);
            long msA = (System.nanoTime() - ini) / 1_000_000;
            ini = System.nanoTime();
            Map<String, Integer> b = mapasLocales(lineas, n);
            long msB = (System.nanoTime() - ini) / 1_000_000;
            System.out.printf("%d hilos · compartido: %4d ms %s · locales: %4d ms %s%n", n,
                    msA, a.equals(referencia) ? "ok" : "MAL", msB, b.equals(referencia) ? "ok" : "MAL");
        }
        System.out.println(new TreeMap<>(referencia));
    }
}
```

Una ejecución en un ordenador de 2 núcleos:

```text
Secuencial:              381 ms
1 hilos · compartido:  245 ms ok · locales:  266 ms ok
2 hilos · compartido:  442 ms ok · locales:   55 ms ok
4 hilos · compartido:  342 ms ok · locales:   70 ms ok
```

- Las dos versiones dan **el mismo resultado** que la secuencial (`ok`).
- **Mapa compartido:** es correcto, pero no mejora con más hilos, e incluso empeora. Cada palabra obliga a coger el cerrojo, así que los hilos pasan casi todo el tiempo haciendo cola: en la práctica trabajan de uno en uno.
- **Mapas locales:** es la más rápida. Mientras trabajan, los hilos no comparten nada; solo al final el `main` fusiona los mapas, una vez por hilo.
- La medición secuencial es la primera y sale más lenta porque la JVM todavía está optimizando el código.
- **Pregunta 5:** sin `synchronized` en el mapa compartido, el resultado sale mal y, a veces, el programa lanza excepciones desde dentro del `HashMap`. En tres ejecuciones con 4 hilos se contaron 1.957.279, 1.489.605 y 1.490.428 palabras, en vez de 2.000.000. `HashMap` no está preparado para varios hilos.
- **Javadoc:** `javadoc -d doc ContarPalabras.java` genera la documentación en la carpeta `doc`. Abre `doc/index.html` en el navegador.
