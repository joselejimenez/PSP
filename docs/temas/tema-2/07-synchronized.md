# 7. synchronized

`synchronized` es la herramienta básica de Java para la **exclusión mutua**: un cerrojo que solo puede tener un hilo a la vez. El hilo que llega y lo encuentra ocupado, espera.

## 7.1 Un bloque `synchronized`

```java
public class ContadorSync {
    static int cuenta = 0;
    static final Object cerrojo = new Object();      // uno solo, compartido por todos

    public static void main(String[] args) throws InterruptedException {
        Thread[] hilos = new Thread[4];
        for (int i = 0; i < 4; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    synchronized (cerrojo) {
                        cuenta++;                    // sección crítica
                    }
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

```text
Esperado 400000, obtenido 400000
```

Sale **siempre** 400.000.

- Todo objeto de Java lleva incorporado un **cerrojo**, también llamado **monitor**. `synchronized (cerrojo) { … }` significa: «coge el cerrojo de este objeto, ejecuta el bloque y suéltalo».
- **Al entrar**, el hilo coge el cerrojo. Si lo tiene otro hilo, se queda esperando en estado **BLOCKED**: el que vimos en el [apartado 3](03-estados.md).
- **Al salir**, lo suelta, **aunque salga por una excepción**. No hay forma de olvidarse de soltarlo.
- El objeto `cerrojo` es `static final`: hay **uno solo** y lo comparten todos los hilos. Es la clave.

Ahora los hilos hacen cola para incrementar, así que el programa va algo más lento que sin protección. Es normal: correcto y un poco más lento es mejor que rápido y mal.

!!! example "La cocina"
    El cerrojo es el **único cuchillo**. Quien lo coge corta; los demás esperan con las manos quietas (BLOCKED) hasta que lo suelte.

## 7.2 Métodos `synchronized`

Poner `synchronized` en la cabecera de un método equivale a envolver todo su cuerpo en un bloque `synchronized`. Es la forma más habitual: el objeto **se protege a sí mismo** y quien lo usa no tiene que acordarse de nada.

```java
public class ContadorMetodo {

    static class Contador {
        private int valor = 0;

        public synchronized void incrementar() {
            valor++;
        }

        public synchronized int getValor() {
            return valor;
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Contador c = new Contador();                 // uno, compartido por todos los hilos
        Thread[] hilos = new Thread[4];
        for (int i = 0; i < 4; i++) {
            hilos[i] = new Thread(() -> {
                for (int j = 0; j < 100_000; j++) {
                    c.incrementar();
                }
            });
            hilos[i].start();
        }
        for (Thread h : hilos) {
            h.join();
        }
        System.out.println("Esperado 400000, obtenido " + c.getValor());
    }
}
```

¿Qué cerrojo usa cada forma?

| Escribes | Cerrojo |
|---|---|
| `synchronized void m()` | `this`: el objeto sobre el que se llama al método |
| `static synchronized void m()` | La clase (`Contador.class`) |
| `synchronized (obj) { … }` | `obj` |

- En un método normal el cerrojo es `this`. Por eso todos los hilos deben usar **el mismo objeto** `Contador`: si cada hilo tuviera el suyo, cada uno tendría su cerrojo y no se protegerían entre sí.
- `getValor()` también va `synchronized`: leer mientras otro hilo escribe tampoco es seguro.
- Dos objetos distintos, `a` y `b`, tienen cerrojos distintos: un hilo puede estar en `a.incrementar()` mientras otro está en `b.incrementar()`. Es correcto, porque no comparten el valor.

## 7.3 Arreglar el cajero

En el cajero del [apartado 6](06-condicion-carrera.md#64-comprobar-y-actuar-el-cajero-que-da-dinero-de-mas), `retirar` y `saldo` son `static`, así que el cerrojo natural es la clase:

```java
static synchronized void retirar(String quien, int cantidad) {
    if (saldo >= cantidad) {
        try {
            Thread.sleep(10);
        } catch (InterruptedException e) {
            return;
        }
        saldo -= cantidad;
        System.out.println(quien + " retira " + cantidad + ". Saldo: " + saldo);
    } else {
        System.out.println(quien + ": saldo insuficiente");
    }
}
```

```text
Ana retira 80. Saldo: 20
Luis: saldo insuficiente
Saldo final: 20
```

Todo el método queda protegido: la comprobación y la resta. Mientras Ana está dentro, Luis espera en BLOCKED. Cuando entra, el saldo ya es 20 y el `if` falla. Puede retirar primero Luis en lugar de Ana; lo que no cambia nunca es que **solo retira uno**.

## 7.4 El error más común: un cerrojo por hilo

```java
hilos[i] = new Thread(() -> {
    Object cerrojo = new Object();              // ¡cada hilo crea el suyo!
    for (int j = 0; j < 100_000; j++) {
        synchronized (cerrojo) {
            cuenta++;
        }
    }
});
```

```text
Esperado 400000, obtenido 326241
```

Compila, parece protegido… y falla igual que sin protección. Cada hilo coge **su propio** cerrojo sin esperar a nadie, porque nadie más lo usa.

!!! tip "Dos reglas"
    1. **Un único cerrojo** compartido por todos los hilos que tocan el dato.
    2. **Sección crítica pequeña**: dentro, solo lo que toca el dato. Mientras un hilo tiene el cerrojo, los demás están parados; si dentro metes un `sleep`, una descarga o una escritura a disco, todos esperan por algo que no necesitaba protección. (En el cajero, la pausa está dentro a propósito, para provocar el error.)

## Preguntas de repaso

1. ¿Qué hace exactamente `synchronized (obj) { … }` al entrar y al salir?
2. ¿En qué estado está un hilo que espera para entrar en un bloque `synchronized`?
3. ¿Qué cerrojo usa un método `synchronized`? ¿Y uno `static synchronized`?
4. Cada hilo crea su propio objeto `Contador` y llama a `incrementar()`, que es `synchronized`. ¿Se protegen entre sí? ¿Por qué?
5. ¿Por qué conviene que la sección crítica sea lo más pequeña posible?
6. ¿Qué pasa con el cerrojo si dentro del bloque `synchronized` salta una excepción?
