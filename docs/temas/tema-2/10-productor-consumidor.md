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
