"""
Hook de MkDocs: oculta temas y páginas que todavía no se han publicado.

Lo que se oculta se indica en mkdocs.yml, en `extra.ocultos`. Cada entrada puede ser:
  - una carpeta (oculta todas sus páginas):   temas/tema-2
  - una página concreta:                      temas/tema-1/practica.md

    extra:
      ocultos:
        - temas/tema-1/practica.md
        - temas/tema-2
        - temas/tema-3

Para PUBLICAR algo, comenta su línea con # (o bórrala) y vuelve a construir la web.

Qué hace con lo oculto:
  1. Lo quita de la navegación.
  2. No genera su HTML: no se puede abrir aunque se conozca la URL
     y no aparece en el buscador.
  3. Elimina de las demás páginas cualquier texto que lo mencione, si ese texto
     está marcado así en el Markdown:

        <!-- si-visible: temas/tema-1/practica.md -->
        Texto que solo aparece si la práctica está publicada.
        <!-- fin -->

        <!-- si-oculto: temas/tema-1/practica.md -->
        Texto alternativo que aparece mientras la práctica esté oculta.
        <!-- fin -->

     Las marcas se eliminan siempre antes de generar el HTML, así que no
     quedan ni siquiera como comentarios en el código fuente de la página.

Para ver la web completa en local (profesorado):
    PSP_MOSTRAR_TODO=1 mkdocs serve
"""

import logging
import os
import re

log = logging.getLogger("mkdocs.hooks.ocultar_temas")

_BLOQUE = re.compile(
    r"^[ \t]*<!--\s*si-(visible|oculto):\s*(\S+)\s*-->[ \t]*\n(.*?)^[ \t]*<!--\s*fin\s*-->[ \t]*\n?",
    re.DOTALL | re.MULTILINE,
)


def _ocultos(config):
    if os.environ.get("PSP_MOSTRAR_TODO") == "1":
        return []
    extra = config.get("extra", {}) or {}
    entradas = (extra.get("ocultos") or []) + (extra.get("temas_ocultos") or [])
    return [e.strip().strip("/") for e in entradas if e and e.strip()]


def _es_oculto(ruta, ocultos):
    ruta = ruta.replace("\\", "/").strip("/")
    for o in ocultos:
        if o.endswith(".md"):
            if ruta == o:
                return True
        elif ruta == o or ruta.startswith(o + "/"):
            return True
    return False


def _filtrar_nav(items, ocultos):
    resultado = []
    for item in items:
        if isinstance(item, str):
            if not _es_oculto(item, ocultos):
                resultado.append(item)
        elif isinstance(item, dict):
            titulo, valor = next(iter(item.items()))
            if isinstance(valor, list):
                hijos = _filtrar_nav(valor, ocultos)
                if hijos:                      # una sección vacía desaparece
                    resultado.append({titulo: hijos})
            elif isinstance(valor, str) and not _es_oculto(valor, ocultos):
                resultado.append(item)
    return resultado


def on_config(config, **kwargs):
    ocultos = _ocultos(config)
    if ocultos and config.get("nav"):
        config["nav"] = _filtrar_nav(config["nav"], ocultos)
        log.info("Ocultos: %s", ", ".join(ocultos))
    return config


def on_files(files, config, **kwargs):
    ocultos = _ocultos(config)
    for f in list(files):
        if f.src_uri.endswith(".md") and _es_oculto(f.src_uri, ocultos):
            files.remove(f)
    return files


def on_page_markdown(markdown, page, config, files, **kwargs):
    ocultos = _ocultos(config)

    def sustituir(m):
        tipo, ruta, contenido = m.group(1), m.group(2), m.group(3)
        oculto = _es_oculto(ruta, ocultos)
        mostrar = (tipo == "visible" and not oculto) or (tipo == "oculto" and oculto)
        return contenido if mostrar else ""

    return _BLOQUE.sub(sustituir, markdown)
