# Boletín de repaso

!!! info "Para qué sirve este boletín"
    Veinte ejercicios para repasar el Java que vas a necesitar en el módulo: de los tipos básicos y las cadenas a las colecciones, la herencia, las lambdas y los ficheros. Están ordenados de menor a mayor dificultad (★ a ★★★★★).

    - Cada apartado de la teoría indica qué ejercicios le corresponden. Si te atascas, vuelve a la [teoría](index.md).
    - Compila con `javac *.java` y ejecuta con `java NombreClase`. Necesitas **JDK 21 o superior** (`java -version`).
    - Cada ejercicio indica la clase que debes crear.
    - El último es un programa «filtro» que conecta directamente con el Tema 1: lee de la entrada estándar y escribe en la salida estándar.

## Índice

| Nº | Ejercicio | Bloque | Nivel | Conceptos |
|---|---|---|---|---|
| 1 | [Conversor de temperaturas](#ejercicio-1) | Fundamentos | ★☆☆☆☆ | Variables, tipos primitivos, operadores, casting, Scanner |
| 2 | [Calificaciones y días de la semana](#ejercicio-2) | Fundamentos | ★☆☆☆☆ | if / else if, switch como expresión, operador ternario |
| 3 | [Tablas, cifras y números primos](#ejercicio-3) | Fundamentos | ★☆☆☆☆ | for, while, do-while, bucles anidados, break, continue, args del main |
| 4 | [Biblioteca de utilidades](#ejercicio-4) | Métodos | ★★☆☆☆ | Métodos static, parámetros y retorno, sobrecarga, varargs, recursividad, paso por valor |
| 5 | [Temperaturas de la semana](#ejercicio-5) | Arrays | ★★☆☆☆ | Arrays unidimensionales, recorridos, Arrays.sort, Arrays.copyOf, Arrays.toString |
| 6 | [Operaciones con matrices](#ejercicio-6) | Arrays | ★★☆☆☆ | Arrays bidimensionales, bucles anidados, for-each |
| 7 | [Análisis de una frase](#ejercicio-7) | Cadenas | ★★☆☆☆ | String: length, charAt, substring, indexOf, contains, replace, toUpperCase, equals frente a == |
| 8 | [Ticket de la cafetería](#ejercicio-8) | Cadenas | ★★☆☆☆ | StringBuilder, String.format, repeat, bloques de texto |
| 9 | [Procesar un fichero CSV](#ejercicio-9) | Cadenas | ★★★☆☆ | split, trim, parseInt, parseDouble, validación, salida de errores, código de salida |
| 10 | [Excepciones bajo control](#ejercicio-10) | Excepciones | ★★★☆☆ | try/catch/finally, multi-catch, throw, throws, excepciones propias |
| 11 | [Cuenta bancaria](#ejercicio-11) | Programación orientada a objetos | ★★★☆☆ | Clases, atributos privados, constructores, this, getters, validación, toString |
| 12 | [Tickets de soporte](#ejercicio-12) | Programación orientada a objetos | ★★★☆☆ | Atributos y métodos static, constantes, clases de utilidad |
| 13 | [Plantilla de empleados](#ejercicio-13) | Herencia | ★★★☆☆ | extends, super, @Override, protected, polimorfismo, instanceof con patrón |
| 14 | [Figuras geométricas](#ejercicio-14) | Herencia | ★★★★☆ | Clases abstractas, interfaces, métodos default, Comparable |
| 15 | [Gestión de alumnos](#ejercicio-15) | Colecciones | ★★★☆☆ | ArrayList, add, size, get, sort con Comparator, Iterator, búsqueda |
| 16 | [Frecuencia de palabras](#ejercicio-16) | Colecciones | ★★★★☆ | HashMap, TreeMap, merge, HashSet, TreeSet, entrySet |
| 17 | [Catálogo con streams](#ejercicio-17) | Programación funcional | ★★★★☆ | Lambdas, Predicate, Runnable, referencias a métodos, streams, Collectors, Optional |
| 18 | [Estado de los pedidos](#ejercicio-18) | Tipos modernos | ★★★☆☆ | enum con atributos y métodos, switch sobre enum, record, constructor compacto |
| 19 | [Notas en un fichero](#ejercicio-19) | Ficheros | ★★★★☆ | java.nio.file: Path, Files, BufferedReader, BufferedWriter, try-with-resources, IOException |
| 20 | [Integrador: calculadora filtro](#ejercicio-20) | Integrador | ★★★★★ | Entrada estándar, BufferedReader, enum, record, excepciones, Map, streams, System.err, System.exit |

## Ejercicio 1 · Conversor de temperaturas { #ejercicio-1 }

**Fundamentos** · ★☆☆☆☆ · *Variables, tipos primitivos, operadores, casting, Scanner*

> Repasa cómo guarda y opera Java los números. Muchos errores de los programas que lanzan procesos vienen de convertir mal un texto en número.

**Qué tienes que hacer**

1. Pide al usuario una temperatura en grados Celsius y conviértela a Fahrenheit (F = C · 9/5 + 32) y a Kelvin (K = C + 273,15). Muestra el resultado con dos decimales usando printf.
2. Acepta también la coma como separador decimal: el usuario puede escribir 21,5.
3. Muestra el resultado de 7 / 2, 7 / 2.0, 7 % 2 y (double) 7 / 2, y explica en un comentario por qué no dan lo mismo.
4. Suma 1 a Integer.MAX_VALUE y muestra lo que ocurre. Repite la operación con long.
5. Muestra el resultado de (int) 9.99 y de Math.round(9.5).

**Datos de prueba**

25

??? tip "Pistas"

    - Scanner sc = new Scanner(System.in); y sc.nextLine() para leer una línea completa.
    - Double.parseDouble(texto.replace(',', '.')) convierte el texto en double.

Clase: `Conversor.java`

## Ejercicio 2 · Calificaciones y días de la semana { #ejercicio-2 }

**Fundamentos** · ★☆☆☆☆ · *if / else if, switch como expresión, operador ternario*

> Practica las estructuras de decisión, incluido el switch moderno de Java 14 o superior.

**Qué tienes que hacer**

1. Escribe un método calificacion(double nota) que devuelva «Insuficiente» (< 5), «Suficiente» (< 6), «Bien» (< 7), «Notable» (< 9) o «Sobresaliente». Si la nota no está entre 0 y 10, devuelve «Nota no válida».
2. Escribe un método diaSemana(int n) que, con un switch como expresión (case 1, 2, 3, 4, 5 ->), devuelva «laborable», «fin de semana» o «día no válido».
3. En el main, pide una nota y un día y muestra los resultados.
4. Muestra «¡Enhorabuena!» o «Ánimo para la recuperación» usando el operador ternario.

**Datos de prueba**

7.8 y después 6

Clase: `Calificaciones.java`

## Ejercicio 3 · Tablas, cifras y números primos { #ejercicio-3 }

**Fundamentos** · ★☆☆☆☆ · *for, while, do-while, bucles anidados, break, continue, args del main*

> Los bucles aparecerán en todo el curso: leer la salida de un proceso línea a línea, repetir un menú, esperar a varios hilos…

**Qué tienes que hacer**

1. Muestra la tabla de multiplicar de un número. El número llega como primer argumento del main (args[0]); si no hay argumentos, usa el 7.
2. Calcula con un while la suma de las cifras de 98765.
3. Muestra los números primos hasta 50 con dos bucles anidados. Usa break para dejar de buscar divisores cuando encuentres uno, y continue para saltar los que no son primos.
4. Escribe un do-while que se ejecute tres veces y explica en qué se diferencia de un while.

??? tip "Pistas"

    - Para pasar argumentos: java Bucles 9. Desde IntelliJ: Run → Edit Configurations → Program arguments.
    - Para comprobar si x es primo basta con probar divisores mientras d · d ≤ x.

Clase: `Bucles.java`

## Ejercicio 4 · Biblioteca de utilidades { #ejercicio-4 }

**Métodos** · ★★☆☆☆ · *Métodos static, parámetros y retorno, sobrecarga, varargs, recursividad, paso por valor*

> Dividir un programa en métodos pequeños es lo que permite después ejecutarlos en otro proceso o en otro hilo.

**Qué tienes que hacer**

1. Escribe factorial(int n) de forma iterativa y factorialRec(int n) de forma recursiva, y comprueba que 10! da lo mismo con los dos.
2. Escribe mcd(int a, int b) con el algoritmo de Euclides, de forma recursiva.
3. Escribe esPrimo(int n).
4. Sobrecarga el método maximo: una versión para dos int, otra para dos double y otra con número variable de argumentos (int... numeros).
5. Escribe un método incrementar(int x) que haga x++ y comprueba que la variable original del main no cambia. Explica por qué.

Clase: `Utilidades.java`

## Ejercicio 5 · Temperaturas de la semana { #ejercicio-5 }

**Arrays** · ★★☆☆☆ · *Arrays unidimensionales, recorridos, Arrays.sort, Arrays.copyOf, Arrays.toString*

> Trabaja con arrays paralelos: uno con los días y otro con las temperaturas.

**Qué tienes que hacer**

1. Crea un array con los días (lun … dom) y otro con siete temperaturas.
2. Calcula la media, la máxima y la mínima, indicando qué día se produjo cada una.
3. Muestra los días cuya temperatura supera la media.
4. Muestra las temperaturas ordenadas sin modificar el array original y comprueba que el original sigue igual.

Clase: `EstadisticasArray.java`

## Ejercicio 6 · Operaciones con matrices { #ejercicio-6 }

**Arrays** · ★★☆☆☆ · *Arrays bidimensionales, bucles anidados, for-each*

> Una matriz es un array de arrays. Practica sus recorridos por filas y por columnas.

**Qué tienes que hacer**

1. Declara la matriz de 3 × 4 con los números del 1 al 12 y muéstrala alineada con printf.
2. Calcula y muestra la suma de cada fila y la de cada columna.
3. Crea su traspuesta (4 × 3) y muéstrala.
4. Escribe un método mostrar(int[][] m) que sirva para las dos matrices.

Clase: `Matrices.java`

## Ejercicio 7 · Análisis de una frase { #ejercicio-7 }

**Cadenas** · ★★☆☆☆ · *String: length, charAt, substring, indexOf, contains, replace, toUpperCase, equals frente a ==*

> Las cadenas aparecen en todos los temas: comandos de ProcessBuilder, mensajes por sockets, contraseñas…

**Qué tienes que hacer**

1. Con la frase «Dábale arroz a la zorra el abad», muestra su longitud, la frase en mayúsculas y el número de vocales (contando también las vocales con tilde).
2. Escribe un método invertir(String s) que recorra la cadena con charAt.
3. Escribe esPalindromo(String s) que ignore mayúsculas, espacios y tildes.
4. Muestra la primera palabra con substring e indexOf, comprueba si contiene «zorra» y reemplázala por «gata».
5. Compara "java" con new String("java") usando == y equals. Explica la diferencia.

??? tip "Pistas"

    - Para quitar tildes: Normalizer.normalize(s, Normalizer.Form.NFD).replaceAll("\\p{M}", "").

Clase: `Cadenas.java`

## Ejercicio 8 · Ticket de la cafetería { #ejercicio-8 }

**Cadenas** · ★★☆☆☆ · *StringBuilder, String.format, repeat, bloques de texto*

> Construir textos con formato es útil para generar informes, logs o mensajes que se envían a otros procesos.

**Qué tienes que hacer**

1. Con tres arrays (productos, cantidades y precios), genera un ticket con columnas alineadas: nombre del producto, unidades e importe.
2. Calcula el total y el IVA incluido (10 %).
3. Construye todo el ticket con un StringBuilder y muéstralo con un único println.
4. Añade un pie de dos líneas usando un bloque de texto (""" … """).

??? tip "Pistas"

    - %-22s alinea un texto a la izquierda en 22 caracteres; %10.2f, un número a la derecha con dos decimales.
    - "=".repeat(40) repite un carácter.

Clase: `Ticket.java`

## Ejercicio 9 · Procesar un fichero CSV { #ejercicio-9 }

**Cadenas** · ★★★☆☆ · *split, trim, parseInt, parseDouble, validación, salida de errores, código de salida*

> Leer datos con un formato y descartar los que están mal es exactamente lo que hará un proceso padre al leer la salida de un hijo.

**Qué tienes que hacer**

1. Parte del array de líneas que tienes debajo. La primera es la cabecera.
2. Separa cada línea por «;», quita los espacios con trim y convierte la edad y la nota en números. La nota puede venir con coma.
3. Las líneas con un número de campos incorrecto o con números no válidos se informan por la salida de errores (System.err) y se cuentan como error.
4. Muestra «APTO» o «NO APTO» según un umbral que llega como argumento (por defecto 5). Al final, muestra el resumen y la media.
5. Termina el programa con System.exit(0) si no hay errores y con System.exit(1) si los hay. Compruébalo con echo $? (Linux y macOS) o echo %errorlevel% (Windows).

**Datos de prueba**

```java
String[] lineas = {
    "nombre;edad;nota",
    "Ana;19;8.5",
    "Luis;20;6,75",
    "Marta;veinte;9",
    "Pablo;21",
    "  Sara ; 22 ; 4.9 "
};
```

Clase: `ProcesarCSV.java`

## Ejercicio 10 · Excepciones bajo control { #ejercicio-10 }

**Excepciones** · ★★★☆☆ · *try/catch/finally, multi-catch, throw, throws, excepciones propias*

> En PSP casi todas las operaciones pueden fallar: lanzar un proceso, esperar a un hilo, conectar con un servidor. Hay que saber capturar las excepciones.

**Qué tienes que hacer**

1. Pide un número entero y repite la pregunta hasta que el usuario escriba uno válido (captura NumberFormatException).
2. Escribe dividir(int a, int b), que lance una ArithmeticException con un mensaje propio si b es 0. Captúrala y añade un bloque finally que muestre un mensaje.
3. Crea la excepción comprobada EdadInvalidaException (extends Exception) y un método validarEdad(int edad) throws EdadInvalidaException que la lance si la edad no está entre 0 y 120.
4. Provoca un error de índice al acceder a args o a un array y captura en un único catch ArrayIndexOutOfBoundsException | NumberFormatException.

**Datos de prueba**

hola y después 0

Clase: `Excepciones.java`

## Ejercicio 11 · Cuenta bancaria { #ejercicio-11 }

**Programación orientada a objetos** · ★★★☆☆ · *Clases, atributos privados, constructores, this, getters, validación, toString*

> La encapsulación protege los datos de un objeto: nadie puede dejar un saldo negativo desde fuera.

**Qué tienes que hacer**

1. Crea la clase CuentaBancaria con los atributos privados iban, titular y saldo. El IBAN y el titular no pueden cambiar (final).
2. Escribe dos constructores: uno con saldo inicial y otro que empiece con 0 y llame al primero con this(...). El saldo inicial no puede ser negativo.
3. Añade los métodos ingresar, retirar (devuelve false si no hay saldo suficiente) y transferir(CuentaBancaria destino, double cantidad).
4. Sobrescribe toString para mostrar «Titular (IBAN): saldo €».
5. En el main, crea dos cuentas, haz varias operaciones y comprueba que un ingreso negativo lanza IllegalArgumentException.

Clase: `CuentaBancaria.java`

## Ejercicio 12 · Tickets de soporte { #ejercicio-12 }

**Programación orientada a objetos** · ★★★☆☆ · *Atributos y métodos static, constantes, clases de utilidad*

> Distingue entre lo que pertenece a cada objeto y lo que comparte toda la clase.

**Qué tienes que hacer**

1. Crea la clase Ticket con un id propio y una descripción. El id se asigna automáticamente con un contador static (1, 2, 3…).
2. Añade un método static creados() que devuelva cuántos tickets se han creado.
3. Crea una clase de utilidad MathUtil con una constante IVA = 0.21, un constructor privado y un método static conIva(double precio).
4. Crea tres tickets, muéstralos y muestra cuántos hay. Calcula 100 € con IVA.

Clase: `Static.java`

## Ejercicio 13 · Plantilla de empleados { #ejercicio-13 }

**Herencia** · ★★★☆☆ · *extends, super, @Override, protected, polimorfismo, instanceof con patrón*

> La herencia permite reutilizar código y tratar de la misma forma objetos distintos.

**Qué tienes que hacer**

1. Crea la clase Empleado con nombre, salarioBase y un método salario() que devuelva el salario base.
2. Crea Desarrollador, que añade horasExtra y cobra 25 € por cada una.
3. Crea Gerente, que añade un bonus y cobra el salario del padre más un 10 %, más el bonus. Reutiliza el cálculo con super.salario().
4. Guarda un empleado de cada tipo en una List<Empleado>, recórrela, muestra el salario de cada uno y el total de nóminas.
5. Usa instanceof Gerente g para acceder al bonus solo cuando el empleado sea un gerente.

Clase: `Empleados.java`

## Ejercicio 14 · Figuras geométricas { #ejercicio-14 }

**Herencia** · ★★★★☆ · *Clases abstractas, interfaces, métodos default, Comparable*

> Las interfaces son la base de los hilos: Runnable y Callable son interfaces que implementarás en el Tema 2.

**Qué tienes que hacer**

1. Crea la clase abstracta Figura con los métodos abstractos area() y perimetro(), y un toString que los muestre.
2. Crea Circulo, Rectangulo y Triangulo (con la fórmula de Herón).
3. Crea la interfaz Dibujable con el método dibujar() y un método default dibujarConMarco(). Haz que solo el círculo y el rectángulo la implementen.
4. Haz que Figura implemente Comparable<Figura> para ordenar por área y ordena una lista con Collections.sort.
5. Recorre la lista y dibuja con marco solo las figuras que sean Dibujable.

Clase: `Figuras.java`

## Ejercicio 15 · Gestión de alumnos { #ejercicio-15 }

**Colecciones** · ★★★☆☆ · *ArrayList, add, size, get, sort con Comparator, Iterator, búsqueda*

> Las listas sustituyen a los arrays cuando no sabemos cuántos elementos habrá. En el Tema 1 guardarás en una lista los procesos lanzados.

**Qué tienes que hacer**

1. Crea la clase Alumno (nombre, grupo, nota) y una lista con cinco alumnos.
2. Ordena la lista por nota de mayor a menor con Comparator.comparing(...).reversed() y muéstrala.
3. Ordénala después por grupo y, dentro de cada grupo, por nombre (thenComparing).
4. Escribe un método buscar(lista, nombre) que no distinga mayúsculas y devuelva el alumno o null.
5. Elimina los suspensos recorriendo la lista con un Iterator.

Clase: `GestionAlumnos.java`

## Ejercicio 16 · Frecuencia de palabras { #ejercicio-16 }

**Colecciones** · ★★★★☆ · *HashMap, TreeMap, merge, HashSet, TreeSet, entrySet*

> Los mapas asocian una clave con un valor: PID → proceso, usuario → conexión… Los usarás en todos los temas.

**Qué tienes que hacer**

1. Parte de un texto de varias líneas (puedes usar un bloque de texto) y sepáralo en palabras en minúsculas.
2. Cuenta cuántas veces aparece cada palabra en un HashMap<String, Integer> usando merge.
3. Muestra las frecuencias ordenadas alfabéticamente con un TreeMap.
4. Muestra las tres palabras más repetidas.
5. Guarda las palabras distintas en un Set, muestra cuántas hay, comprueba si contiene «pid» y qué devuelve add de una palabra repetida.

Clase: `FrecuenciaPalabras.java`

## Ejercicio 17 · Catálogo con streams { #ejercicio-17 }

**Programación funcional** · ★★★★☆ · *Lambdas, Predicate, Runnable, referencias a métodos, streams, Collectors, Optional*

> Las lambdas son imprescindibles en Java moderno: con ellas se crean hilos, se reacciona cuando termina un proceso (onExit) y se procesan listas.

**Qué tienes que hacer**

1. Define un record Producto(nombre, categoria, precio, stock) y una lista con seis productos.
2. Guarda en una variable un Predicate<Producto> que indique si hay stock.
3. Con un stream, obtén los nombres de los productos con stock y precio menor de 100 €, ordenados alfabéticamente.
4. Calcula el valor total del almacén (precio · stock), cuenta los productos de cada categoría con groupingBy y busca el más caro con max (devuelve un Optional).
5. Lista los productos agotados usando negate() del predicado.
6. Crea un Runnable con una lambda que muestre un mensaje y ejecútalo con run().

Clase: `Streams.java`

## Ejercicio 18 · Estado de los pedidos { #ejercicio-18 }

**Tipos modernos** · ★★★☆☆ · *enum con atributos y métodos, switch sobre enum, record, constructor compacto*

> Los enum representan un conjunto cerrado de valores, como los estados de un proceso o de un hilo. Los record son clases de datos inmutables.

**Qué tienes que hacer**

1. Crea el enum Estado con PENDIENTE, PAGADO, ENVIADO, ENTREGADO y CANCELADO. Cada valor guarda un texto descriptivo.
2. Añade el método siguiente(), que con un switch devuelva el estado siguiente. ENTREGADO y CANCELADO se quedan como están.
3. Crea record Pedido(int id, String cliente, double importe, Estado estado). Valida en el constructor compacto que el importe sea positivo y que el cliente no esté vacío.
4. Añade avanzar(), que devuelva un pedido nuevo con el estado siguiente, ya que los record son inmutables.
5. Avanza el estado de tres pedidos, recorre Estado.values() y comprueba que dos record con los mismos datos son equals.

Clase: `Pedidos.java`

## Ejercicio 19 · Notas en un fichero { #ejercicio-19 }

**Ficheros** · ★★★★☆ · *java.nio.file: Path, Files, BufferedReader, BufferedWriter, try-with-resources, IOException*

> Los ficheros son el mecanismo más sencillo para que dos procesos compartan información.

**Qué tienes que hacer**

1. Escribe un fichero notas.txt con cuatro líneas «nombre;nota» usando Files.write.
2. Léelo línea a línea con un BufferedReader en un try-with-resources y calcula la media y la mejor nota.
3. Escribe un informe.txt con un BufferedWriter y muéstralo después con Files.readAllLines.
4. Intenta leer un fichero que no existe y captura la excepción mostrando su tipo.

Clase: `FicherosNotas.java`

## Ejercicio 20 · Integrador: calculadora filtro { #ejercicio-20 }

**Integrador** · ★★★★★ · *Entrada estándar, BufferedReader, enum, record, excepciones, Map, streams, System.err, System.exit*

> Este programa junta lo repasado y es el puente directo con el Tema 1: un programa «filtro» que lee de su entrada y escribe en su salida puede lanzarse como proceso hijo y comunicarse con el padre por tuberías.

**Qué tienes que hacer**

1. Lee líneas de System.in con un BufferedReader hasta el final de la entrada (readLine() devuelve null). Ignora las líneas vacías y las que empiezan por #.
2. Cada línea tiene el formato «número operador número», por ejemplo 3 + 4. Crea un enum Operador (+, -, *, /) con un método aplicar(a, b) y un record Operacion con un método static parsear(String linea).
3. Escribe cada resultado en la salida estándar y cada error en la salida de errores, indicando el número de línea: formato incorrecto, operador desconocido, número no válido o división entre cero.
4. Al final, muestra cuántas operaciones han ido bien, cuántos errores ha habido, la suma de los resultados y cuántas veces se ha usado cada operador (Map).
5. Termina con código 0 si no ha habido errores y con 1 si los ha habido.
6. Pruébalo redirigiendo un fichero: java CalculadoraFiltro < operaciones.txt. Prueba también: java CalculadoraFiltro < operaciones.txt 2> errores.txt.

**Datos de prueba**

```text
3 + 4
10 / 4
# comentario
2 * 2.5
8 / 0
5 % 2
hola + 1
100 - 1
```

Clase: `CalculadoraFiltro.java`
