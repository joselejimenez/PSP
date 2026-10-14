# 1. Programa, proceso, servicio e hilo

Estos cuatro conceptos aparecen en todo el módulo. Merece la pena tenerlos muy claros desde el principio.

## 1.1 Programa y programa ejecutable

Un **programa** es un conjunto de instrucciones escritas para resolver una tarea. Mientras está guardado en el disco **no hace nada**: es como una receta escrita en un libro de cocina.

Para que el ordenador pueda ejecutarlo, el código fuente tiene que traducirse a un formato que entienda el sistema:

| Lenguaje | Proceso de traducción | Resultado |
|---|---|---|
| C, C++, Rust | El compilador traduce a código máquina del procesador. | Ejecutable nativo: `.exe` (Windows), ELF (Linux), Mach-O (macOS). |
| Java, Kotlin | `javac` traduce a **bytecode**, que ejecuta la máquina virtual (JVM). | Ficheros `.class` o `.jar`. El mismo `.class` funciona en cualquier sistema con JVM. |
| Python, JavaScript | Un intérprete lee y ejecuta el código. | No hay ejecutable: se lanza el intérprete con el fichero fuente. |

!!! note "¿Son todos los ejecutables iguales?"
    No. Un `.exe` de Windows no funciona en Linux, y un ejecutable compilado para un procesador Intel no funciona directamente en uno ARM. Por eso Java usa bytecode: lo que se adapta a cada sistema es la JVM, no nuestro programa.

## 1.2 Proceso

Un **proceso** es un **programa en ejecución**. Cuando haces doble clic en un programa o escribes `java HolaMundo` en la terminal, el sistema operativo:

1. Carga el código del programa en la memoria RAM.
2. Le reserva una zona de memoria **propia y aislada**.
3. Le asigna un número identificador único, el **PID** (*Process Identifier*).
4. Crea su ficha de control, el **PCB**.
5. Lo pone en la cola de procesos que esperan usar la CPU.

Con el ejemplo de la cocina:

| Cocina | Ordenador |
|---|---|
| La receta escrita en el libro | El **programa**, guardado en disco |
| El cocinero | La **CPU**: cada núcleo sigue las instrucciones una a una |
| Los ingredientes | Los **datos** de entrada |
| Estar cocinando la receta | El **proceso**: el programa en marcha |

!!! example "Un programa, varios procesos"
    Si abres tres ventanas del Bloc de notas, hay **un programa** (`notepad.exe`) y **tres procesos**, cada uno con su PID y su memoria. Si escribes en una ventana, las otras no se enteran: cada proceso tiene su propia memoria.

### La memoria de un proceso

Cada proceso tiene su propio **espacio de direcciones**, dividido en zonas:

| Zona | Qué guarda | Ejemplo en Java |
|---|---|---|
| **Código** (*text*) | Las instrucciones del programa. Solo lectura. | El bytecode cargado de los `.class`. |
| **Datos** | Variables globales y estáticas. | Los atributos `static`. |
| **Heap** (montículo) | Memoria que se pide durante la ejecución. | Todo lo que se crea con `new`. |
| **Pila** (*stack*) | Llamadas a métodos en curso, parámetros y variables locales. | Cada llamada a un método añade un marco a la pila. |

El sistema operativo **impide** que un proceso lea o escriba en la memoria de otro. Si un programa falla, no corrompe a los demás. La contrapartida es que, para que dos procesos se comuniquen, hace falta un mecanismo del sistema operativo (apartado 6).

## 1.3 El PCB: la ficha de cada proceso

El sistema operativo guarda la información de cada proceso en una estructura llamada **PCB** (*Process Control Block*, bloque de control de proceso):

| Campo | Para qué sirve |
|---|---|
| **PID y PPID** | Quién es el proceso y quién lo creó. |
| **Estado** | Nuevo, listo, en ejecución, bloqueado o terminado (apartado 3). |
| **Contador de programa** | La dirección de la siguiente instrucción que hay que ejecutar. |
| **Registros de la CPU** | Los valores con los que estaba calculando. |
| **Información de memoria** | Dónde están su código, sus datos, su heap y su pila. |
| **Ficheros y conexiones abiertos** | Los recursos que está usando. |
| **Usuario y permisos** | Qué puede hacer y a qué puede acceder. |
| **Prioridad y estadísticas** | Datos que usa el planificador (apartado 4). |

Cuando el sistema operativo quita la CPU a un proceso para dársela a otro, guarda en su PCB por dónde iba. Cuando le vuelve a tocar, restaura esos datos y el proceso continúa **exactamente donde lo dejó**, como si nada hubiera pasado. Es como el pósit que deja el cocinero cuando aparta la sopa para atender otro plato: «iba por el paso 4, el fuego estaba al medio».

## 1.4 PID, PPID y jerarquía de procesos

Todo proceso es creado por otro, su **padre**. Cada proceso guarda el PID de su padre, el **PPID** (*Parent PID*). Así se forma un **árbol de procesos**:

```
systemd (PID 1)
├── sshd (PID 812)
└── gnome-shell (PID 1500)
    └── bash (PID 2201)
        └── java HolaMundo (PID 2345)
```

- En Linux, el primer proceso que arranca es `systemd` (o `init`), con PID 1. Todos los demás descienden de él.
- En Windows, la mayoría de los programas que abres con doble clic son hijos de `explorer.exe`.
- Si en una terminal escribes `java HolaMundo`, la terminal es el **padre** y el proceso `java` es el **hijo**.

### Ver los procesos del sistema

| Sistema | Herramienta gráfica | Terminal |
|---|---|---|
| Windows | Administrador de tareas → pestaña **Detalles** (muestra el PID) | `tasklist`, o en PowerShell `Get-Process` |
| Linux | Monitor del sistema | `ps -ef` (con PPID), `top`, `htop`, `pstree` |
| macOS | Monitor de Actividad | `ps -ef`, `top` |

### Ver el PID desde Java

Desde Java 9, la clase `ProcessHandle` permite consultar el propio proceso y su padre:

```java
public class MiPid {
    public static void main(String[] args) {
        ProcessHandle yo = ProcessHandle.current();
        System.out.println("Mi PID:  " + yo.pid());
        yo.parent().ifPresent(padre ->
            System.out.println("Mi PPID: " + padre.pid() + " (" + padre.info().command().orElse("?") + ")"));
    }
}
```

Salida de ejemplo, ejecutado desde una terminal de Linux:

```
Mi PID:  745
Mi PPID: 665 (/usr/bin/bash)
```

`parent()` devuelve un `Optional` porque el padre podría haber terminado ya.

## 1.5 Procesos zombis y huérfanos

Cuando un proceso hijo termina, devuelve un **código de salida** (0 si todo fue bien). El padre tiene la obligación de **recoger** ese código.

- **Proceso zombi.** El hijo ya ha terminado, pero el padre todavía no ha recogido su código de salida. El zombi no usa CPU ni memoria, pero sigue ocupando una entrada en la tabla de procesos y un PID. Si se acumulan miles, el sistema se queda sin PID libres. En `ps` aparece con el estado `Z` o la palabra `<defunct>`.
- **Proceso huérfano.** El padre termina **antes** que el hijo. El hijo sigue funcionando y el sistema lo «adopta»: pasa a ser hijo del PID 1, que recogerá su código cuando termine. No es un error; muchos servicios se lanzan así a propósito.

!!! tip "En Java"
    El método `waitFor()` de la clase `Process` espera a que el hijo termine y recoge su código de salida. Es lo que evita que quede zombi (apartado 5).

!!! warning "No confundir"
    Un proceso que se queda **bloqueado para siempre** esperando un dato que nunca llega **no es un zombi**: sigue vivo. Es un error de programación. El zombi, en cambio, ya está muerto.

## 1.6 Servicios

Un **servicio** (en Linux, **demonio** o *daemon*) es un proceso que:

- Se ejecuta en **segundo plano**, sin ventana ni interacción con el usuario.
- Normalmente **arranca con el sistema** y sigue funcionando aunque nadie haya iniciado sesión.
- **Atiende peticiones**: imprimir, conexiones remotas, consultas a una base de datos, páginas web…

Ejemplos: el servicio de cola de impresión, `sshd` (conexiones SSH), un servidor web, MySQL o el servicio de actualizaciones.

| Sistema | Ver y gestionar servicios |
|---|---|
| Windows | `services.msc`, o en PowerShell `Get-Service` y `Restart-Service Spooler` |
| Linux | `systemctl status ssh`, `systemctl restart ssh`, `systemctl list-units --type=service` |
| macOS | `launchctl list` |

En los Temas 3 y 4 programarás tus propios servicios: programas que esperan conexiones de clientes por la red.

## 1.7 Hilos

Un **hilo** (*thread*) es un **flujo de ejecución dentro de un proceso**. Todo proceso tiene al menos uno, el hilo principal, que en Java es el que ejecuta el método `main`.

Un proceso puede tener **varios hilos**. Por ejemplo, un procesador de textos tiene un hilo que atiende el teclado, otro que revisa la ortografía y otro que guarda una copia automática.

| | Proceso | Hilo |
|---|---|---|
| **Memoria** | Propia y aislada | **Compartida** con los demás hilos del proceso (solo la pila es propia) |
| **Coste de crearlo** | Alto: el SO reserva memoria, crea el PCB… En Java, arrancar otra JVM tarda décimas de segundo. | Bajo: microsegundos |
| **Comunicación** | Necesita mecanismos del SO (tuberías, ficheros, sockets) | Directa, a través de variables compartidas |
| **Si falla** | No afecta a los demás procesos | Puede hacer caer todo el proceso |
| **Quién lo ejecuta** | La CPU ejecuta los hilos del proceso | Es la unidad que realmente ejecuta la CPU |

!!! note "¿Procesos o hilos?"
    Se usan **procesos** cuando queremos **aislamiento** (que un fallo no tumbe al resto) o ejecutar **otro programa**. Se usan **hilos** cuando queremos hacer varias cosas dentro del mismo programa compartiendo datos de forma rápida. Los hilos se estudian a fondo en el Tema 2.

## Preguntas de repaso

1. ¿Qué diferencia hay entre un programa y un proceso? Pon un ejemplo con una aplicación que uses a diario.
2. ¿Qué cuatro zonas tiene la memoria de un proceso? ¿En cuál se guarda un objeto creado con `new`?
3. ¿Para qué sirve el contador de programa del PCB?
4. Si cierras la terminal desde la que has lanzado un programa con `nohup`, ¿qué tipo de proceso queda? ¿Quién pasa a ser su padre?
5. ¿Por qué un servicio no tiene ventana? ¿Cómo lo reiniciarías en tu sistema operativo?
6. Indica dos ventajas de los hilos frente a los procesos y una ventaja de los procesos frente a los hilos.
