# 3. Ciclo de vida de un hilo

Igual que un proceso, un hilo pasa por varios **estados** desde que se crea hasta que termina. Java los define exactamente en el enum `Thread.State`, y un hilo solo puede estar en uno en cada momento.

## 3.1 Los seis estados

<svg class="diagrama" viewBox="0 0 760 360" role="img" aria-label="Diagrama de los seis estados de un hilo en Java y sus transiciones">
<defs><marker id="punta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>
<rect class="caja" x="10" y="157" width="110" height="46" rx="10"/><text class="txt" x="65" y="180">NEW</text>
<text class="etq" x="270" y="135">(listo o ejecutándose)</text>
<rect class="caja activa" x="180" y="147" width="180" height="66" rx="10"/><text class="txt" x="270" y="180">RUNNABLE</text>
<rect class="caja" x="190" y="290" width="160" height="46" rx="10"/><text class="txt" x="270" y="313">TERMINATED</text>
<rect class="caja" x="480" y="20" width="260" height="60" rx="10"/><text class="txt" x="610" y="41">BLOCKED</text><text class="etq" x="610" y="64">espera un cerrojo ocupado</text>
<rect class="caja" x="480" y="150" width="260" height="60" rx="10"/><text class="txt" x="610" y="171">WAITING</text><text class="etq" x="610" y="194">join() o wait() sin límite</text>
<rect class="caja" x="480" y="280" width="260" height="60" rx="10"/><text class="txt" x="610" y="301">TIMED_WAITING</text><text class="etq" x="610" y="324">sleep(ms) o join(ms)</text>
<path class="flecha" d="M120,180 L178,180"/><text class="etq" x="150" y="170">start()</text>
<path class="flecha" d="M270,213 L270,288"/><text class="etq" x="318" y="255">acaba run()</text>
<path class="flecha" marker-start="url(#punta)" d="M360,160 L478,58"/>
<path class="flecha" marker-start="url(#punta)" d="M360,180 L478,180"/>
<path class="flecha" marker-start="url(#punta)" d="M360,200 L478,302"/>
</svg>

| Estado | Qué significa | Cómo se llega |
|---|---|---|
| **NEW** | El objeto `Thread` existe, pero todavía no se ha arrancado. | `new Thread(tarea)` |
| **RUNNABLE** | Está listo para ejecutarse o ejecutándose. | `start()`, o al terminar una espera |
| **BLOCKED** | Quiere entrar en un bloque `synchronized` y el cerrojo lo tiene otro hilo. | Lo verás en el [apartado 7](07-synchronized.md) |
| **WAITING** | Espera, **sin límite de tiempo**, a que ocurra algo. | `otro.join()`, `wait()` |
| **TIMED_WAITING** | Espera, pero **con un tiempo máximo**. Si se cumple, vuelve solo. | `Thread.sleep(ms)`, `otro.join(ms)` |
| **TERMINATED** | Ha terminado `run()`, bien o lanzando una excepción. No se puede volver a arrancar. | Fin de `run()` |

De los tres estados de espera se vuelve siempre a **RUNNABLE**.

!!! note "Java no distingue entre «listo» y «en ejecución»"
    En el Tema 1 viste que un proceso puede estar **Listo** o **En ejecución**. En Java las dos cosas son **RUNNABLE**, porque quién usa la CPU en cada momento lo decide el sistema operativo y la JVM no lo controla. Por eso en Java **no existe** un estado `RUNNING`.

## 3.2 Qué provoca cada cambio

| Lo que ocurre | Estado del hilo |
|---|---|
| `new Thread(tarea)` | NEW |
| `t.start()` | RUNNABLE |
| `Thread.sleep(500)` | TIMED_WAITING |
| `otro.join()` | WAITING |
| `otro.join(2000)` | TIMED_WAITING |
| Entrar en un `synchronized` cuyo cerrojo tiene otro hilo | BLOCKED |
| Esperar una tecla (`Scanner.nextLine()`) o datos de la red | **RUNNABLE** (¡ojo!) |
| Acaba `run()` o lanza una excepción | TERMINATED |

Fíjate en dos filas:

- Con **`join()`**, el que cambia de estado es el hilo que **llama** a `join()`, no el hilo al que se espera.
- Un hilo parado en `scanner.nextLine()` o leyendo de un socket aparece como **RUNNABLE**, no como BLOCKED: para la JVM está ejecutando código nativo. En Java, **BLOCKED significa solo esperar un cerrojo**.

!!! warning "`stop()` ya no existe"
    En Internet verás ejemplos antiguos que paran hilos con `stop()`, `suspend()` o `resume()`. Se eliminaron por peligrosos: paraban el hilo en cualquier punto, incluso a mitad de modificar un objeto, y lo dejaban corrupto. Desde JDK 20, `stop()` lanza `UnsupportedOperationException`. Para pedir a un hilo que pare se usa **`interrupt()`**, que verás en el [apartado 4](04-controlar-hilos.md).

## 3.3 Ver los estados con `getState()`

```java
public class Estados {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                return;
            }
        });
        System.out.println("1: " + t.getState());   // NEW
        t.start();
        System.out.println("2: " + t.getState());   // RUNNABLE
        Thread.sleep(100);                          // damos tiempo a que se duerma
        System.out.println("3: " + t.getState());   // TIMED_WAITING
        t.join();
        System.out.println("4: " + t.getState());   // TERMINATED
    }
}
```

```text
1: NEW
2: RUNNABLE
3: TIMED_WAITING
4: TERMINATED
```

También puedes preguntar `t.isAlive()`: devuelve `true` si el hilo ya ha arrancado y todavía no ha terminado (RUNNABLE, BLOCKED, WAITING o TIMED_WAITING), y `false` en NEW y TERMINATED.

!!! warning "`getState()` es una foto"
    Cuando lees el estado, el hilo ya puede haber cambiado. Úsalo para aprender y depurar, nunca para decidir qué hace el programa. Para coordinar hilos están `join()` y los mecanismos de sincronización de los apartados siguientes.

## Preguntas de repaso

1. ¿Por qué en Java no existe un estado `RUNNING`?
2. Un hilo hace `Thread.sleep(1000)`. ¿En qué estado está? ¿Está usando la CPU?
3. El hilo `main` llama a `t.join()`. ¿Quién pasa a WAITING, `main` o `t`?
4. ¿Qué diferencia hay entre WAITING y TIMED_WAITING? Pon un método que lleve a cada uno.
5. Un hilo espera en `scanner.nextLine()`. ¿Qué devuelve `getState()`? ¿Es lo que esperabas?
6. ¿Por qué se eliminó `stop()`?
