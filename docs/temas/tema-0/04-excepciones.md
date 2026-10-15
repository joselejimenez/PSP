# 4. Excepciones

## 4.1 ¿Qué es una excepción?

Una **excepción** es un objeto que representa un **error durante la ejecución**: dividir entre cero, abrir un fichero que no existe, convertir `"abc"` a número… Cuando ocurre, Java **interrumpe** el flujo normal y busca quién la gestione. Si nadie lo hace, el programa termina mostrando la **traza de la pila** (*stack trace*):

```text
Exception in thread "main" java.lang.NumberFormatException: For input string: "abc"
    at java.base/java.lang.Integer.parseInt(Integer.java:661)
    at Prueba.main(Prueba.java:5)
```

La traza se lee **de arriba abajo**: el tipo de excepción, el mensaje y la línea exacta donde se produjo (`Prueba.java:5`).

## 4.2 Jerarquía

```text
Throwable
├── Error                       → fallos graves de la JVM (OutOfMemoryError, StackOverflowError). No se capturan.
└── Exception
    ├── IOException, InterruptedException, ...   → COMPROBADAS (checked)
    └── RuntimeException                          → NO COMPROBADAS (unchecked)
        ├── NullPointerException
        ├── ArithmeticException
        ├── ArrayIndexOutOfBoundsException
        ├── NumberFormatException (hija de IllegalArgumentException)
        └── IllegalStateException
```

| | Comprobadas (*checked*) | No comprobadas (*unchecked*) |
|---|---|---|
| Hereda de | `Exception` (pero no de `RuntimeException`) | `RuntimeException` |
| ¿Obliga el compilador a tratarla? | **Sí**: hay que capturarla o declararla con `throws`. | No. |
| Suelen indicar | Problemas externos: ficheros, red, procesos, interrupciones. | Errores de programación: `null`, índices, argumentos inválidos. |
| Ejemplos | `IOException`, `InterruptedException` | `NullPointerException`, `NumberFormatException` |

!!! tip "Las vas a ver mucho en PSP"
    `IOException` aparece al lanzar procesos y usar sockets (Temas 1 y 3). `InterruptedException` aparece con `waitFor()`, `sleep()` y `join()` (Temas 1 y 2). Ambas son **comprobadas**.

## 4.3 Capturar: `try` / `catch` / `finally`

```java
try {
    int n = Integer.parseInt(texto);
    System.out.println(100 / n);
} catch (NumberFormatException e) {
    System.err.println("No es un número: " + texto);
} catch (ArithmeticException e) {
    System.err.println("No se puede dividir entre cero");
} finally {
    System.out.println("Esto se ejecuta siempre");
}
```

- Los `catch` se comprueban **en orden**; se ejecuta el primero cuyo tipo coincide. Pon primero las excepciones **más concretas**.
- `finally` se ejecuta **siempre**, haya error o no, incluso si hay un `return` dentro del `try`. Sirve para liberar recursos.
- **Multi-catch**: `catch (NumberFormatException | ArithmeticException e)` agrupa casos que se tratan igual.

Métodos útiles del objeto excepción: `e.getMessage()` (mensaje), `e.printStackTrace()` (traza completa), `e.getClass().getSimpleName()` (tipo).

!!! danger "No silencies las excepciones"
    Un `catch (Exception e) { }` vacío oculta los errores y hace imposible depurar. Como mínimo, informa con `System.err.println(...)`.

### `try` con recursos

Los objetos que hay que cerrar (ficheros, *streams*, sockets) implementan `AutoCloseable`. Si se declaran en el paréntesis del `try`, Java los **cierra automáticamente** al terminar, aunque haya una excepción:

```java
try (BufferedReader br = Files.newBufferedReader(Path.of("datos.txt"))) {
    System.out.println(br.readLine());
} catch (IOException e) {
    System.err.println("Error de lectura: " + e.getMessage());
}   // br.close() se llama solo
```

Es la forma recomendada de trabajar con ficheros (apartado 8) y sockets (Tema 3).

## 4.4 Lanzar y declarar: `throw` y `throws`

- `throw` **lanza** una excepción.
- `throws` en la cabecera de un método **avisa** de que puede lanzar una excepción comprobada y delega su tratamiento en quien lo llame.

```java
static void retirar(double saldo, double cantidad) {
    if (cantidad <= 0) {
        throw new IllegalArgumentException("La cantidad debe ser positiva");
    }
    if (cantidad > saldo) {
        throw new IllegalStateException("Saldo insuficiente");
    }
}

static String primeraLinea(String fichero) throws IOException {
    return Files.readAllLines(Path.of(fichero)).get(0);   // no la capturamos aquí
}
```

En un `main` pequeño se puede declarar `throws Exception` para no capturar nada, pero en programas reales hay que tratar los errores y dar mensajes claros.

## 4.5 Excepciones propias

Se crea una clase que hereda de `Exception` (comprobada) o de `RuntimeException` (no comprobada):

```java
public class SaldoInsuficienteException extends Exception {
    public SaldoInsuficienteException(String mensaje) {
        super(mensaje);
    }
}
```

```java
void retirar(double cantidad) throws SaldoInsuficienteException {
    if (cantidad > saldo) {
        throw new SaldoInsuficienteException("Faltan " + (cantidad - saldo) + " €");
    }
    saldo -= cantidad;
}
```

Así el código que llama sabe exactamente **qué** ha fallado y puede reaccionar de forma específica.

## Preguntas de repaso

1. ¿Qué diferencia hay entre una excepción comprobada y una no comprobada? Pon un ejemplo de cada una.
2. ¿En qué orden deben ir los `catch`? ¿Por qué?
3. ¿Cuándo se ejecuta el bloque `finally`?
4. ¿Qué ventaja tiene `try` con recursos?
5. ¿Qué diferencia hay entre `throw` y `throws`?

!!! example "Practica"
    [Ejercicio 10](boletin.md#ejercicio-10). Los ejercicios 9, 19 y 20 también gestionan errores.
