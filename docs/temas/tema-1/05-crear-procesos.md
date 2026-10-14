# 5. Crear procesos en Java

Hasta ahora has lanzado programas desde la terminal o con doble clic. En este apartado aprenderás a hacer que **tu programa Java lance otros procesos**: comandos del sistema, otras clases Java o el navegador.

## 5.1 Punto de partida: cada `java` es un proceso

```java
public class HolaMundo {
    public static void main(String[] args) {
        System.out.println("¡Hola, mundo!");
    }
}
```

```bash
javac HolaMundo.java     # crea HolaMundo.class: el programa, en disco
java HolaMundo           # el SO crea un proceso: una JVM con su PID que ejecuta el main
```

1. `javac` genera `HolaMundo.class`. Es el **programa**: está en disco y no hace nada.
2. `java HolaMundo` pide al sistema operativo que cree un **proceso**: arranca una máquina virtual de Java, carga la clase y ejecuta `main`.
3. La terminal es el **padre** y el proceso `java` es el **hijo**. Cuando `main` termina, el proceso termina y devuelve un **código de salida**: 0 si todo ha ido bien.

Lo que hace la terminal, crear un proceso hijo y esperar a que termine, lo puede hacer también **nuestro programa**.

## 5.2 Las dos clases: `ProcessBuilder` y `Process`

| Clase | Papel | Métodos principales |
|---|---|---|
| `ProcessBuilder` | **Prepara y lanza** el proceso: qué comando, con qué argumentos, en qué carpeta, con qué variables de entorno y adónde van su entrada y su salida. | `command()`, `directory()`, `environment()`, `inheritIO()`, `redirect…()`, **`start()`** |
| `Process` | **Controla** el proceso ya lanzado. Es como un mando a distancia del hijo. | `pid()`, `waitFor()`, `exitValue()`, `isAlive()`, `destroy()`, flujos de entrada y salida |

`start()` es un método de `ProcessBuilder` y devuelve un objeto `Process`.

!!! warning "No uses `Runtime.exec(String)`"
    En código antiguo verás `Runtime.getRuntime().exec("ping -c 3 8.8.8.8")`. Esa versión está **obsoleta desde Java 18**: trocea el texto por los espacios y falla con rutas que los contienen. Usa siempre `ProcessBuilder`.

## 5.3 Lanzar un proceso y esperar a que termine

```java
import java.io.File;
import java.io.IOException;

public class EjemploProcessBuilder {
    public static void main(String[] args) {
        try {
            ProcessBuilder pb = new ProcessBuilder("ping", "-c", "3", "8.8.8.8"); // Windows: "-n"
            pb.directory(new File(System.getProperty("user.home")));            // carpeta de trabajo
            pb.environment().put("MODO", "prueba");                            // variable de entorno
            pb.inheritIO();                                                     // el hijo usa nuestra consola

            Process p = pb.start();                                             // crea el proceso
            System.out.println("PID del hijo: " + p.pid());

            int codigo = p.waitFor();                                           // espera a que termine
            System.out.println("Terminó con código " + codigo);                 // 0 = todo bien
        } catch (IOException e) {
            System.err.println("Error al lanzar el proceso: " + e.getMessage());
        } catch (InterruptedException e) {
            System.err.println("El proceso fue interrumpido: " + e.getMessage());
            Thread.currentThread().interrupt();
        }
    }
}
```

Línea a línea:

1. **El constructor** recibe el comando **troceado**: primero el programa y luego cada argumento como una cadena distinta. Si escribieras `new ProcessBuilder("ping -c 3 8.8.8.8")`, Java buscaría un programa llamado literalmente «ping -c 3 8.8.8.8» y fallaría.
2. **`directory()`** fija la carpeta de trabajo del hijo. Si no se indica, hereda la del padre.
3. **`environment()`** devuelve un `Map` con las variables de entorno, heredadas del padre; podemos añadir o quitar.
4. **`inheritIO()`** hace que el hijo escriba en nuestra misma consola. Sin esto, su salida va a una tubería que habría que leer (apartado 6).
5. **`start()`** pide al sistema operativo que cree el proceso y devuelve el objeto `Process`.
6. **`waitFor()`** **bloquea** al padre hasta que el hijo termina y devuelve su código de salida. Además, recoge al hijo: así no queda zombi.

### Las dos excepciones

| Excepción | Cuándo ocurre | Qué hacer |
|---|---|---|
| `IOException` | `start()` no puede crear el proceso: el programa no existe, no está en el `PATH` o no tiene permisos de ejecución. | Avisar al usuario con un mensaje claro. |
| `InterruptedException` | Otro hilo interrumpe al padre mientras espera en `waitFor()`. | Volver a marcar la interrupción con `Thread.currentThread().interrupt()`, para que quien llame a nuestro código sepa que ocurrió. |

En ejemplos cortos verás a veces `throws IOException, InterruptedException` en el `main`, para ahorrar espacio. En un programa real, captúralas.

## 5.4 Comandos diferentes según el sistema operativo

Muchos comandos cambian entre sistemas. Para que el programa sea **portable**, se consulta el sistema con `System.getProperty("os.name")`:

```java
String so = System.getProperty("os.name").toLowerCase();
boolean windows = so.contains("win");

ProcessBuilder pb = windows
        ? new ProcessBuilder("cmd", "/c", "dir")   // dir es una orden interna de cmd
        : new ProcessBuilder("ls", "-l");
pb.inheritIO().start().waitFor();
```

| Tarea | Windows | Linux y macOS |
|---|---|---|
| Listar ficheros | `cmd /c dir` | `ls -l` |
| Ping de 3 paquetes | `ping -n 3 host` | `ping -c 3 host` |
| Ver la configuración de red | `ipconfig` | `ip a` (Linux), `ifconfig` (macOS) |
| Abrir una URL o un fichero | `cmd /c start "" url` | `xdg-open url` (Linux), `open url` (macOS) |

!!! note "¿Por qué `cmd /c`?"
    `dir`, `start`, `cd` o `echo` no son programas `.exe`, sino **órdenes internas** del intérprete `cmd`. Para ejecutarlas hay que lanzar `cmd` y pasarle la orden con `/c` («ejecuta esto y termina»). En Linux ocurre algo parecido con `bash -c "orden"`.

## 5.5 El código de salida

Por convenio, un proceso termina con:

- **0** si todo ha ido bien.
- **Cualquier otro valor** si ha habido un error. Cada programa decide el significado de cada número.

En Java, un programa elige su código de salida con **`System.exit(n)`**. Si el `main` termina normalmente, el código es 0. Si termina por una excepción no capturada, es 1.

El padre lo recibe como resultado de `waitFor()`, o después con `exitValue()`.

!!! warning
    El código de salida solo sirve para **números pequeños**: de 0 a 255 en Linux y macOS. Para devolver datos de verdad (un texto, un número grande, una lista), el hijo los **escribe** en su salida y el padre los **lee** (apartado 6).

## 5.6 Ejecutar otra clase Java como proceso: el cocinero y el pinche

Para ejecutar código nuestro en un proceso independiente, lanzamos **otra máquina virtual de Java** con esa clase como programa principal.

El ejemplo: un **cocinero** (proceso padre) encarga a un **pinche** (proceso hijo) que mezcle dos ingredientes y le diga si la mezcla cabe en la olla, que admite 1000 g. El pinche recibe las cantidades **por argumentos** y responde con su **código de salida**.

```
Cocinero (padre)                                  Pinche (hijo)
      │                                                │
      │── start(): java -cp … Pinche 300 400 ────────►│
      │                                                │  suma 300 + 400 = 700 g
      │   waitFor(): el cocinero espera                │
      │◄──────────────────── System.exit(0) ───────────│
      │                                                ✕  el pinche termina
      │  interpreta el código: 0 = cabe, 1 = se pasa
```

### El hijo: `Pinche`

```java
public class Pinche {
    static final int CAPACIDAD_OLLA = 1000;   // gramos

    public static void main(String[] args) {
        int ing1 = Integer.parseInt(args[0]);   // los argumentos llegan como texto
        int ing2 = Integer.parseInt(args[1]);
        int total = ing1 + ing2;

        System.out.println("Pinche (PID " + ProcessHandle.current().pid()
                + "): mezclo " + ing1 + "g + " + ing2 + "g = " + total + "g");

        // Devolvemos el resultado al padre con el código de salida
        System.exit(total <= CAPACIDAD_OLLA ? 0 : 1);
    }
}
```

### El padre: `Cocinero`

```java
import java.io.IOException;

public class Cocinero {

    public static void main(String[] args) {
        mandarTareaAlPinche(300, 400);    // 700 g: cabe
        mandarTareaAlPinche(700, 500);    // 1200 g: se pasa
    }

    public static void mandarTareaAlPinche(int ing1, int ing2) {
        try {
            // El classpath dice a la nueva JVM dónde están nuestras clases compiladas
            String cp = System.getProperty("java.class.path");

            ProcessBuilder pb = new ProcessBuilder(
                    "java", "-cp", cp, "Pinche",
                    String.valueOf(ing1), String.valueOf(ing2));
            pb.inheritIO();                                 // para ver lo que dice el pinche

            System.out.println("Cocinero: Le pido al pinche que mezcle " + ing1 + "g y " + ing2 + "g...");
            Process procesoPinche = pb.start();

            int codigoSalida = procesoPinche.waitFor();     // el cocinero espera al pinche

            if (codigoSalida == 0) {
                System.out.println("Cocinero: Perfectas noticias, la mezcla CABE en la olla.\n");
            } else if (codigoSalida == 1) {
                System.out.println("Cocinero: ¡Atención! La mezcla SE PASA de la capacidad de la olla.\n");
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

Salida real:

```
Cocinero: Le pido al pinche que mezcle 300g y 400g...
Pinche (PID 708): mezclo 300g + 400g = 700g
Cocinero: Perfectas noticias, la mezcla CABE en la olla.

Cocinero: Le pido al pinche que mezcle 700g y 500g...
Pinche (PID 727): mezclo 700g + 500g = 1200g
Cocinero: ¡Atención! La mezcla SE PASA de la capacidad de la olla.
```

Fíjate en que:

- Cada pinche tiene un **PID distinto**: son dos procesos de verdad, dos JVM independientes.
- Los datos **bajan** del padre al hijo como **argumentos** del `main`, siempre como `String`. Por eso se usan `String.valueOf` en el padre e `Integer.parseInt` en el hijo.
- La respuesta **sube** del hijo al padre como **código de salida**, con `System.exit`. Un `return` en el `main` devolvería siempre 0.
- Hay que compilar **las dos clases** (`javac *.java`). Si falta `Pinche.class`, el hijo falla con «Could not find or load main class Pinche».

!!! tip "Usar la misma JVM que el padre"
    En lugar de `"java"` a secas, se puede usar la ruta de la JVM que está ejecutando el padre. Así funciona aunque `java` no esté en el `PATH` o haya varias versiones instaladas:

    ```java
    String java = Path.of(System.getProperty("java.home"), "bin", "java").toString();
    ```

!!! note "¿Procesos o hilos?"
    Arrancar una JVM entera cuesta decenas de megas de memoria y unas décimas de segundo. Si solo queremos hacer algo en paralelo dentro de nuestro programa, es mucho más barato un hilo (Tema 2). Se usan procesos cuando queremos **aislamiento**: si el pinche falla, el cocinero sigue funcionando.

## 5.7 Abrir una página web desde Java

Para abrir una web no programamos un navegador: le pedimos al sistema operativo que abra la URL con el **navegador predeterminado**. Y eso se hace lanzando un proceso.

En macOS, el comando es `open`:

```java
import java.io.IOException;

public class AbrirWeb {
    public static void main(String[] args) {
        String url = "https://www.sevillafc.es/";
        try {
            ProcessBuilder pb = new ProcessBuilder("open", url);   // macOS
            pb.inheritIO();
            Process p = pb.start();
            System.out.println("Abriendo la web " + url + " ... (PID: " + p.pid() + ")");
            int codigo = p.waitFor();
            System.out.println("Proceso finalizado con código: " + codigo);
        } catch (IOException | InterruptedException e) {
            System.err.println("Ocurrió un error al intentar abrir el navegador:");
            e.printStackTrace();
        }
    }
}
```

### ¿Qué proceso se ha lanzado?

1. Java lanza **`open`**: ese es nuestro proceso hijo, y su PID es el que se imprime.
2. `open` consulta cuál es el navegador predeterminado y le pide que abra la URL. Si el navegador ya estaba abierto, solo añade una pestaña.
3. `open` **termina enseguida** con código 0. El navegador sigue abierto, pero **no es hijo nuestro**: si cerramos el programa Java, la web sigue abierta.

### Versión para cualquier sistema

```java
static void abrir(String url) throws IOException, InterruptedException {
    String so = System.getProperty("os.name").toLowerCase();
    List<String> cmd;
    if (so.contains("win"))      cmd = List.of("cmd", "/c", "start", "", url);
    else if (so.contains("mac")) cmd = List.of("open", url);
    else                         cmd = List.of("xdg-open", url);        // Linux

    Process p = new ProcessBuilder(cmd).inheritIO().start();
    System.out.println("Lanzado " + cmd.get(0) + " con PID " + p.pid());
    System.out.println("Código de salida: " + p.waitFor());
}
```

!!! warning "El `""` de Windows"
    `start` interpreta el primer argumento entre comillas como el **título de la ventana**. Sin la cadena vacía `""`, tomaría la URL como título y no abriría nada.

!!! note "Alternativa sin procesos"
    `java.awt.Desktop.getDesktop().browse(new URI(url))` también abre una web y elige el comando por nosotros. Pero no crea un proceso que podamos controlar, no da PID ni código de salida y no funciona en equipos sin entorno gráfico. En este tema usamos `ProcessBuilder` porque lo que estudiamos son los procesos.

## 5.8 Errores frecuentes

| Error | Qué pasa | Solución |
|---|---|---|
| Pasar el comando en una sola cadena | `IOException`: no encuentra el programa | Trocear: `"ping", "-c", "3", "8.8.8.8"` |
| Usar `ping` sin límite en Linux | El hijo no termina nunca y `waitFor()` espera para siempre | `-c 3` en Linux y macOS, `-n 3` en Windows |
| No compilar la clase hija | «Could not find or load main class» | `javac *.java` |
| Devolver el resultado con `return` | El código de salida siempre es 0 | `System.exit(n)` |
| Lanzar procesos dentro de un bucle sin control | El equipo se llena de procesos y se queda sin recursos | Comprobar bien la condición del bucle y esperar a los hijos |
| Concatenar lo que escribe el usuario en una orden de `cmd` o `bash` | **Inyección de órdenes**: el usuario puede ejecutar lo que quiera | Pasar los datos como argumentos separados y validarlos |

## Preguntas de repaso

1. ¿Qué diferencia hay entre `ProcessBuilder` y `Process`? ¿De cuál es el método `start()`?
2. ¿Por qué hay que trocear el comando? ¿Qué pasa si no se hace?
3. ¿Para qué sirve `inheritIO()`? ¿Qué pasa con la salida del hijo si no se llama?
4. En el ejemplo del cocinero, ¿por dónde viajan los datos del padre al hijo? ¿Y la respuesta del hijo al padre?
5. Al abrir una web, ¿por qué el proceso termina enseguida aunque el navegador siga abierto?
6. ¿Qué excepción lanza `start()` si el programa no existe? ¿Y `waitFor()` si interrumpen al padre?
