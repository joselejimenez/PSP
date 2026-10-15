# 3. Cadenas de texto

## 3.1 La clase `String`

Un `String` es una secuencia de caracteres. Es una **clase**, pero se crea normalmente con un literal:

```java
String saludo = "Hola";
String vacio = "";
String nombre = null;        // no apunta a ningún objeto
```

!!! note "Los `String` son inmutables"
    Un `String` **nunca cambia** una vez creado. Métodos como `toUpperCase()` o `replace()` no modifican la cadena: **devuelven una nueva**.

    ```java
    String s = "hola";
    s.toUpperCase();          // se pierde el resultado
    s = s.toUpperCase();      // correcto: s ahora vale "HOLA"
    ```

### Métodos más usados

| Método | Ejemplo con `s = "Programación"` | Resultado |
|---|---|---|
| `length()` | `s.length()` | `12` |
| `charAt(i)` | `s.charAt(0)` | `'P'` |
| `substring(ini, fin)` | `s.substring(0, 4)` | `"Prog"` (fin **no incluido**) |
| `indexOf(texto)` | `s.indexOf("gra")` | `3` (`-1` si no está) |
| `contains(texto)` | `s.contains("ama")` | `true` |
| `startsWith` / `endsWith` | `s.endsWith("ión")` | `true` |
| `toUpperCase` / `toLowerCase` | `s.toLowerCase()` | `"programación"` |
| `replace(a, b)` | `s.replace("a", "4")` | `"Progr4m4ción"` |
| `trim()` / `strip()` | `"  hola ".strip()` | `"hola"` |
| `isEmpty()` / `isBlank()` | `"  ".isBlank()` | `true` |
| `split(sep)` | `"a;b;c".split(";")` | `{"a", "b", "c"}` |
| `repeat(n)` | `"-".repeat(5)` | `"-----"` |
| `String.join(sep, ...)` | `String.join(", ", "a", "b")` | `"a, b"` |

### Recorrer una cadena carácter a carácter

```java
String frase = "Hola Mundo";
int mayusculas = 0;
for (int i = 0; i < frase.length(); i++) {
    char c = frase.charAt(i);
    if (Character.isUpperCase(c)) mayusculas++;
}
```

La clase `Character` tiene métodos útiles: `isLetter`, `isDigit`, `isWhitespace`, `isUpperCase`, `toUpperCase`…

## 3.2 Comparar cadenas: `equals` frente a `==`

!!! danger "Nunca compares textos con `==`"
    `==` compara **referencias** (si son el mismo objeto en memoria), no el contenido. Dos cadenas con el mismo texto pueden ser objetos distintos.

```java
String a = "java";
String b = new Scanner(System.in).nextLine();   // el usuario escribe "java"

a == b                    // false: son objetos distintos
a.equals(b)               // true: mismo contenido
a.equalsIgnoreCase("JAVA")// true: ignora mayúsculas
"java".equals(nombre)     // seguro aunque nombre sea null
a.compareTo("python")     // negativo: "java" va antes en orden alfabético
```

## 3.3 Construir texto: `StringBuilder`

Como `String` es inmutable, concatenar con `+` dentro de un bucle crea un objeto nuevo en cada vuelta. Para construir texto por partes se usa `StringBuilder`, que **sí es modificable**:

```java
StringBuilder sb = new StringBuilder();
for (int i = 1; i <= 5; i++) {
    sb.append(i).append(", ");
}
sb.setLength(sb.length() - 2);    // quita la última ", "
String resultado = sb.toString(); // "1, 2, 3, 4, 5"

new StringBuilder("hola").reverse().toString();  // "aloh"
```

Otros métodos: `insert(pos, texto)`, `deleteCharAt(pos)`, `replace(ini, fin, texto)`.

## 3.4 Dar formato al texto

`String.format` (o el método `formatted`) y `System.out.printf` usan **especificadores de formato**:

| Especificador | Significado | Ejemplo | Resultado |
|---|---|---|---|
| `%s` | Texto | `"%s"`, `"Ana"` | `Ana` |
| `%d` | Entero | `"%d"`, `42` | `42` |
| `%.2f` | Decimal con 2 decimales | `"%.2f"`, `3.14159` | `3,14` (según el idioma del sistema) |
| `%10s` / `%-10s` | Ancho 10, a la derecha / izquierda | `"%-6s"`, `"ab"` | `ab` seguido de 4 espacios |
| `%05d` | Rellenar con ceros | `"%05d"`, `42` | `00042` |
| `%n` | Salto de línea | | |

```java
String linea = String.format("%-12s %6.2f €", "Café", 1.2);
String otra = "%s tiene %d años".formatted("Luis", 20);
System.out.printf("Total: %.2f%n", 12.5);
```

!!! tip "Punto o coma decimal"
    El formato usa el idioma del sistema. Para forzar el punto: `String.format(Locale.US, "%.2f", x)`.

### Bloques de texto (Java 15+)

Para textos de varias líneas se usan tres comillas dobles. Se respetan los saltos de línea y se elimina la sangría común:

```java
String menu = """
        1. Nuevo pedido
        2. Listar pedidos
        0. Salir
        """;
```

## 3.5 Convertir entre texto y números

```java
int n = Integer.parseInt("42");
double d = Double.parseDouble("3.75");      // con punto, independientemente del idioma
boolean b = Boolean.parseBoolean("true");

String s1 = String.valueOf(42);
String s2 = "" + 3.5;                         // también funciona
String s3 = Integer.toString(255, 2);         // "11111111" (base 2)
```

Si el texto no es un número válido, `parseInt` y `parseDouble` lanzan `NumberFormatException` (apartado 4). Antes de convertir conviene limpiar con `strip()`.

### Ejemplo: procesar una línea CSV

```java
String linea = "Ana; 19 ; 7.5";
String[] campos = linea.split(";");
String nombre = campos[0].strip();
int edad = Integer.parseInt(campos[1].strip());
double nota = Double.parseDouble(campos[2].strip());
```

!!! note "`split` usa expresiones regulares"
    Caracteres como `.`, `|` o `+` tienen significado especial. Para separar por un punto: `split("\\.")`. Para separar por uno o más espacios: `split("\\s+")`.

## Preguntas de repaso

1. ¿Qué imprime `String s = "abc"; s.toUpperCase(); System.out.println(s);`? ¿Por qué?
2. ¿Por qué no se deben comparar cadenas con `==`?
3. ¿Cuándo conviene usar `StringBuilder` en lugar de `+`?
4. ¿Qué devuelve `"Hola mundo".substring(5)`?
5. ¿Qué excepción lanza `Integer.parseInt("12a")`?

!!! example "Practica"
    [Ejercicio 7](boletin.md#ejercicio-7) · [Ejercicio 8](boletin.md#ejercicio-8) · [Ejercicio 9](boletin.md#ejercicio-9)
