# 6. Condición de carrera

Todo lo que has programado hasta ahora funcionaba porque **cada hilo trabajaba con sus propios datos**. En cuanto dos hilos escriben en el mismo dato sin ponerse de acuerdo, el programa empieza a fallar, y lo hace sin dar ningún error.

## 6.1 Un programa que falla en silencio

Cuatro hilos suman 1 a la misma variable, 100.000 veces cada uno:

```java
public class Contador {
    static int cuenta = 0;                       // compartida: está en el heap

    public static void main(String[] args) throws InterruptedException {
        Thread[] hilos = new Thread[4];
        for (int i = 0; i < 4; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    cuenta++;
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Esperado 400000, obtenido " + cuenta);
    }
}
```

Tres ejecuciones reales con JDK 21:

```text
Esperado 400000, obtenido 380354
Esperado 400000, obtenido 338007
Esperado 400000, obtenido 383246
```

Casi nunca sale 400.000, y cada vez sale un número distinto. No hay error de compilación ni excepción: simplemente, el resultado es incorrecto.

## 6.2 `cuenta++` no es una operación, son tres

Lo que en Java parece una sola instrucción, en la máquina son tres:

1. **Leer**: copiar el valor de `cuenta` desde la memoria.
2. **Sumar**: sumarle 1 a esa copia.
3. **Escribir**: guardar el resultado en `cuenta`.

El planificador puede quitarle la CPU a un hilo **entre cualquiera de los tres pasos**, y otro hilo puede entrar justo ahí:

| t | Hilo A | Hilo B | `cuenta` |
|---|---|---|---|
| 1 | lee 5 | | 5 |
| 2 | | lee 5 | 5 |
| 3 | suma: 6 | | 5 |
| 4 | | suma: 6 | 5 |
| 5 | escribe 6 | | 6 |
| 6 | | escribe 6 | **6, no 7** |

B leyó **antes** de que A escribiera. Se han hecho dos incrementos y la variable solo ha subido uno: el de A se ha perdido. Pasa pocas veces en cada incremento, pero en 400.000 incrementos pasa miles de veces.

!!! note "Con un solo núcleo también pasa"
    No hace falta que los hilos se ejecuten a la vez: basta con que el planificador cambie de hilo entre la lectura y la escritura.

Estos errores son de los más difíciles de encontrar: el programa puede funcionar bien cien veces y fallar en la ciento uno, o funcionar en tu ordenador y fallar en el del cliente.

## 6.3 Cuatro palabras para todo el tema

| Concepto | Qué es | En el contador |
|---|---|---|
| **Recurso compartido** | Un dato al que acceden varios hilos: una variable `static`, un objeto, un fichero. | `cuenta` |
| **Condición de carrera** | El resultado depende del orden en que se intercalan los hilos. | Sale un número distinto cada vez |
| **Sección crítica** | El trozo de código que usa el recurso compartido. | `cuenta++` |
| **Exclusión mutua** | La solución: que solo **un hilo a la vez** pueda estar dentro de la sección crítica. | Lo verás en el [apartado 7](07-synchronized.md) |

!!! tip "Cómo reconocer una condición de carrera"
    Hacen falta **las tres cosas a la vez**:

    1. Varios hilos.
    2. Un dato compartido.
    3. Al menos uno de ellos **escribe**.

    Si todos solo leen, no hay problema. Si cada hilo tiene sus propios datos, tampoco: por eso la [práctica guiada](practica-guiada.md) funcionaba bien.

## 6.4 Comprobar y actuar: el cajero que da dinero de más

La condición de carrera no es solo cosa de contadores. El patrón más peligroso en la vida real es **comprobar y actuar**: miro si se cumple algo y, si se cumple, hago algo. Entre mirar y hacer, otro hilo puede cambiar la situación.

```java
public class Banco {
    static int saldo = 100;

    static void retirar(String quien, int cantidad) {
        if (saldo >= cantidad) {                                   // 1. comprobar
            try {
                Thread.sleep(10);                                  // el cajero cuenta los billetes
            } catch (InterruptedException e) {
                return;
            }
            saldo -= cantidad;                                     // 2. actuar
            System.out.println(quien + " retira " + cantidad + ". Saldo: " + saldo);
        } else {
            System.out.println(quien + ": saldo insuficiente");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread ana = new Thread(() -> retirar("Ana", 80));
        Thread luis = new Thread(() -> retirar("Luis", 80));
        ana.start();
        luis.start();
        ana.join();
        luis.join();
        System.out.println("Saldo final: " + saldo);
    }
}
```

```text
Ana retira 80. Saldo: 20
Luis retira 80. Saldo: -60
Saldo final: -60
```

Ana y Luis intentan sacar 80 € de una cuenta con 100 €. Solo debería poder uno, pero los dos ejecutan el `if` cuando el saldo todavía es 100, así que **los dos entran**. Luego los dos restan.

La pausa de 10 ms hace que el error salga casi siempre. Sin ella también puede pasar, aunque mucho menos, y justo por eso estos errores pasan las pruebas y aparecen en producción.

El mismo patrón aparece al vender la última entrada de un concierto a dos personas, al reservar el mismo asiento de avión o en «si el fichero no existe, créalo».

!!! warning "La sección crítica es comprobar **y** actuar"
    Va desde el `if` hasta la resta, ambos incluidos. Proteger solo la resta no arregla nada: los dos hilos ya han comprobado que había saldo.

## 6.5 Las colecciones normales tampoco son seguras

```java
List<Integer> lista = new ArrayList<>();
// cuatro hilos hacen lista.add(j) 10.000 veces cada uno
```

En tres ejecuciones salieron 37728, 38359 y 37740 elementos en vez de 40.000. A veces, en lugar de un número incorrecto, salta una `ArrayIndexOutOfBoundsException`. Por dentro, `add()` también son varios pasos: mirar el tamaño, guardar el elemento y aumentar el tamaño.

## Preguntas de repaso

1. ¿Por qué `cuenta++` no es seguro con varios hilos, si es una sola línea de código?
2. Explica con una tabla como la de 6.2 cómo dos hilos pueden perder un incremento.
3. ¿Qué tres condiciones tienen que darse para que haya una condición de carrera?
4. Cinco hilos leen la misma lista de precios para mostrarla y nadie la modifica. ¿Hay condición de carrera?
5. En el cajero, ¿dónde empieza y dónde acaba la sección crítica? ¿Por qué no basta con proteger la resta?
6. ¿Por qué estos errores son tan difíciles de detectar con pruebas?
