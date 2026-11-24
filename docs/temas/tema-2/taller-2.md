# Taller 2 · Lock, productor-consumidor e interbloqueo

!!! info "Cómo funciona este taller"
    - **Parte 1, en la pizarra:** resolvemos juntos un ejercicio de cada tema.
    - **Parte 2, por tu cuenta:** un ejercicio de cada tema. Entrega un proyecto con una clase por programa y un `README.md` con las salidas y las respuestas.
    - Antes de empezar, repasa los apartados [9. Lock](09-lock.md), [10. Productor-consumidor](10-productor-consumidor.md) y [11. Interbloqueo](11-interbloqueo.md).

| Tema | En la pizarra | Por tu cuenta |
|---|---|---|
| `Lock` | P1 · El aparcamiento con barrera | L1 · La hucha con `Lock` |
| Productor-consumidor | P2 · La panadería | PC1 · La cocina del restaurante |
| Interbloqueo | P3 · El tenedor y el cuchillo | I1 · Las transferencias que se quedan colgadas |

## Parte 1 · En la pizarra

### P1 · Lock: el aparcamiento con barrera

Es el aparcamiento del primer taller: 3 plazas y 5 coches. Allí lo arreglamos con `synchronized`; ahora lo hacemos con un `ReentrantLock`, que hace de **barrera**: el coche que la coge entra a mirar si hay plaza, y al salir la suelta para el siguiente.

```java
import java.util.concurrent.locks.ReentrantLock;

public class AparcamientoLock {
    static int plazasLibres = 3;
    static final ReentrantLock barrera = new ReentrantLock();   // la barrera del aparcamiento

    static void entrar(String coche) {
        barrera.lock();                         // espera su turno en la barrera
        try {
            if (plazasLibres > 0) {
                try {
                    Thread.sleep(10);           // el coche maniobra
                } catch (InterruptedException e) {
                    return;                     // el finally suelta la barrera igualmente
                }
                plazasLibres--;
                System.out.println(coche + " aparca. Quedan " + plazasLibres);
            } else {
                System.out.println(coche + ": completo");
            }
        } finally {
            barrera.unlock();                   // deja pasar al siguiente
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread[] coches = new Thread[5];
        for (int i = 0; i < coches.length; i++) {
            String nombre = "Coche-" + (i + 1);
            coches[i] = new Thread(() -> entrar(nombre));
            coches[i].start();
        }
        for (Thread c : coches) {
            c.join();
        }
        System.out.println("Plazas libres al final: " + plazasLibres);
    }
}
```

```text
Coche-1 aparca. Quedan 2
Coche-2 aparca. Quedan 1
Coche-3 aparca. Quedan 0
Coche-4: completo
Coche-5: completo
Plazas libres al final: 0
```

- `barrera.lock()` hace lo mismo que el `synchronized` del primer taller: solo entra un coche a la vez.
- El `unlock()` va en el `finally`. Así la barrera se suelta **siempre**: cuando el coche aparca, cuando está completo y también si el `sleep` es interrumpido y se sale con `return`.
- Prueba a quitar el `finally` y poner el `unlock()` al final: si un coche saliera por el `return`, los demás se quedarían esperando para siempre.

### P2 · Productor-consumidor: la panadería

Un panadero hace 8 panes rápido y los deja en un mostrador donde caben 3. Un cliente se los lleva despacio. Es el ejemplo del [apartado 10](10-productor-consumidor.md#103-ejemplo-la-panaderia):

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class Panaderia {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> mostrador = new ArrayBlockingQueue<>(3);   // caben 3 panes

        Thread panadero = new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    Thread.sleep(100);          // hornear es rápido
                    String pan = "pan " + i;
                    System.out.println("Panadero tiene listo el " + pan);
                    mostrador.put(pan);         // si el mostrador está lleno, espera aquí
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        Thread cliente = new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    String pan = mostrador.take();   // si el mostrador está vacío, espera aquí
                    System.out.println("    Cliente se lleva " + pan);
                    Thread.sleep(400);          // comer es lento
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        panadero.start();
        cliente.start();
        panadero.join();
        cliente.join();
        System.out.println("Panadería cerrada");
    }
}
```

En la pizarra, dibuja el mostrador como tres casillas y ve rellenándolas con la salida:

```text
Panadero tiene listo el pan 1
    Cliente se lleva pan 1
Panadero tiene listo el pan 2
Panadero tiene listo el pan 3
Panadero tiene listo el pan 4
    Cliente se lleva pan 2
Panadero tiene listo el pan 5
Panadero tiene listo el pan 6
    Cliente se lleva pan 3
...
```

- Cuando el panadero tiene listo el pan 6, en el mostrador están el 3, el 4 y el 5: está **lleno**. El `put()` del pan 6 espera hasta que el cliente se lleve el 3.
- Si cambias los tiempos para que el cliente sea más rápido que el panadero, será `take()` el que espere con el mostrador **vacío**.

### P3 · Interbloqueo: el tenedor y el cuchillo

Ana coge primero el tenedor y Luis primero el cuchillo. Es el ejemplo del [apartado 11](11-interbloqueo.md):

```java
public class Interbloqueo {
    static final Object tenedor = new Object();
    static final Object cuchillo = new Object();

    static void pausa() {
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            // nada
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread ana = new Thread(() -> {
            synchronized (tenedor) {
                System.out.println("Ana coge el tenedor");
                pausa();
                System.out.println("Ana espera el cuchillo...");
                synchronized (cuchillo) {
                    System.out.println("Ana come");
                }
            }
        }, "Ana");
        Thread luis = new Thread(() -> {
            synchronized (cuchillo) {
                System.out.println("Luis coge el cuchillo");
                pausa();
                System.out.println("Luis espera el tenedor...");
                synchronized (tenedor) {
                    System.out.println("Luis come");
                }
            }
        }, "Luis");
        ana.setDaemon(true);                    // para que el programa pueda terminar
        luis.setDaemon(true);
        ana.start();
        luis.start();

        ana.join(2000);                         // esperamos como mucho 2 segundos
        luis.join(2000);
        if (ana.isAlive() && luis.isAlive()) {
            System.out.println("¡Interbloqueo! Ana: " + ana.getState() + " · Luis: " + luis.getState());
        } else {
            System.out.println("Los dos han comido");
        }
    }
}
```

```text
Ana coge el tenedor
Luis coge el cuchillo
Luis espera el tenedor...
Ana espera el cuchillo...
¡Interbloqueo! Ana: BLOCKED · Luis: BLOCKED
```

1. Haz en la pizarra la tabla de pasos: Ana tiene el tenedor y espera el cuchillo; Luis tiene el cuchillo y espera el tenedor. Ninguno avanza.
2. Señala las cuatro condiciones del interbloqueo en el ejemplo.
3. **Arréglalo:** que Luis coja también primero el tenedor. Ahora sale «Los dos han comido».

## Parte 2 · Por tu cuenta

### L1 · Lock: la hucha con `Lock`

Retoma la clase `Hucha` del ejercicio R2 del primer taller (dos hermanos meten 1 € 10.000 veces y dos sacan 1 € 10.000 veces; empieza con 20.000 €).

1. Cambia los `synchronized` por un `ReentrantLock` guardado como atributo de la hucha.
2. Protege `meter`, `sacar` y `getDinero` con `lock()` y `unlock()`. El `unlock()`, siempre en un `finally`.
3. Comprueba que sale siempre 20.000.
4. En `sacar` hay un `return false` dentro del `try`. ¿Se suelta el cerrojo en ese caso? ¿Por qué?

### PC1 · Productor-consumidor: la cocina del restaurante

Escribe el programa completo:

1. Un **camarero** (productor) apunta 8 comandas, una cada 100 ms, y las mete en una `LinkedBlockingQueue<String>` llamada `comandas`. Por ejemplo: paella, tortilla, gazpacho, croquetas, ensalada, pescaíto, flamenquín y salmorejo.
2. Dos **cocineros** (consumidores) sacan comandas de la cola con `take()` y tardan 300 ms en cocinar cada plato. Cada uno imprime qué cocina.
3. Cuando el camarero termina, mete en la cola **un `"FIN"` por cada cocinero**. Cuando un cocinero saca `"FIN"`, imprime cuántos platos ha cocinado y termina.
4. El `main` espera a los tres hilos e imprime «Cocina cerrada».
5. ¿Qué pasaría si el camarero solo metiera un `"FIN"`? Pruébalo.
6. ¿Por qué no hace falta `synchronized` para usar la cola?

### I1 · Interbloqueo: las transferencias que se quedan colgadas

Este programa hace 100.000 transferencias de Ana a Luis y, a la vez, 100.000 de Luis a Ana:

```java
public class Transferencias {

    static class Cuenta {
        final String nombre;
        int saldo;

        Cuenta(String nombre, int saldo) {
            this.nombre = nombre;
            this.saldo = saldo;
        }
    }

    static void transferir(Cuenta origen, Cuenta destino, int cantidad) {
        synchronized (origen) {                 // primero bloqueo el origen...
            synchronized (destino) {            // ...y luego el destino
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

1. Ejecútalo varias veces. ¿Qué pasa?
2. Explica con una tabla de pasos por qué se queda colgado. Pista: ¿qué cerrojo coge primero cada hilo?
3. Arréglalo haciendo que los dos hilos cojan los cerrojos **en el mismo orden**: primero la cuenta cuyo nombre va antes en orden alfabético, sea el origen o el destino. Para comparar dos nombres, usa `nombre1.compareTo(nombre2)`, que da un número negativo si `nombre1` va antes.
4. Comprueba que termina siempre y que el total sigue siendo 2000.

<!-- si-visible: temas/tema-2/taller-2-soluciones.md -->
!!! success "Soluciones"
    Cuando termines, revisa tus programas con las [soluciones del taller 2](taller-2-soluciones.md).
<!-- fin -->
