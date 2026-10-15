# 5. Programación orientada a objetos

## 5.1 Clases y objetos

Una **clase** es un molde que describe cómo son y qué hacen un tipo de objetos. Un **objeto** es un ejemplar concreto creado a partir de ese molde.

| Clase | Objetos |
|---|---|
| `Alumno` (nombre, nota) | Ana con un 8, Luis con un 6 |
| `CuentaBancaria` (titular, saldo) | La cuenta de Ana con 300 € |

Una clase tiene:

- **Atributos**: los datos que guarda cada objeto (su **estado**).
- **Constructores**: el código que inicializa un objeto al crearlo con `new`.
- **Métodos**: lo que el objeto sabe hacer (su **comportamiento**).

```java title="Alumno.java"
public class Alumno {
    // atributos
    private String nombre;
    private double nota;

    // constructor
    public Alumno(String nombre, double nota) {
        this.nombre = nombre;          // this.nombre es el atributo; nombre, el parámetro
        this.nota = nota;
    }

    // métodos
    public boolean estaAprobado() {
        return nota >= 5;
    }

    public String getNombre() { return nombre; }
    public double getNota()   { return nota; }

    @Override
    public String toString() {
        return nombre + " (" + nota + ")";
    }
}
```

```java
Alumno a = new Alumno("Ana", 8.5);    // new reserva memoria y llama al constructor
System.out.println(a.estaAprobado()); // true
System.out.println(a);                // Ana (8.5): println llama a toString()
```

!!! note "Variables que guardan referencias"
    `a` no contiene el objeto: contiene una **referencia** a él. Por eso `Alumno b = a;` no crea otro alumno; `a` y `b` apuntan al mismo. Si una referencia vale `null` y llamas a un método, obtienes `NullPointerException`.

### Constructores

- Si no escribes ninguno, Java crea uno **por defecto** sin parámetros. Si escribes uno, el de por defecto desaparece.
- Puede haber varios (sobrecarga). Uno puede llamar a otro con `this(...)`, que debe ser la primera instrucción:

```java
public Alumno(String nombre) {
    this(nombre, 0);       // reutiliza el otro constructor
}
```

## 5.2 Encapsulación

La **encapsulación** consiste en ocultar los atributos (`private`) y permitir el acceso solo a través de métodos que **controlan** su uso. Así el objeto nunca queda en un estado inválido.

| Modificador | Accesible desde |
|---|---|
| `private` | Solo la propia clase. |
| *(sin modificador)* | Las clases del mismo paquete. |
| `protected` | El mismo paquete y las subclases. |
| `public` | Cualquier clase. |

```java
public void setNota(double nota) {
    if (nota < 0 || nota > 10) {
        throw new IllegalArgumentException("Nota fuera de rango: " + nota);
    }
    this.nota = nota;
}
```

Regla general: **atributos `private`**, métodos `public` solo para lo que deba usarse desde fuera, y *setters* únicamente cuando tenga sentido cambiar el valor.

## 5.3 Miembros `static`

Un miembro `static` pertenece a la **clase**, no a cada objeto. Hay **una sola copia** compartida por todos.

```java
public class Ticket {
    private static int contador = 0;      // compartido por todos los tickets
    public static final int MAX = 999;    // constante de clase

    private final int numero;             // propio de cada ticket

    public Ticket() {
        contador++;
        numero = contador;
    }

    public static int getEmitidos() { return contador; }
}
```

```java
new Ticket(); new Ticket();
System.out.println(Ticket.getEmitidos());   // 2: se llama con el nombre de la clase
```

- Un método `static` **no puede** usar atributos de instancia ni `this`, porque no se ejecuta sobre ningún objeto.
- Las **clases de utilidad** (como `Math` o `Arrays`) solo tienen métodos `static` y un constructor `private` para que nadie las instancie.

!!! warning "`static` y concurrencia"
    En el Tema 2 verás que un atributo `static` compartido por varios hilos puede dar resultados incorrectos si no se **sincroniza**. Tenlo en mente.

## 5.4 Herencia

La **herencia** permite crear una clase nueva (**subclase**) a partir de otra (**superclase**), reutilizando sus atributos y métodos y añadiendo o modificando lo necesario. Expresa una relación **«es un»**: un `Gerente` *es un* `Empleado`.

```java
public class Empleado {
    protected String nombre;
    protected double sueldoBase;

    public Empleado(String nombre, double sueldoBase) {
        this.nombre = nombre;
        this.sueldoBase = sueldoBase;
    }

    public double sueldo() { return sueldoBase; }
}

public class Gerente extends Empleado {
    private double plus;

    public Gerente(String nombre, double sueldoBase, double plus) {
        super(nombre, sueldoBase);     // llama al constructor de Empleado: primera línea
        this.plus = plus;
    }

    @Override
    public double sueldo() {
        return super.sueldo() + plus;  // reutiliza el método del padre
    }

    public double getPlus() { return plus; }
}
```

| Concepto | Significado |
|---|---|
| `extends` | Indica la superclase. Java solo permite **una**. |
| `super(...)` | Llama al constructor del padre. Si no lo pones, se llama a `super()` sin parámetros. |
| `super.metodo()` | Llama a la versión del padre de un método sobrescrito. |
| `@Override` | Indica que sobrescribes un método. El compilador comprueba que exista en el padre. |
| `Object` | Toda clase hereda, directa o indirectamente, de `Object` (`toString`, `equals`, `hashCode`…). |
| `final` | Una clase `final` no se puede heredar; un método `final` no se puede sobrescribir. |

## 5.5 Polimorfismo

Una variable del tipo de la superclase puede guardar **cualquier objeto de sus subclases**. Al llamar a un método, se ejecuta la versión **del objeto real**, no la del tipo de la variable:

```java
Empleado[] plantilla = {
    new Empleado("Eva", 1500),
    new Gerente("Juan", 2000, 500)
};
for (Empleado e : plantilla) {
    System.out.println(e.nombre + ": " + e.sueldo());   // 1500.0 y 2500.0
}
```

Para saber el tipo real se usa `instanceof`. Desde Java 16 puede declarar a la vez una variable del tipo comprobado (*pattern matching*):

```java
if (e instanceof Gerente g) {
    System.out.println("Gerente con plus: " + g.getPlus());
}
```

## 5.6 Clases abstractas e interfaces

### Clase abstracta

Una clase `abstract` **no se puede instanciar**. Sirve de base común y puede tener métodos `abstract` (sin cuerpo) que las subclases **están obligadas** a implementar:

```java
public abstract class Figura {
    public abstract double area();       // cada figura la calcula a su manera

    public String descripcion() {        // método normal, heredado
        return getClass().getSimpleName() + " de área " + String.format("%.2f", area());
    }
}

public class Circulo extends Figura {
    private final double radio;
    public Circulo(double radio) { this.radio = radio; }
    @Override public double area() { return Math.PI * radio * radio; }
}
```

### Interfaz

Una **interfaz** define un **contrato**: un conjunto de métodos que una clase se compromete a ofrecer. Una clase puede implementar **varias** interfaces.

```java
public interface Redimensionable {
    void escalar(double factor);                  // abstracto por defecto

    default void duplicar() { escalar(2); }       // método con implementación (Java 8+)
}

public class Rectangulo extends Figura implements Redimensionable, Comparable<Rectangulo> {
    private double base, altura;
    public Rectangulo(double base, double altura) { this.base = base; this.altura = altura; }

    @Override public double area() { return base * altura; }
    @Override public void escalar(double f) { base *= f; altura *= f; }
    @Override public int compareTo(Rectangulo otro) { return Double.compare(area(), otro.area()); }
}
```

| | Clase abstracta | Interfaz |
|---|---|---|
| Relación | «es un» (jerarquía) | «sabe hacer» (capacidad) |
| Herencia | Solo una (`extends`) | Varias (`implements`) |
| Atributos | Puede tener estado | Solo constantes |
| Constructores | Sí | No |

!!! tip "Interfaces que aparecen en PSP"
    `Runnable` (Tema 2: la tarea que ejecuta un hilo), `Comparable` y `Comparator` (ordenar), `AutoCloseable` (try con recursos). Todas son interfaces de **un solo método**, así que se pueden escribir con lambdas (apartado 7).

## 5.7 `equals` y `hashCode`

`==` compara referencias. Para que dos objetos con los mismos datos se consideren **iguales** hay que sobrescribir `equals`, y siempre que se sobrescriba `equals` hay que sobrescribir también `hashCode` (lo usan `HashSet` y `HashMap`):

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Alumno otro)) return false;
    return nombre.equals(otro.nombre);
}

@Override
public int hashCode() {
    return java.util.Objects.hash(nombre);
}
```

Los `record` (apartado 7) generan `equals`, `hashCode` y `toString` automáticamente.

## Preguntas de repaso

1. ¿Qué diferencia hay entre una clase y un objeto?
2. ¿Por qué los atributos suelen ser `private`?
3. Si una clase tiene un atributo `static int total`, ¿cuántas copias hay con 10 objetos creados?
4. ¿Qué hace `super(...)` y dónde debe ir?
5. Con `Empleado e = new Gerente(...)`, ¿qué versión de `sueldo()` se ejecuta?
6. ¿Cuándo usarías una interfaz en lugar de una clase abstracta?

!!! example "Practica"
    [Ejercicio 11](boletin.md#ejercicio-11) · [Ejercicio 12](boletin.md#ejercicio-12) · [Ejercicio 13](boletin.md#ejercicio-13) · [Ejercicio 14](boletin.md#ejercicio-14)
