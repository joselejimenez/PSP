# PSP · Web del módulo (MkDocs)

## Ver la web en local

```bash
python3 -m venv .venv
source .venv/bin/activate          # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve                       # web tal como la ve el alumnado
PSP_MOSTRAR_TODO=1 mkdocs serve    # vista del profesorado: todo visible
```

Abre http://127.0.0.1:8000

## Publicar en GitHub Pages

```bash
mkdocs gh-deploy
```

## Ocultar o publicar contenido

En `mkdocs.yml`:

```yaml
extra:
  ocultos:
    - temas/tema-1/practica.md     # Práctica evaluable del Tema 1
    - temas/tema-2                 # Tema 2 completo
    - temas/tema-3                 # Tema 3 completo
```

- Cada línea es algo que **no** ve el alumnado: una carpeta entera o una página concreta.
- Para **publicarlo**, comenta la línea con `#` (o bórrala) y vuelve a desplegar.

El hook `hooks/ocultar_temas.py` hace tres cosas con lo oculto:

1. Lo quita del menú.
2. No genera su página: no se puede abrir por URL ni aparece en el buscador.
3. Borra de las demás páginas los textos que lo mencionan, si están marcados así:

```markdown
<!-- si-visible: temas/tema-1/practica.md -->
Este texto solo aparece cuando la práctica está publicada.
<!-- fin -->

<!-- si-oculto: temas/tema-1/practica.md -->
Este texto aparece mientras la práctica esté oculta.
<!-- fin -->
```

Las marcas se eliminan antes de generar el HTML, así que no quedan ni en el código fuente de la página.

## Versión de MkDocs

`requirements.txt` fija MkDocs 1.x. MkDocs 2.0 elimina el sistema de plugins y hooks, y esta web dejaría de funcionar con esa versión.
