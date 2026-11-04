# Boletín de ejercicios · Tema 2

!!! info "Cómo trabajar este boletín"
    - **Diez ejercicios** ordenados de menor a mayor dificultad. El 1 y el 6 son de análisis; el resto se programa en **Java (JDK 21 o superior)**.
    - Cubren los apartados 1 a 4 y 6 a 8. Cada ejercicio indica los **criterios de evaluación del RA2** que trabaja.
    - Entrega: un proyecto con una clase por programa y un `README.md` con las respuestas de análisis, las tablas de tiempos y una captura de cada ejecución.
    - Ejecuta cada programa **varias veces**: con hilos, una sola ejecución correcta no demuestra que el programa esté bien.

| Nº | Ejercicio | Nivel | CE |
|---|---|---|---|
| 1 | ¿Proceso o hilo? | ★ | a, i |
| 2 | Tres corredores | ★ | b, c |
| 3 | Predice los estados | ★★ | d |
| 4 | Cuenta atrás cancelable | ★★ | b, d |
| 5 | Copias de seguridad con límite de tiempo | ★★ | b, d, c |
| 6 | Encuentra la condición de carrera | ★★ | k |
| 7 | Sumar un array en paralelo | ★★★ | a, c, i |
| 8 | Contador de visitas: tres versiones | ★★★ | e, f, k |
| 9 | El banco: transferencias sin perder dinero | ★★★★ | e, f, k |
| 10 | Contar palabras en paralelo | ★★★★ | c, e, f, h, j |

---

## 1. ¿Proceso o hilo? ★

1. Para cada caso, indica si usarías **un proceso nuevo** o **un hilo**, y si la tarea es sobre todo **CPU-bound** o **IO-bound**. Justifica en una frase:
    1. Un reproductor de música descarga la siguiente canción mientras suena la actual.
    2. Un editor de vídeo exporta una película repartiendo los fotogramas entre los núcleos.
    3. Un programa Java ejecuta un script de Python que ya existe.
    4. Un servidor de chat atiende a 500 usuarios conectados a la vez.
    5. Un navegador abre cada extensión de forma que, si una falla, no afecte al resto.
2. ¿Qué comparten dos hilos del mismo proceso? ¿Qué tiene cada uno que no comparte?
3. Averigua cuántos núcleos ve la JVM en tu ordenador con `Runtime.getRuntime().availableProcessors()`. Si un programa CPU-bound crea 64 hilos, ¿irá más rápido que con ese número de hilos? ¿Por qué?

## 2. Tres corredores ★

1. Crea `Carrera`: lanza **tres hilos** llamados `Corredor-1`, `Corredor-2` y `Corredor-3`.
2. Cada corredor da **5 vueltas**. En cada vuelta imprime «Corredor-2: vuelta 3» y duerme un tiempo aleatorio entre 100 y 500 ms (`ThreadLocalRandom.current().nextInt(100, 501)`).
3. Al terminar su quinta vuelta, cada corredor imprime «Corredor-2 llega a meta».
4. El `main` imprime «Carrera terminada» **solo** cuando hayan llegado los tres.
5. Ejecuta cinco veces. ¿Gana siempre el mismo? ¿Por qué?

## 3. Predice los estados ★★

Sin ejecutarlo, escribe qué imprimirá cada línea. Después ejecútalo y compara.

```java
public class Predice {
    public static void main(String[] args) throws InterruptedException {
        Thread lento = new Thread(() -> {
            try { Thread.sleep(2000); } catch (InterruptedException e) { }
        });
        Thread espera = new Thread(() -> {
            try { lento.join(); } catch (InterruptedException e) { }
        });
        System.out.println("A: " + espera.getState());
        lento.start();
        espera.start();
        Thread.sleep(500);
        System.out.println("B: " + lento.getState());
        System.out.println("C: " + espera.getState());
        espera.join();
        System.out.println("D: " + espera.getState());
        System.out.println("E: " + lento.isAlive());
    }
}
```

1. Escribe tu predicción para A, B, C, D y E, y justifícala.
2. Cambia `lento.join()` por `lento.join(5000)`. ¿Qué línea cambia y por qué?
3. Cambia ahora `Thread.sleep(500)` del `main` por `Thread.sleep(3000)`. ¿Qué imprimen B y C?
4. ¿Por qué en Java no aparece nunca un estado `RUNNING`?

## 4. Cuenta atrás cancelable ★★

1. Crea `CuentaAtras`: un hilo cuenta de 10 a 0, un número por segundo, y al llegar a 0 imprime «¡Despegue!».
2. Mientras tanto, el `main` lee líneas del teclado con `Scanner`. Si el usuario escribe `abortar`, el `main` **interrumpe** la cuenta atrás.
3. Al ser interrumpido, el hilo imprime «Despegue abortado en el segundo N» y termina.
4. El `main` espera a que termine la cuenta atrás antes de acabar. Si la cuenta llega a 0 sin que nadie escriba nada, el programa también debe terminar. Pista: lee el teclado en un **hilo demonio** y deja que el `main` espere a la cuenta atrás con `join()`.
5. ¿Qué pasaría si en el `catch` de la cuenta atrás no hicieras nada? Pruébalo y explícalo.

## 5. Copias de seguridad con límite de tiempo ★★

Un programa hace copias de seguridad de cuatro carpetas. Las copias se simulan con `sleep`: `Documentos` tarda 2 s, `Fotos` 6 s, `Proyectos` 3 s y `Música` 5 s.

1. Lanza las cuatro copias a la vez, cada una en un hilo con el nombre de la carpeta.
2. El usuario solo puede esperar **4 segundos en total**. Lo que no haya terminado a los 4 s se cancela con `interrupt()`. Usa un único instante límite para todas, no `join(4000)` en cada hilo.
3. Al final, muestra una tabla con cada carpeta y su resultado: `completada` o `cancelada`.
4. Comprueba que el programa tarda unos 4 segundos, no 6 ni 16.
5. ¿Por qué no basta con hacer `join(4000)` a cada hilo, uno detrás de otro?

## 6. Encuentra la condición de carrera ★★

Para cada fragmento, di si hay condición de carrera. Si la hay, indica cuál es la **sección crítica** y cómo la arreglarías.

1. Ocho hilos leen el mismo `String[] provincias` para mostrarlo por pantalla.
2. Cuatro hilos ejecutan `total = total + importe;` sobre un `static double total`.
3. Cada hilo crea su propio `StringBuilder`, le añade texto y lo imprime.
4. Una web de reservas: `if (asientosLibres > 0) { asientosLibres--; confirmar(); }`.
5. Dos hilos hacen `lista.add(x)` sobre el mismo `ArrayList`.
6. Un hilo rellena una lista; el `main` espera con `join()` a que termine y después la recorre.

Ejecuta el 2 con 4 hilos y 100.000 sumas de 1.0 cada uno, y comprueba el resultado varias veces.

## 7. Sumar un array en paralelo ★★★

1. Crea un array de **100 millones** de `int` con valores aleatorios entre 0 y 9.
2. Súmalo en el hilo `main` y mide el tiempo con `System.nanoTime()`.
3. Súmalo ahora con **N hilos**: cada hilo suma un trozo del array y guarda su resultado en **su propia posición** de un array `long[] parciales`. Cuando terminen todos, el `main` suma los parciales.
4. Comprueba que el resultado es el mismo y completa la tabla con N = 1, 2, 4 y el número de núcleos de tu ordenador. La aceleración es S = T₁ / Tₙ.

    | Hilos | Tiempo (ms) | Aceleración |
    |---|---|---|
    | 1 | | 1 |
    | 2 | | |
    | 4 | | |
    | núcleos | | |

5. ¿Por qué aquí no hace falta `synchronized` aunque todos los hilos escriban en el mismo array `parciales`?
6. ¿Es un problema CPU-bound o IO-bound? ¿Qué pasa si usas el doble de hilos que núcleos?

## 8. Contador de visitas: tres versiones ★★★

Una web recibe visitas desde **10 hilos**. Cada hilo registra **100.000 visitas** incrementando un contador común.

1. **Versión 1:** contador `static int` sin protección.
2. **Versión 2:** clase `Contador` con métodos `synchronized incrementar()` y `synchronized getValor()`.
3. **Versión 3:** `AtomicInteger`.
4. Ejecuta cada versión 5 veces y completa la tabla:

    | Versión | ¿Resultado correcto? | Tiempo medio (ms) |
    |---|---|---|
    | Sin protección | | |
    | `synchronized` | | |
    | `AtomicInteger` | | |

5. Haz una **versión 4** sin ninguna sincronización que dé siempre el resultado correcto: cada hilo cuenta en una variable propia y el `main` suma al final.
6. Introduce a propósito el error de crear el cerrojo **dentro** de cada hilo (`Object cerrojo = new Object();`). ¿Qué ocurre? Explícalo.

## 9. El banco: transferencias sin perder dinero ★★★★

1. Crea la clase `Cuenta` con un número, un saldo y los métodos `ingresar(int)` y `retirar(int)`. `retirar` devuelve `false`, sin tocar el saldo, si no hay dinero suficiente.
2. Crea `Banco` con **5 cuentas** de 1000 € cada una y un método `transferir(origen, destino, cantidad)`.
3. Lanza **10 hilos**. Cada uno hace **10.000 transferencias** de cantidades aleatorias entre 1 y 100 € entre cuentas aleatorias.
4. Al final, el dinero total del banco debe seguir siendo exactamente **5000 €** y ninguna cuenta puede quedar en negativo.
5. Hazlo primero **sin protección** y comprueba que falla. Después protégelo con **un único cerrojo para todo el banco**.
6. Explica por qué no basta con que `ingresar` y `retirar` sean `synchronized` cada uno por separado.
7. ¿Por qué aquí no sirve `AtomicInteger` para los saldos?

!!! note
    Proteger cada transferencia con los cerrojos de las **dos cuentas** a la vez es más eficiente, pero puede provocar un **interbloqueo**. Lo estudiaremos en la siguiente sesión.

## 10. Contar palabras en paralelo ★★★★

1. Genera un fichero `texto.txt` con **200.000 líneas**, cada una formada por 10 palabras elegidas al azar de una lista de 20.
2. Crea `ContarPalabras`: lee todas las líneas en una lista y repártelas entre **N hilos**. Cada hilo cuenta cuántas veces aparece cada palabra.
3. Haz dos versiones:
    1. **Mapa compartido:** todos los hilos actualizan el mismo `HashMap<String, Integer>`, protegido con `synchronized`.
    2. **Mapas locales:** cada hilo cuenta en su propio `HashMap` y el `main` los fusiona al final, sin sincronización.
4. Comprueba que las dos versiones dan el mismo resultado que una versión secuencial y compara los tiempos con 1, 2 y 4 hilos.
5. ¿Qué pasa si quitas el `synchronized` de la versión de mapa compartido? Pruébalo varias veces.
6. Documenta las clases con **Javadoc** y genera la documentación con `javadoc -d doc *.java`.
