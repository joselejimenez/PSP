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
