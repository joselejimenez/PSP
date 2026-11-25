# Boletín 2 · Soluciones

Soluciones del [boletín 2](boletin-2.md). Todos los programas son completos: puedes copiarlos y ejecutarlos con JDK 21 o superior. Muchos ejercicios admiten otras soluciones igual de válidas: lo importante es que la tuya dé el resultado correcto **siempre**.

## Bloque A · Lock

### A1. Contador de visitas ★

```java
import java.util.concurrent.locks.ReentrantLock;

public class Visitas {
    static int visitas = 0;
    static final ReentrantLock cerrojo = new ReentrantLock();

    public static void main(String[] args) throws InterruptedException {
        Thread[] servidores = new Thread[3];
        for (int i = 0; i < 3; i++) {
            servidores[i] = new Thread(() -> {
                for (int j = 0; j < 50_000; j++) {
                    cerrojo.lock();
                    try {
                        visitas++;
                    } finally {
                        cerrojo.unlock();
                    }
                }
            });
            servidores[i].start();
        }
        for (Thread s : servidores) {
            s.join();
        }
        System.out.println("Visitas: " + visitas + " (esperadas 150000)");
    }
}
```

```text
Visitas: 150000 (esperadas 150000)
```

**3.** Sin el cerrojo salen números menores de 150 000 y distintos en cada ejecución: `visitas++` son tres pasos (leer, sumar, escribir) y dos servidores pueden leer el mismo valor a la vez.

### A2. La sala de reuniones ★★★

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class SalaReuniones {
    static final ReentrantLock sala = new ReentrantLock();
    static final AtomicInteger reuniones = new AtomicInteger();
    static final AtomicInteger sinSala = new AtomicInteger();

    static void reservar(String quien) {
        try {
            if (sala.tryLock(1, TimeUnit.SECONDS)) {
                try {
                    System.out.println(quien + " entra en la sala");
                    Thread.sleep(700);                  // la reunión dura 700 ms
                    reuniones.incrementAndGet();
                    System.out.println(quien + " sale de la sala");
                } finally {
                    sala.unlock();
                }
            } else {
                sinSala.incrementAndGet();
                System.out.println(quien + " se cansa de esperar y hace la reunión por videollamada");
            }
        } catch (InterruptedException e) {
            System.out.println(quien + " interrumpido");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        String[] empleados = {"Ana", "Luis", "Marta", "Pepe", "Sara"};
        Thread[] hilos = new Thread[empleados.length];
        for (int i = 0; i < empleados.length; i++) {
            String nombre = empleados[i];
            hilos[i] = new Thread(() -> reservar(nombre));
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Reuniones en la sala: " + reuniones.get() + " · Por videollamada: " + sinSala.get());
    }
}
```

```text
Ana entra en la sala
Ana sale de la sala
Luis entra en la sala
Marta se cansa de esperar y hace la reunión por videollamada
Sara se cansa de esperar y hace la reunión por videollamada
Pepe se cansa de esperar y hace la reunión por videollamada
Luis sale de la sala
Reuniones en la sala: 2 · Por videollamada: 3
```

**4.** Caben **2**. El primero entra al momento y sale a los 700 ms. El segundo entra entonces (lleva 700 ms esperando, menos de 1 s). El tercero tendría que esperar hasta los 1400 ms, y se cansa a los 1000 ms. Los nombres cambian en cada ejecución; los números, no.
**5.** Con 300 ms caben 4: entran a los 0, 300, 600 y 900 ms; el quinto tendría que esperar hasta los 1200 ms. Con `lock()` todos esperan sin límite y los 5 acaban usando la sala (el último entra a los 2,8 s).

### A3. La fotocopiadora de la sala de profesores ★★★

```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class Fotocopiadora {
    static final ReentrantLock fotocopiadora = new ReentrantLock();
    static final AtomicInteger copias = new AtomicInteger();
    static final AtomicInteger rendidos = new AtomicInteger();

    static void pausa(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            // nada
        }
    }

    static void fotocopiar(String quien) {
        for (int intento = 1; intento <= 3; intento++) {
            if (fotocopiadora.tryLock()) {
                try {
                    System.out.println(quien + " fotocopia (intento " + intento + ")");
                    pausa(150);
                    copias.incrementAndGet();
                    return;                             // hecho: no hay más intentos
                } finally {
                    fotocopiadora.unlock();
                }
            }
            System.out.println(quien + " la ve ocupada (intento " + intento + ")");
            pausa(200);                                 // da una vuelta y vuelve
        }
        rendidos.incrementAndGet();
        System.out.println(quien + " se rinde");
    }

    public static void main(String[] args) throws InterruptedException {
        String[] profes = {"Ana", "Luis", "Marta", "Pepe", "Sara", "Toni"};
        Thread[] hilos = new Thread[profes.length];
        for (int i = 0; i < profes.length; i++) {
            String nombre = profes[i];
            hilos[i] = new Thread(() -> fotocopiar(nombre));
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Fotocopias: " + copias.get() + " · Se rinden: " + rendidos.get()
                + " · Total: " + (copias.get() + rendidos.get()));
    }
}
```

```text
Luis la ve ocupada (intento 1)
Ana fotocopia (intento 1)
Marta la ve ocupada (intento 1)
...
Sara fotocopia (intento 3)
...
Toni se rinde
Marta se rinde
Pepe se rinde
Fotocopias: 3 · Se rinden: 3 · Total: 6
```

**4.** Sin el `return`, el profesor que ya ha fotocopiado seguiría intentándolo y haría hasta 3 copias. Además, al acabar el bucle se contaría como rendido.
**5.** Con `synchronized`, el que la encuentra ocupada **espera sin límite**: no puede probar e irse a dar una vuelta. Eso solo se puede hacer con `tryLock()`.

## Bloque B · Productor-consumidor

### B1. La cinta de equipajes ★

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class CintaEquipaje {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> cinta = new ArrayBlockingQueue<>(3);   // caben 3 maletas

        Thread facturacion = new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    cinta.put("maleta-" + i);
                    System.out.println("Facturada maleta-" + i);
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        Thread operario = new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    String maleta = cinta.take();
                    System.out.println("    El operario carga " + maleta + " en el avión");
                    Thread.sleep(300);
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        facturacion.start();
        operario.start();
        facturacion.join();
        operario.join();
        System.out.println("Todas las maletas están en el avión");
    }
}
```

**4.** Al principio la cinta está vacía y el mostrador factura de golpe hasta llenarla (3 maletas, más la que el operario ya ha cogido). Después, cada `put` tiene que esperar a que el operario haga un `take`, y el operario tarda 300 ms: a partir de ahí van al ritmo del más lento.

### B2. La cadena de montaje ★★★

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class CadenaMontaje {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> cortadas = new ArrayBlockingQueue<>(2);
        BlockingQueue<String> pintadas = new ArrayBlockingQueue<>(2);

        Thread cortador = new Thread(() -> {
            try {
                for (int i = 1; i <= 5; i++) {
                    String pieza = "silla-" + i;
                    Thread.sleep(100);
                    System.out.println("Cortada " + pieza);
                    cortadas.put(pieza);
                }
                cortadas.put("FIN");                    // ya no hay más piezas
            } catch (InterruptedException e) {
                return;
            }
        });

        Thread pintor = new Thread(() -> {
            try {
                while (true) {
                    String pieza = cortadas.take();
                    if (pieza.equals("FIN")) {
                        pintadas.put("FIN");            // pasa el aviso al siguiente
                        break;
                    }
                    Thread.sleep(200);
                    System.out.println("    Pintada " + pieza);
                    pintadas.put(pieza);
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        Thread empaquetador = new Thread(() -> {
            int cajas = 0;
            try {
                while (true) {
                    String pieza = pintadas.take();
                    if (pieza.equals("FIN")) {
                        break;
                    }
                    Thread.sleep(50);
                    cajas++;
                    System.out.println("        Empaquetada " + pieza);
                }
            } catch (InterruptedException e) {
                return;
            }
            System.out.println("        El empaquetador termina: " + cajas + " cajas");
        });

        cortador.start();
        pintor.start();
        empaquetador.start();
        cortador.join();
        pintor.join();
        empaquetador.join();
        System.out.println("Cadena de montaje parada");
    }
}
```

```text
Cortada silla-1
Cortada silla-2
    Pintada silla-1
Cortada silla-3
        Empaquetada silla-1
Cortada silla-4
    Pintada silla-2
...
        El empaquetador termina: 5 cajas
Cadena de montaje parada
```

**2.** El `"FIN"` de `cortadas` lo pone el **cortador** al terminar sus 5 sillas. El de `pintadas` lo pone el **pintor** cuando recibe el `"FIN"` de `cortadas`: el aviso **se pasa** de un puesto al siguiente. (Aquí sí lo puede poner el propio productor, porque cada cola tiene un único productor.)
**4.** Cuando `cortadas` tiene 2 sillas esperando, el `put` del cortador se bloquea hasta que el pintor coge una. El cortador acaba trabajando al ritmo del pintor.

### B3. Los sensores de temperatura ★★★

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;

public class Sensores {
    static final BlockingQueue<Integer> cola = new ArrayBlockingQueue<>(5);
    static final AtomicInteger sumaEnviada = new AtomicInteger();
    static final AtomicInteger sumaProcesada = new AtomicInteger();
    static final AtomicInteger lecturas = new AtomicInteger();
    static final int FIN = -1;                          // aviso de fin (una temperatura nunca es -1 aquí)

    public static void main(String[] args) throws InterruptedException {
        Thread[] sensores = new Thread[3];
        for (int s = 0; s < 3; s++) {
            String nombre = "Sensor-" + (s + 1);
            sensores[s] = new Thread(() -> {
                try {
                    for (int i = 0; i < 4; i++) {
                        int temperatura = ThreadLocalRandom.current().nextInt(15, 35);
                        sumaEnviada.addAndGet(temperatura);
                        cola.put(temperatura);
                        System.out.println(nombre + " mide " + temperatura + " ºC");
                        Thread.sleep(50);
                    }
                } catch (InterruptedException e) {
                    return;
                }
            });
        }

        Runnable procesar = () -> {
            String yo = Thread.currentThread().getName();
            try {
                while (true) {
                    int t = cola.take();
                    if (t == FIN) {
                        break;
                    }
                    Thread.sleep(80);
                    sumaProcesada.addAndGet(t);
                    lecturas.incrementAndGet();
                    System.out.println("    " + yo + " procesa " + t + " ºC");
                }
            } catch (InterruptedException e) {
                return;
            }
        };
        Thread p1 = new Thread(procesar, "Procesador-1");
        Thread p2 = new Thread(procesar, "Procesador-2");

        for (Thread s : sensores) s.start();
        p1.start();
        p2.start();
        for (Thread s : sensores) s.join();             // los sensores han terminado...
        cola.put(FIN);                                  // ...un FIN por cada procesador
        cola.put(FIN);
        p1.join();
        p2.join();

        System.out.println("Lecturas: " + lecturas.get() + " (esperadas 12)");
        System.out.println("Suma enviada " + sumaEnviada.get() + " · procesada " + sumaProcesada.get());
        System.out.printf("Media: %.1f ºC%n", sumaProcesada.get() / (double) lecturas.get());
    }
}
```

```text
...
    Procesador-1 procesa 26 ºC
Lecturas: 12 (esperadas 12)
Suma enviada 272 · procesada 272
Media: 22.7 ºC
```

**2.** **Dos** avisos de fin, uno por procesador.
**5.** Porque cuando un sensor termina, los otros pueden seguir enviando. Si el sensor más rápido pusiera el `-1`, un procesador se apagaría antes de tiempo. Y con tres sensores habría tres `-1` para dos procesadores: sobraría uno. Quien sabe que **todos** han terminado es el `main`, después de hacer `join()` de los tres.

## Bloque C · Interbloqueo

### C1. ¿Puede haber interbloqueo? ★

| Caso | ¿Interbloqueo? | Por qué |
|---|---|---|
| 1 | **No** | Los dos cogen los cerrojos en el mismo orden (`a` y luego `b`). El que no consigue `a` espera sin tener nada cogido. |
| 2 | **Sí** | Orden cruzado: el hilo 1 puede tener `a` y esperar `b` mientras el hilo 2 tiene `b` y espera `a`. Es el ejemplo del apartado 11. |
| 3 | **No** | Los bloques no están anidados: cada hilo suelta un cerrojo antes de coger el otro. Nunca tiene uno cogido mientras espera el otro. |
| 4 | **No** | El segundo cerrojo se pide con `tryLock()`, que no espera. Si está ocupado, el hilo sigue y suelta el primero. Eso sí: puede que ese hilo no haga su trabajo y tenga que reintentarlo. |

### C2. Los tres filósofos ★★★

**1 y 2.** Se queda colgado siempre: Aristóteles tiene el tenedor 1 y espera el 2; Platón tiene el 2 y espera el 3; Sócrates tiene el 3 y espera el 1. Es un círculo de esperas.

```text
Sócrates coge el tenedor 3
Platón coge el tenedor 2
Aristóteles coge el tenedor 1
¡Interbloqueo! Nadie come
```

**3.** Hay que cambiar a **Sócrates**, que es el único que coge primero un tenedor con número más alto (el 3 antes que el 1):

```java
public class FilosofosArreglado {
    static final Object tenedor1 = new Object();
    static final Object tenedor2 = new Object();
    static final Object tenedor3 = new Object();

    static void pausa(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            // nada
        }
    }

    static void comer(String filosofo, Object izquierdo, String nIzq, Object derecho, String nDer) {
        synchronized (izquierdo) {
            System.out.println(filosofo + " coge el " + nIzq);
            pausa(100);
            synchronized (derecho) {
                System.out.println(filosofo + " coge el " + nDer + " y come");
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread a = new Thread(() -> comer("Aristóteles", tenedor1, "tenedor 1", tenedor2, "tenedor 2"));
        Thread b = new Thread(() -> comer("Platón", tenedor2, "tenedor 2", tenedor3, "tenedor 3"));
        // Sócrates también coge primero el tenedor de número más bajo
        Thread c = new Thread(() -> comer("Sócrates", tenedor1, "tenedor 1", tenedor3, "tenedor 3"));
        Thread[] todos = {a, b, c};
        for (Thread t : todos) {
            t.setDaemon(true);
            t.start();
        }
        for (Thread t : todos) {
            t.join(2000);
        }
        boolean bloqueados = a.isAlive() && b.isAlive() && c.isAlive();
        System.out.println(bloqueados ? "¡Interbloqueo! Nadie come" : "Los tres han comido");
    }
}
```

```text
...
Aristóteles coge el tenedor 2 y come
Sócrates coge el tenedor 1
Sócrates coge el tenedor 3 y come
Los tres han comido
```

**4.** Aristóteles y Sócrates compiten ahora por el tenedor 1 **antes** de coger nada más. El que lo pierde espera con las manos vacías, así que el círculo se rompe: siempre hay alguien que puede coger sus dos tenedores, comer y soltarlos.

### C3. Transferencias en círculo ★★★

**1.** Cada hilo coge el cerrojo de su cuenta origen y espera el de la cuenta destino, que es el origen del hilo siguiente: el 0 espera al 1, el 1 al 2 y el 2 al 0. Un círculo, como en los filósofos.

**2 a 4.**

```java
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class Transferencias3 {
    static int[] saldos = {1000, 1000, 1000};
    static final ReentrantLock[] cerrojos = {new ReentrantLock(), new ReentrantLock(), new ReentrantLock()};
    static final AtomicInteger reintentos = new AtomicInteger();

    static void pausa(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            // nada
        }
    }

    static void transferir(int origen, int destino, int cantidad) {
        while (true) {
            cerrojos[origen].lock();
            try {
                pausa(1);                               // la operación tarda un poco
                if (cerrojos[destino].tryLock()) {      // ¿está libre la segunda cuenta?
                    try {
                        saldos[origen] -= cantidad;
                        saldos[destino] += cantidad;
                        return;
                    } finally {
                        cerrojos[destino].unlock();
                    }
                }
            } finally {
                cerrojos[origen].unlock();
            }
            reintentos.incrementAndGet();               // no pude: suelto y lo vuelvo a intentar
            pausa(ThreadLocalRandom.current().nextInt(1, 5));
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // Cada hilo transfiere de una cuenta a la siguiente: 0→1, 1→2, 2→0 (un círculo)
        Thread[] hilos = new Thread[3];
        for (int i = 0; i < 3; i++) {
            int origen = i;
            int destino = (i + 1) % 3;
            hilos[i] = new Thread(() -> {
                for (int k = 0; k < 1000; k++) {
                    transferir(origen, destino, 10);
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        int total = saldos[0] + saldos[1] + saldos[2];
        System.out.println("Saldos: " + saldos[0] + ", " + saldos[1] + ", " + saldos[2]);
        System.out.println("Total: " + total + " (debe ser 3000) · Reintentos: " + reintentos.get());
    }
}
```

```text
Saldos: 1000, 1000, 1000
Total: 3000 (debe ser 3000) · Reintentos: 2570
```

**4.** El total es 3000 porque cada transferencia resta y suma la misma cantidad con los dos cerrojos cogidos. Cada cuenta acaba con 1000 € porque recibe 1000 transferencias de 10 € y hace otras 1000 de 10 €. El número de reintentos cambia en cada ejecución.

**5.** Coger siempre primero el cerrojo de la cuenta con **número más bajo**: el hilo 2 (de la cuenta 2 a la 0) cogería primero el cerrojo 0 y después el 2. Así no hace falta reintentar.
