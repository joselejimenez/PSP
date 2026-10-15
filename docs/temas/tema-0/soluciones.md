# Tema 0 · Soluciones del boletín

!!! warning "Página para el profesorado"
    Soluciones completas del boletín de repaso. Todo el código está compilado y ejecutado con JDK 21; las salidas son reales.

## Ejercicio 1 · Conversor de temperaturas

**Fundamentos** · ★☆☆☆☆

```java title="Conversor.java"
import java.util.Scanner;

/** Ejercicio 1 · Variables, tipos y operadores. */
public class Conversor {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Temperatura en grados Celsius: ");
        double celsius = Double.parseDouble(sc.nextLine().trim().replace(',', '.'));

        double fahrenheit = celsius * 9 / 5 + 32;
        double kelvin = celsius + 273.15;
        System.out.printf("%.2f ºC = %.2f ºF = %.2f K%n", celsius, fahrenheit, kelvin);

        // División entera frente a división real
        int a = 7, b = 2;
        System.out.println("7 / 2   = " + (a / b));          // 3: los dos operandos son int
        System.out.println("7 / 2.0 = " + (a / 2.0));        // 3.5: uno es double
        System.out.println("7 % 2   = " + (a % b));          // 1: resto
        System.out.println("(double) 7 / 2 = " + ((double) a / b));

        // Desbordamiento y conversiones
        int grande = Integer.MAX_VALUE;
        System.out.println("MAX_VALUE + 1 = " + (grande + 1)); // se da la vuelta
        long seguro = (long) grande + 1;
        System.out.println("como long     = " + seguro);
        int truncado = (int) 9.99;
        System.out.println("(int) 9.99    = " + truncado);
        System.out.println("Math.round(9.5) = " + Math.round(9.5));
    }
}
```

**Salida (entrada: 25)**

```text
Temperatura en grados Celsius: 25.00 ºC = 77.00 ºF = 298.15 K
7 / 2   = 3
7 / 2.0 = 3.5
7 % 2   = 1
(double) 7 / 2 = 3.5
MAX_VALUE + 1 = -2147483648
como long     = 2147483648
(int) 9.99    = 9
Math.round(9.5) = 10
```

**Claves para corregir**

- En 7 / 2 los dos operandos son int, así que la división es entera (3). Basta con que uno sea double para obtener 3.5.
- Un int ocupa 32 bits: al sumar 1 al máximo se «da la vuelta» al mínimo (desbordamiento). Un long tiene 64 bits.
- El casting (int) trunca, no redondea. Math.round sí redondea.

## Ejercicio 2 · Calificaciones y días de la semana

**Fundamentos** · ★☆☆☆☆

```java title="Calificaciones.java"
import java.util.Scanner;

/** Ejercicio 2 · Condicionales y switch. */
public class Calificaciones {
    static String calificacion(double nota) {
        if (nota < 0 || nota > 10) return "Nota no válida";
        if (nota < 5) return "Insuficiente";
        if (nota < 6) return "Suficiente";
        if (nota < 7) return "Bien";
        if (nota < 9) return "Notable";
        return "Sobresaliente";
    }

    static String diaSemana(int n) {
        return switch (n) {                              // switch como expresión (Java 14+)
            case 1, 2, 3, 4, 5 -> "laborable";
            case 6, 7 -> "fin de semana";
            default -> "día no válido";
        };
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Nota: ");
        double nota = Double.parseDouble(sc.nextLine().trim().replace(',', '.'));
        System.out.println(calificacion(nota));

        System.out.print("Día de la semana (1-7): ");
        int dia = Integer.parseInt(sc.nextLine().trim());
        System.out.println("Es " + diaSemana(dia));

        boolean aprobado = nota >= 5;
        // operador ternario
        String mensaje = aprobado ? "¡Enhorabuena!" : "Ánimo para la recuperación";
        System.out.println(mensaje);
    }
}
```

**Salida (entrada: 7.8 y después 6)**

```text
Nota: Notable
Día de la semana (1-7): Es fin de semana
¡Enhorabuena!
```

**Claves para corregir**

- Ordenar las condiciones de menor a mayor permite usar solo «<» en cada if, porque los casos anteriores ya se han descartado.
- El switch con flechas no necesita break y puede devolver un valor directamente.

## Ejercicio 3 · Tablas, cifras y números primos

**Fundamentos** · ★☆☆☆☆

```java title="Bucles.java"
/** Ejercicio 3 · Bucles for, while y do-while. */
public class Bucles {
    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : 7;

        // a) Tabla de multiplicar con for
        System.out.println("Tabla del " + n);
        for (int i = 1; i <= 10; i++) {
            System.out.printf("%2d x %2d = %3d%n", n, i, n * i);
        }

        // b) Suma de las cifras con while
        int numero = 98765, suma = 0, copia = numero;
        while (copia > 0) {
            suma += copia % 10;
            copia /= 10;
        }
        System.out.println("Suma de las cifras de " + numero + ": " + suma);

        // c) Primos hasta 50 con bucles anidados, break y continue
        System.out.print("Primos hasta 50:");
        for (int x = 2; x <= 50; x++) {
            boolean primo = true;
            for (int d = 2; d * d <= x; d++) {
                if (x % d == 0) { primo = false; break; }
            }
            if (!primo) continue;
            System.out.print(" " + x);
        }
        System.out.println();

        // d) do-while: se ejecuta al menos una vez
        int intentos = 0;
        do {
            intentos++;
        } while (intentos < 3);
        System.out.println("Intentos: " + intentos);
    }
}
```

**Salida**

```text
Tabla del 7
 7 x  1 =   7
 7 x  2 =  14
 7 x  3 =  21
 7 x  4 =  28
 7 x  5 =  35
 7 x  6 =  42
 7 x  7 =  49
 7 x  8 =  56
 7 x  9 =  63
 7 x 10 =  70
Suma de las cifras de 98765: 35
Primos hasta 50: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47
Intentos: 3
```

**Claves para corregir**

- copia % 10 da la última cifra y copia / 10 la elimina.
- El do-while comprueba la condición al final, así que se ejecuta al menos una vez.

## Ejercicio 4 · Biblioteca de utilidades

**Métodos** · ★★☆☆☆

```java title="Utilidades.java"
/** Ejercicio 4 · Métodos, parámetros, sobrecarga y recursividad. */
public class Utilidades {
    static long factorial(int n) {                       // iterativo
        long r = 1;
        for (int i = 2; i <= n; i++) r *= i;
        return r;
    }

    static long factorialRec(int n) {                    // recursivo
        return n <= 1 ? 1 : n * factorialRec(n - 1);
    }

    static int mcd(int a, int b) {                       // algoritmo de Euclides
        return b == 0 ? a : mcd(b, a % b);
    }

    static boolean esPrimo(int n) {
        if (n < 2) return false;
        for (int d = 2; d * d <= n; d++) if (n % d == 0) return false;
        return true;
    }

    // Sobrecarga: mismo nombre, distintos parámetros
    static int maximo(int a, int b) { return a > b ? a : b; }
    static double maximo(double a, double b) { return Math.max(a, b); }
    static int maximo(int... numeros) {                  // número variable de argumentos
        int m = numeros[0];
        for (int x : numeros) if (x > m) m = x;
        return m;
    }

    // paso por valor: no cambia el original
    static void incrementar(int x) { x++; }

    public static void main(String[] args) {
        System.out.println("10! = " + factorial(10) + " = " + factorialRec(10));
        System.out.println("mcd(84, 36) = " + mcd(84, 36));
        System.out.println("¿97 es primo? " + esPrimo(97));
        System.out.println("máximo(3, 8) = " + maximo(3, 8));
        System.out.println("máximo(2.5, 1.5) = " + maximo(2.5, 1.5));
        System.out.println("máximo(4, 9, 1, 7) = " + maximo(4, 9, 1, 7));
        int v = 5;
        incrementar(v);
        System.out.println("v sigue valiendo " + v);
    }
}
```

**Salida**

```text
10! = 3628800 = 3628800
mcd(84, 36) = 12
¿97 es primo? true
máximo(3, 8) = 8
máximo(2.5, 1.5) = 2.5
máximo(4, 9, 1, 7) = 9
v sigue valiendo 5
```

**Claves para corregir**

- Java pasa siempre los parámetros por valor: el método recibe una copia del int. Con objetos se copia la referencia, así que sí se puede modificar el objeto, pero no hacer que la variable apunte a otro.
- La recursividad necesita un caso base (n <= 1) para terminar.
- Con sobrecarga, Java elige el método según el tipo y el número de los argumentos.

## Ejercicio 5 · Temperaturas de la semana

**Arrays** · ★★☆☆☆

```java title="EstadisticasArray.java"
import java.util.Arrays;

/** Ejercicio 5 · Arrays. */
public class EstadisticasArray {
    public static void main(String[] args) {
        String[] dias = {"lun", "mar", "mié", "jue", "vie", "sáb", "dom"};
        double[] temp = {18.5, 21.0, 19.2, 24.8, 23.1, 16.4, 20.0};

        double suma = 0, max = temp[0], min = temp[0];
        int iMax = 0, iMin = 0;
        for (int i = 0; i < temp.length; i++) {
            suma += temp[i];
            if (temp[i] > max) { max = temp[i]; iMax = i; }
            if (temp[i] < min) { min = temp[i]; iMin = i; }
        }
        double media = suma / temp.length;
        System.out.printf("Media: %.2f ºC%n", media);
        System.out.printf("Máxima: %.1f ºC (%s) · Mínima: %.1f ºC (%s)%n",
                max, dias[iMax], min, dias[iMin]);

        System.out.print("Días por encima de la media:");
        for (int i = 0; i < temp.length; i++)
            if (temp[i] > media) System.out.print(" " + dias[i]);
        System.out.println();

        // copia: no tocamos el original
        double[] ordenadas = Arrays.copyOf(temp, temp.length);
        Arrays.sort(ordenadas);
        System.out.println("Ordenadas: " + Arrays.toString(ordenadas));
        System.out.println("Original:  " + Arrays.toString(temp));
    }
}
```

**Salida**

```text
Media: 20.43 ºC
Máxima: 24.8 ºC (jue) · Mínima: 16.4 ºC (sáb)
Días por encima de la media: mar jue vie
Ordenadas: [16.4, 18.5, 19.2, 20.0, 21.0, 23.1, 24.8]
Original:  [18.5, 21.0, 19.2, 24.8, 23.1, 16.4, 20.0]
```

**Claves para corregir**

- Guardar el índice de la máxima y de la mínima permite saber a qué día corresponden.
- Arrays.sort ordena el array que recibe; para no perder el original hay que copiarlo antes con Arrays.copyOf.

## Ejercicio 6 · Operaciones con matrices

**Arrays** · ★★☆☆☆

```java title="Matrices.java"
/** Ejercicio 6 · Arrays bidimensionales. */
public class Matrices {
    static void mostrar(int[][] m) {
        for (int[] fila : m) {
            for (int x : fila) System.out.printf("%4d", x);
            System.out.println();
        }
    }

    public static void main(String[] args) {
        int[][] m = {
            {1, 2, 3, 4},
            {5, 6, 7, 8},
            {9, 10, 11, 12}
        };
        System.out.println("Matriz " + m.length + "x" + m[0].length + ":");
        mostrar(m);

        for (int f = 0; f < m.length; f++) {
            int suma = 0;
            for (int c = 0; c < m[f].length; c++) suma += m[f][c];
            System.out.println("Suma fila " + f + ": " + suma);
        }
        for (int c = 0; c < m[0].length; c++) {
            int suma = 0;
            for (int[] fila : m) suma += fila[c];
            System.out.println("Suma columna " + c + ": " + suma);
        }

        int[][] t = new int[m[0].length][m.length];
        for (int f = 0; f < m.length; f++)
            for (int c = 0; c < m[0].length; c++)
                t[c][f] = m[f][c];
        System.out.println("Traspuesta:");
        mostrar(t);
    }
}
```

**Salida**

```text
Matriz 3x4:
   1   2   3   4
   5   6   7   8
   9  10  11  12
Suma fila 0: 10
Suma fila 1: 26
Suma fila 2: 42
Suma columna 0: 15
Suma columna 1: 18
Suma columna 2: 21
Suma columna 3: 24
Traspuesta:
   1   5   9
   2   6  10
   3   7  11
   4   8  12
```

**Claves para corregir**

- m.length es el número de filas y m[0].length el de columnas.
- En la traspuesta, el elemento [f][c] pasa a la posición [c][f].

## Ejercicio 7 · Análisis de una frase

**Cadenas** · ★★☆☆☆

```java title="Cadenas.java"
import java.text.Normalizer;

/** Ejercicio 7 · Cadenas de texto (String). */
public class Cadenas {
    static int contarVocales(String s) {
        int n = 0;
        for (char c : quitarTildes(s.toLowerCase()).toCharArray())
            if ("aeiou".indexOf(c) >= 0) n++;
        return n;
    }

    static String invertir(String s) {
        String r = "";
        for (int i = s.length() - 1; i >= 0; i--) r += s.charAt(i);
        return r;
    }

    static String quitarTildes(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFD).replaceAll("\\p{M}", "");
    }

    static boolean esPalindromo(String s) {
        String limpio = quitarTildes(s.toLowerCase()).replaceAll("[^a-z0-9]", "");
        return limpio.equals(invertir(limpio));
    }

    public static void main(String[] args) {
        String frase = "Dábale arroz a la zorra el abad";
        System.out.println("Frase: " + frase);
        System.out.println("Longitud: " + frase.length());
        System.out.println("Mayúsculas: " + frase.toUpperCase());
        System.out.println("Vocales: " + contarVocales(frase));
        System.out.println("Invertida: " + invertir(frase));
        System.out.println("¿Palíndromo? " + esPalindromo(frase));
        System.out.println("Primera palabra: " + frase.substring(0, frase.indexOf(' ')));
        System.out.println("¿Contiene 'zorra'? " + frase.contains("zorra"));
        System.out.println("Reemplazo: " + frase.replace("zorra", "gata"));

        String a = "java";
        String b = new String("java");
        System.out.println("a == b      -> " + (a == b));        // compara referencias
        System.out.println("a.equals(b) -> " + a.equals(b));     // compara contenido
        System.out.println("equalsIgnoreCase: " + "JAVA".equalsIgnoreCase(a));
    }
}
```

**Salida**

```text
Frase: Dábale arroz a la zorra el abad
Longitud: 31
Mayúsculas: DÁBALE ARROZ A LA ZORRA EL ABAD
Vocales: 12
Invertida: daba le arroz al a zorra elabáD
¿Palíndromo? true
Primera palabra: Dábale
¿Contiene 'zorra'? true
Reemplazo: Dábale arroz a la gata el abad
a == b      -> false
a.equals(b) -> true
equalsIgnoreCase: true
```

**Claves para corregir**

- == compara si dos variables apuntan al mismo objeto; equals compara el contenido. Con cadenas, usa siempre equals.
- Los String son inmutables: replace o toUpperCase devuelven una cadena nueva y no cambian la original.

## Ejercicio 8 · Ticket de la cafetería

**Cadenas** · ★★☆☆☆

```java title="Ticket.java"
/** Ejercicio 8 · StringBuilder, String.format y bloques de texto. */
public class Ticket {
    public static void main(String[] args) {
        String[] productos = {"Café", "Tostada con tomate", "Zumo de naranja"};
        int[] cantidades = {2, 1, 2};
        double[] precios = {1.30, 2.50, 2.20};

        StringBuilder sb = new StringBuilder();
        sb.append("=".repeat(40)).append('\n');
        sb.append(String.format("%-22s %4s %12s%n", "Producto", "Ud.", "Importe"));
        sb.append("-".repeat(40)).append('\n');
        double total = 0;
        for (int i = 0; i < productos.length; i++) {
            double importe = cantidades[i] * precios[i];
            total += importe;
            sb.append(String.format("%-22s %4d %10.2f €%n",
                    productos[i], cantidades[i], importe));
        }
        sb.append("-".repeat(40)).append('\n');
        sb.append(String.format("%-27s %10.2f €%n", "TOTAL", total));
        double iva = total - total / 1.10;
        sb.append(String.format("%-27s %10.2f €%n", "IVA incluido (10 %)", iva));
        sb.append("=".repeat(40));
        System.out.println(sb);

        String pie = """
                Gracias por su visita
                Cafetería del IES Rafael Alberti""";   // bloque de texto (Java 15+)
        System.out.println(pie);
    }
}
```

**Salida**

```text
========================================
Producto                Ud.      Importe
----------------------------------------
Café                      2       2.60 €
Tostada con tomate        1       2.50 €
Zumo de naranja           2       4.40 €
----------------------------------------
TOTAL                             9.50 €
IVA incluido (10 %)               0.86 €
========================================
Gracias por su visita
Cafetería del IES Rafael Alberti
```

**Claves para corregir**

- Concatenar con + dentro de un bucle crea muchas cadenas intermedias; StringBuilder va añadiendo sobre el mismo objeto.
- El IVA incluido se calcula como total − total / 1,10.

## Ejercicio 9 · Procesar un fichero CSV

**Cadenas** · ★★★☆☆

```java title="ProcesarCSV.java"
/** Ejercicio 9 · split, parseo y argumentos del main. */
public class ProcesarCSV {
    public static void main(String[] args) {
        String[] lineas = {
            "nombre;edad;nota",
            "Ana;19;8.5",
            "Luis;20;6,75",
            "Marta;veinte;9",
            "Pablo;21",
            "  Sara ; 22 ; 4.9 "
        };
        double umbral = args.length > 0 ? Double.parseDouble(args[0]) : 5.0;

        int validas = 0, errores = 0, aprobados = 0;
        double suma = 0;
        for (int i = 1; i < lineas.length; i++) {              // la 0 es la cabecera
            String[] campos = lineas[i].split(";");
            if (campos.length != 3) {
                System.err.println("Línea " + i + ": se esperaban 3 campos -> " + lineas[i]);
                errores++;
                continue;
            }
            try {
                String nombre = campos[0].trim();
                int edad = Integer.parseInt(campos[1].trim());
                double nota = Double.parseDouble(campos[2].trim().replace(',', '.'));
                validas++;
                suma += nota;
                if (nota >= umbral) aprobados++;
                System.out.printf("%-6s %2d años  %5.2f %s%n",
                        nombre, edad, nota, nota >= umbral ? "APTO" : "NO APTO");
            } catch (NumberFormatException e) {
                System.err.println("Línea " + i + ": número no válido -> " + lineas[i]);
                errores++;
            }
        }
        System.out.printf("Válidas: %d · Errores: %d · Aprobados: %d · Media: %.2f%n",
                validas, errores, aprobados, suma / validas);
        // código de salida para quien nos lance
        System.exit(errores == 0 ? 0 : 1);
    }
}
```

**Salida**

```text
Ana    19 años   8.50 APTO
Luis   20 años   6.75 APTO
Línea 3: número no válido -> Marta;veinte;9
Línea 4: se esperaban 3 campos -> Pablo;21
Sara   22 años   4.90 NO APTO
Válidas: 3 · Errores: 2 · Aprobados: 2 · Media: 6.72
Código de salida: 1
```

**Claves para corregir**

- System.err es un flujo distinto de System.out. En el Tema 1 verás cómo el padre los lee por separado.
- El código de salida es la forma más sencilla de que un proceso le diga a su padre si todo ha ido bien.

## Ejercicio 10 · Excepciones bajo control

**Excepciones** · ★★★☆☆

```java title="Excepciones.java"
import java.util.Scanner;

/** Ejercicio 10 · Excepciones: try/catch/finally, throw y excepciones propias. */
public class Excepciones {

    static class EdadInvalidaException extends Exception {   // excepción comprobada propia
        EdadInvalidaException(String mensaje) { super(mensaje); }
    }

    static int validarEdad(int edad) throws EdadInvalidaException {
        if (edad < 0 || edad > 120)
            throw new EdadInvalidaException("Edad fuera de rango: " + edad);
        return edad;
    }

    static double dividir(int a, int b) {
        if (b == 0) throw new ArithmeticException("No se puede dividir entre cero");
        return (double) a / b;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 1) Leer un entero repitiendo hasta que sea válido
        int numero;
        while (true) {
            System.out.print("Escribe un número entero: ");
            try {
                numero = Integer.parseInt(sc.nextLine().trim());
                break;
            } catch (NumberFormatException e) {
                System.out.println("  Eso no es un entero, prueba otra vez");
            }
        }

        // 2) Excepción no comprobada con finally
        try {
            System.out.println("100 / " + numero + " = " + dividir(100, numero));
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("(el bloque finally se ejecuta siempre)");
        }

        // 3) Excepción propia
        try {
            validarEdad(25);
            System.out.println("25 es una edad válida");
            validarEdad(150);
        } catch (EdadInvalidaException e) {
            System.out.println("Error: " + e.getMessage());
        }

        // 4) Varias excepciones en un solo catch
        String[] datos = {"10"};
        try {
            int x = Integer.parseInt(datos[1]);
            System.out.println(x);
        } catch (ArrayIndexOutOfBoundsException | NumberFormatException e) {
            System.out.println("Error de datos: " + e.getClass().getSimpleName());
        }
    }
}
```

**Salida (entrada: hola y después 0)**

```text
Escribe un número entero:   Eso no es un entero, prueba otra vez
Escribe un número entero: Error: No se puede dividir entre cero
(el bloque finally se ejecuta siempre)
25 es una edad válida
Error: Edad fuera de rango: 150
Error de datos: ArrayIndexOutOfBoundsException
```

**Claves para corregir**

- Las excepciones comprobadas (extends Exception) obligan a capturarlas o a declararlas con throws; las no comprobadas (extends RuntimeException) no.
- finally se ejecuta siempre, haya excepción o no. Se usa para liberar recursos.
- IOException e InterruptedException, que verás con ProcessBuilder, son comprobadas.

## Ejercicio 11 · Cuenta bancaria

**Programación orientada a objetos** · ★★★☆☆

```java title="CuentaBancaria.java"
/** Ejercicio 11 · Clases, objetos y encapsulación. */
public class CuentaBancaria {
    private final String iban;
    private final String titular;
    private double saldo;

    public CuentaBancaria(String iban, String titular, double saldoInicial) {
        if (saldoInicial < 0)
            throw new IllegalArgumentException("El saldo inicial no puede ser negativo");
        this.iban = iban;
        this.titular = titular;
        this.saldo = saldoInicial;
    }

    public CuentaBancaria(String iban, String titular) {     // constructor sobrecargado
        this(iban, titular, 0);
    }

    public String getIban() { return iban; }
    public String getTitular() { return titular; }
    // sin setSaldo: solo se cambia con operaciones
    public double getSaldo() { return saldo; }

    public void ingresar(double cantidad) {
        if (cantidad <= 0) throw new IllegalArgumentException("Cantidad no válida");
        saldo += cantidad;
    }

    public boolean retirar(double cantidad) {
        if (cantidad <= 0 || cantidad > saldo) return false;
        saldo -= cantidad;
        return true;
    }

    public boolean transferir(CuentaBancaria destino, double cantidad) {
        if (!retirar(cantidad)) return false;
        destino.ingresar(cantidad);
        return true;
    }

    @Override
    public String toString() {
        return String.format("%s (%s): %.2f €", titular, iban, saldo);
    }

    public static void main(String[] args) {
        CuentaBancaria ana = new CuentaBancaria("ES11-0001", "Ana", 500);
        CuentaBancaria luis = new CuentaBancaria("ES22-0002", "Luis");
        ana.ingresar(150);
        System.out.println("¿Retira 1000? " + ana.retirar(1000));
        System.out.println("¿Transfiere 200 a Luis? " + ana.transferir(luis, 200));
        System.out.println(ana);
        System.out.println(luis);
        try {
            luis.ingresar(-50);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

**Salida**

```text
¿Retira 1000? false
¿Transfiere 200 a Luis? true
Ana (ES11-0001): 450.00 €
Luis (ES22-0002): 200.00 €
Error: Cantidad no válida
```

**Claves para corregir**

- No hay setSaldo: el saldo solo cambia a través de operaciones que validan los datos.
- transferir reutiliza retirar e ingresar, así las reglas están en un solo sitio.

## Ejercicio 12 · Tickets de soporte

**Programación orientada a objetos** · ★★★☆☆

```java title="Static.java"
/** Ejercicio 12 · Miembros static, constantes y clases de utilidad. */
public class Static {

    static final class MathUtil {                       // clase de utilidad: no se instancia
        public static final double IVA = 0.21;
        private MathUtil() { }
        static double conIva(double precio) { return precio * (1 + IVA); }
    }

    static class Ticket {
        private static int siguienteId = 1;              // compartido por todos los objetos
        private final int id;                             // propio de cada objeto
        private final String descripcion;

        Ticket(String descripcion) {
            this.id = siguienteId++;
            this.descripcion = descripcion;
        }

        static int creados() { return siguienteId - 1; }

        @Override public String toString() { return "#" + id + " " + descripcion; }
    }

    public static void main(String[] args) {
        Ticket t1 = new Ticket("Impresora sin tóner");
        Ticket t2 = new Ticket("No arranca el PC 12");
        Ticket t3 = new Ticket("Wifi lenta");
        System.out.println(t1 + " | " + t2 + " | " + t3);
        System.out.println("Tickets creados: " + Ticket.creados());
        System.out.printf("100 € con IVA: %.2f €%n", MathUtil.conIva(100));
        System.out.println("Math también es una clase de utilidad: " + Math.max(3, 9));
    }
}
```

**Salida**

```text
#1 Impresora sin tóner | #2 No arranca el PC 12 | #3 Wifi lenta
Tickets creados: 3
100 € con IVA: 121.00 €
Math también es una clase de utilidad: 9
```

**Claves para corregir**

- Un atributo static existe una sola vez y lo comparten todos los objetos; uno normal, uno por objeto.
- El constructor privado impide crear objetos de una clase que solo tiene métodos static, como Math.

## Ejercicio 13 · Plantilla de empleados

**Herencia** · ★★★☆☆

```java title="Empleados.java"
import java.util.List;

/** Ejercicio 13 · Herencia y polimorfismo. */
public class Empleados {

    static class Empleado {
        protected final String nombre;
        protected final double salarioBase;

        Empleado(String nombre, double salarioBase) {
            this.nombre = nombre;
            this.salarioBase = salarioBase;
        }

        double salario() { return salarioBase; }

        String descripcion() {
            return String.format("%-8s %-14s %8.2f €",
                    nombre, getClass().getSimpleName(), salario());
        }
    }

    static class Desarrollador extends Empleado {
        private final int horasExtra;

        Desarrollador(String nombre, double salarioBase, int horasExtra) {
            super(nombre, salarioBase);                  // llama al constructor del padre
            this.horasExtra = horasExtra;
        }

        @Override
        double salario() { return salarioBase + horasExtra * 25; }
    }

    static class Gerente extends Empleado {
        private final double bonus;

        Gerente(String nombre, double salarioBase, double bonus) {
            super(nombre, salarioBase);
            this.bonus = bonus;
        }

        @Override
        // reutiliza el cálculo del padre
        double salario() { return super.salario() * 1.10 + bonus; }
    }

    public static void main(String[] args) {
        List<Empleado> plantilla = List.of(
            new Empleado("Carmen", 1500),
            new Desarrollador("Iván", 1900, 10),
            new Gerente("Lucía", 2600, 400));

        double total = 0;
        // polimorfismo: cada uno usa su salario()
        for (Empleado e : plantilla) {
            System.out.println(e.descripcion());
            total += e.salario();
        }
        System.out.printf("Total nóminas: %.2f €%n", total);

        Empleado e = plantilla.get(2);
        if (e instanceof Gerente g) {                     // pattern matching (Java 16+)
            System.out.println(g.nombre + " es gerente con bonus de " + g.bonus + " €");
        }
    }
}
```

**Salida**

```text
Carmen   Empleado        1500.00 €
Iván     Desarrollador   2150.00 €
Lucía    Gerente         3260.00 €
Total nóminas: 6910.00 €
Lucía es gerente con bonus de 400.0 €
```

**Claves para corregir**

- Polimorfismo: la variable es de tipo Empleado, pero se ejecuta el salario() de la clase real del objeto.
- super(...) llama al constructor del padre y debe ser la primera línea del constructor de la hija.

## Ejercicio 14 · Figuras geométricas

**Herencia** · ★★★★☆

```java title="Figuras.java"
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Ejercicio 14 · Clases abstractas e interfaces. */
public class Figuras {

    interface Dibujable {
        void dibujar();
        default void dibujarConMarco() {                 // método por defecto (Java 8+)
            System.out.println("+-----------------+");
            dibujar();
            System.out.println("+-----------------+");
        }
    }

    static abstract class Figura implements Comparable<Figura> {
        abstract double area();                          // cada hija decide cómo se calcula
        abstract double perimetro();

        @Override
        public int compareTo(Figura otra) { return Double.compare(area(), otra.area()); }

        @Override
        public String toString() {
            return String.format("%-10s área %7.2f  perímetro %6.2f",
                    getClass().getSimpleName(), area(), perimetro());
        }
    }

    static class Circulo extends Figura implements Dibujable {
        private final double radio;
        Circulo(double radio) { this.radio = radio; }
        double area() { return Math.PI * radio * radio; }
        double perimetro() { return 2 * Math.PI * radio; }
        public void dibujar() { System.out.println("   (  círculo  )"); }
    }

    static class Rectangulo extends Figura implements Dibujable {
        private final double base, altura;
        Rectangulo(double base, double altura) { this.base = base; this.altura = altura; }
        double area() { return base * altura; }
        double perimetro() { return 2 * (base + altura); }
        public void dibujar() { System.out.println("   [ rectángulo ]"); }
    }

    static class Triangulo extends Figura {
        private final double a, b, c;
        Triangulo(double a, double b, double c) { this.a = a; this.b = b; this.c = c; }
        double area() {                                  // fórmula de Herón
            double s = perimetro() / 2;
            return Math.sqrt(s * (s - a) * (s - b) * (s - c));
        }
        double perimetro() { return a + b + c; }
    }

    public static void main(String[] args) {
        List<Figura> figuras = new ArrayList<>(List.of(
            new Rectangulo(4, 5), new Circulo(2), new Triangulo(3, 4, 5)));
        Collections.sort(figuras);                       // usa compareTo: de menor a mayor área
        figuras.forEach(System.out::println);

        for (Figura f : figuras)
            if (f instanceof Dibujable d) d.dibujarConMarco();
    }
}
```

**Salida**

```text
Triangulo  área    6.00  perímetro  12.00
Circulo    área   12.57  perímetro  12.57
Rectangulo área   20.00  perímetro  18.00
+-----------------+
   (  círculo  )
+-----------------+
+-----------------+
   [ rectángulo ]
+-----------------+
```

**Claves para corregir**

- Una clase abstracta no se puede instanciar y puede tener código común; una interfaz define un contrato que pueden cumplir clases que no tienen nada que ver.
- Una clase solo puede heredar de una clase, pero implementar varias interfaces.

## Ejercicio 15 · Gestión de alumnos

**Colecciones** · ★★★☆☆

```java title="GestionAlumnos.java"
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;

/** Ejercicio 15 · Listas (ArrayList) y ordenación. */
public class GestionAlumnos {

    static class Alumno {
        private final String nombre;
        private final String grupo;
        private final double nota;
        Alumno(String nombre, String grupo, double nota) {
            this.nombre = nombre;
            this.grupo = grupo;
            this.nota = nota;
        }
        String getNombre() { return nombre; }
        String getGrupo() { return grupo; }
        double getNota() { return nota; }
        @Override
        public String toString() { return String.format("%-7s %-5s %5.2f", nombre, grupo, nota); }
    }

    static Alumno buscar(List<Alumno> lista, String nombre) {
        for (Alumno a : lista) if (a.getNombre().equalsIgnoreCase(nombre)) return a;
        return null;
    }

    public static void main(String[] args) {
        List<Alumno> alumnos = new ArrayList<>();
        alumnos.add(new Alumno("Lucía", "2DAM", 8.2));
        alumnos.add(new Alumno("Mario", "2DAM", 4.5));
        alumnos.add(new Alumno("Elena", "2DAW", 9.1));
        alumnos.add(new Alumno("Hugo", "2DAM", 6.8));
        alumnos.add(new Alumno("Nora", "2DAW", 3.9));
        System.out.println("Total: " + alumnos.size());

        alumnos.sort(Comparator.comparing(Alumno::getNota).reversed());
        System.out.println("Por nota (mayor a menor):");
        alumnos.forEach(System.out::println);

        alumnos.sort(Comparator.comparing(Alumno::getGrupo).thenComparing(Alumno::getNombre));
        System.out.println("Por grupo y nombre:");
        alumnos.forEach(System.out::println);

        System.out.println("Buscar 'hugo': " + buscar(alumnos, "hugo"));

        // borrar mientras se recorre: con Iterator
        Iterator<Alumno> it = alumnos.iterator();
        while (it.hasNext()) if (it.next().getNota() < 5) it.remove();
        System.out.println("Aprobados: " + alumnos.size());
        alumnos.forEach(System.out::println);
    }
}
```

**Salida**

```text
Total: 5
Por nota (mayor a menor):
Elena   2DAW   9.10
Lucía   2DAM   8.20
Hugo    2DAM   6.80
Mario   2DAM   4.50
Nora    2DAW   3.90
Por grupo y nombre:
Hugo    2DAM   6.80
Lucía   2DAM   8.20
Mario   2DAM   4.50
Elena   2DAW   9.10
Nora    2DAW   3.90
Buscar 'hugo': Hugo    2DAM   6.80
Aprobados: 3
Hugo    2DAM   6.80
Lucía   2DAM   8.20
Elena   2DAW   9.10
```

**Claves para corregir**

- Borrar de una lista dentro de un for-each lanza ConcurrentModificationException; con Iterator.remove() o removeIf es seguro.
- Alumno::getNota es una referencia a método: equivale a la lambda a -> a.getNota().

## Ejercicio 16 · Frecuencia de palabras

**Colecciones** · ★★★★☆

```java title="FrecuenciaPalabras.java"
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;

/** Ejercicio 16 · Map y Set. */
public class FrecuenciaPalabras {
    public static void main(String[] args) {
        String texto = """
                El proceso padre crea un proceso hijo. El hijo hereda el entorno del padre
                y el padre espera al hijo con waitFor. Cada proceso tiene su PID.""";

        String[] palabras = texto.toLowerCase().split("[^\\p{L}]+");

        Map<String, Integer> frecuencia = new HashMap<>();
        for (String p : palabras) {
            if (p.isBlank()) continue;
            frecuencia.merge(p, 1, Integer::sum);         // suma 1 o crea con 1
        }

        Map<String, Integer> ordenado = new TreeMap<>(frecuencia);   // ordenado por clave
        System.out.println("Frecuencias: " + ordenado);

        System.out.println("Las 3 más repetidas:");
        frecuencia.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed()
                        .thenComparing(Map.Entry.comparingByKey()))
                .limit(3)
                .forEach(e -> System.out.println("  " + e.getKey() + " = " + e.getValue()));

        Set<String> unicas = new HashSet<>(frecuencia.keySet());
        Set<String> alfabetico = new TreeSet<>(unicas);
        System.out.println("Palabras distintas: " + unicas.size());
        System.out.println("En orden alfabético: " + alfabetico);
        System.out.println("¿Aparece 'pid'? " + unicas.contains("pid"));
        System.out.println("¿Se puede añadir 'padre' otra vez? " + unicas.add("padre"));
    }
}
```

**Salida**

```text
Frecuencias: {al=1, cada=1, con=1, crea=1, del=1, el=4, entorno=1, espera=1, hereda=1, hijo=3, padre=3, pid=1, proceso=3, su=1, tiene=1, un=1, waitfor=1, y=1}
Las 3 más repetidas:
  el = 4
  hijo = 3
  padre = 3
Palabras distintas: 18
En orden alfabético: [al, cada, con, crea, del, el, entorno, espera, hereda, hijo, padre, pid, proceso, su, tiene, un, waitfor, y]
¿Aparece 'pid'? true
¿Se puede añadir 'padre' otra vez? false
```

**Claves para corregir**

- merge(p, 1, Integer::sum) pone 1 si la clave no existe y, si existe, le suma 1.
- HashMap y HashSet no garantizan ningún orden; TreeMap y TreeSet mantienen las claves ordenadas.
- Un Set no admite duplicados: add devuelve false si el elemento ya estaba.

## Ejercicio 17 · Catálogo con streams

**Programación funcional** · ★★★★☆

```java title="Streams.java"
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/** Ejercicio 17 · Lambdas, interfaces funcionales y streams. */
public class Streams {
    record Producto(String nombre, String categoria, double precio, int stock) { }

    public static void main(String[] args) {
        List<Producto> catalogo = List.of(
            new Producto("Ratón", "Periféricos", 19.90, 40),
            new Producto("Teclado", "Periféricos", 45.00, 0),
            new Producto("Monitor 27\"", "Pantallas", 229.00, 8),
            new Producto("Portátil", "Equipos", 899.00, 3),
            new Producto("Webcam", "Periféricos", 59.90, 12),
            new Producto("Monitor 24\"", "Pantallas", 159.00, 0));

        // lambda guardada en una variable
        Predicate<Producto> hayStock = p -> p.stock() > 0;

        List<String> baratosConStock = catalogo.stream()
                .filter(hayStock)
                .filter(p -> p.precio() < 100)
                .map(Producto::nombre)
                .sorted()
                .toList();
        System.out.println("Con stock y < 100 €: " + baratosConStock);

        double valorAlmacen = catalogo.stream().mapToDouble(p -> p.precio() * p.stock()).sum();
        System.out.printf("Valor del almacén: %.2f €%n", valorAlmacen);

        Map<String, Long> porCategoria = catalogo.stream()
                .collect(Collectors.groupingBy(Producto::categoria, Collectors.counting()));
        System.out.println("Productos por categoría: " + porCategoria);

        Optional<Producto> masCaro = catalogo.stream()
                .max((a, b) -> Double.compare(a.precio(), b.precio()));
        masCaro.ifPresent(p -> System.out.println("El más caro: " + p.nombre()));

        List<String> agotados = catalogo.stream()
                .filter(hayStock.negate()).map(Producto::nombre).toList();
        System.out.println("Agotados: " + agotados);

        Runnable aviso = () -> System.out.println("Runnable: tarea sin parámetros ni resultado");
        // en el Tema 2 la ejecutará un hilo
        aviso.run();
    }
}
```

**Salida**

```text
Con stock y < 100 €: [Ratón, Webcam]
Valor del almacén: 6043.80 €
Productos por categoría: {Pantallas=2, Periféricos=3, Equipos=1}
El más caro: Portátil
Agotados: [Teclado, Monitor 24"]
Runnable: tarea sin parámetros ni resultado
```

**Claves para corregir**

- Una lambda es una forma corta de implementar una interfaz con un único método abstracto (interfaz funcional), como Runnable o Predicate.
- Un stream no modifica la lista original: crea una tubería de operaciones que termina en toList, sum, count…
- En el Tema 2 harás new Thread(aviso).start() para que esa tarea la ejecute otro hilo.

## Ejercicio 18 · Estado de los pedidos

**Tipos modernos** · ★★★☆☆

```java title="Pedidos.java"
import java.util.ArrayList;
import java.util.List;

/** Ejercicio 18 · Enumeraciones y records. */
public class Pedidos {

    enum Estado {
        PENDIENTE("Pendiente de pago"),
        PAGADO("Pagado"),
        ENVIADO("En camino"),
        ENTREGADO("Entregado"),
        CANCELADO("Cancelado");

        private final String texto;
        Estado(String texto) { this.texto = texto; }
        String texto() { return texto; }

        Estado siguiente() {
            return switch (this) {
                case PENDIENTE -> PAGADO;
                case PAGADO -> ENVIADO;
                case ENVIADO, ENTREGADO -> ENTREGADO;
                case CANCELADO -> CANCELADO;
            };
        }
    }

    record Pedido(int id, String cliente, double importe, Estado estado) {
        Pedido {                                          // constructor compacto: validación
            if (importe <= 0)
                throw new IllegalArgumentException("Importe no válido: " + importe);
            if (cliente == null || cliente.isBlank())
                throw new IllegalArgumentException("Falta el cliente");
        }

        // inmutable: devuelve uno nuevo
        Pedido avanzar() { return new Pedido(id, cliente, importe, estado.siguiente()); }
    }

    public static void main(String[] args) {
        List<Pedido> pedidos = new ArrayList<>(List.of(
            new Pedido(1, "Ana", 35.5, Estado.PENDIENTE),
            new Pedido(2, "Luis", 120.0, Estado.PAGADO),
            new Pedido(3, "Sara", 18.9, Estado.ENVIADO)));

        for (int i = 0; i < pedidos.size(); i++) pedidos.set(i, pedidos.get(i).avanzar());
        pedidos.forEach(p -> System.out.printf("%d %-5s %7.2f € -> %s%n",
                p.id(), p.cliente(), p.importe(), p.estado().texto()));

        System.out.println("Estados posibles:");
        for (Estado e : Estado.values())
            System.out.println("  " + e.ordinal() + " " + e + " (" + e.texto() + ")");
        System.out.println("valueOf(\"ENVIADO\"): " + Estado.valueOf("ENVIADO"));

        Pedido copia = new Pedido(2, "Luis", 120.0, Estado.ENVIADO);
        // record: equals por contenido
        System.out.println("¿Iguales? " + copia.equals(pedidos.get(1)));
        // record: toString automático
        System.out.println(copia);

        try {
            new Pedido(4, "", 10, Estado.PENDIENTE);
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

**Salida**

```text
1 Ana     35.50 € -> Pagado
2 Luis   120.00 € -> En camino
3 Sara    18.90 € -> Entregado
Estados posibles:
  0 PENDIENTE (Pendiente de pago)
  1 PAGADO (Pagado)
  2 ENVIADO (En camino)
  3 ENTREGADO (Entregado)
  4 CANCELADO (Cancelado)
valueOf("ENVIADO"): ENVIADO
¿Iguales? true
Pedido[id=2, cliente=Luis, importe=120.0, estado=ENVIADO]
Error: Falta el cliente
```

**Claves para corregir**

- Un record genera automáticamente el constructor, los métodos de acceso (id(), cliente()…), equals, hashCode y toString.
- Thread.State, que verás en el Tema 2, es un enum con los estados de un hilo.

## Ejercicio 19 · Notas en un fichero

**Ficheros** · ★★★★☆

```java title="FicherosNotas.java"
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Ejercicio 19 · Ficheros de texto con java.nio y try-with-resources. */
public class FicherosNotas {
    public static void main(String[] args) {
        Path datos = Path.of("notas.txt");
        Path informe = Path.of("informe.txt");
        try {
            // 1) Escribir el fichero de datos
            Files.write(datos, List.of("Ana;7.5", "Luis;4.0", "Sara;9.25", "Pablo;5.5"),
                    StandardCharsets.UTF_8);
            System.out.println("Creado " + datos.toAbsolutePath());

            // 2) Leerlo línea a línea
            double suma = 0;
            int n = 0;
            String mejor = "";
            double notaMejor = -1;
            try (BufferedReader br = Files.newBufferedReader(datos, StandardCharsets.UTF_8)) {
                String linea;
                while ((linea = br.readLine()) != null) {
                    String[] p = linea.split(";");
                    double nota = Double.parseDouble(p[1]);
                    suma += nota;
                    n++;
                    if (nota > notaMejor) { notaMejor = nota; mejor = p[0]; }
                }
            }

            // 3) Escribir el informe
            try (BufferedWriter bw = Files.newBufferedWriter(informe, StandardCharsets.UTF_8)) {
                bw.write(String.format("Alumnos: %d%n", n));
                bw.write(String.format("Media: %.2f%n", suma / n));
                bw.write(String.format("Mejor nota: %s (%.2f)%n", mejor, notaMejor));
            }                                                    // se cierra solo

            System.out.println("Informe:");
            Files.readAllLines(informe).forEach(l -> System.out.println("  " + l));
            System.out.println("Tamaño del informe: " + Files.size(informe) + " bytes");

            // 4) Intentar leer un fichero que no existe
            Files.readAllLines(Path.of("no_existe.txt"));
        } catch (IOException e) {
            System.out.println("Error de E/S: " + e.getClass().getSimpleName()
                    + " -> " + e.getMessage());
        }
    }
}
```

**Salida**

```text
Creado /home/alumno/psp/notas.txt
Informe:
  Alumnos: 4
  Media: 6.56
  Mejor nota: Sara (9.25)
Tamaño del informe: 47 bytes
Error de E/S: NoSuchFileException -> no_existe.txt
```

**Claves para corregir**

- El try-with-resources cierra el lector o el escritor automáticamente, aunque haya una excepción.
- Indicar StandardCharsets.UTF_8 evita problemas con las tildes entre Windows, Linux y macOS.
- Los ficheros que no existen provocan NoSuchFileException, una subclase de IOException.

## Ejercicio 20 · Integrador: calculadora filtro

**Integrador** · ★★★★★

```java title="CalculadoraFiltro.java"
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Ejercicio 20 · Integrador: un programa "filtro".
 * Lee operaciones de la entrada estándar hasta el final, escribe los resultados
 * en la salida estándar,
 * los errores en la salida de errores y termina con un código de salida.
 * Así podrá lanzarse como proceso hijo y comunicarse por tuberías (Tema 1).
 */
public class CalculadoraFiltro {

    enum Operador {
        SUMA("+"), RESTA("-"), MULT("*"), DIV("/");
        final String simbolo;
        Operador(String s) { simbolo = s; }
        static Operador de(String s) {
            for (Operador o : values()) if (o.simbolo.equals(s)) return o;
            throw new IllegalArgumentException("Operador desconocido: " + s);
        }
        double aplicar(double a, double b) {
            return switch (this) {
                case SUMA -> a + b;
                case RESTA -> a - b;
                case MULT -> a * b;
                case DIV -> {
                    if (b == 0) throw new ArithmeticException("División entre cero");
                    yield a / b;
                }
            };
        }
    }

    record Operacion(double a, Operador op, double b) {
        static Operacion parsear(String linea) {
            String[] p = linea.trim().split("\\s+");
            if (p.length != 3)
                throw new IllegalArgumentException("Formato: número operador número");
            return new Operacion(Double.parseDouble(p[0]), Operador.de(p[1]),
                    Double.parseDouble(p[2]));
        }
        double resultado() { return op.aplicar(a, b); }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        List<Double> resultados = new ArrayList<>();
        Map<Operador, Integer> usos = new TreeMap<>();
        int errores = 0, numLinea = 0;
        String linea;
        while ((linea = in.readLine()) != null) {               // hasta el fin de la entrada
            numLinea++;
            if (linea.isBlank() || linea.startsWith("#")) continue;
            try {
                Operacion o = Operacion.parsear(linea);
                double r = o.resultado();
                resultados.add(r);
                usos.merge(o.op(), 1, Integer::sum);
                System.out.println(linea.trim() + " = " + r);
            // NumberFormatException es IllegalArgumentException
            } catch (IllegalArgumentException | ArithmeticException e) {
                errores++;
                System.err.println("Línea " + numLinea + ": " + e.getMessage());
            }
        }
        double total = resultados.stream().mapToDouble(Double::doubleValue).sum();
        System.out.printf("Operaciones correctas: %d · errores: %d · suma: %.2f%n",
                resultados.size(), errores, total);
        System.out.println("Uso de operadores: " + usos);
        System.exit(errores == 0 ? 0 : 1);
    }
}
```

**Salida (`java CalculadoraFiltro < operaciones.txt`)**

```text
3 + 4 = 7.0
10 / 4 = 2.5
2 * 2.5 = 5.0
Línea 5: División entre cero
Línea 6: Operador desconocido: %
Línea 7: For input string: "hola"
100 - 1 = 99.0
Operaciones correctas: 4 · errores: 3 · suma: 113.50
Uso de operadores: {SUMA=1, RESTA=1, MULT=1, DIV=1}
Código de salida: 1
```

**Claves para corregir**

- NumberFormatException es una subclase de IllegalArgumentException, así que el mismo catch captura los números no válidos.
- En el Tema 1, un programa Java podrá lanzar esta calculadora con ProcessBuilder, escribirle operaciones con outputWriter() y leer los resultados con inputReader().
