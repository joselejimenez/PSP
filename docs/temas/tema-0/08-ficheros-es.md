# 8. Ficheros y entrada/salida estándar

## 8.1 Rutas: `Path`

Desde Java 7 se trabaja con ficheros a través del paquete `java.nio.file`. Una **ruta** se representa con `Path`:

```java
import java.nio.file.*;

Path ruta = Path.of("datos", "notas.txt");   // datos/notas.txt (o datos\notas.txt en Windows)
ruta.getFileName();                           // notas.txt
ruta.getParent();                             // datos
ruta.toAbsolutePath();                        // ruta completa desde la raíz
```

!!! note "Rutas relativas"
    Una ruta relativa se resuelve desde el **directorio de trabajo** del programa: la carpeta desde la que lo lanzas (`System.getProperty("user.dir")`). En el Tema 1 verás que al lanzar un proceso hijo puedes elegir su directorio de trabajo con `ProcessBuilder.directory(...)`.

## 8.2 La clase `Files`

`Files` ofrece métodos `static` para las operaciones habituales:

| Método | Hace |
|---|---|
| `Files.exists(ruta)` | Comprueba si existe. |
| `Files.isDirectory(ruta)` | Comprueba si es un directorio. |
| `Files.createDirectories(ruta)` | Crea el directorio y los que falten por encima. |
| `Files.readString(ruta)` | Lee el fichero completo como texto. |
| `Files.readAllLines(ruta)` | Lee todas las líneas en una `List<String>`. |
| `Files.lines(ruta)` | Stream de líneas (para ficheros grandes; hay que cerrarlo). |
| `Files.writeString(ruta, texto)` | Escribe (crea o sobrescribe). |
| `Files.write(ruta, lineas)` | Escribe una lista de líneas. |
| `Files.copy`, `Files.move`, `Files.delete` | Copiar, mover y borrar. |
| `Files.size(ruta)` | Tamaño en bytes. |

```java
Path f = Path.of("saludo.txt");
Files.writeString(f, "Hola\nAdiós\n");
List<String> lineas = Files.readAllLines(f);          // [Hola, Adiós]
Files.writeString(f, "Otra línea\n", StandardOpenOption.APPEND);   // añadir al final
```

Casi todos lanzan `IOException`, que es **comprobada**: hay que capturarla o declararla.

## 8.3 Leer y escribir con *buffer*

Para ficheros grandes, o cuando hay que procesar línea a línea, se usan `BufferedReader` y `BufferedWriter`. El **buffer** agrupa las lecturas y escrituras para no acceder al disco en cada carácter. Siempre dentro de un **try con recursos**:

```java
try (BufferedReader br = Files.newBufferedReader(Path.of("notas.txt"))) {
    String linea;
    while ((linea = br.readLine()) != null) {     // null = fin del fichero
        System.out.println(linea);
    }
} catch (IOException e) {
    System.err.println("No se pudo leer: " + e.getMessage());
}

try (BufferedWriter bw = Files.newBufferedWriter(Path.of("informe.txt"))) {
    bw.write("Informe de notas");
    bw.newLine();
} catch (IOException e) {
    System.err.println("No se pudo escribir: " + e.getMessage());
}
```

!!! warning "Codificación de caracteres"
    `Files` usa **UTF-8** por defecto. Si un fichero se ve con caracteres extraños (`Ã±` en lugar de `ñ`), probablemente se escribió con otra codificación. Se puede indicar: `Files.newBufferedReader(ruta, StandardCharsets.ISO_8859_1)`.

## 8.4 Los tres flujos estándar

Todo proceso, también un programa Java, tiene tres **flujos estándar** abiertos al arrancar:

| Flujo | En Java | Por defecto | Uso |
|---|---|---|---|
| Entrada estándar (*stdin*) | `System.in` | Teclado | Datos que recibe el programa. |
| Salida estándar (*stdout*) | `System.out` | Pantalla | Resultados. |
| Salida de error (*stderr*) | `System.err` | Pantalla | Mensajes de error y avisos. |

Aunque `out` y `err` salen los dos por pantalla, son **canales distintos**. La terminal permite **redirigirlos** por separado:

```bash
java Programa < entrada.txt              # stdin desde un fichero
java Programa > resultado.txt            # stdout a un fichero (los errores siguen en pantalla)
java Programa 2> errores.txt             # stderr a un fichero
java Programa < datos.txt > salida.txt 2> errores.txt
cat datos.txt | java Programa            # la salida de un programa es la entrada de otro
```

### Leer de la entrada estándar línea a línea

Un programa que lee de `System.in` hasta el final y escribe en `System.out` se llama **filtro**. Funciona igual con teclado, con un fichero redirigido o con otro proceso:

```java title="Mayusculas.java"
import java.io.*;

public class Mayusculas {
    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String linea;
        int n = 0;
        while ((linea = in.readLine()) != null) {
            System.out.println(linea.toUpperCase());
            n++;
        }
        System.err.println("Líneas procesadas: " + n);
    }
}
```

```bash
java Mayusculas < poema.txt > POEMA.txt     # en pantalla solo aparece "Líneas procesadas: ..."
```

Desde teclado, el fin de la entrada se indica con <kbd>Ctrl</kbd>+<kbd>D</kbd> (Linux y macOS) o <kbd>Ctrl</kbd>+<kbd>Z</kbd> seguido de <kbd>Intro</kbd> (Windows).

## 8.5 El código de salida

Al terminar, todo proceso devuelve al sistema un número entero: su **código de salida** (*exit code*).

| Código | Significado por convenio |
|---|---|
| `0` | Todo ha ido bien. |
| Distinto de `0` | Ha habido un error. Cada programa define qué significa cada valor. |

```java
if (args.length == 0) {
    System.err.println("Uso: java Programa <fichero>");
    System.exit(2);          // termina el proceso con código 2
}
```

Si `main` termina con normalidad, el código es `0`; si termina por una excepción no capturada, es `1`. Para consultarlo desde la terminal:

```bash
java Programa
echo $?                 # Linux y macOS
echo %ERRORLEVEL%       # Windows (cmd)
echo $LASTEXITCODE      # Windows (PowerShell)
```

!!! tip "La conexión directa con el Tema 1"
    En el Tema 1 un programa Java lanzará **otros procesos** con `ProcessBuilder` y:

    - les escribirá en su **entrada estándar**,
    - leerá su **salida estándar** y su **salida de error**,
    - esperará a que terminen y consultará su **código de salida** con `waitFor()` y `exitValue()`.

    Un programa filtro bien hecho, que separa resultados (`out`), errores (`err`) y devuelve un código coherente, es exactamente lo que necesitas para esa comunicación. El ejercicio 20 del boletín es un ejemplo completo.

## Preguntas de repaso

1. ¿Desde qué carpeta se resuelve una ruta relativa?
2. ¿Qué devuelve `readLine()` al llegar al final del fichero?
3. ¿Por qué conviene usar try con recursos al trabajar con ficheros?
4. ¿Por qué tiene sentido escribir los errores en `System.err` y no en `System.out`?
5. ¿Qué código de salida devuelve un programa que termina por una excepción no capturada?

!!! example "Practica"
    [Ejercicio 19](boletin.md#ejercicio-19) · [Ejercicio 20](boletin.md#ejercicio-20)
