# Práctica guiada · Solución

Solución de los cuatro pasos de la [práctica guiada del gestor de descargas](practica-guiada.md). Cada pestaña es un **programa completo e independiente**: puedes copiarlo y ejecutarlo tal cual con JDK 21 o superior.

!!! tip "Antes de mirar"
    Intenta cada paso por tu cuenta y usa esta página para comprobarlo. Ejecuta tu versión y la de aquí **varias veces**: el orden de las líneas cambia de una ejecución a otra, y eso es normal.

## Código de cada paso

=== "Paso 1 · Secuencial"

    `Paso1Secuencial.java`

    ```java
    public class Paso1Secuencial {
        static final String[] FICHEROS = {"foto.jpg", "video.mp4",
                "musica.mp3", "juego.zip", "apuntes.pdf"};
        static final int[] SEGUNDOS = {1, 4, 2, 2, 1};

        // Simula una descarga: tarda seg segundos y dice qué hilo la hace
        static void descargar(String nombre, int seg) {
            String hilo = Thread.currentThread().getName();
            System.out.printf("[%s] empieza %s%n", hilo, nombre);
            try {
                Thread.sleep(seg * 1000L);
                System.out.printf("[%s] terminado %s (%d s)%n", hilo, nombre, seg);
            } catch (InterruptedException e) {
                System.out.printf("[%s] CANCELADO %s%n", hilo, nombre);
            }
        }

        // PASO 1: una descarga detrás de otra, todas en el hilo main
        static void secuencial() {
            for (int i = 0; i < FICHEROS.length; i++) {
                descargar(FICHEROS[i], SEGUNDOS[i]);
            }
        }

        public static void main(String[] args) throws InterruptedException {
            long ini = System.currentTimeMillis();
            secuencial();
            long ms = System.currentTimeMillis() - ini;
            System.out.printf("Total: %.1f s%n", ms / 1000.0);
        }
    }
    ```

    Salida:

    ```text
    [main] empieza foto.jpg
    [main] terminado foto.jpg (1 s)
    [main] empieza video.mp4
    [main] terminado video.mp4 (4 s)
    [main] empieza musica.mp3
    [main] terminado musica.mp3 (2 s)
    [main] empieza juego.zip
    [main] terminado juego.zip (2 s)
    [main] empieza apuntes.pdf
    [main] terminado apuntes.pdf (1 s)
    Total: 10,0 s
    ```

    - Todo lo hace el hilo **`main`**: por eso todas las líneas empiezan por `[main]`.
    - Las descargas van en orden y el total es la **suma**: 1 + 4 + 2 + 2 + 1 = 10 s.
    - El `catch` de `descargar()` no se usa todavía: lo dejamos preparado para el paso 4.
    - `seg * 1000L`: la `L` hace la multiplicación en `long`, que es el tipo que espera `sleep`.

=== "Paso 2 · Un hilo por descarga"

    `Paso2ConHilos.java`

    ```java
    import java.util.ArrayList;
    import java.util.List;

    public class Paso2ConHilos {
        static final String[] FICHEROS = {"foto.jpg", "video.mp4",
                "musica.mp3", "juego.zip", "apuntes.pdf"};
        static final int[] SEGUNDOS = {1, 4, 2, 2, 1};

        // Simula una descarga: tarda seg segundos y dice qué hilo la hace
        static void descargar(String nombre, int seg) {
            String hilo = Thread.currentThread().getName();
            System.out.printf("[%s] empieza %s%n", hilo, nombre);
            try {
                Thread.sleep(seg * 1000L);
                System.out.printf("[%s] terminado %s (%d s)%n", hilo, nombre, seg);
            } catch (InterruptedException e) {
                System.out.printf("[%s] CANCELADO %s%n", hilo, nombre);
            }
        }

        // PASO 2: un hilo de plataforma por descarga
        static void conHilos() throws InterruptedException {
            List<Thread> hilos = new ArrayList<>();
            for (int i = 0; i < FICHEROS.length; i++) {
                int n = i;                                   // la lambda necesita una variable que no cambie
                Thread t = new Thread(() -> descargar(FICHEROS[n], SEGUNDOS[n]), "D-" + n);
                hilos.add(t);
                t.start();                                   // arrancar todos primero...
            }
            for (Thread t : hilos) {
                t.join();                                    // ...y esperar a todos después
            }
        }

        public static void main(String[] args) throws InterruptedException {
            long ini = System.currentTimeMillis();
            conHilos();
            long ms = System.currentTimeMillis() - ini;
            System.out.printf("Total: %.1f s%n", ms / 1000.0);
        }
    }
    ```

    Salida (el orden exacto puede cambiar):

    ```text
    [D-0] empieza foto.jpg
    [D-1] empieza video.mp4
    [D-2] empieza musica.mp3
    [D-3] empieza juego.zip
    [D-4] empieza apuntes.pdf
    [D-0] terminado foto.jpg (1 s)
    [D-4] terminado apuntes.pdf (1 s)
    [D-3] terminado juego.zip (2 s)
    [D-2] terminado musica.mp3 (2 s)
    [D-1] terminado video.mp4 (4 s)
    Total: 4,0 s
    ```

    - **`int n = i`**: la lambda no puede usar `i`, porque cambia en cada vuelta. `n` es una variable nueva en cada vuelta y no cambia.
    - **Dos bucles**: el primero crea y arranca los cinco hilos; el segundo los espera. Si hicieras `start()` y `join()` en el mismo bucle, volvería a tardar 10 s.
    - Las cinco descargas empiezan casi a la vez y terminan por orden de duración. El orden exacto de las líneas cambia de una ejecución a otra.
    - El total es lo que tarda la descarga **más lenta**: 4 s.

=== "Paso 3 · Hilos virtuales"

    `Paso3ConVirtuales.java`

    ```java
    import java.util.ArrayList;
    import java.util.List;

    public class Paso3ConVirtuales {
        static final String[] FICHEROS = {"foto.jpg", "video.mp4",
                "musica.mp3", "juego.zip", "apuntes.pdf"};
        static final int[] SEGUNDOS = {1, 4, 2, 2, 1};

        // Simula una descarga: tarda seg segundos y dice qué hilo la hace
        static void descargar(String nombre, int seg) {
            String hilo = Thread.currentThread().getName();
            System.out.printf("[%s] empieza %s%n", hilo, nombre);
            try {
                Thread.sleep(seg * 1000L);
                System.out.printf("[%s] terminado %s (%d s)%n", hilo, nombre, seg);
            } catch (InterruptedException e) {
                System.out.printf("[%s] CANCELADO %s%n", hilo, nombre);
            }
        }

        // PASO 3: igual que el paso 2, pero con hilos virtuales
        static void conVirtuales() throws InterruptedException {
            List<Thread> hilos = new ArrayList<>();
            for (int i = 0; i < FICHEROS.length; i++) {
                int n = i;
                Thread t = Thread.ofVirtual().name("V-" + n) // lo único que cambia
                        .start(() -> descargar(FICHEROS[n], SEGUNDOS[n]));
                hilos.add(t);
            }
            for (Thread t : hilos) {
                t.join();
            }
        }

        public static void main(String[] args) throws InterruptedException {
            long ini = System.currentTimeMillis();
            conVirtuales();
            long ms = System.currentTimeMillis() - ini;
            System.out.printf("Total: %.1f s%n", ms / 1000.0);
        }
    }
    ```

    Salida (el orden exacto puede cambiar):

    ```text
    [V-0] empieza foto.jpg
    [V-1] empieza video.mp4
    [V-2] empieza musica.mp3
    [V-3] empieza juego.zip
    [V-4] empieza apuntes.pdf
    [V-0] terminado foto.jpg (1 s)
    [V-4] terminado apuntes.pdf (1 s)
    [V-2] terminado musica.mp3 (2 s)
    [V-3] terminado juego.zip (2 s)
    [V-1] terminado video.mp4 (4 s)
    Total: 4,0 s
    ```

    - Solo cambia **cómo se crea** el hilo: `Thread.ofVirtual().name("V-" + n).start(...)` lo crea y lo arranca a la vez, así que ya no hace falta el `t.start()` aparte.
    - La lista, el `join()` y la tarea quedan exactamente igual: un hilo virtual es un `Thread`.
    - Con cinco descargas tarda lo mismo que el paso 2. La diferencia se notaría con decenas de miles de descargas a la vez: los hilos virtuales apenas gastan memoria mientras esperan.

=== "Paso 4 · Límite de 3 segundos"

    `Paso4ConLimite.java`

    ```java
    import java.util.ArrayList;
    import java.util.List;

    public class Paso4ConLimite {
        static final String[] FICHEROS = {"foto.jpg", "video.mp4",
                "musica.mp3", "juego.zip", "apuntes.pdf"};
        static final int[] SEGUNDOS = {1, 4, 2, 2, 1};

        // Simula una descarga: tarda seg segundos y dice qué hilo la hace
        static void descargar(String nombre, int seg) {
            String hilo = Thread.currentThread().getName();
            System.out.printf("[%s] empieza %s%n", hilo, nombre);
            try {
                Thread.sleep(seg * 1000L);
                System.out.printf("[%s] terminado %s (%d s)%n", hilo, nombre, seg);
            } catch (InterruptedException e) {
                System.out.printf("[%s] CANCELADO %s%n", hilo, nombre);
            }
        }

        // PASO 4: límite de 3 segundos en total; lo que no haya acabado se cancela
        static void conLimite() throws InterruptedException {
            List<Thread> hilos = new ArrayList<>();
            for (int i = 0; i < FICHEROS.length; i++) {
                int n = i;
                hilos.add(Thread.ofVirtual().name("V-" + n)
                        .start(() -> descargar(FICHEROS[n], SEGUNDOS[n])));
            }
            long limite = System.currentTimeMillis() + 3000; // un único instante límite para todas
            for (Thread t : hilos) {
                long queda = limite - System.currentTimeMillis();
                if (queda > 0) {
                    t.join(queda);                           // espera como mucho lo que queda
                }
                if (t.isAlive()) {
                    t.interrupt();                           // se ha pasado del límite: cancelar
                }
            }
            for (Thread t : hilos) {
                t.join();                                    // que los cancelados terminen de imprimir
            }
        }

        public static void main(String[] args) throws InterruptedException {
            long ini = System.currentTimeMillis();
            conLimite();
            long ms = System.currentTimeMillis() - ini;
            System.out.printf("Total: %.1f s%n", ms / 1000.0);
        }
    }
    ```

    Salida (el orden exacto puede cambiar):

    ```text
    [V-0] empieza foto.jpg
    [V-1] empieza video.mp4
    [V-2] empieza musica.mp3
    [V-3] empieza juego.zip
    [V-4] empieza apuntes.pdf
    [V-0] terminado foto.jpg (1 s)
    [V-4] terminado apuntes.pdf (1 s)
    [V-2] terminado musica.mp3 (2 s)
    [V-3] terminado juego.zip (2 s)
    [V-1] CANCELADO video.mp4
    Total: 3,0 s
    ```

    - **`limite`** es un instante absoluto: ahora + 3 s. Para cada hilo se calcula cuánto **queda** hasta ese instante y se espera como mucho eso. Así el total nunca pasa de 3 s, por muchos hilos que haya.
    - Al volver de `join(queda)`, **`isAlive()`** dice si el hilo terminó a tiempo. Si sigue vivo, **`interrupt()`** le pide que pare.
    - La interrupción despierta el `sleep` de `descargar()` con `InterruptedException` y se imprime `CANCELADO`: por eso lo dejamos preparado en el paso 1.
    - **`if (queda > 0)`**: `join(0)` no significa «no esperes», sino «espera sin límite». Sin el `if`, cuando ya no queda tiempo te quedarías esperando entera a la descarga lenta.
    - El último bucle de `join()` espera a que los cancelados terminen de imprimir antes del `Total`.

## Tabla de tiempos

| Paso | Versión | Total |
|---|---|---|
| 1 | Secuencial | 10,0 s: la suma de todas |
| 2 | Un hilo por descarga | 4,0 s: la más lenta |
| 3 | Hilos virtuales | 4,0 s: la más lenta |
| 4 | Límite de 3 s | 3,0 s: el límite |

Los tiempos pueden variar unas décimas según el ordenador.

## Respuestas a las preguntas

1. **¿Por qué en el paso 2 el total es lo que tarda la más lenta y no la suma?** Porque las cinco descargas esperan **a la vez**, cada una en su hilo. Mientras una duerme, las demás también avanzan. El `main` termina cuando ha acabado la última, `video.mp4`, que tarda 4 s.
2. **¿Cuántos hilos hay vivos durante el primer segundo del paso 2? ¿En qué estado está cada uno?** Seis: `main` y los cinco de descarga. `main` está en **WAITING**, dentro de `join()`. Los cinco de descarga están en **TIMED_WAITING**, dentro de `sleep()`.
3. **Los pasos 2 y 3 tardan lo mismo. ¿En qué situación se notaría la diferencia?** Con muchísimas descargas a la vez, por ejemplo 100.000. Cada hilo de plataforma reserva alrededor de 1 MB de pila, y el sistema se quedaría sin memoria. Los hilos virtuales ocupan unos pocos KB mientras esperan, así que la versión del paso 3 sí aguantaría.
4. **En el paso 4, ¿por qué no basta con hacer `join(3000)` a cada hilo?** Porque cada `join(3000)` puede esperar hasta 3 s, uno detrás de otro. Con varias descargas lentas, el total podría ser de 6, 9 o más segundos. Con un único instante límite, cada `join()` solo espera lo que queda.
5. **¿Qué pasaría en el paso 4 si `descargar()` tuviera un `catch` vacío?** En este programa, la descarga cancelada terminaría igualmente, porque después del `catch` no hay más trabajo, pero no se imprimiría `CANCELADO` y no sabrías que se ha cancelado. Si la descarga estuviera dentro de un bucle, por ejemplo descargando por trozos, el `catch` vacío se tragaría la interrupción y el hilo **seguiría trabajando** como si nadie le hubiera pedido parar.
