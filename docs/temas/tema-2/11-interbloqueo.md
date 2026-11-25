# 11. Interbloqueo

Los cerrojos evitan las condiciones de carrera, pero traen un problema nuevo: dos hilos pueden quedarse **esperándose el uno al otro para siempre**. Es el **interbloqueo** (*deadlock*).

## 11.1 Ana, Luis, un tenedor y un cuchillo

Para comer hacen falta un tenedor y un cuchillo, y solo hay uno de cada. Ana coge primero el tenedor y Luis coge primero el cuchillo:

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

| t | Ana | Luis |
|---|---|---|
| 1 | coge el tenedor | |
| 2 | | coge el cuchillo |
| 3 | quiere el cuchillo: lo tiene Luis, **espera** | |
| 4 | | quiere el tenedor: lo tiene Ana, **espera** |
| 5 | sigue esperando… | sigue esperando… |

Ninguno suelta lo que tiene hasta que consiga lo otro, así que **ninguno avanza nunca**. Los dos están en estado BLOCKED. No hay ningún error ni excepción: el programa simplemente se queda parado.

!!! note "Por qué este ejemplo sí termina"
    En un programa normal, el interbloqueo deja el programa colgado y hay que pararlo a mano. Aquí los dos hilos son **demonios** y el `main` espera como mucho 2 segundos con `join(2000)`. Así podemos ver el interbloqueo, imprimir el estado de los hilos y terminar.

## 11.2 Cuándo puede haber interbloqueo

Hacen falta **cuatro condiciones a la vez**:

| Condición | En el ejemplo |
|---|---|
| **Exclusión mutua:** cada recurso solo lo puede tener un hilo. | Solo hay un tenedor y un cuchillo. |
| **Retener y esperar:** un hilo tiene un recurso y espera otro. | Ana tiene el tenedor y espera el cuchillo. |
| **Sin expropiación:** nadie puede quitarle a un hilo lo que tiene. | Nadie le quita el tenedor a Ana. |
| **Espera circular:** cada hilo espera algo que tiene el siguiente, en círculo. | Ana espera a Luis y Luis espera a Ana. |

Basta con **romper una** de las cuatro para que no pueda haber interbloqueo.

## 11.3 La solución más sencilla: coger los cerrojos siempre en el mismo orden

Si los dos cogen **primero el tenedor y después el cuchillo**, ya no puede haber espera circular. El que consigue el tenedor come; el otro espera al tenedor sin tener nada, y cuando el primero termina, come él.

```java
Thread luis = new Thread(() -> {
    synchronized (tenedor) {            // el mismo orden que Ana: primero el tenedor
        System.out.println("Luis coge el tenedor");
        pausa();
        System.out.println("Luis espera el cuchillo...");
        synchronized (cuchillo) {
            System.out.println("Luis come");
        }
    }
}, "Luis");
```

```text
Ana coge el tenedor
Ana espera el cuchillo...
Ana come
Luis coge el tenedor
Luis espera el cuchillo...
Luis come
Los dos han comido
```

!!! tip "Regla práctica"
    Si un hilo necesita **varios cerrojos a la vez**, todos los hilos deben cogerlos **en el mismo orden**. Y si puedes, evita necesitar varios cerrojos: con uno solo no puede haber interbloqueo.

## 11.4 Inanición

La **inanición** (*starvation*) es un problema parecido, pero distinto: el programa sí avanza, pero **un hilo concreto nunca consigue el recurso**, porque siempre se lo quitan otros. Por ejemplo, si en una taquilla con `tryLock()` un cliente siempre llega cuando está ocupada, ese cliente nunca compra.

| | Interbloqueo | Inanición |
|---|---|---|
| ¿Avanza el programa? | No: los hilos implicados se quedan parados | Sí: los demás hilos siguen trabajando |
| ¿A quién afecta? | A todos los que se esperan en círculo | A uno o pocos hilos, que nunca consiguen su turno |

## Preguntas de repaso

1. ¿Qué es un interbloqueo? ¿En qué estado quedan los hilos?
2. ¿Cuáles son las cuatro condiciones que tienen que darse a la vez?
3. ¿Por qué coger los cerrojos siempre en el mismo orden evita el interbloqueo?
4. ¿Puede haber interbloqueo si cada hilo solo usa un cerrojo? ¿Por qué?
5. ¿Qué diferencia hay entre interbloqueo e inanición?

## Ejercicio autoguiado: los dos robots

En una fábrica hay dos robots y solo **un martillo** y **un destornillador**. Para montar una pieza, cada robot necesita las dos herramientas. Cada herramienta es un `ReentrantLock`.

### Paso 1 · Provocar el interbloqueo

Escribe `RobotsPaso1` con:

- dos cerrojos `static final ReentrantLock martillo` y `destornillador`.
- un método `montar(String robot, ReentrantLock primera, String nombre1, ReentrantLock segunda, String nombre2)` que coja la primera herramienta, espere 100 ms, coja la segunda y monte la pieza. Cada `lock()` con su `try`/`finally`.
- en el `main`, el Robot-1 coge martillo → destornillador y el Robot-2 coge destornillador → martillo.

Para que el programa no se quede colgado para siempre:

- marca los dos hilos como **demonio** con `setDaemon(true)` (antes del `start()`);
- espéralos con `join(2000)`;
- si después de eso los dos siguen vivos (`isAlive()`), imprime «¡Interbloqueo!» con el estado de cada uno (`getState()`).

Salida esperada, siempre:

```text
Robot-1 coge el martillo
Robot-2 coge el destornillador
Robot-1 espera el destornillador...
Robot-2 espera el martillo...
¡Interbloqueo! Robot-1: WAITING · Robot-2: WAITING
```

**Piensa:** ¿qué cuatro condiciones del apartado 11.2 se cumplen aquí?

??? success "Solución del paso 1"
    ```java
    import java.util.concurrent.locks.ReentrantLock;

    public class RobotsPaso1 {
        static final ReentrantLock martillo = new ReentrantLock();
        static final ReentrantLock destornillador = new ReentrantLock();

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        // Coge las dos herramientas en el orden indicado y monta una pieza
        static void montar(String robot, ReentrantLock primera, String nombre1,
                           ReentrantLock segunda, String nombre2) {
            primera.lock();
            try {
                System.out.println(robot + " coge el " + nombre1);
                pausa(100);
                System.out.println(robot + " espera el " + nombre2 + "...");
                segunda.lock();
                try {
                    System.out.println(robot + " monta la pieza");
                } finally {
                    segunda.unlock();
                }
            } finally {
                primera.unlock();
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread r1 = new Thread(() -> montar("Robot-1", martillo, "martillo", destornillador, "destornillador"));
            Thread r2 = new Thread(() -> montar("Robot-2", destornillador, "destornillador", martillo, "martillo"));
            r1.setDaemon(true);
            r2.setDaemon(true);
            r1.start();
            r2.start();
            r1.join(2000);
            r2.join(2000);
            if (r1.isAlive() && r2.isAlive()) {
                System.out.println("¡Interbloqueo! Robot-1: " + r1.getState() + " · Robot-2: " + r2.getState());
            } else {
                System.out.println("Los dos robots han montado su pieza");
            }
        }
    }
    ```

    Los dos están en `WAITING`: es el estado de un hilo parado en `lock()`. (Con `synchronized` saldría `BLOCKED`.)

### Paso 2 · Arreglarlo con el mismo orden

Copia la clase como `RobotsPaso2` y cambia **una sola línea**: que los dos robots cojan las herramientas en el mismo orden (primero el martillo).

Salida esperada, siempre:

```text
Robot-1 coge el martillo
Robot-1 espera el destornillador...
Robot-1 monta la pieza
Robot-2 coge el martillo
Robot-2 espera el destornillador...
Robot-2 monta la pieza
Los dos robots han montado su pieza
```

??? success "Solución del paso 2"
    ```java
    import java.util.concurrent.locks.ReentrantLock;

    public class RobotsPaso2 {
        static final ReentrantLock martillo = new ReentrantLock();
        static final ReentrantLock destornillador = new ReentrantLock();

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        // Coge las dos herramientas en el orden indicado y monta una pieza
        static void montar(String robot, ReentrantLock primera, String nombre1,
                           ReentrantLock segunda, String nombre2) {
            primera.lock();
            try {
                System.out.println(robot + " coge el " + nombre1);
                pausa(100);
                System.out.println(robot + " espera el " + nombre2 + "...");
                segunda.lock();
                try {
                    System.out.println(robot + " monta la pieza");
                } finally {
                    segunda.unlock();
                }
            } finally {
                primera.unlock();
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread r1 = new Thread(() -> montar("Robot-1", martillo, "martillo", destornillador, "destornillador"));
            Thread r2 = new Thread(() -> montar("Robot-2", martillo, "martillo", destornillador, "destornillador"));   // mismo orden
            r1.setDaemon(true);
            r2.setDaemon(true);
            r1.start();
            r2.start();
            r1.join(2000);
            r2.join(2000);
            if (r1.isAlive() && r2.isAlive()) {
                System.out.println("¡Interbloqueo! Robot-1: " + r1.getState() + " · Robot-2: " + r2.getState());
            } else {
                System.out.println("Los dos robots han montado su pieza");
            }
        }
    }
    ```

    Ya no hay espera circular: el que no consigue el martillo espera sin tener nada cogido, así que el otro puede terminar.

### Paso 3 · Otra solución: soltar y reintentar

A veces no puedes cambiar el orden. Copia `RobotsPaso1` como `RobotsPaso3`, **con el orden cruzado del paso 1**, y cambia `montar`:

- en un `while (true)`, coge la primera herramienta con `lock()`;
- intenta la segunda con `tryLock()`. Si la consigue, monta la pieza y sale con `return`;
- si no, imprime «no consigue el …: suelta el …», suelta la primera y espera un rato **al azar** (entre 50 y 200 ms) antes de volver a intentarlo. Cuenta los intentos.

Salida aproximada (cambia en cada ejecución):

```text
Robot-1 coge el martillo
Robot-2 coge el destornillador
Robot-2 no consigue el martillo: suelta el destornillador
Robot-1 no consigue el destornillador: suelta el martillo
Robot-1 coge el martillo
Robot-2 coge el destornillador
Robot-1 no consigue el destornillador: suelta el martillo
Robot-2 monta la pieza (intento 2)
Robot-1 coge el martillo
Robot-1 monta la pieza (intento 3)
Los dos robots han montado su pieza
```

**Piensa:** ¿por qué la espera es al azar? ¿Qué podría pasar si los dos esperasen siempre exactamente 100 ms?

??? success "Solución del paso 3"
    ```java
    import java.util.concurrent.ThreadLocalRandom;
    import java.util.concurrent.locks.ReentrantLock;

    public class RobotsPaso3 {
        static final ReentrantLock martillo = new ReentrantLock();
        static final ReentrantLock destornillador = new ReentrantLock();

        static void pausa(int ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                // nada
            }
        }

        // Si no consigue la segunda herramienta, suelta la primera y lo vuelve a intentar
        static void montar(String robot, ReentrantLock primera, String nombre1,
                           ReentrantLock segunda, String nombre2) {
            int intentos = 0;
            while (true) {
                intentos++;
                primera.lock();
                try {
                    System.out.println(robot + " coge el " + nombre1);
                    pausa(100);
                    if (segunda.tryLock()) {                 // ¿está libre la segunda?
                        try {
                            System.out.println(robot + " monta la pieza (intento " + intentos + ")");
                            return;                         // los finally sueltan las dos
                        } finally {
                            segunda.unlock();
                        }
                    }
                    System.out.println(robot + " no consigue el " + nombre2 + ": suelta el " + nombre1);
                } finally {
                    primera.unlock();
                }
                pausa(ThreadLocalRandom.current().nextInt(50, 200));   // espera un rato al azar
            }
        }

        public static void main(String[] args) throws InterruptedException {
            Thread r1 = new Thread(() -> montar("Robot-1", martillo, "martillo", destornillador, "destornillador"));
            Thread r2 = new Thread(() -> montar("Robot-2", destornillador, "destornillador", martillo, "martillo"));
            r1.setDaemon(true);
            r2.setDaemon(true);
            r1.start();
            r2.start();
            r1.join(5000);
            r2.join(5000);
            if (r1.isAlive() || r2.isAlive()) {
                System.out.println("Siguen bloqueados");
            } else {
                System.out.println("Los dos robots han montado su pieza");
            }
        }
    }
    ```

    Si los dos esperasen siempre lo mismo, podrían repetir los mismos pasos a la vez una y otra vez: los dos cogen, los dos fallan, los dos sueltan… Ninguno se bloquea, pero ninguno avanza. Con una espera al azar, uno acaba adelantándose al otro.
