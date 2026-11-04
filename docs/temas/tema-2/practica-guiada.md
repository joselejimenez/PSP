# Práctica guiada · Gestor de descargas

!!! info "Práctica guiada"
    Se hace **en clase, paso a paso** y no se evalúa. Junta en un solo programa todo lo de los apartados 1 a 4.

Vas a programar un gestor que descarga cinco ficheros y a mejorarlo en cuatro pasos: primero sin hilos, después con un hilo por descarga, luego con hilos virtuales y, por último, cancelando lo que tarde demasiado. En cada paso medirás el tiempo total.

Las descargas son **simuladas**: cada una espera con `Thread.sleep` los segundos que le toca. No se baja nada de Internet, así que funciona igual en todos los ordenadores.

| Fichero | Tarda |
|---|---|
| foto.jpg | 1 s |
| video.mp4 | 4 s |
| musica.mp3 | 2 s |
| juego.zip | 2 s |
| apuntes.pdf | 1 s |

!!! question "Antes de empezar, apunta tu predicción"
    ¿Cuánto tardará si descargas los ficheros uno detrás de otro? ¿Y si los descargas todos a la vez?

## Plantilla

```java
import java.util.ArrayList;
import java.util.List;

public class Descargas {
    static final String[] FICHEROS = {"foto.jpg", "video.mp4",
            "musica.mp3", "juego.zip", "apuntes.pdf"};
    static final int[] SEGUNDOS = {1, 4, 2, 2, 1};

    // PASO 1: descargar(nombre, seg) y secuencial()
    // PASO 2: conHilos()
    // PASO 3: conVirtuales()
    // PASO 4: conLimite()

    public static void main(String[] args) throws InterruptedException {
        long ini = System.currentTimeMillis();
        // secuencial();     // en cada paso cambiamos esta llamada
        long ms = System.currentTimeMillis() - ini;
        System.out.printf("Total: %.1f s%n", ms / 1000.0);
    }
}
```

En cada paso añadirás un método nuevo y cambiarás **solo** la llamada del `main`. No borres los anteriores: al final compararás los cuatro.

## Paso 1 · Secuencial

1. Escribe `static void descargar(String nombre, int seg)`, que:
    - guarde el nombre del hilo que lo ejecuta (`Thread.currentThread().getName()`);
    - imprima `[hilo] empieza nombre`;
    - duerma `seg` segundos;
    - imprima `[hilo] terminado nombre (N s)`;
    - si salta `InterruptedException`, imprima `[hilo] CANCELADO nombre` (lo usarás en el paso 4).
2. Escribe `static void secuencial()`, que llame a `descargar` para cada fichero con un `for`.

**Resultado esperado:** todas las líneas con `[main]`, en orden, y `Total: 10,0 s`.

## Paso 2 · Un hilo por descarga

1. Escribe `static void conHilos()`, que cree un hilo de plataforma por fichero, con los nombres `D-0`, `D-1`…, y lo arranque.
2. Guarda los hilos en una `List<Thread>` y, **en un segundo bucle**, espera a todos con `join()`.

Pista: dentro de la lambda no puedes usar el `i` del bucle. Cópialo antes en una variable nueva (`int n = i;`).

**Resultado esperado:** las cinco descargas empiezan a la vez, en un orden que cambia entre ejecuciones, y `Total: 4,0 s`. Si te sale 10 s, revisa si has llamado a `run()` o si has hecho el `join()` dentro del primer bucle.

## Paso 3 · Hilos virtuales

1. Copia `conHilos()` como `conVirtuales()`.
2. Cambia la creación del hilo por `Thread.ofVirtual().name("V-" + n).start(...)`, que lo crea y lo arranca a la vez.

**Resultado esperado:** `Total: 4,0 s` y las líneas con `[V-0]`, `[V-1]`… Fíjate en todo lo que **no** has tenido que cambiar. Con cinco descargas no se nota la diferencia; con cien mil, solo la versión con hilos virtuales aguantaría.

## Paso 4 · Límite de 3 segundos

El usuario no quiere esperar más de 3 segundos **en total**. Lo que no haya terminado a los 3 s debe cancelarse.

1. Escribe `conLimite()`: arranca las cinco descargas con hilos virtuales, como en el paso 3.
2. Calcula el instante límite: `long limite = System.currentTimeMillis() + 3000;`
3. Para cada hilo:
    - calcula cuánto tiempo **queda** hasta el límite;
    - si queda tiempo, espéralo como mucho ese tiempo con `join(queda)`;
    - si después sigue vivo (`isAlive()`), pídele que pare con `interrupt()`.
4. Termina con otro bucle de `join()` para que los cancelados acaben de imprimir.

!!! warning "`join(0)` espera para siempre"
    `join(0)` no significa «no esperes», sino «espera sin límite». Llama a `join(queda)` solo si `queda > 0`.

**Resultado esperado:** terminan cuatro descargas, `video.mp4` sale como `CANCELADO` y `Total: 3,0 s`.

## Para terminar

Completa la tabla con tus tiempos:

| Paso | Versión | Tu tiempo total |
|---|---|---|
| 1 | Secuencial | |
| 2 | Un hilo por descarga | |
| 3 | Hilos virtuales | |
| 4 | Límite de 3 s | |

Y responde:

1. ¿Por qué en el paso 2 el total es lo que tarda la descarga más lenta y no la suma?
2. ¿Cuántos hilos hay vivos durante el primer segundo del paso 2? ¿En qué estado está cada uno?
3. Los pasos 2 y 3 tardan lo mismo. ¿En qué situación se notaría la diferencia?
4. En el paso 4, ¿por qué no basta con hacer `join(3000)` a cada hilo?
5. ¿Qué pasaría en el paso 4 si `descargar()` tuviera un `catch` vacío?

!!! success "Solución"
    Cuando termines, compara tu programa con la [solución de los cuatro pasos](practica-guiada-solucion.md).

!!! tip "Para el apartado 8"
    Más adelante añadirás a este programa un contador de descargas completadas y canceladas. Guarda tu `Descargas.java`.
