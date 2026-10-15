# 7. Java moderno

Desde Java 8 el lenguaje ha incorporado herramientas que hacen el código más corto y claro. Las vas a encontrar continuamente en la documentación y en los ejemplos del módulo.

## 7.1 Lambdas e interfaces funcionales

Una **interfaz funcional** es una interfaz con **un único método abstracto**. Una **lambda** es una forma abreviada de escribir una implementación de ese método, sin crear una clase:

```java
// Con una clase anónima (forma antigua)
Comparator<String> porLongitud = new Comparator<String>() {
    @Override
    public int compare(String a, String b) {
        return Integer.compare(a.length(), b.length());
    }
};

// Con una lambda: mismo significado
Comparator<String> porLongitud2 = (a, b) -> Integer.compare(a.length(), b.length());
```

### Sintaxis

| Forma | Ejemplo |
|---|---|
| Sin parámetros | `() -> System.out.println("Hola")` |
| Un parámetro (paréntesis opcionales) | `x -> x * 2` |
| Varios parámetros | `(a, b) -> a + b` |
| Varias instrucciones | `(a, b) -> { int s = a + b; return s; }` |

### Interfaces funcionales más comunes

| Interfaz | Método | Recibe → devuelve | Ejemplo |
|---|---|---|---|
| `Runnable` | `run()` | nada → nada | `() -> System.out.println("tarea")` |
| `Supplier<T>` | `get()` | nada → `T` | `() -> new Random().nextInt(10)` |
| `Consumer<T>` | `accept(t)` | `T` → nada | `s -> System.out.println(s)` |
| `Function<T,R>` | `apply(t)` | `T` → `R` | `s -> s.length()` |
| `Predicate<T>` | `test(t)` | `T` → `boolean` | `n -> n % 2 == 0` |
| `BiFunction<T,U,R>` | `apply(t, u)` | `T`, `U` → `R` | `(a, b) -> a * b` |
| `Comparator<T>` | `compare(a, b)` | `T`, `T` → `int` | `(a, b) -> a.compareTo(b)` |

```java
Predicate<Integer> esPar = n -> n % 2 == 0;
System.out.println(esPar.test(4));                // true
Predicate<Integer> esParYPositivo = esPar.and(n -> n > 0);
```

!!! tip "`Runnable`: el puente con el Tema 2"
    Un hilo ejecuta un `Runnable`. Con lambdas, crear y lanzar un hilo es una línea:

    ```java
    Runnable tarea = () -> System.out.println("Hola desde " + Thread.currentThread().getName());
    new Thread(tarea).start();
    ```

### Referencias a métodos

Cuando la lambda solo llama a un método existente, se puede abreviar con `::`

| Lambda | Referencia a método |
|---|---|
| `s -> System.out.println(s)` | `System.out::println` |
| `s -> s.toUpperCase()` | `String::toUpperCase` |
| `s -> Integer.parseInt(s)` | `Integer::parseInt` |
| `() -> new ArrayList<>()` | `ArrayList::new` |

Las variables locales que use una lambda deben ser **efectivamente finales**: no se pueden modificar después de asignarlas.

## 7.2 Streams

Un **stream** es una secuencia de elementos sobre la que se encadenan operaciones, como en una tubería. Se escribe **qué** quieres obtener, no **cómo** recorrer la colección:

```java
List<String> nombres = List.of("Ana", "Luis", "Marta", "Alba", "Pedro");

List<String> resultado = nombres.stream()          // 1. origen
        .filter(n -> n.startsWith("A"))            // 2. operaciones intermedias
        .map(String::toUpperCase)
        .sorted()
        .toList();                                 // 3. operación final
// [ALBA, ANA]
```

Un stream tiene tres partes: un **origen** (`lista.stream()`, `Arrays.stream(array)`, `IntStream.range(0, 10)`, `Files.lines(ruta)`), **operaciones intermedias**, que devuelven otro stream y no se ejecutan hasta que hay una final, y **una operación final**, que produce el resultado.

| Intermedias | Hace |
|---|---|
| `filter(predicado)` | Deja pasar los que cumplen la condición. |
| `map(función)` | Transforma cada elemento. `mapToInt`, `mapToDouble` para números. |
| `sorted()` / `sorted(comparador)` | Ordena. |
| `distinct()` | Elimina duplicados. |
| `limit(n)` / `skip(n)` | Toma o salta los `n` primeros. |

| Finales | Devuelve |
|---|---|
| `toList()` | Una lista (inmutable). |
| `forEach(acción)` | Nada; ejecuta la acción con cada elemento. |
| `count()` | El número de elementos. |
| `sum()`, `average()`, `max()`, `min()` | En streams numéricos (`IntStream`, `DoubleStream`). |
| `anyMatch`, `allMatch`, `noneMatch` | `boolean`. |
| `findFirst()` | Un `Optional` con el primero. |
| `collect(Collectors...)` | Listas, mapas, textos, agrupaciones. |

```java
double media = alumnos.stream().mapToDouble(Alumno::getNota).average().orElse(0);

long aprobados = alumnos.stream().filter(Alumno::estaAprobado).count();

String lista = nombres.stream().collect(Collectors.joining(", "));     // "Ana, Luis, ..."

Map<Boolean, List<Alumno>> partidos =
        alumnos.stream().collect(Collectors.partitioningBy(Alumno::estaAprobado));

Map<String, Long> porCurso =
        alumnos.stream().collect(Collectors.groupingBy(Alumno::getCurso, Collectors.counting()));
```

!!! note "Un stream se usa una sola vez"
    Después de la operación final, el stream queda consumido. Si lo necesitas otra vez, crea uno nuevo desde la colección. Los streams **no modifican** la colección original.

### `Optional`

Algunas operaciones pueden no tener resultado (el máximo de una lista vacía, buscar algo que no existe). En lugar de devolver `null`, devuelven un `Optional`:

```java
Optional<Alumno> mejor = alumnos.stream().max(Comparator.comparingDouble(Alumno::getNota));

mejor.ifPresent(a -> System.out.println("Mejor nota: " + a));
String nombre = mejor.map(Alumno::getNombre).orElse("Nadie");
```

## 7.3 Tipos enumerados: `enum`

Un `enum` define un tipo con un **conjunto cerrado de valores**. Es más seguro que usar números o textos sueltos:

```java
public enum Estado {
    PENDIENTE, ENVIADO, ENTREGADO, CANCELADO
}

Estado e = Estado.ENVIADO;
e.name();                         // "ENVIADO"
e.ordinal();                      // 1
Estado.valueOf("CANCELADO");      // texto -> enum (IllegalArgumentException si no existe)
Estado.values();                  // array con todos los valores
```

Un `enum` es una clase: puede tener **atributos, constructor y métodos**:

```java
public enum Operacion {
    SUMA("+"), RESTA("-"), MULTIPLICACION("*"), DIVISION("/");

    private final String simbolo;
    Operacion(String simbolo) { this.simbolo = simbolo; }
    public String getSimbolo() { return simbolo; }

    public double aplicar(double a, double b) {
        return switch (this) {
            case SUMA -> a + b;
            case RESTA -> a - b;
            case MULTIPLICACION -> a * b;
            case DIVISION -> a / b;
        };
    }
}
```

En un `switch` sobre un `enum` que cubre todos los valores no hace falta `default`: el compilador comprueba que no falte ninguno.

## 7.4 Registros: `record` (Java 16+)

Un `record` es una clase pensada para **guardar datos inmutables**. En una línea, Java genera los atributos `private final`, el constructor, los métodos de acceso, `equals`, `hashCode` y `toString`:

```java
public record Producto(String nombre, double precio, int stock) { }

Producto p = new Producto("Teclado", 25.5, 10);
p.nombre();             // "Teclado"  (sin "get")
p.precio();             // 25.5
System.out.println(p);  // Producto[nombre=Teclado, precio=25.5, stock=10]
```

Se pueden añadir métodos y un **constructor compacto** para validar:

```java
public record Producto(String nombre, double precio, int stock) {
    public Producto {                                  // compacto: sin parámetros
        if (precio < 0) throw new IllegalArgumentException("Precio negativo");
        nombre = nombre.strip();
    }

    public double valorStock() { return precio * stock; }
}
```

| ¿Clase o `record`? | |
|---|---|
| Datos que no cambian (un punto, un mensaje, una línea leída de un fichero) | `record` |
| Objeto con estado que cambia (una cuenta con saldo, un contador) | Clase normal |

!!! tip "Inmutabilidad y concurrencia"
    Un objeto inmutable se puede compartir entre varios hilos **sin sincronización**, porque nadie puede modificarlo. Por eso los `record` serán muy útiles en el Tema 2.

## Preguntas de repaso

1. ¿Qué es una interfaz funcional? Nombra tres.
2. Escribe una lambda que reciba un `String` y devuelva si tiene más de 5 caracteres. ¿Qué interfaz funcional implementa?
3. ¿Qué diferencia hay entre una operación intermedia y una final en un stream?
4. ¿Qué ventaja tiene devolver un `Optional` en lugar de `null`?
5. ¿Qué genera automáticamente un `record`?

!!! example "Practica"
    [Ejercicio 17](boletin.md#ejercicio-17) · [Ejercicio 18](boletin.md#ejercicio-18)
