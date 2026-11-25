# Boletín 2 · Lock, productor-consumidor e interbloqueo

Nueve ejercicios: tres de cada bloque. En cada bloque, el primero (★) es sencillo y los otros dos (★★★) son más completos.

!!! info "Antes de empezar"
    - Haz primero el **ejercicio autoguiado** del final de cada apartado: [Lock](09-lock.md#ejercicio-autoguiado-el-cajero-con-lock), [productor-consumidor](10-productor-consumidor.md#ejercicio-autoguiado-la-impresora-compartida) e [interbloqueo](11-interbloqueo.md#ejercicio-autoguiado-los-dos-robots).
    - Ejecuta cada programa **varias veces**. Un programa con hilos que sale bien una vez no está bien: tiene que salir bien siempre.
    - Si tus ficheros están dentro de una carpeta (un paquete), la primera línea de cada uno tiene que ser `package nombreCarpeta;`. Si falta, VS Code da el error «Unresolved compilation problem».

## Bloque A · Lock

### A1. Contador de visitas ★

Una web tiene **3 servidores** y cada uno registra **50 000 visitas** en un contador compartido `static int visitas`.

1. Escribe el programa con 3 hilos y protege el `visitas++` con un `ReentrantLock`.
2. Al final imprime `Visitas: 150000 (esperadas 150000)`.
3. Quita el `lock()` y el `unlock()` y ejecútalo tres veces. ¿Qué números salen?

### A2. La sala de reuniones ★★★

En una empresa hay **una sola sala de reuniones** y cinco empleados (Ana, Luis, Marta, Pepe y Sara) quieren usarla a la vez. Cada reunión dura **700 ms**. Ningún empleado está dispuesto a esperar más de **1 segundo**: si en ese tiempo no consigue la sala, hace la reunión por videollamada.

1. La sala es un `ReentrantLock`. Cada empleado es un hilo que llama a `reservar(nombre)`.
2. Usa `tryLock(1, TimeUnit.SECONDS)`. Si lo consigue: imprime «entra en la sala», espera 700 ms, imprime «sale de la sala». Si no: imprime «se cansa de esperar y hace la reunión por videollamada».
3. Cuenta cuántas reuniones se hacen en la sala y cuántas por videollamada con dos `AtomicInteger`, e imprímelo al final.
4. **Antes de ejecutar**, calcula cuántas reuniones caben en la sala. Después comprueba si aciertas.
5. ¿Qué pasa si cada reunión dura 300 ms? ¿Y si cambias `tryLock(1, …)` por `lock()`?

Salida de ejemplo:

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

### A3. La fotocopiadora de la sala de profesores ★★★

Seis profesores quieren usar **la única fotocopiadora** a la vez. Cada copia tarda **150 ms**. Ninguno quiere hacer cola: si la ve ocupada, da una vuelta (200 ms) y vuelve. Lo intenta **como mucho 3 veces**; si a la tercera sigue ocupada, se rinde.

1. Escribe el método `fotocopiar(String quien)` con un bucle de 3 intentos y `tryLock()` (sin tiempo).
2. Imprime en cada intento si fotocopia o si la ve ocupada, y al final «se rinde» si no lo consigue.
3. Cuenta las fotocopias hechas y los que se rinden con `AtomicInteger`. Al final imprime los dos números y su suma: la suma tiene que ser siempre 6.
4. Cuidado: cuando un profesor consigue la fotocopiadora, tiene que salir del bucle (`return`). ¿Qué pasaría si no lo hicieras?
5. ¿Por qué aquí no sirve `synchronized`?

## Bloque B · Productor-consumidor

### B1. La cinta de equipajes ★

En el aeropuerto, el mostrador de facturación (productor) pone **8 maletas** en una cinta donde solo caben **3**. Un operario (consumidor) las va cogiendo y tarda **300 ms** en cargar cada una en el avión.

1. La cinta es una `ArrayBlockingQueue<String>` de capacidad 3. Las maletas se llaman `"maleta-1"`, `"maleta-2"`…
2. El productor hace `put` de las 8 e imprime «Facturada maleta-N». El consumidor hace `take` 8 veces e imprime «El operario carga maleta-N en el avión».
3. Al terminar los dos, el `main` imprime «Todas las maletas están en el avión».
4. Mira la salida: ¿por qué al principio se facturan varias maletas seguidas y luego van de una en una?

### B2. La cadena de montaje ★★★

Una fábrica de sillas tiene tres puestos en cadena, cada uno un hilo:

```text
cortador  ──cola cortadas──▶  pintor  ──cola pintadas──▶  empaquetador
```

- El **cortador** fabrica 5 sillas (`"silla-1"`…`"silla-5"`), tarda 100 ms en cada una y las pone en la cola `cortadas`.
- El **pintor** las coge de `cortadas`, tarda 200 ms en pintar cada una y las pone en `pintadas`.
- El **empaquetador** las coge de `pintadas`, tarda 50 ms y cuenta las cajas.

Las dos colas son `ArrayBlockingQueue` de capacidad 2.

1. Programa los tres hilos. Ni el pintor ni el empaquetador saben cuántas sillas van a llegar: usa el aviso `"FIN"`.
2. ¿Quién pone el `"FIN"` en `cortadas`? ¿Y quién lo pone en `pintadas`?
3. Al terminar, el empaquetador imprime cuántas cajas ha hecho (5) y el `main` imprime «Cadena de montaje parada».
4. El pintor es el puesto más lento. Fíjate en la salida: ¿qué le pasa al cortador cuando la cola `cortadas` se llena?

### B3. Los sensores de temperatura ★★★

Tres sensores (productores) miden la temperatura de un invernadero y dos procesadores (consumidores) analizan las lecturas.

- Cada sensor hace **4 lecturas**: un número al azar entre 15 y 34 (`ThreadLocalRandom.current().nextInt(15, 35)`), lo pone en una `BlockingQueue<Integer>` de capacidad 5 y espera 50 ms.
- Cada procesador coge lecturas de la cola y tarda 80 ms en procesar cada una.

1. Usa como aviso de fin el número `-1` (una temperatura de este invernadero nunca vale `-1`).
2. El `main` arranca todo, espera a los tres sensores y entonces pone los avisos de fin. ¿Cuántos?
3. Usa tres `AtomicInteger`: la suma de lo que envían los sensores, la suma de lo que procesan los procesadores y el número de lecturas procesadas.
4. Al final imprime el número de lecturas (tienen que ser 12), las dos sumas (tienen que coincidir) y la temperatura media con `printf("%.1f", …)`.
5. ¿Por qué no puede poner el `-1` cada sensor al terminar sus lecturas?

## Bloque C · Interbloqueo

### C1. ¿Puede haber interbloqueo? ★

En cada caso hay dos hilos que se ejecutan a la vez y dos cerrojos, `a` y `b`. Di si **puede** haber interbloqueo y por qué. No hace falta programar nada.

**Caso 1**

```java
// Hilo 1                         // Hilo 2
synchronized (a) {                synchronized (a) {
    synchronized (b) {                synchronized (b) {
        ...                               ...
    }                                 }
}                                 }
```

**Caso 2**

```java
// Hilo 1                         // Hilo 2
synchronized (a) {                synchronized (b) {
    synchronized (b) {                synchronized (a) {
        ...                               ...
    }                                 }
}                                 }
```

**Caso 3**

```java
// Hilo 1                         // Hilo 2
synchronized (a) {                synchronized (b) {
    ...                               ...
}                                 }
synchronized (b) {                synchronized (a) {
    ...                               ...
}                                 }
```

**Caso 4**

```java
// Hilo 1                         // Hilo 2
a.lock();                         b.lock();
try {                             try {
    if (b.tryLock()) {                if (a.tryLock()) {
        try { ... }                       try { ... }
        finally { b.unlock(); }           finally { a.unlock(); }
    }                                 }
} finally {                       } finally {
    a.unlock();                       b.unlock();
}                                 }
```

### C2. Los tres filósofos ★★★

Tres filósofos se sientan en una mesa redonda con **tres tenedores**, uno entre cada dos. Para comer, cada uno necesita el tenedor de su izquierda y el de su derecha:

| Filósofo | Coge primero | Después |
|---|---|---|
| Aristóteles | tenedor 1 | tenedor 2 |
| Platón | tenedor 2 | tenedor 3 |
| Sócrates | tenedor 3 | tenedor 1 |

Este programa lo implementa:

```java
public class Filosofos {
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
        Thread c = new Thread(() -> comer("Sócrates", tenedor3, "tenedor 3", tenedor1, "tenedor 1"));
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

1. **Antes de ejecutarlo**, di qué crees que va a pasar. Luego ejecútalo varias veces.
2. Explica con tus palabras el círculo de esperas: quién tiene qué y quién espera a quién.
3. Arréglalo cambiando **una sola línea** para que se coja siempre primero el tenedor con el número más bajo. ¿A qué filósofo hay que cambiarle el orden?
4. ¿Por qué con solo cambiar a uno ya no puede haber interbloqueo?

### C3. Transferencias en círculo ★★★

Tres cuentas con 1000 € cada una. Tres hilos hacen 1000 transferencias de 10 € cada uno, en círculo: el hilo 0 pasa dinero de la cuenta 0 a la 1, el hilo 1 de la 1 a la 2 y el hilo 2 de la 2 a la 0. Cada cuenta tiene su propio `ReentrantLock`.

Este programa se queda colgado:

```java
import java.util.concurrent.locks.ReentrantLock;

public class Transferencias3Mal {
    static int[] saldos = {1000, 1000, 1000};
    static final ReentrantLock[] cerrojos = {new ReentrantLock(), new ReentrantLock(), new ReentrantLock()};

    static void pausa(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            // nada
        }
    }

    static void transferir(int origen, int destino, int cantidad) {
        cerrojos[origen].lock();
        try {
            pausa(1);
            cerrojos[destino].lock();
            try {
                saldos[origen] -= cantidad;
                saldos[destino] += cantidad;
            } finally {
                cerrojos[destino].unlock();
            }
        } finally {
            cerrojos[origen].unlock();
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
            hilos[i].setDaemon(true);                   // para que el programa pueda acabar
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join(3000);
        }
        if (hilos[0].isAlive()) {
            System.out.println("¡Interbloqueo! El programa se ha quedado colgado");
            return;
        }
        int total = saldos[0] + saldos[1] + saldos[2];
        System.out.println("Saldos: " + saldos[0] + ", " + saldos[1] + ", " + saldos[2]);
        System.out.println("Total: " + total + " (debe ser 3000)");
    }
}
```

1. Ejecútalo. ¿Por qué se queda colgado? Dibuja el círculo de esperas.
2. Arréglalo **sin cambiar el orden** en que se cogen los cerrojos: si el hilo no consigue el cerrojo de la cuenta destino con `tryLock()`, suelta el de origen, espera entre 1 y 4 ms al azar y vuelve a intentarlo.
3. Cuenta los reintentos con un `AtomicInteger` e imprímelos al final.
4. Comprueba que el total sigue siendo 3000 en todas las ejecuciones. ¿Por qué cada cuenta acaba otra vez con 1000 €?
5. Propón la otra solución, la del apartado 11.3: ¿en qué orden habría que coger los cerrojos?

!!! success "Soluciones"
<!-- si-visible: temas/tema-2/boletin-2-soluciones.md -->
    Las soluciones están en [Boletín 2: soluciones](boletin-2-soluciones.md).
<!-- fin -->
<!-- si-oculto: temas/tema-2/boletin-2-soluciones.md -->
    Las soluciones se publicarán cuando lo hayamos corregido en clase.
<!-- fin -->
