# Taller 2 · Soluciones

Soluciones de la [Parte 2 del taller 2](taller-2.md#parte-2-por-tu-cuenta). Los programas son completos y están probados con JDK 21.

## L1 · La hucha con `Lock`

```java
import java.util.concurrent.locks.ReentrantLock;

public class HuchaLock {
    private int dinero = 20_000;
    private final ReentrantLock cerrojo = new ReentrantLock();

    public void meter(int cantidad) {
        cerrojo.lock();
        try {
            dinero += cantidad;
        } finally {
            cerrojo.unlock();
        }
    }

    public boolean sacar(int cantidad) {
        cerrojo.lock();
        try {
            if (dinero < cantidad) {
                return false;                   // el finally suelta el cerrojo antes de salir
            }
            dinero -= cantidad;
            return true;
        } finally {
            cerrojo.unlock();
        }
    }

    public int getDinero() {
        cerrojo.lock();
        try {
            return dinero;
        } finally {
            cerrojo.unlock();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        HuchaLock hucha = new HuchaLock();
        Thread[] hermanos = new Thread[4];
        for (int i = 0; i < hermanos.length; i++) {
            boolean mete = i < 2;
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

```text
Esperado 20000, obtenido 20000
```

- El cerrojo es un **atributo** de la hucha: como los cuatro hermanos usan la misma hucha, usan el mismo cerrojo.
- Cada método sigue el mismo patrón: `lock()`, `try` con la sección crítica y `unlock()` en el `finally`.
- **Pregunta 4:** sí, el cerrojo se suelta. El `finally` se ejecuta **siempre** al salir del `try`, también cuando se sale con `return`. Por eso el `unlock()` va ahí. Lo mismo pasa con el `return dinero;` de `getDinero()`.

## PC1 · La cocina del restaurante

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class Cocina {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> comandas = new LinkedBlockingQueue<>();

        Thread camarero = new Thread(() -> {
            String[] platos = {"paella", "tortilla", "gazpacho", "croquetas",
                               "ensalada", "pescaíto", "flamenquín", "salmorejo"};
            try {
                for (String plato : platos) {
                    comandas.put(plato);
                    System.out.println("Camarero apunta: " + plato);
                    Thread.sleep(100);
                }
                comandas.put("FIN");            // un aviso de cierre por cada cocinero
                comandas.put("FIN");
            } catch (InterruptedException e) {
                return;
            }
        }, "Camarero");

        Runnable cocinar = () -> {
            String yo = Thread.currentThread().getName();
            int hechos = 0;
            try {
                while (true) {
                    String plato = comandas.take();
                    if (plato.equals("FIN")) {
                        break;                  // no hay más comandas: termino
                    }
                    System.out.println("    " + yo + " cocina " + plato);
                    Thread.sleep(300);
                    hechos++;
                }
            } catch (InterruptedException e) {
                return;
            }
            System.out.println("    " + yo + " termina: " + hechos + " platos");
        };
        Thread cocinero1 = new Thread(cocinar, "Cocinero-1");
        Thread cocinero2 = new Thread(cocinar, "Cocinero-2");

        camarero.start();
        cocinero1.start();
        cocinero2.start();
        camarero.join();
        cocinero1.join();
        cocinero2.join();
        System.out.println("Cocina cerrada");
    }
}
```

```text
Camarero apunta: paella
    Cocinero-1 cocina paella
Camarero apunta: tortilla
    Cocinero-2 cocina tortilla
Camarero apunta: gazpacho
Camarero apunta: croquetas
    Cocinero-1 cocina gazpacho
    Cocinero-2 cocina croquetas
...
    Cocinero-1 termina: 4 platos
    Cocinero-2 termina: 4 platos
Cocina cerrada
```

- Los dos cocineros ejecutan la misma tarea (`cocinar`) en dos hilos con nombres distintos.
- `take()` espera si no hay comandas: cuando el camarero va más lento que los cocineros, estos esperan sin gastar CPU.
- El reparto entre los dos cocineros puede cambiar entre ejecuciones; lo importante es que entre los dos cocinan los 8 platos.
- **Pregunta 5:** con un solo `"FIN"`, lo saca uno de los cocineros y termina, pero el otro se queda esperando en `take()` para siempre, y el programa no acaba. Cada aviso solo lo saca un consumidor.
- **Pregunta 6:** porque `put()` y `take()` ya están protegidos por dentro. La cola está hecha para que la usen varios hilos a la vez.

## I1 · Las transferencias que se quedan colgadas

1. El programa se queda colgado casi siempre. En tres ejecuciones, las tres veces imprimió:

    ```text
    ¡Se ha quedado bloqueado! t1: BLOCKED · t2: BLOCKED
    ```

2. El hilo 1 transfiere de Ana a Luis, así que coge primero el cerrojo de **Ana**. El hilo 2 transfiere de Luis a Ana, así que coge primero el de **Luis**:

    | t | Hilo 1 (Ana → Luis) | Hilo 2 (Luis → Ana) |
    |---|---|---|
    | 1 | coge el cerrojo de Ana | |
    | 2 | | coge el cerrojo de Luis |
    | 3 | quiere el de Luis: **espera** | |
    | 4 | | quiere el de Ana: **espera** |

    Es el mismo interbloqueo que el del tenedor y el cuchillo.

3. Se cogen siempre en orden alfabético de nombre:

```java
public class TransferenciasArreglado {

    static class Cuenta {
        final String nombre;
        int saldo;

        Cuenta(String nombre, int saldo) {
            this.nombre = nombre;
            this.saldo = saldo;
        }
    }

    static void transferir(Cuenta origen, Cuenta destino, int cantidad) {
        // Siempre se bloquea primero la cuenta cuyo nombre va antes en orden alfabético,
        // sea origen o destino. Así los dos hilos cogen los cerrojos en el mismo orden.
        Cuenta primera = origen;
        Cuenta segunda = destino;
        if (origen.nombre.compareTo(destino.nombre) > 0) {
            primera = destino;
            segunda = origen;
        }
        synchronized (primera) {
            synchronized (segunda) {
                origen.saldo -= cantidad;
                destino.saldo += cantidad;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Cuenta ana = new Cuenta("Ana", 1000);
        Cuenta luis = new Cuenta("Luis", 1000);

        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 100_000; i++) transferir(ana, luis, 1);
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 100_000; i++) transferir(luis, ana, 1);
        });
        t1.setDaemon(true);
        t2.setDaemon(true);
        t1.start();
        t2.start();
        t1.join(3000);
        t2.join(3000);

        if (t1.isAlive() || t2.isAlive()) {
            System.out.println("¡Se ha quedado bloqueado! t1: " + t1.getState() + " · t2: " + t2.getState());
        } else {
            System.out.println("Terminado. Ana: " + ana.saldo + " · Luis: " + luis.saldo
                    + " · Total: " + (ana.saldo + luis.saldo));
        }
    }
}
```

```text
Terminado. Ana: 1000 · Luis: 1000 · Total: 2000
```

4. Termina siempre, y el total es 2000 porque cada transferencia resta y suma la misma cantidad dentro de los dos cerrojos. Como cada hilo hace el mismo número de transferencias en cada sentido, los dos saldos vuelven a quedarse en 1000.
