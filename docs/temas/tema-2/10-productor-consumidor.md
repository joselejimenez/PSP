# 10. Productor-consumidor

Hasta ahora, los hilos trabajaban cada uno por su lado y solo se protegían para no pisarse. Muchas veces, además, un hilo **produce** cosas que otro hilo **consume**: un panadero hace pan y un cliente se lo lleva; un camarero apunta comandas y los cocineros las cocinan. Es el problema del **productor-consumidor**, uno de los más habituales en programación concurrente.

## 10.1 El problema

Entre el productor y el consumidor hay un sitio donde se dejan las cosas: el **mostrador**, en el caso de la panadería. Y hay dos situaciones en las que alguien tiene que esperar:

| Situación | Quién espera | Hasta cuándo |
|---|---|---|
| El mostrador está **lleno** | El productor | Hasta que el consumidor se lleve algo |
| El mostrador está **vacío** | El consumidor | Hasta que el productor deje algo |

Además, el mostrador lo usan los dos hilos a la vez, así que es un recurso compartido y hay que protegerlo.

Se podría programar a mano con `synchronized` y los métodos `wait()` y `notify()`, que sirven para que un hilo se duerma hasta que otro lo avise. Pero es fácil equivocarse. Java ya trae una estructura que lo hace todo: la **cola bloqueante**.

## 10.2 `BlockingQueue`: una cola que espera por ti

Una `BlockingQueue`, del paquete `java.util.concurrent`, es una cola preparada para varios hilos:

| Método | Qué hace |
|---|---|
| `cola.put(x)` | Mete `x` al final. Si la cola está **llena**, el hilo espera hasta que haya sitio. |
| `cola.take()` | Saca el primero. Si la cola está **vacía**, el hilo espera hasta que haya algo. |
| `cola.size()` | Cuántos elementos hay ahora mismo. |

Las dos implementaciones más usadas son:

- `new ArrayBlockingQueue<>(3)`: tiene un **tamaño máximo**, en este caso 3.
- `new LinkedBlockingQueue<>()`: **sin límite** de tamaño; `put()` nunca espera.

`put()` y `take()` ya están protegidos por dentro: no hace falta `synchronized` ni `Lock`. Y como pueden esperar, lanzan `InterruptedException`.

## 10.3 Ejemplo: la panadería

Un panadero hornea 8 panes, uno cada 100 ms, y los deja en un mostrador donde caben 3. Un cliente se lleva un pan cada 400 ms.

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class Panaderia {
    public static void main(String[] args) throws InterruptedException {
        BlockingQueue<String> mostrador = new ArrayBlockingQueue<>(3);   // caben 3 panes

        Thread panadero = new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    Thread.sleep(100);          // hornear es rápido
                    String pan = "pan " + i;
                    System.out.println("Panadero tiene listo el " + pan);
                    mostrador.put(pan);         // si el mostrador está lleno, espera aquí
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        Thread cliente = new Thread(() -> {
            try {
                for (int i = 1; i <= 8; i++) {
                    String pan = mostrador.take();   // si el mostrador está vacío, espera aquí
                    System.out.println("    Cliente se lleva " + pan);
                    Thread.sleep(400);          // comer es lento
                }
            } catch (InterruptedException e) {
                return;
            }
        });

        panadero.start();
        cliente.start();
        panadero.join();
        cliente.join();
        System.out.println("Panadería cerrada");
    }
}
```

```text
Panadero tiene listo el pan 1
    Cliente se lleva pan 1
Panadero tiene listo el pan 2
Panadero tiene listo el pan 3
Panadero tiene listo el pan 4
    Cliente se lleva pan 2
Panadero tiene listo el pan 5
Panadero tiene listo el pan 6
    Cliente se lleva pan 3
Panadero tiene listo el pan 7
    Cliente se lleva pan 4
Panadero tiene listo el pan 8
    Cliente se lleva pan 5
    Cliente se lleva pan 6
    Cliente se lleva pan 7
    Cliente se lleva pan 8
Panadería cerrada
```

- Al principio, el panadero va **mucho más rápido** que el cliente y llena el mostrador.
- Cuando el mostrador está lleno, `put()` hace que el panadero **espere**. A partir de ahí, solo puede poner un pan cada vez que el cliente se lleva uno: va **al ritmo del cliente**.
- Al final, el panadero ya ha terminado y el cliente se lleva los panes que quedan.
- Nadie ha escrito `synchronized`, ni `wait()`, ni `sleep()` para esperar al otro: lo hace todo la cola.

## 10.4 ¿Cómo sabe el consumidor que ya no hay más?

En la panadería, el cliente sabe que son 8 panes. Pero muchas veces el consumidor no sabe cuántas cosas van a llegar. La solución habitual es que el productor, al terminar, meta en la cola un **aviso de fin**: un valor especial, como `"FIN"`. Cuando el consumidor lo saca, sabe que tiene que terminar.

```java
String plato = comandas.take();
if (plato.equals("FIN")) {
    break;                  // no hay más: termino
}
```

Si hay **varios consumidores**, el productor tiene que meter **un aviso de fin por cada consumidor**, porque cada aviso solo lo saca uno.

## Preguntas de repaso

1. ¿En qué dos situaciones tiene que esperar alguien en el problema del productor-consumidor?
2. ¿Qué hace `put()` si la cola está llena? ¿Y `take()` si está vacía?
3. ¿Qué diferencia hay entre `ArrayBlockingQueue` y `LinkedBlockingQueue`?
4. En la panadería, ¿por qué a partir del cuarto pan el panadero va al ritmo del cliente?
5. Hay un productor y tres consumidores. ¿Cuántos avisos de `"FIN"` tiene que meter el productor? ¿Por qué?

## Ejercicio autoguiado: la impresora compartida

En una oficina, los empleados mandan documentos a una impresora. La impresora tiene una **bandeja de entrada donde solo caben 2 documentos**. Si está llena, quien envía espera; si está vacía, la impresora espera. Es exactamente un productor-consumidor.

### Paso 1 · Un empleado y una impresora

Escribe `ImpresoraPaso1` con:

- una `BlockingQueue<String> cola = new ArrayBlockingQueue<>(2);`
- un hilo **empleado** (productor) que haga `put` de 3 documentos: `"Ana-doc1"`, `"Ana-doc2"`, `"Ana-doc3"`, e imprima «Ana envía …».
- un hilo **impresora** (consumidor) que haga `take` 3 veces, imprima «Imprimiendo …» y tarde 500 ms en cada uno.
- el `main` arranca los dos, espera con `join()` e imprime «Impresión terminada».

Salida aproximada (el orden de las primeras líneas cambia):

```text
Ana envía Ana-doc1
Ana envía Ana-doc2
    Imprimiendo Ana-doc1
Ana envía Ana-doc3
    Imprimiendo Ana-doc2
    Imprimiendo Ana-doc3
Impresión terminada
```

**Piensa:** ¿por qué Ana no puede enviar el tercer documento hasta que se imprime el primero?

??? success "Solución del paso 1"
    ```java
    import java.util.concurrent.ArrayBlockingQueue;
    import java.util.concurrent.BlockingQueue;

    public class ImpresoraPaso1 {
        public static void main(String[] args) throws InterruptedException {
            BlockingQueue<String> cola = new ArrayBlockingQueue<>(2);   // caben 2 documentos

            Thread empleado = new Thread(() -> {
                try {
                    for (int i = 1; i <= 3; i++) {
                        String doc = "Ana-doc" + i;
                        cola.put(doc);
                        System.out.println("Ana envía " + doc);
                    }
                } catch (InterruptedException e) {
                    return;
                }
            });

            Thread impresora = new Thread(() -> {
                try {
                    for (int i = 1; i <= 3; i++) {
                        String doc = cola.take();
                        System.out.println("    Imprimiendo " + doc);
                        Thread.sleep(500);                  // imprimir es lento
                    }
                } catch (InterruptedException e) {
                    return;
                }
            });

            empleado.start();
            impresora.start();
            empleado.join();
            impresora.join();
            System.out.println("Impresión terminada");
        }
    }
    ```

### Paso 2 · Tres empleados

Copia la clase como `ImpresoraPaso2`. Ahora hay tres empleados, `Ana`, `Luis` y `Marta`, y cada uno envía 3 documentos (`"Luis-doc1"`…). Crea los hilos con un bucle sobre un array de nombres.

¿Cuántas veces tiene que hacer `take` la impresora ahora?

Salida aproximada: se mezclan los envíos de los tres y salen 9 líneas «Imprimiendo», y al final «Impresión terminada».

??? success "Solución del paso 2"
    ```java
    import java.util.concurrent.ArrayBlockingQueue;
    import java.util.concurrent.BlockingQueue;

    public class ImpresoraPaso2 {
        public static void main(String[] args) throws InterruptedException {
            BlockingQueue<String> cola = new ArrayBlockingQueue<>(2);
            String[] nombres = {"Ana", "Luis", "Marta"};

            Thread[] empleados = new Thread[nombres.length];
            for (int e = 0; e < nombres.length; e++) {
                String nombre = nombres[e];
                empleados[e] = new Thread(() -> {
                    try {
                        for (int i = 1; i <= 3; i++) {
                            String doc = nombre + "-doc" + i;
                            cola.put(doc);
                            System.out.println(nombre + " envía " + doc);
                        }
                    } catch (InterruptedException ex) {
                        return;
                    }
                });
            }

            Thread impresora = new Thread(() -> {
                try {
                    for (int i = 1; i <= 9; i++) {           // 3 empleados x 3 documentos
                        String doc = cola.take();
                        System.out.println("    Imprimiendo " + doc);
                        Thread.sleep(500);
                    }
                } catch (InterruptedException e) {
                    return;
                }
            });

            for (Thread t : empleados) t.start();
            impresora.start();
            for (Thread t : empleados) t.join();
            impresora.join();
            System.out.println("Impresión terminada");
        }
    }
    ```

    La impresora hace 9 `take`: 3 empleados × 3 documentos. Fíjate en el problema: la impresora tiene que **saber de antemano** cuántos documentos van a llegar. En el paso 3 lo arreglamos.

### Paso 3 · El aviso de fin

Copia la clase como `ImpresoraPaso3`. La impresora ya no cuenta: hace `take` en un `while (true)` y, cuando recibe `"FIN"`, sale del bucle e imprime cuántos documentos ha impreso.

¿Quién manda el `"FIN"`? No puede ser un empleado (no sabe si los otros han terminado). Lo manda el **`main`**, después de hacer `join()` de los tres empleados.

Final de la salida:

```text
    La impresora se apaga tras 9 documentos
Impresión terminada
```

??? success "Solución del paso 3"
    ```java
    import java.util.concurrent.ArrayBlockingQueue;
    import java.util.concurrent.BlockingQueue;

    public class ImpresoraPaso3 {
        public static void main(String[] args) throws InterruptedException {
            BlockingQueue<String> cola = new ArrayBlockingQueue<>(2);
            String[] nombres = {"Ana", "Luis", "Marta"};

            Thread[] empleados = new Thread[nombres.length];
            for (int e = 0; e < nombres.length; e++) {
                String nombre = nombres[e];
                empleados[e] = new Thread(() -> {
                    try {
                        for (int i = 1; i <= 3; i++) {
                            String doc = nombre + "-doc" + i;
                            cola.put(doc);
                            System.out.println(nombre + " envía " + doc);
                        }
                    } catch (InterruptedException ex) {
                        return;
                    }
                });
            }

            Thread impresora = new Thread(() -> {
                int impresos = 0;
                try {
                    while (true) {
                        String doc = cola.take();
                        if (doc.equals("FIN")) {
                            break;                          // ya no llegan más documentos
                        }
                        System.out.println("    Imprimiendo " + doc);
                        Thread.sleep(500);
                        impresos++;
                    }
                } catch (InterruptedException e) {
                    return;
                }
                System.out.println("    La impresora se apaga tras " + impresos + " documentos");
            });

            for (Thread t : empleados) t.start();
            impresora.start();
            for (Thread t : empleados) t.join();            // cuando han enviado todo...
            cola.put("FIN");                                // ...el main manda el aviso de fin
            impresora.join();
            System.out.println("Impresión terminada");
        }
    }
    ```

### Paso 4 · Dos impresoras

Copia la clase como `ImpresoraPaso4`. Ahora hay **dos impresoras** que leen de la misma cola. Escribe el código de la impresora en un `Runnable` y crea dos hilos con nombre: `new Thread(imprimir, "Impresora-1")`. Dentro, el nombre se obtiene con `Thread.currentThread().getName()`.

**Piensa antes de ejecutar:** ¿cuántos `"FIN"` tiene que mandar el `main`? ¿Qué pasa si solo manda uno?

Final de la salida (los números cambian, pero suman 9):

```text
    Impresora-2 se apaga tras 4 documentos
    Impresora-1 se apaga tras 5 documentos
Impresión terminada
```

??? success "Solución del paso 4"
    ```java
    import java.util.concurrent.ArrayBlockingQueue;
    import java.util.concurrent.BlockingQueue;

    public class ImpresoraPaso4 {
        public static void main(String[] args) throws InterruptedException {
            BlockingQueue<String> cola = new ArrayBlockingQueue<>(2);
            String[] nombres = {"Ana", "Luis", "Marta"};

            Thread[] empleados = new Thread[nombres.length];
            for (int e = 0; e < nombres.length; e++) {
                String nombre = nombres[e];
                empleados[e] = new Thread(() -> {
                    try {
                        for (int i = 1; i <= 3; i++) {
                            String doc = nombre + "-doc" + i;
                            cola.put(doc);
                            System.out.println(nombre + " envía " + doc);
                        }
                    } catch (InterruptedException ex) {
                        return;
                    }
                });
            }

            Runnable imprimir = () -> {
                String yo = Thread.currentThread().getName();
                int impresos = 0;
                try {
                    while (true) {
                        String doc = cola.take();
                        if (doc.equals("FIN")) {
                            break;                          // ya no llegan más documentos
                        }
                        System.out.println("    " + yo + " imprime " + doc);
                        Thread.sleep(500);
                        impresos++;
                    }
                } catch (InterruptedException e) {
                    return;
                }
                System.out.println("    " + yo + " se apaga tras " + impresos + " documentos");
            };
            Thread impresora1 = new Thread(imprimir, "Impresora-1");
            Thread impresora2 = new Thread(imprimir, "Impresora-2");

            for (Thread t : empleados) t.start();
            impresora1.start();
            impresora2.start();
            for (Thread t : empleados) t.join();
            cola.put("FIN");                                // un aviso de fin por cada impresora
            cola.put("FIN");
            impresora1.join();
            impresora2.join();
            System.out.println("Impresión terminada");
        }
    }
    ```

    Hay que mandar **un `"FIN"` por cada consumidor**. Cada impresora se lleva uno y se apaga. Si solo mandas uno, la otra impresora se queda esperando en `take()` para siempre y el programa no termina.
