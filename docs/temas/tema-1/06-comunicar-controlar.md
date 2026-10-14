# 6. Comunicar y controlar procesos

El código de salida solo permite devolver un número pequeño. En este apartado aprenderás a **intercambiar datos** con un proceso hijo a través de sus flujos, a **esperarlo con límite**, a **terminarlo** y a **observar** cualquier proceso del sistema.

## 6.1 Los tres flujos estándar

Todo proceso tiene tres **flujos estándar**:

- **stdin** (entrada estándar): de donde lee los datos. Normalmente, el teclado.
- **stdout** (salida estándar): donde escribe los resultados. Normalmente, la consola. En Java, `System.out`.
- **stderr** (salida de errores): donde escribe los mensajes de error. En Java, `System.err`.

Cuando Java lanza un proceso con `ProcessBuilder`, **por defecto los tres flujos del hijo se conectan con el padre mediante tuberías**. El padre accede a ellas con estos métodos de `Process`:

| Flujo del hijo | Método en el padre | Dirección |
|---|---|---|
| stdin | `getOutputStream()` · `outputWriter()` (Java 17+) | padre → hijo |
| stdout | `getInputStream()` · `inputReader()` (Java 17+) | hijo → padre |
| stderr | `getErrorStream()` · `errorReader()` (Java 17+) | hijo → padre |

!!! warning "¡Ojo con los nombres!"
    Están escritos **desde el punto de vista del padre**. `getInputStream()` lee la **salida** del hijo (para el padre es una entrada). `getOutputStream()` escribe en la **entrada** del hijo (para el padre es una salida).

```
          PADRE                                   HIJO
   outputWriter()   ───── tubería ─────►   stdin   (entrada)
   inputReader()    ◄──── tubería ──────   stdout  (salida)
   errorReader()    ◄──── tubería ──────   stderr  (errores)
```

Una **tubería** (*pipe*) funciona como un tubo: lo que se mete por un extremo sale por el otro, **en el mismo orden** y en **una sola dirección**. Para hablar en los dos sentidos hacen falta dos tuberías.

## 6.2 Leer la salida del hijo

```java
import java.io.BufferedReader;
import java.nio.charset.StandardCharsets;

public class LeerSalida {
    public static void main(String[] args) throws Exception {
        ProcessBuilder pb = new ProcessBuilder("java", "-version");
        pb.redirectErrorStream(true);                  // mezcla stderr con stdout

        Process p = pb.start();
        try (BufferedReader br = p.inputReader(StandardCharsets.UTF_8)) {
            String linea;
            while ((linea = br.readLine()) != null) {  // null = el hijo ha cerrado su salida
                System.out.println("[hijo] " + linea);
            }
        }
        System.out.println("Código: " + p.waitFor()); // esperar DESPUÉS de leer
    }
}
```

1. **`redirectErrorStream(true)`** une la salida de errores con la normal, así basta con leer un flujo. Curiosidad: `java -version` escribe en **stderr**, así que sin esta línea no leerías nada.
2. **`inputReader()`** devuelve un `BufferedReader` sobre la salida del hijo. En versiones anteriores a Java 17: `new BufferedReader(new InputStreamReader(p.getInputStream()))`.
3. **`readLine()`** devuelve `null` cuando el hijo cierra su salida, normalmente al terminar.
4. **`waitFor()` va después de leer.** Lo explica el siguiente aviso.

!!! danger "El bloqueo por tubería llena"
    Las tuberías tienen un **búfer limitado** (unos 64 KB). Si el hijo escribe mucho y el padre no lee, el búfer se llena y el hijo **se bloquea** esperando a que alguien lo vacíe. Si a la vez el padre está esperando en `waitFor()`, **ninguno de los dos avanza nunca**. Solución: leer la salida **antes** de `waitFor()` o redirigirla a un fichero.

### Devolver un resultado leyendo la salida

Así, el hijo puede devolver cualquier dato, no solo un número del 0 al 255:

```java
// Hijo: escribe el resultado
System.out.println(a + b);

// Padre: lo lee
String resultado;
try (BufferedReader r = p.inputReader()) {
    resultado = r.readLine();
}
double valor = Double.parseDouble(resultado);
```

## 6.3 Redirigir en lugar de leer

Si no necesitamos procesar la salida en Java, es más sencillo **redirigirla**: el sistema operativo conecta directamente el flujo del hijo con un fichero o con la consola, sin tuberías ni riesgo de bloqueo.

| Método de `ProcessBuilder` | Efecto | Equivale en la terminal a |
|---|---|---|
| `inheritIO()` | Los tres flujos van a la consola del padre | — |
| `redirectOutput(new File("f.txt"))` | La salida va a un fichero, que se sobrescribe | `programa > f.txt` |
| `redirectOutput(Redirect.appendTo(f))` | La salida se añade al final del fichero | `programa >> f.txt` |
| `redirectInput(new File("datos.txt"))` | La entrada se lee de un fichero | `programa < datos.txt` |
| `redirectError(Redirect.INHERIT)` | Los errores van a la consola del padre | — |
| `redirectOutput(Redirect.DISCARD)` | La salida se tira | `> /dev/null` o `> NUL` |

```java
ProcessBuilder pb = new ProcessBuilder("ls", "-la");
pb.redirectOutput(ProcessBuilder.Redirect.appendTo(new File("log.txt")));
pb.redirectError(ProcessBuilder.Redirect.INHERIT);
pb.start().waitFor();
```

Todas las redirecciones se configuran **antes** de llamar a `start()`.

## 6.4 Enviar datos a la entrada del hijo

El padre puede escribir en la entrada estándar del hijo como si fuera el teclado:

```java
Process p = new ProcessBuilder("sort").start();

try (BufferedWriter w = p.outputWriter()) {
    w.write("pera\nmanzana\nkiwi\n");
}                                                  // cerrar = fin de los datos

String ordenado = new String(p.getInputStream().readAllBytes());
System.out.print(ordenado);                        // kiwi, manzana, pera
```

- `sort` lee líneas hasta el final de la entrada, las ordena y las escribe. Existe en Windows, Linux y macOS.
- **Hay que cerrar el flujo.** Al cerrarlo, el hijo recibe el «fin de fichero» y sabe que no llegarán más datos. Si no se cierra, `sort` sigue esperando, el padre también, y el programa se queda colgado.

## 6.5 Invocar la shell del sistema, con cuidado

A veces necesitamos funciones de la shell: tuberías (`|`), comodines (`*`) u órdenes internas.

```java
// Windows
new ProcessBuilder("cmd", "/c", "ipconfig").inheritIO().start();
// Linux y macOS
new ProcessBuilder("bash", "-c", "ip a | grep inet").inheritIO().start();
```

!!! danger "Inyección de órdenes"
    **Nunca** construyas la orden concatenando lo que escribe el usuario. Con `"ping " + host`, alguien puede escribir `8.8.8.8 & del *` y ejecutaría también su orden. Es una de las vulnerabilidades más graves (la veremos en el Tema 5). La defensa: pasar cada dato como un argumento separado de `ProcessBuilder`, sin shell, y validar la entrada.

## 6.6 Esperar con límite y terminar procesos

Nunca conviene esperar indefinidamente a un proceso externo: puede colgarse. `Process` ofrece:

| Método | Qué hace |
|---|---|
| `waitFor()` | Espera sin límite y devuelve el código de salida. |
| `waitFor(t, TimeUnit)` | Espera como mucho ese tiempo. Devuelve `true` si terminó y `false` si se agotó el tiempo. |
| `isAlive()` | `true` si el hijo sigue en marcha. |
| `exitValue()` | El código de salida. Lanza una excepción si el proceso aún no ha terminado. |
| `destroy()` | Pide al proceso que termine (en Linux y macOS, la señal **SIGTERM**). El hijo puede guardar sus datos y cerrar ordenadamente. |
| `destroyForcibly()` | Lo mata sin avisar (**SIGKILL**). No puede reaccionar. |
| `onExit()` | Devuelve un `CompletableFuture` que se completa cuando termina: permite reaccionar sin bloquearse. |

El patrón recomendado es **pedir por las buenas y, si no responde, forzar**:

```java
Process p = pb.start();
if (!p.waitFor(5, TimeUnit.SECONDS)) {        // ¿ha terminado en 5 s?
    p.destroy();                              // pide que termine
    if (!p.waitFor(2, TimeUnit.SECONDS)) {    // le da 2 s para cerrar
        p.destroyForcibly();                  // último recurso
    }
}
```

!!! note "Códigos al terminar por una señal"
    En Linux y macOS, un proceso terminado por una señal devuelve 128 + el número de la señal: **143** con `destroy()` (SIGTERM es la 15) y **137** con `destroyForcibly()` (SIGKILL es la 9). Un programa Java puede ejecutar código al recibir SIGTERM con `Runtime.getRuntime().addShutdownHook(...)`; con SIGKILL, no. En Windows no hay señales y los dos métodos terminan el proceso directamente.

Los recursos del proceso terminado (memoria, ficheros abiertos) los libera el **sistema operativo**. El recolector de basura de Java solo recoge el objeto `Process` de nuestra JVM.

## 6.7 `ProcessHandle`: observar cualquier proceso

Desde Java 9, `ProcessHandle` permite ver y controlar **cualquier proceso** del sistema, no solo los que hemos lanzado. Es como un Administrador de tareas desde Java.

```java
ProcessHandle yo = ProcessHandle.current();
System.out.println("Mi PID: " + yo.pid());
yo.parent().ifPresent(padre -> System.out.println("Mi padre: " + padre.pid()));

ProcessHandle.allProcesses()                                   // todos los del sistema
        .filter(ph -> ph.info().command().isPresent())
        .limit(10)
        .forEach(ph -> System.out.println(ph.pid() + " " + ph.info().command().get()));
```

| Método | Qué devuelve |
|---|---|
| `current()` | Nuestro propio proceso. |
| `parent()` | El padre, como `Optional`, porque puede haber terminado. |
| `children()` · `descendants()` | Los hijos directos · todo el árbol por debajo. |
| `allProcesses()` | Un `Stream` con todos los procesos visibles. |
| `info()` | `command()`, `arguments()`, `user()`, `startInstant()` y `totalCpuDuration()`, todos `Optional` porque, por permisos, puede que no se puedan leer. |
| `destroy()`, `isAlive()`, `onExit()` | Igual que en `Process`. |

Para pasar de un `Process` a su `ProcessHandle`: `p.toHandle()`.

## 6.8 Mecanismos de comunicación entre procesos (IPC)

Como la memoria de cada proceso está **aislada**, toda comunicación entre procesos pasa por el sistema operativo. Los mecanismos de **IPC** (*Inter-Process Communication*) más habituales son:

| Mecanismo | Cómo funciona | En Java |
|---|---|---|
| **Tuberías** | Flujo de bytes en una dirección, entre procesos relacionados | Flujos de `Process`, `startPipeline` |
| **Ficheros** | Uno escribe y otro lee. Sencillo, pero hay que saber cuándo ha terminado de escribir el otro. | `java.nio.file.Files` |
| **Sockets** | Comunicación por red, en el mismo equipo o entre equipos distintos. Es el mecanismo universal. | `Socket`, `ServerSocket` (Tema 3) |
| **Memoria compartida** | Una zona de memoria accesible por varios procesos. Es la más rápida, pero exige sincronizar el acceso. | `FileChannel.map` |
| **Colas de mensajes** | Los mensajes se guardan en orden y varios procesos pueden escribir y leer. | Brokers como RabbitMQ o Kafka |
| **Señales** | Avisos breves del SO: terminar, interrumpir… | `destroy()`, ganchos de cierre |

!!! example "Dos imágenes para recordarlo"
    - **Memoria compartida** = la nevera de un piso compartido. Uno deja algo en una balda y avisa; los demás lo cogen de ahí. Es rápido, pero si dos van a por lo mismo a la vez hay conflicto: hay que **sincronizarse** (Tema 2).
    - **Tubería** = un tubo por el que echas pelotas: entran por un lado y salen por el otro en el mismo orden, en una sola dirección.

## 6.9 Encadenar procesos: `startPipeline`

`ProcessBuilder.startPipeline` (Java 9+) crea varios procesos **conectados por tuberías**: la salida de cada uno es la entrada del siguiente, igual que la barra vertical `|` de la terminal.

```java
// Equivale a: ps -e | grep java | wc -l
List<Process> tuberia = ProcessBuilder.startPipeline(List.of(
        new ProcessBuilder("ps", "-e"),
        new ProcessBuilder("grep", "java"),
        new ProcessBuilder("wc", "-l")));

Process ultimo = tuberia.get(tuberia.size() - 1);
String n = new String(ultimo.getInputStream().readAllBytes()).trim();
System.out.println("Procesos java: " + n);
```

- Los datos intermedios los pasa **el sistema operativo**: Java no interviene.
- Solo leemos la salida del **último** proceso.
- Frente a `bash -c "ps -e | grep java | wc -l"`, no depende de la shell y no hay riesgo de inyección.
- En Windows: `new ProcessBuilder("tasklist")` y `new ProcessBuilder("findstr", "java")`.

## 6.10 Resumen del tema

| Concepto | Lo esencial |
|---|---|
| Proceso | Programa en ejecución, con PID, memoria propia y al menos un hilo. |
| Servicio | Proceso en segundo plano, sin interfaz, que atiende peticiones. |
| Concurrencia | Varias tareas en curso; paralelismo: en el mismo instante. |
| Estados | Nuevo, listo, ejecución, bloqueado y terminado. |
| Planificación | FCFS, SJF, SRTF, prioridades y Round Robin. Cuidado con la inanición. |
| `ProcessBuilder` | Comando troceado, `directory`, `environment`, redirecciones, `start()`. |
| `Process` | `pid`, `waitFor` (con límite), `exitValue`, `destroy`, flujos. |
| Flujos | `getInputStream()` lee la **salida** del hijo. Leer antes de `waitFor()` o redirigir. |
| `ProcessHandle` | Observar y controlar cualquier proceso del sistema. |

## Preguntas de repaso

1. ¿Con qué método lee el padre la salida estándar del hijo? ¿Por qué el nombre puede confundir?
2. Explica por qué un programa puede quedarse bloqueado si llama a `waitFor()` antes de leer la salida del hijo.
3. ¿Qué diferencia hay entre `redirectOutput(f)` y `redirectOutput(Redirect.appendTo(f))`?
4. Al enviar datos a la entrada de un hijo, ¿por qué hay que cerrar el flujo?
5. ¿Qué diferencia hay entre `destroy()` y `destroyForcibly()`? ¿Qué código de salida da cada uno en Linux?
6. Escribe con `ProcessHandle` un fragmento que muestre cuántos hijos tiene tu proceso.
7. ¿Qué mecanismo de IPC usarías para comunicar dos programas que están en ordenadores distintos?
