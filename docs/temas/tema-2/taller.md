# Taller práctico · Condición de carrera, synchronized y clases atómicas

!!! info "Cómo funciona este taller"
    - **Parte 1, en la pizarra:** resolvemos juntos un ejercicio de cada tipo, paso a paso.
    - **Parte 2, por tu cuenta:** haces **dos ejercicios de cada tipo**. Entrega un proyecto con una clase por programa y un `README.md` con las tablas, las salidas y las respuestas.
    - Ejecuta cada programa **varias veces**: una ejecución correcta no demuestra que el programa esté bien.

| Tipo | En la pizarra | Por tu cuenta |
|---|---|---|
| Condición de carrera | P1 · ¿Qué saldo queda? | C1 · El termostato · C2 · La última entrada |
| `synchronized` | P2 · El aparcamiento | S1 · La urna de votación · S2 · El marcador que no protege |
| Clases atómicas | P3 · Los likes | A1 · Los tickets de la cola · A2 · Estadísticas de descargas |

!!! tip "Lo que tienes que tener claro antes de empezar"
    - Hay **condición de carrera** cuando se dan tres cosas a la vez: varios hilos, un dato compartido y al menos un hilo que escribe.
    - La **sección crítica** es el código que usa ese dato. Si hay que comprobar y luego actuar, incluye las dos cosas.
    - **`synchronized`** deja entrar a un solo hilo a la vez, siempre que todos usen **el mismo cerrojo**.
    - Una **clase atómica** hace leer, modificar y escribir en un solo paso, pero solo sobre **una** variable.

## Parte 1 · En la pizarra

### P1 · Condición de carrera: ¿qué saldo queda?

Una cuenta tiene **100 €**. A la vez, el hilo A ingresa 50 € y el hilo B paga 30 €. Cada operación se hace en tres pasos: **leer** el saldo, **calcular** el nuevo y **escribirlo**.

**¿Qué saldos finales son posibles?**

Hay tres. El correcto, 120 €, sale cuando una operación termina antes de que empiece la otra:

| t | Hilo A (+50) | Hilo B (−30) | `saldo` |
|---|---|---|---|
| 1 | lee 100 | | 100 |
| 2 | escribe 150 | | 150 |
| 3 | | lee 150 | 150 |
| 4 | | escribe 120 | **120**: correcto |

Pero si los dos leen **antes** de que ninguno escriba, gana el que escribe el último:

| t | Hilo A (+50) | Hilo B (−30) | `saldo` |
|---|---|---|---|
| 1 | lee 100 | | 100 |
| 2 | | lee 100 | 100 |
| 3 | | escribe 70 | 70 |
| 4 | escribe 150 | | **150**: se ha perdido el pago |

| t | Hilo A (+50) | Hilo B (−30) | `saldo` |
|---|---|---|---|
| 1 | lee 100 | | 100 |
| 2 | | lee 100 | 100 |
| 3 | escribe 150 | | 150 |
| 4 | | escribe 70 | **70**: se ha perdido el ingreso |

Lo comprobamos repitiendo la operación 200 veces:

```java
public class Saldo {
    static int saldo;

    // Cada operación en tres pasos: leer, calcular y escribir
    static void operar(int cantidad) {
        int leido = saldo;                          // 1. leer
        int nuevo = leido + cantidad;               // 2. calcular
        try {
            Thread.sleep(1);                        // da ocasión a que el otro hilo se cuele
        } catch (InterruptedException e) {
            return;
        }
        saldo = nuevo;                              // 3. escribir
    }

    public static void main(String[] args) throws InterruptedException {
        int veces70 = 0;
        int veces120 = 0;
        int veces150 = 0;

        for (int prueba = 0; prueba < 200; prueba++) {
            saldo = 100;
            Thread a = new Thread(() -> operar(+50));   // ingreso
            Thread b = new Thread(() -> operar(-30));   // pago
            a.start();
            b.start();
            a.join();
            b.join();

            if (saldo == 70) {
                veces70++;
            } else if (saldo == 120) {
                veces120++;
            } else if (saldo == 150) {
                veces150++;
            }
        }

        System.out.println("Saldo 120 (correcto): " + veces120 + " veces");
        System.out.println("Saldo 150 (se pierde el pago): " + veces150 + " veces");
        System.out.println("Saldo 70 (se pierde el ingreso): " + veces70 + " veces");
    }
}
```

```text
Saldo 120 (correcto): 1 veces
Saldo 150 (se pierde el pago): 33 veces
Saldo 70 (se pierde el ingreso): 166 veces
```

!!! note "¿Por qué casi nunca sale 120?"
    La pausa de 1 ms entre leer y escribir hace que casi siempre los dos hilos lean antes de que el otro escriba. Sin la pausa, 120 saldría casi siempre y el error, muy de vez en cuando. Eso es justo lo peligroso: el fallo puede no aparecer en las pruebas.

**Sección crítica:** desde que se lee el saldo hasta que se escribe.

#### Cómo solucionarlo

Hay que conseguir que leer, calcular y escribir se hagan **sin que el otro hilo pueda colarse en medio**. Basta con añadir `synchronized` al método `operar`. Como es `static`, el cerrojo es la clase, el mismo para los dos hilos:

```java
// synchronized: leer, calcular y escribir sin que el otro hilo pueda colarse
static synchronized void operar(int cantidad) {
    int leido = saldo;                          // 1. leer
    int nuevo = leido + cantidad;               // 2. calcular
    try {
        Thread.sleep(1);
    } catch (InterruptedException e) {
        return;
    }
    saldo = nuevo;                              // 3. escribir
}
```

El resto del programa no cambia. Ahora sale **siempre** 120:

```text
Saldo 120 (correcto): 200 veces
Saldo 150 (se pierde el pago): 0 veces
Saldo 70 (se pierde el ingreso): 0 veces
```

Qué pasa ahora cuando los dos hilos llegan a la vez:

| t | Hilo A (+50) | Hilo B (−30) | `saldo` |
|---|---|---|---|
| 1 | coge el cerrojo y lee 100 | quiere entrar: espera (BLOCKED) | 100 |
| 2 | escribe 150 y suelta el cerrojo | | 150 |
| 3 | | coge el cerrojo y lee 150 | 150 |
| 4 | | escribe 120 y suelta el cerrojo | **120** |

Da igual quién entre primero: si entra antes B, A lee 70 y escribe 120. El resultado es siempre el correcto, porque **nunca leen los dos antes de que el otro escriba**.

!!! note "¿Y con una clase atómica?"
    También valdría un `AtomicInteger saldo` y `saldo.addAndGet(cantidad)`, que suma en un solo paso. Aquí usamos `synchronized` porque así se ve el leer, calcular y escribir dentro de la sección crítica.

### P2 · synchronized: el aparcamiento

Un aparcamiento tiene **3 plazas** y llegan **5 coches** a la vez, cada uno en su hilo.

```java
public class Aparcamiento {
    static int plazasLibres = 3;

    // Sin protección: dos coches pueden ver la misma plaza libre
    static void entrar(String coche) {
        if (plazasLibres > 0) {                     // comprobar
            try {
                Thread.sleep(10);                   // el coche maniobra
            } catch (InterruptedException e) {
                return;
            }
            plazasLibres--;                         // actuar
            System.out.println(coche + " aparca. Quedan " + plazasLibres);
        } else {
            System.out.println(coche + ": completo");
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
Coche-5 aparca. Quedan -2
Coche-3 aparca. Quedan 1
Coche-1 aparca. Quedan 2
Coche-4 aparca. Quedan -1
Coche-2 aparca. Quedan 0
Plazas libres al final: -2
```

Aparcan los cinco y quedan **−2 plazas**. Es un **comprobar y actuar**: todos ven que hay plazas libres antes de que ninguno reste.

**La solución:** añadir la palabra `synchronized` al método `entrar`. El resto del código no cambia:

```java
static synchronized void entrar(String coche) {
    // el mismo cuerpo que antes
}
```

`synchronized` funciona como **la única llave de la barrera del aparcamiento**. Para entrar en el método, un coche tiene que coger la llave; al salir, la devuelve. Mientras un coche tiene la llave, los demás esperan en la cola.

Para que funcione, todos los coches tienen que pelearse por **la misma llave**. Aquí es así porque `entrar` es `static`: pertenece a la clase `Aparcamiento`, no a ningún objeto, y Java usa la propia clase como llave. Como solo hay una clase `Aparcamiento`, solo hay una llave para los cinco coches.

```text
Coche-1 aparca. Quedan 2
Coche-5 aparca. Quedan 1
Coche-4 aparca. Quedan 0
Coche-3: completo
Coche-2: completo
Plazas libres al final: 0
```

Ahora entran de uno en uno: mientras un coche está dentro de `entrar`, los demás esperan en estado BLOCKED. Cuando le toca al cuarto, ya no quedan plazas.

### P3 · Clases atómicas: los likes

Cuatro usuarios dan 50.000 likes cada uno a la misma publicación. Contamos con un `int` y con un `AtomicInteger` a la vez:

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Likes {
    static int likesInt = 0;                                  // sin protección
    static AtomicInteger likesAtomico = new AtomicInteger();  // atómico

    public static void main(String[] args) throws InterruptedException {
        Thread[] usuarios = new Thread[4];
        for (int i = 0; i < usuarios.length; i++) {
            usuarios[i] = new Thread(() -> {
                for (int j = 0; j < 50_000; j++) {
                    likesInt++;
                    likesAtomico.incrementAndGet();
                }
            });
            usuarios[i].start();
        }
        for (Thread u : usuarios) {
            u.join();
        }
        System.out.println("Esperado:      200000");
        System.out.println("int:           " + likesInt);
        System.out.println("AtomicInteger: " + likesAtomico.get());
    }
}
```

```text
Esperado:      200000
int:           198692
AtomicInteger: 200000
```

- `likesInt++` son tres pasos y se pierden incrementos. El número cambia en cada ejecución.
- `likesAtomico.incrementAndGet()` hace los tres pasos de una vez: sale siempre 200.000, sin `synchronized` y sin que ningún hilo se quede bloqueado.

## Parte 2 · Por tu cuenta

### C1 · Condición de carrera: el termostato

Una calefacción sube la temperatura 100.000 veces y un aire acondicionado la baja otras 100.000. Empieza en 20 °C.

```java
public class Termostato {
    static int temperatura = 20;

    public static void main(String[] args) throws InterruptedException {
        Thread calefaccion = new Thread(() -> {
            for (int i = 0; i < 100_000; i++) temperatura++;
        });
        Thread aire = new Thread(() -> {
            for (int i = 0; i < 100_000; i++) temperatura--;
        });
        calefaccion.start();
        aire.start();
        calefaccion.join();
        aire.join();
        System.out.println("Esperado 20, obtenido " + temperatura);
    }
}
```

1. Ejecútalo **5 veces** y apunta los resultados en una tabla.
2. Explica, con una tabla de pasos como las de P1, cómo puede perderse una subida o una bajada.
3. ¿Cuál es el recurso compartido? ¿Y la sección crítica?
4. Arréglalo con `synchronized` y comprueba que sale siempre 20.

### C2 · Condición de carrera: la última entrada

Queda **una entrada** para un concierto y Ana y Luis intentan comprarla a la vez:

```java
static int asientos = 1;

static void comprar(String quien) {
    if (asientos > 0) {                                   // 1
        System.out.println(quien + " ve que queda una entrada");
        asientos--;                                       // 2
        System.out.println(quien + " compra. Quedan " + asientos);
    } else {
        System.out.println(quien + ": agotado");
    }
}
```

1. Completa una tabla de pasos en la que **los dos compran** la misma entrada. Usa las líneas 1 y 2 del código.
2. Haz otra tabla en la que todo va bien: uno compra y el otro recibe «agotado».
3. Marca la sección crítica. ¿Por qué no basta con proteger solo la línea 2?
4. Copia el código en una clase `Entradas` con un `main` que lance los dos hilos y ejecútalo varias veces. ¿Falla siempre? ¿Por qué?

### S1 · synchronized: la urna de votación

Cuatro mesas electorales meten 25.000 votos cada una en la misma urna. La urna lleva tres contadores: votos de A, votos de B y total.

```java
import java.util.concurrent.ThreadLocalRandom;

public class Votacion {

    static class Urna {
        private int votosA = 0;
        private int votosB = 0;
        private int total = 0;

        public void votar(char candidato) {
            if (candidato == 'A') {
                votosA++;
            } else {
                votosB++;
            }
            total++;
        }

        public String resultados() {
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

1. Ejecútalo varias veces. ¿Sale `total=100000`? ¿Cuadra `A + B` con el total?
2. Arréglalo con `synchronized`. ¿Qué métodos tienes que proteger? ¿Por qué también `resultados()`?
3. ¿Cuál es el cerrojo de esos métodos? ¿Por qué es importante que las cuatro mesas usen el mismo objeto `urna`?

### S2 · synchronized: el marcador que no protege

Este programa usa `synchronized`… y aun así falla:

```java
public class Marcador {

    static class Puntos {
        private static int puntos = 0;                        // static: compartido por TODOS los objetos

        public synchronized void sumar() {                    // cerrojo: this
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
                Puntos p = new Puntos();                      // cada jugador crea su objeto
                for (int j = 0; j < 100_000; j++) {
                    p.sumar();
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

1. Ejecútalo varias veces y comprueba que no sale 400.000.
2. Explica por qué `synchronized` no está protegiendo nada. Pista: ¿cuál es el cerrojo de `sumar()`? ¿Cuántos objetos `Puntos` hay?
3. Arréglalo de **dos formas distintas** y comprueba que las dos funcionan.

### A1 · Clases atómicas: los tickets de la cola

Cinco taquillas reparten números de turno a la vez. Cada número debe darse **una sola vez**.

```java
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

public class Tickets {
    static AtomicInteger siguiente = new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        int taquillas = 5;
        int porTaquilla = 20_000;
        List<List<Integer>> repartidos = new ArrayList<>();
        Thread[] hilos = new Thread[taquillas];
        for (int i = 0; i < taquillas; i++) {
            List<Integer> mios = new ArrayList<>();           // cada taquilla, su lista
            repartidos.add(mios);
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < porTaquilla; j++) {
                    mios.add(siguiente.getAndIncrement());    // da el número y pasa al siguiente
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        Set<Integer> distintos = new HashSet<>();
        int total = 0;
        for (List<Integer> l : repartidos) {
            distintos.addAll(l);
            total += l.size();
        }
        System.out.println("Tickets repartidos: " + total + " · distintos: " + distintos.size()
                + " · repetidos: " + (total - distintos.size()));
    }
}
```

1. Ejecútalo varias veces. ¿Hay tickets repetidos?
2. Cambia el `AtomicInteger` por un `static int siguiente` y `siguiente++`. Ejecútalo varias veces. ¿Qué pasa ahora?
3. ¿Por qué `getAndIncrement()` garantiza que dos taquillas nunca den el mismo número?
4. ¿Qué diferencia hay entre `getAndIncrement()` e `incrementAndGet()`? ¿Cuál de los dos da el 0 como primer ticket?

### A2 · Clases atómicas: estadísticas de descargas

Escribe tú el programa completo:

1. Cuatro hilos simulan **250 descargas cada uno**. Cada descarga tiene un tamaño aleatorio entre 1 y 100 MB.
2. Lleva dos estadísticas compartidas: el **número de ficheros** descargados (`AtomicInteger`) y el **total de megas** (`AtomicLong`, con `addAndGet`).
3. Para comprobar que no se pierde nada, cada hilo suma también sus megas en una **variable local** y la guarda en su posición de un array al terminar.
4. Al final, el `main` muestra los ficheros (deben ser 1000) y compara los megas de la `AtomicLong` con la suma del array. Deben coincidir siempre.
5. ¿Por qué el total de megas se guarda en un `AtomicLong` y no en un `AtomicInteger`?
6. ¿Podrías usar tres clases atómicas en la urna de S1 en lugar de `synchronized`? ¿Qué problema tendría `resultados()`?

<!-- si-visible: temas/tema-2/taller-soluciones.md -->
!!! success "Soluciones"
    Cuando termines, revisa tus programas con las [soluciones del taller](taller-soluciones.md).
<!-- fin -->
