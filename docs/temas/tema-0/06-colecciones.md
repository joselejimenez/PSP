# 6. Colecciones

## 6.1 Por qué colecciones

Los arrays tienen **tamaño fijo**. Las **colecciones** del paquete `java.util` crecen y decrecen solas y ofrecen operaciones ya programadas: buscar, ordenar, eliminar duplicados, asociar claves con valores…

| Interfaz | Qué guarda | Orden | Duplicados | Implementaciones |
|---|---|---|---|---|
| `List` | Secuencia de elementos por posición | Sí, el de inserción | Sí | `ArrayList`, `LinkedList` |
| `Set` | Conjunto de elementos únicos | `HashSet`: ninguno; `LinkedHashSet`: inserción; `TreeSet`: ordenado | **No** | `HashSet`, `LinkedHashSet`, `TreeSet` |
| `Map` | Pares **clave → valor** | Igual que en `Set` (según la clave) | Claves no; valores sí | `HashMap`, `LinkedHashMap`, `TreeMap` |

!!! tip "Declara con la interfaz"
    Escribe `List<String> nombres = new ArrayList<>();` y no `ArrayList<String> nombres = ...`. Así puedes cambiar de implementación sin tocar el resto del código.

## 6.2 Genéricos

Lo que va entre `< >` indica el **tipo de los elementos**. El compilador comprueba que solo metas ese tipo y no hace falta convertir al sacarlos:

```java
List<String> nombres = new ArrayList<>();    // <> : el tipo se deduce de la izquierda
nombres.add("Ana");
// nombres.add(5);                            // error de compilación
String primero = nombres.get(0);             // sin casting
```

Las colecciones **no admiten primitivos**: se usan sus **clases envoltorio** (`Integer`, `Double`, `Character`, `Boolean`…). Java convierte automáticamente (*autoboxing*):

```java
List<Integer> numeros = new ArrayList<>();
numeros.add(7);              // int -> Integer automáticamente
int n = numeros.get(0);      // Integer -> int
```

## 6.3 `List` y `ArrayList`

```java
List<String> lista = new ArrayList<>();
lista.add("Ana");                 // añade al final
lista.add(0, "Luis");             // inserta en la posición 0
lista.size();                     // 2
lista.get(1);                     // "Ana"
lista.set(1, "Ana María");        // sustituye
lista.contains("Luis");           // true
lista.indexOf("Luis");            // 0
lista.remove("Luis");             // elimina por valor
lista.remove(0);                  // elimina por posición
lista.isEmpty();
lista.clear();

List<String> fija = List.of("a", "b", "c");   // inmutable: no admite add ni remove
```

### Recorrer y eliminar

```java
for (String s : lista) {             // for-each: para leer
    System.out.println(s);
}

Iterator<String> it = lista.iterator();
while (it.hasNext()) {
    if (it.next().startsWith("A")) {
        it.remove();                 // forma segura de borrar mientras recorres
    }
}

lista.removeIf(s -> s.startsWith("A"));   // lo mismo con una lambda (apartado 7)
```

!!! danger "`ConcurrentModificationException`"
    Si borras con `lista.remove(...)` **dentro de un for-each** sobre la misma lista, Java lanza esta excepción. Usa `Iterator.remove()` o `removeIf`. (Ojo: el nombre dice *concurrent*, pero aquí no hay hilos; en el Tema 2 verás colecciones pensadas para varios hilos.)

## 6.4 Ordenar: `Comparable` y `Comparator`

- **`Comparable`**: el orden **natural** de una clase, definido dentro de ella con `compareTo`. `String`, `Integer` y `LocalDate` ya lo tienen.
- **`Comparator`**: un criterio de orden **externo**, que puedes elegir en cada momento.

```java
Collections.sort(nombres);                                     // orden natural
alumnos.sort(Comparator.comparing(Alumno::getNombre));          // por nombre
alumnos.sort(Comparator.comparingDouble(Alumno::getNota).reversed());   // nota descendente
alumnos.sort(Comparator.comparing(Alumno::getCurso)
                       .thenComparing(Alumno::getNombre));      // dos criterios
```

`compareTo` y `compare` devuelven un número **negativo** si el primero va antes, **0** si son iguales y **positivo** si va después.

## 6.5 `Set`

```java
Set<String> asignaturas = new HashSet<>();
asignaturas.add("PSP");
asignaturas.add("PMDM");
asignaturas.add("PSP");               // devuelve false: ya estaba
asignaturas.size();                   // 2

Set<String> ordenadas = new TreeSet<>(asignaturas);   // [PMDM, PSP]
```

Uso típico: **eliminar duplicados** de una lista: `new ArrayList<>(new LinkedHashSet<>(lista))`.

## 6.6 `Map`

Un `Map` asocia cada **clave** (única) con un **valor**:

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("café", 20);
stock.put("té", 5);
stock.put("café", 18);                     // sustituye el valor anterior
stock.get("café");                         // 18
stock.get("zumo");                         // null: no existe
stock.getOrDefault("zumo", 0);             // 0
stock.containsKey("té");                   // true
stock.remove("té");

for (Map.Entry<String, Integer> e : stock.entrySet()) {
    System.out.println(e.getKey() + " → " + e.getValue());
}
stock.forEach((clave, valor) -> System.out.println(clave + " → " + valor));
```

### Contar apariciones

Es uno de los usos más frecuentes. `merge` suma 1 si la clave existe y la crea con 1 si no:

```java
Map<String, Integer> frecuencia = new TreeMap<>();     // TreeMap: claves ordenadas
for (String palabra : texto.toLowerCase().split("\\s+")) {
    frecuencia.merge(palabra, 1, Integer::sum);
}
```

!!! warning "`hashCode` y `equals` en las claves"
    `HashMap` y `HashSet` usan `hashCode` y `equals` para encontrar los elementos. Si usas objetos propios como clave o elemento, deben sobrescribir ambos (apartado 5.7) o usa un `record`.

## Preguntas de repaso

1. ¿Qué colección usarías para guardar los alumnos de una clase en orden de lista? ¿Y para saber qué ciudades distintas aparecen? ¿Y para guardar la nota de cada alumno por su DNI?
2. ¿Por qué no se puede escribir `List<int>`?
3. ¿Qué diferencia hay entre `HashMap` y `TreeMap`?
4. ¿Cómo eliminas elementos de una lista mientras la recorres sin que falle?
5. ¿Qué diferencia hay entre `Comparable` y `Comparator`?

!!! example "Practica"
    [Ejercicio 15](boletin.md#ejercicio-15) · [Ejercicio 16](boletin.md#ejercicio-16)
