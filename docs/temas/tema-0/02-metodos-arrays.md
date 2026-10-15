# 2. Métodos y arrays

## 2.1 Métodos

Un **método** es un bloque de código con nombre que realiza una tarea. Sirve para no repetir código y para dividir un problema en partes pequeñas.

```java
//  modificadores  tipo de retorno  nombre   parámetros
    public static  double           media   (int a, int b) {
        return (a + b) / 2.0;      // devuelve un valor del tipo indicado
    }
```

- Si el método no devuelve nada, su tipo de retorno es `void`.
- `return` termina el método. En un método `void` se puede usar `return;` para salir antes.
- Un método `static` pertenece a la clase y se llama sin crear objetos: `media(4, 7)` dentro de la misma clase o `Utilidades.media(4, 7)` desde otra. Los métodos sin `static` (de instancia) se ven en el apartado 5.

### Paso de parámetros: siempre por valor

Java **copia** el valor de cada argumento en el parámetro.

- Con un **primitivo**, el método recibe una copia: cambiarla no afecta a la variable original.
- Con un **objeto o array**, se copia la **referencia** (la dirección). El método puede modificar el contenido del objeto, pero no hacer que la variable original apunte a otro.

```java
static void duplicar(int x)      { x = x * 2; }        // no cambia nada fuera
static void duplicar(int[] v)    { v[0] = v[0] * 2; }  // SÍ cambia el array original

int n = 5;      duplicar(n);   // n sigue valiendo 5
int[] a = {5};  duplicar(a);   // a[0] vale 10
```

### Sobrecarga

Varios métodos pueden **llamarse igual** si tienen distintos parámetros (número o tipo). El compilador elige el adecuado según los argumentos:

```java
static int maximo(int a, int b)          { return a > b ? a : b; }
static int maximo(int a, int b, int c)   { return maximo(maximo(a, b), c); }
static double maximo(double a, double b) { return Math.max(a, b); }
```

El tipo de retorno **no basta** para distinguir dos métodos sobrecargados.

### Número variable de argumentos (*varargs*)

```java
static int suma(int... numeros) {     // dentro, numeros es un int[]
    int total = 0;
    for (int n : numeros) total += n;
    return total;
}

suma();            // 0
suma(3, 4);        // 7
suma(1, 2, 3, 4);  // 10
```

El parámetro *varargs* tiene que ser **el último**. `String.format` y `printf` lo usan.

### Recursividad

Un método **recursivo** se llama a sí mismo. Necesita siempre un **caso base** que detenga las llamadas:

```java
static long factorial(int n) {
    if (n <= 1) return 1;            // caso base
    return n * factorial(n - 1);     // caso recursivo
}
```

!!! warning "Sin caso base, desbordamiento"
    Cada llamada ocupa espacio en la **pila** del hilo. Si la recursión no termina, el programa falla con `StackOverflowError`. En el Tema 2 verás que cada hilo tiene su propia pila.

## 2.2 Arrays

Un **array** guarda un número **fijo** de elementos del mismo tipo, accesibles por su posición (índice), empezando en **0**.

```java
int[] notas = new int[5];                // 5 enteros, todos a 0
double[] temps = {21.5, 23.0, 19.8};     // declaración con valores
String[] dias = new String[7];           // 7 referencias a null

notas[0] = 8;                            // primera posición
int ultima = notas[notas.length - 1];    // última posición
```

| Concepto | Detalle |
|---|---|
| `length` | Es un **atributo**, sin paréntesis: `notas.length`. (En `String` es el método `length()`.) |
| Valores por defecto | `0` en números, `false` en `boolean`, `null` en objetos. |
| Índice fuera de rango | `ArrayIndexOutOfBoundsException`. |
| Tamaño | No cambia. Si necesitas crecer, usa `ArrayList` (apartado 6). |

### Recorridos

```java
for (int i = 0; i < temps.length; i++) {          // cuando necesitas el índice
    System.out.println("Día " + (i + 1) + ": " + temps[i]);
}

double suma = 0;
for (double t : temps) {                          // for-each: solo lectura
    suma += t;
}
double media = suma / temps.length;
```

### La clase `Arrays`

```java
import java.util.Arrays;

int[] v = {5, 2, 9, 1};
Arrays.sort(v);                          // ordena: [1, 2, 5, 9]
System.out.println(Arrays.toString(v));  // "[1, 2, 5, 9]"
int[] copia = Arrays.copyOf(v, 6);       // [1, 2, 5, 9, 0, 0]
int pos = Arrays.binarySearch(v, 5);     // 2 (el array debe estar ordenado)
boolean iguales = Arrays.equals(v, copia);
Arrays.fill(v, 0);                       // todo a 0
```

!!! danger "Imprimir un array directamente"
    `System.out.println(v)` muestra algo como `[I@1b6d3586` (tipo y código hash), no el contenido. Usa `Arrays.toString(v)`.

!!! warning "Asignar no es copiar"
    `int[] b = a;` no copia el array: `a` y `b` apuntan **al mismo**. Si cambias `b[0]`, cambia `a[0]`. Para copiar usa `Arrays.copyOf` o `a.clone()`.

## 2.3 Arrays bidimensionales

Una matriz es un **array de arrays**:

```java
int[][] m = {
    {1, 2, 3},
    {4, 5, 6}
};                                 // 2 filas, 3 columnas

int filas = m.length;              // 2
int columnas = m[0].length;        // 3

for (int i = 0; i < m.length; i++) {
    for (int j = 0; j < m[i].length; j++) {
        System.out.print(m[i][j] + "\t");
    }
    System.out.println();
}

for (int[] fila : m) {                       // for-each anidado
    System.out.println(Arrays.toString(fila));
}
```

Para imprimir una matriz completa en una línea: `Arrays.deepToString(m)`.

## Preguntas de repaso

1. Si pasas un `int` a un método y lo modificas dentro, ¿cambia fuera? ¿Y si pasas un `int[]`?
2. ¿Pueden existir dos métodos `calcular(int)` y `calcular(double)` en la misma clase? ¿Y `int calcular(int)` y `double calcular(int)`?
3. ¿Qué ocurre si un método recursivo no tiene caso base?
4. ¿Por qué `System.out.println(miArray)` no muestra los valores?
5. Tras `int[] b = a; b[0] = 99;`, ¿cuánto vale `a[0]`?

!!! example "Practica"
    [Ejercicio 4](boletin.md#ejercicio-4) · [Ejercicio 5](boletin.md#ejercicio-5) · [Ejercicio 6](boletin.md#ejercicio-6)
