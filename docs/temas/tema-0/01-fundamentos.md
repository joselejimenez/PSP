# 1. Fundamentos

## 1.1 Estructura de un programa

Todo programa Java está formado por **clases**. Para que una clase se pueda ejecutar necesita un método `main`, que es el punto de entrada:

```java title="HolaMundo.java"
public class HolaMundo {
    public static void main(String[] args) {
        System.out.println("Hola, mundo");
    }
}
```

| Elemento | Significado |
|---|---|
| `public class HolaMundo` | Declara la clase. El fichero **debe llamarse igual**: `HolaMundo.java`. |
| `public static void main(String[] args)` | Método que ejecuta la JVM al lanzar la clase. `args` contiene los argumentos de la línea de órdenes. |
| `System.out.println(...)` | Escribe un texto en la salida estándar y salta de línea. `print` no salta de línea. |
| `;` y `{ }` | Cada instrucción termina en punto y coma; las llaves delimitan bloques. |

!!! note "Del código fuente a la ejecución"
    `javac` traduce el `.java` a **bytecode** (`.class`) y la **JVM** lo ejecuta. Por eso el mismo `.class` funciona en Windows, Linux y macOS.

Los **comentarios** se escriben así:

```java
// comentario de una línea
/* comentario de
   varias líneas */
/** comentario de documentación (Javadoc) */
```

## 1.2 Tipos de datos y variables

Una **variable** es un nombre que guarda un valor de un tipo concreto. Java es un lenguaje de **tipado estático**: el tipo se fija al declararla y no cambia.

### Tipos primitivos

| Tipo | Tamaño | Ejemplo | Uso típico |
|---|---|---|---|
| `byte` | 8 bits | `byte b = 100;` | Datos binarios. |
| `short` | 16 bits | `short s = 3000;` | Poco usado. |
| `int` | 32 bits | `int edad = 19;` | **Enteros en general.** |
| `long` | 64 bits | `long ms = 1_700_000_000_000L;` | Enteros grandes, tiempos en milisegundos. |
| `float` | 32 bits | `float f = 3.5f;` | Decimales con poca precisión. |
| `double` | 64 bits | `double precio = 2.75;` | **Decimales en general.** |
| `char` | 16 bits | `char letra = 'A';` | Un carácter (comillas simples). |
| `boolean` | — | `boolean activo = true;` | `true` o `false`. |

`String` **no es primitivo**: es una clase (apartado 3), pero se usa tanto que tiene literales propios: `"texto"`.

```java
int contador = 0;            // declarar e inicializar
final double IVA = 0.21;     // final: constante, no se puede reasignar
var nombre = "Lucía";        // var: el compilador deduce el tipo (String)
```

!!! warning "`var` no es tipado dinámico"
    `var x = 5;` declara un `int`. Si después escribes `x = "hola";` el compilador da error. `var` solo ahorra escribir el tipo cuando es evidente.

### Conversión entre tipos (*casting*)

- **Implícita (ensanchamiento)**: de un tipo pequeño a uno mayor, sin pérdida. `int` → `long` → `double`.
- **Explícita (estrechamiento)**: hay que indicarla y puede perder información.

```java
int i = 7;
double d = i;          // 7.0, automático
double nota = 6.8;
int entera = (int) nota;   // 6: el casting TRUNCA, no redondea
long redondeada = Math.round(nota); // 7
```

## 1.3 Operadores

| Tipo | Operadores | Ejemplo |
|---|---|---|
| Aritméticos | `+ - * / %` | `7 / 2` vale `3`; `7 % 2` vale `1` |
| Asignación | `= += -= *= /= %=` | `total += precio;` |
| Incremento | `++ --` | `i++` |
| Relacionales | `== != < > <= >=` | `edad >= 18` |
| Lógicos | <code>&amp;&amp; &#124;&#124; !</code> | `edad >= 18 && carnet` |
| Ternario | `cond ? a : b` | `n % 2 == 0 ? "par" : "impar"` |

!!! danger "La división entera"
    Si los dos operandos son enteros, el resultado es entero: `5 / 2` es `2`, no `2.5`. Para obtener decimales, al menos uno debe ser `double`: `5 / 2.0` o `(double) a / b`.

`&&` y `||` son **perezosos** (*short-circuit*): si la primera condición ya decide el resultado, la segunda no se evalúa. Por eso es seguro escribir `texto != null && texto.length() > 0`.

## 1.4 Leer datos del teclado con `Scanner`

```java title="Saludo.java"
import java.util.Scanner;

public class Saludo {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("¿Cómo te llamas? ");
        String nombre = sc.nextLine();
        System.out.print("¿Cuántos años tienes? ");
        int edad = sc.nextInt();
        System.out.println("Hola, " + nombre + ". El año que viene tendrás " + (edad + 1));
    }
}
```

| Método | Lee |
|---|---|
| `nextLine()` | Una línea completa (hasta el salto de línea). |
| `next()` | Una palabra. |
| `nextInt()`, `nextDouble()` | Un número. Lanza `InputMismatchException` si no lo es. |
| `hasNextInt()` | Comprueba, sin leer, si lo siguiente es un entero. |

!!! warning "La trampa de `nextInt()` + `nextLine()`"
    `nextInt()` lee el número pero **deja el salto de línea** en la entrada. Un `nextLine()` posterior lee esa línea vacía. Soluciones: llamar a un `nextLine()` extra para descartarla, o leer siempre con `nextLine()` y convertir con `Integer.parseInt(...)`.

!!! note "Decimales y configuración regional"
    `Scanner` usa la configuración regional del sistema: en español espera `3,5` en lugar de `3.5`. Para aceptar el punto usa `sc.useLocale(java.util.Locale.US);`.

## 1.5 Estructuras condicionales

### `if` / `else if` / `else`

```java
if (nota >= 9) {
    System.out.println("Sobresaliente");
} else if (nota >= 5) {
    System.out.println("Aprobado");
} else {
    System.out.println("Suspenso");
}
```

Las condiciones se evalúan **en orden** y solo se ejecuta el primer bloque cuya condición sea cierta.

### `switch` moderno (Java 14+)

El `switch` con flecha no necesita `break` y puede **devolver un valor** (*switch expression*):

```java
String tipo = switch (dia) {
    case 1, 2, 3, 4, 5 -> "Laborable";
    case 6, 7 -> "Fin de semana";
    default -> "Día no válido";
};
```

Si un caso necesita varias instrucciones, se usa un bloque y `yield` para devolver el valor:

```java
int dias = switch (mes) {
    case 2 -> {
        boolean bisiesto = (anio % 4 == 0 && anio % 100 != 0) || anio % 400 == 0;
        yield bisiesto ? 29 : 28;
    }
    case 4, 6, 9, 11 -> 30;
    default -> 31;
};
```

!!! tip "`switch` clásico"
    Seguirás viendo el `switch` con `case X:` y `break;`. Funciona, pero si olvidas un `break` la ejecución «cae» al caso siguiente. En código nuevo, usa la flecha.

## 1.6 Bucles

| Bucle | Cuándo usarlo |
|---|---|
| `for` | Sabes cuántas veces se repite. |
| `while` | Se repite mientras se cumpla una condición; puede no ejecutarse nunca. |
| `do-while` | Se ejecuta **al menos una vez**: típico en menús y validación de datos. |
| `for-each` | Recorrer todos los elementos de un array o colección (apartados 2 y 6). |

```java
for (int i = 1; i <= 10; i++) {
    System.out.println("7 x " + i + " = " + 7 * i);
}

int n = 12345, cifras = 0;
while (n > 0) {
    n /= 10;
    cifras++;
}

int opcion;
do {
    System.out.print("Opción (0 para salir): ");
    opcion = sc.nextInt();
} while (opcion != 0);
```

- `break` sale del bucle inmediatamente.
- `continue` salta a la siguiente iteración.

### Los argumentos de `main`

```bash
java Bucles 7 10
```

```java
public static void main(String[] args) {
    if (args.length < 2) {
        System.err.println("Uso: java Bucles <número> <límite>");
        return;
    }
    int numero = Integer.parseInt(args[0]);   // "7" -> 7
    int limite = Integer.parseInt(args[1]);
}
```

Los argumentos llegan siempre como **texto**: hay que convertirlos. En el Tema 1 los usaremos para pasar datos a los procesos hijos.

## Preguntas de repaso

1. ¿Qué vale `(int) 9.99`? ¿Y `Math.round(9.99)`?
2. ¿Por qué `10 / 4` vale `2`? ¿Cómo obtienes `2.5`?
3. ¿Qué diferencia hay entre `while` y `do-while`?
4. ¿Qué ventaja tiene el `switch` con flecha sobre el clásico?
5. ¿En qué tipo llegan siempre los argumentos de `main`?

!!! example "Practica"
    [Ejercicio 1](boletin.md#ejercicio-1) · [Ejercicio 2](boletin.md#ejercicio-2) · [Ejercicio 3](boletin.md#ejercicio-3)
