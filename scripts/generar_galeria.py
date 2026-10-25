#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_galeria.py — Genera la galería (index.html de la raíz) desde assets/benchmark.json.

Sustituye al paso manual «reinyectar el array DATA en index.html» (CLAUDE.md): ahora la galería
entera —tarjetas, podio, cifras, JSON-LD y metas— sale de los datos, y ninguna cifra se escribe a mano.

  Lee      assets/benchmark.json · docs/rubric.md · docs/methodology.md (vía el build del manual)
           docs/Manual_Marca_UniversoArena/v1.0 (paleta, el Sol, el logotipo y la órbita de la portada)
  Escribe  index.html                                      la galería (abre con doble clic: sin fetch)
           assets/hub/fichas.js                            los datos de las fichas (se cargan al abrir una)
           assets/hub/previews/<carpeta>-{480,800}.webp    capturas a la medida de la tarjeta
           assets/hub/carteles/trampas-{640,960,1280}.webp la parada 04: la órbita del manual, no una IA
           assets/og-universo-arena-v1.png                 imagen para compartir (1200 × 630)

Las carpetas de las entregas NO se tocan: son los resultados del experimento.
La galería no lleva scripts en línea: las tarjetas están en el HTML, los datos de las fichas en
assets/hub/fichas.js (un <script>, no un fetch: sigue abriendo con doble clic) y el comportamiento en
assets/hub/galeria.js, para que la portada admita una CSP sin 'unsafe-inline'. Salida determinista.

Uso:  python3 -B scripts/generar_galeria.py        (desde cualquier carpeta)
      Antes, si cambió la marca: python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/build_v1.py
"""
import html
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
MANUAL = REPO / "docs" / "Manual_Marca_UniversoArena" / "v1.0"
SITIO = "https://universo-arena.alexanderoviedofadul.dev"
GITHUB = "https://github.com/alexanderoviedofadul/Universo-Arena"
OG = "assets/og-universo-arena-v1.png"     # cambia de nombre con cada versión: las redes la guardan por URL

_spec = importlib.util.spec_from_file_location("marca", MANUAL / "scripts" / "build_v1.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

BENCH, DATOS, RUBRICA, TIERS = M.BENCH, M.DATOS, M.RUBRICA, M.TIERS
hexa = M.hexa


def esc(s):
    return html.escape(str(s), quote=True)


# Claves de scores en el mismo orden que la tabla de docs/rubric.md (el audit lo comprueba)
CLAVES = list(BENCH[0]["scores"].keys())
CATS = [(k, c["nombre"], c["max"]) for k, c in zip(CLAVES, RUBRICA)]
CORTO = {"completitudEscena": "Escena", "fidelidadOrbital": "Órbitas", "cometaHalley": "Halley", "esteticaWow": "Estética",
         "panelUI": "Panel UI", "camaraControles": "Cámara", "postProcesado": "Post-pro", "rendimiento": "Rendimiento",
         "robustez": "Robustez", "calidadCodigo": "Código"}
FEATS = [("orbitasElipticas", "Órbitas elípticas"), ("colaOpuestaAlSol", "Cola lejos del Sol"), ("cinturonAsteroides", "Cinturón"),
         ("instanciasAsteroides", "Instancing"), ("saturnoAnillos", "Anillos de Saturno"), ("plutonEnano", "Plutón"),
         ("estrellas3000", "3000+ estrellas"), ("nebulosas", "Nebulosas"), ("bloomGlow", "Bloom/Glow"),
         ("panelCompleto", "Panel completo"), ("vistasCamara", "Vistas de cámara"), ("deltaTime", "deltaTime")]
N = len(BENCH)
COLA_BIEN = sum(1 for b in BENCH if b["features"].get("colaOpuestaAlSol"))
INSTANCING = sum(1 for b in BENCH if b["features"].get("instanciasAsteroides"))
EMPATADOS = [b for b in BENCH if b["total"] == BENCH[0]["total"]]
DESCRIPCION = (f"Un mismo prompt, {N} combinaciones de LLM + agente de código. Benchmark abierto de simulaciones 3D "
               "del Sistema Solar con BabylonJS, juzgado por ejecución real.")
TITULO = "Universo-Arena · Benchmark de LLMs + Agentes de Código"


def lista_nombres(bs):
    n = [f"{b['modelo']} · {b['agente']}" for b in bs]
    return n[0] if len(n) == 1 else ", ".join(n[:-1]) + " y " + n[-1]


# ─────────────────────────────────────────────────────────────────────────────
# Imágenes derivadas
# ─────────────────────────────────────────────────────────────────────────────

def previews():
    dst = REPO / "assets" / "hub" / "previews"
    dst.mkdir(parents=True, exist_ok=True)
    for b in BENCH:
        src = REPO / b["preview"]
        for w in (480, 800):
            out = dst / f"{b['folder']}-{w}.webp"
            if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
                continue
            im = Image.open(src).convert("RGB")
            im.resize((w, round(w * im.height / im.width)), Image.LANCZOS).save(out, "WEBP", quality=70, method=6)
    vivos = {f"{b['folder']}-{w}.webp" for b in BENCH for w in (480, 800)}
    for p in dst.glob("*.webp"):
        if p.name not in vivos:
            p.unlink()


def rsvg(svg_txt, png, w, h):
    tmp = png.with_suffix(".svg")
    tmp.write_text(svg_txt, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", str(png), str(tmp)], check=True)
    tmp.unlink()


def cartel_trampas():
    """La parada de las dos trampas lleva la órbita del manual (el Sol en el foco y la cola lejos del
    Sol), dibujada por el código: una imagen generada por IA no garantiza la física (la que se pidió
    puso la cola hacia el Sol)."""
    M._contador_port["n"] = 0
    svg = M.portada_html(en_capas=False).replace('class="grafica" ', 'xmlns="http://www.w3.org/2000/svg" ', 1)
    svg = re.sub(r' width="100%" height="100%"', ' width="1600" height="900"', svg, count=1)
    dst = REPO / "assets" / "hub" / "carteles"
    png = dst / "trampas.png"
    rsvg(svg, png, 1280, 720)
    im = Image.open(png).convert("RGB")
    for w in (640, 960, 1280):
        im.resize((w, round(w * 9 / 16)), Image.LANCZOS).save(dst / f"trampas-{w}.webp", "WEBP", quality=74, method=6)
    png.unlink()


def imagen_og():
    """1200 × 630: la órbita del manual, el logotipo y el titular en curvas (no depende de fuentes)."""
    M._contador_port["n"] = 0
    fondo = M.portada_html(en_capas=False)
    fondo = fondo.replace('<svg class="grafica" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" aria-hidden="true">',
                          '<svg x="0" y="0" width="1200" height="630" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">', 1)
    logo = (MANUAL / "assets" / "logos" / "ua-horizontal-negativo.svg").read_text(encoding="utf-8")
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', logo)
    lw, lh = float(vb.group(1)), float(vb.group(2))
    alto_logo = 64
    logo = logo.replace("<svg ", f'<svg x="64" y="60" width="{lw * alto_logo / lh:.0f}" height="{alto_logo}" ', 1)
    estelar, polvo = hexa("ua-estelar"), hexa("ua-polvo")
    t1, _, _ = M.texto_trazado(f"Un prompt. {N} universos.", 800, 64, -1.3, 64, 260)
    t2, _, _ = M.texto_trazado("Benchmark abierto de LLM + agente de código,", 500, 30, 0, 64, 320)
    t3, _, _ = M.texto_trazado("juzgado por ejecución real.", 500, 30, 0, 64, 360)
    t4, _, _ = M.texto_trazado("universo-arena.alexanderoviedofadul.dev", 600, 22, 0, 64, 570)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">{fondo}'
           f'<defs><linearGradient id="og-velo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{hexa("ua-vacio")}" stop-opacity=".75"/>'
           f'<stop offset=".55" stop-color="{hexa("ua-vacio")}" stop-opacity=".45"/><stop offset=".8" stop-color="{hexa("ua-vacio")}" stop-opacity="0"/></linearGradient></defs>'
           f'<rect width="1200" height="630" fill="url(#og-velo)"/>{logo}'
           f'<path d="{t1}" fill="{estelar}"/><path d="{t2} {t3}" fill="{polvo}"/><path d="{t4}" fill="{hexa("ua-orbita")}"/></svg>')
    png = REPO / OG
    rsvg(svg, png, 1200, 630)
    im = Image.open(png).convert("RGB")
    im.save(png, "PNG", optimize=True)


# ─────────────────────────────────────────────────────────────────────────────
# Piezas de la página
# ─────────────────────────────────────────────────────────────────────────────

TIER_VAR = {t: f"var(--{M.TIER_COLOR[t]})" for t in "SABCD"}
PIXEL = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


def img_preview(b, clase, sizes, eager=False):
    f = b["folder"]
    carga = 'loading="eager" fetchpriority="low"' if eager else 'loading="lazy"'
    return (f'<img class="{clase}" src="assets/hub/previews/{esc(f)}-480.webp" '
            f'srcset="assets/hub/previews/{esc(f)}-480.webp 480w, assets/hub/previews/{esc(f)}-800.webp 800w" sizes="{sizes}" '
            f'width="480" height="302" alt="Captura de la simulación de {esc(b["modelo"])} con {esc(b["agente"])}" {carga} decoding="async">')


def errores(b):
    n = b["runtime"]["consoleErrors"]
    return '<span class="ok">✓ 0 errores</span>' if n == 0 else f'<span class="aviso">⚠ {n} error{"es" if n > 1 else ""}</span>'


def tarjeta(b):
    f = b["folder"]
    attrs = " ".join(f'data-{k.lower()}="{b["scores"][k]}"' for k in ("esteticaWow", "panelUI", "fidelidadOrbital", "rendimiento"))
    return (f'<article class="tarjeta" style="--c:{esc(b["color"])};--tc:{TIER_VAR[b["tier"]]}" data-folder="{esc(f)}" data-tier="{b["tier"]}" '
            f'data-total="{b["total"]}" data-rank="{b["rank"]}" {attrs}>'
            f'<div class="t-foto">{img_preview(b, "t-img", "(min-width: 1100px) 380px, (min-width: 700px) 46vw, 92vw")}'
            f'<span class="t-rank"><span class="sr">Puesto </span>{b["rank"]}</span><span class="t-tier">Tier {b["tier"]}</span>'
            f'<span class="t-nota" style="--p:{b["total"]}"><b>{b["total"]}</b><small>/100</small></span></div>'
            f'<div class="t-cuerpo"><h3 class="t-modelo">{esc(b["modelo"])}</h3><p class="t-agente"><span class="t-punto" aria-hidden="true"></span>{esc(b["agente"])}</p>'
            f'<p class="t-meta"><span><b>{b["runtime"]["meshes"]}</b> objetos</span><span><b>{b["lineas"]}</b> líneas</span>{errores(b)}</p>'
            f'<p class="t-veredicto">{esc(b["veredicto"])}</p>'
            f'<p class="t-acciones"><button type="button" class="btn btn-borde" data-ficha="{esc(f)}" hidden>Ver ficha</button>'
            f'<a class="btn btn-sol" href="{esc(f)}/index.html" target="_blank" rel="noopener">▶ Abrir demo<span class="sr"> de {esc(b["modelo"])} con {esc(b["agente"])} (nueva pestaña)</span></a></p></div></article>')


def podio():
    medallas = {1: "Primer puesto", 2: "Segundo puesto", 3: "Tercer puesto"}
    orden = [BENCH[1], BENCH[0], BENCH[2]]
    out = []
    for b in orden:
        out.append(f'<li class="podio-{b["rank"]}" style="--c:{esc(b["color"])}"><div class="p-foto">{img_preview(b, "p-img", "(min-width: 900px) 360px, 92vw")}'
                   f'<span class="p-puesto">{b["rank"]}</span></div><div class="p-cuerpo"><p class="p-medalla">{medallas[b["rank"]]}</p>'
                   f'<h3>{esc(b["modelo"])}</h3><p class="p-agente">{esc(b["agente"])}</p><p class="p-nota"><b>{b["total"]}</b>/100 · tier {b["tier"]}</p>'
                   f'<p class="p-acciones"><button type="button" class="btn btn-borde" data-ficha="{esc(b["folder"])}" hidden>Ver ficha</button>'
                   f'<a class="btn btn-sol" href="{esc(b["folder"])}/index.html" target="_blank" rel="noopener">▶ Demo<span class="sr"> de {esc(b["modelo"])} (nueva pestaña)</span></a></p></div></li>')
    return '<ol class="podio-lista">' + "".join(out) + "</ol>"


def stats_hero():
    filas = [(DATOS["entregas"], "entregas"), (str(len(RUBRICA)), "criterios"), (DATOS["limpias"], "sin errores de consola"), (DATOS["media"], "nota media")]
    return '<dl class="cifras">' + "".join(f'<div><dt>{esc(l)}</dt><dd>{esc(v)}</dd></div>' for v, l in filas) + "</dl>"


def cartel(nombre, primero=False):
    srcset = ", ".join(f"assets/hub/carteles/{nombre}-{w}.webp {w}w" for w in (640, 960, 1280))
    # src = GIF transparente de 1 px (W3C exige src; galeria.js pone el real al acercarse) y data-sizes (sizes sin
    # srcset tampoco es válido). Kit «confianza y recorrido», 25-oct-2026.
    img = (f'<img src="{PIXEL}" data-src="assets/hub/carteles/{nombre}-1280.webp" data-srcset="{srcset}" data-sizes="(min-aspect-ratio: 16/9) 100vw, 178vh" '
           'alt="" width="1280" height="720" decoding="async">')
    ns = (f'<noscript><img src="assets/hub/carteles/{nombre}-1280.webp" alt="" width="1280" height="720"></noscript>' if primero else "")
    clase = "frame" if primero else "frame frame-diferido"
    estilo = "" if primero else ' style="opacity:0"'
    return f'<div class="{clase}" data-frame{estilo}>{img}{ns}</div>'


PARADAS = [
    ("reto", "El reto", "50", "01", "Un prompt, una sola pasada",
     f'<p>Cada combinación de modelo y agente recibe el mismo <a href="Prompt-Maestro_v2.txt">Prompt-Maestro_v2.txt</a>: una simulación 3D del Sistema Solar con BabylonJS, en un único <code>index.html</code> que se abre con doble clic, sin servidor ni assets locales.</p>'
     '<p class="chips"><span class="sr">Lo que pide: </span><span>Sol con corona</span><span>8 planetas + Plutón</span><span>Cometa Halley</span><span>Cinturón 200+</span><span>3000+ estrellas</span><span>Panel de 4 secciones</span></p>'),
    ("rubrica", "La rúbrica", "50", "02", f"{DATOS['puntos']} puntos en {len(RUBRICA)} categorías",
     '<p>Un jurado por entrega lee el archivo completo y el reto, y puntúa verificando el código, no los comentarios.</p>'
     '<p class="chips"><span class="sr">Categorías: </span>' + "".join(f'<span>{esc(n)} <b>{m}</b></span>' for _, n, m in CATS) + "</p>"),
    ("ejecucion", "La ejecución", "70", "03", "Juzgado por lo que hace al abrirse",
     f'<p>Cada entrega se abre en Chrome sin pantalla (WebGL por SwiftShader): se captura lo que se ve y se cuentan los objetos en escena, los FPS y los errores de consola. <b>{esc(DATOS["limpias"])}</b> abren sin un solo error.</p>'),
    ("trampas", "Las dos trampas", "75", "04", "El Sol en el foco y la cola lejos del Sol",
     '<p>Casi todas se ven bien. Lo que separó a las mejores: el Sol en el <b>foco</b> de la elipse, no en el centro, y la cola del cometa en el sentido <code>cometa − Sol</code>, recalculada en cada fotograma.</p>'
     f'<p class="formula"><code>x = a·cosθ − a·e</code><code>z = b·sinθ</code></p><p>{COLA_BIEN} de {N} entregas apuntan bien la cola.</p>'),
    ("calibracion", "La calibración", "50", "05", "Donde el código y la ejecución discrepan, manda la ejecución",
     '<p>Un juez normaliza las notas entre jurados. Una revisión estática declaró «pantalla negra» a una entrega que, al abrirla, tenía 279 objetos y 0 errores: su nota pasó de 38 a 89. Y en los empates de cabeza, las entradas del mismo sistema que ejecuta el benchmark van por debajo.</p>'),
]


def recorrido():
    frames = "".join(cartel(p[0], i == 0) for i, p in enumerate(PARADAS))
    rail = "".join(f'<li><a href="#{p[0]}" data-goto aria-current="{"true" if i == 0 else "false"}"><span class="rail-label">{esc(p[1])}</span><span class="rail-dot"></span></a></li>'
                   for i, p in enumerate(PARADAS))
    stops = "".join(
        f'<article id="{p[0]}" class="stop" data-stop data-focus="{p[2]}"><div class="stop-body">'
        f'<p class="stop-num"><span>{p[3]} / {len(PARADAS):02d}</span><span class="stop-dot" aria-hidden="true"></span><span>{esc(p[1])}</span></p>'
        f'<h3>{esc(p[4])}</h3>{p[5]}</div></article>' for p in PARADAS)
    return (f'<section id="recorrido" class="world" data-world aria-labelledby="recorrido-tit"><h2 id="recorrido-tit" class="sr">Cómo se mide</h2>'
            f'<div class="stage" data-stage><div class="frames" aria-hidden="true">{frames}</div>'
            '<div class="velo velo-arriba" aria-hidden="true"></div><div class="velo velo-lado" aria-hidden="true"></div>'
            f'<nav class="rail" aria-label="Paradas del recorrido"><ol>{rail}</ol><span class="rail-linea" aria-hidden="true"><span data-rail-fill></span></span></nav></div>'
            f'<div class="stops">{stops}</div></section>')


def hero():
    M._contador_port["n"] = 0
    capas = M.capas_portada()
    pre = "h-"
    svgs = "".join(f'<svg class="hero-capa" data-capa="{z}" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{c.replace("PORT-", pre)}</svg>'
                   for n, z, c in capas)
    return ('<section class="hero" data-hero aria-labelledby="hero-tit"><div class="hero-fondo" aria-hidden="true">' + svgs + "</div>"
            '<div class="hero-texto" data-hero-texto><p class="eyebrow">Benchmark abierto · LLM + agente de código</p>'
            f'<h1 id="hero-tit">Un prompt.<br><span class="sol-texto">{N} universos.</span></h1>'
            '<p class="hero-sub">Distintos modelos y agentes de código recibieron el mismo reto: construir, en una sola pasada, el Sistema Solar en 3D con BabylonJS. '
            'Aquí está lo que entregaron, y cómo se midió.</p>'
            f'{stats_hero()}<p class="hero-acciones"><a class="btn btn-sol" href="#podio">Ver el ranking</a><a class="btn btn-borde" href="#galeria">Explorar las {N} entregas</a></p>'
            '<p class="hero-guia"><a href="conozca/">¿Primera vez aquí? Haz el recorrido guiado</a></p></div>'
            '<p class="hero-sigue" aria-hidden="true" data-hint>Desliza</p></section>')


def chips():
    orden = [("total", "Por puntuación")] + [(k, CORTO[k]) for k in ("esteticaWow", "panelUI", "fidelidadOrbital", "rendimiento")]
    tiers = [("todos", "Todos")] + [(t, t) for t, _ in TIERS]
    return ('<div class="barra" hidden data-barra><div class="grupo" role="group" aria-label="Ordenar por">'
            + "".join(f'<button type="button" class="chip" data-orden="{k}" aria-pressed="{"true" if k == "total" else "false"}">{esc(n)}</button>' for k, n in orden)
            + '</div><div class="grupo" role="group" aria-label="Filtrar por tier">'
            + "".join(f'<button type="button" class="chip" data-filtro="{k}" aria-pressed="{"true" if k == "todos" else "false"}">{"Tier " + n if k != "todos" else n}</button>' for k, n in tiers)
            + '</div><p class="contador" aria-live="polite" data-contador></p></div>')


def hallazgos():
    grupos = DATOS
    items = [
        ("La cola del cometa", f"El fallo que más separó: el vector «lejos del Sol» es cometa − Sol. Muchas lo invirtieron y la cola acabó apuntando hacia el Sol. Hoy {COLA_BIEN} de {N} lo aciertan."),
        ("El Sol en el foco", "Una elipse con el Sol centrado parece correcta, pero es física falsa. Las de cabeza lo pusieron en el foco: x = a·cosθ − a·e."),
        ("Instancing", f"Doscientos asteroides piden createInstance. {INSTANCING} de {N} lo usan; el resto crea cientos de mallas sueltas y lo paga en FPS."),
        ("El agente pesa tanto como el modelo", f"{grupos['dispersion_modelo']} aparece con {grupos['dispersion_n']} agentes y sus notas van de {grupos['dispersion_rango']}: {grupos['dispersion']} puntos con el mismo modelo base."),
        ("Verificar la documentación", "Quienes no consultaron la documentación de BabylonJS inventaron APIs (emissionRange, mesh.diameter) que se tradujeron en fallos visibles."),
        ("El juez alucina; el runtime corrige", "Una revisión estática declaró rota una entrega que funcionaba con 279 objetos y 0 errores. Sin ejecución real, un benchmark de agentes no es fiable."),
    ]
    return '<ul class="hallazgos">' + "".join(f'<li data-reveal><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for t, x in items) + "</ul>"


def estado():
    filas = [(DATOS["arrancan"], "entregas arrancan y pintan una escena WebGL compleja en una sola pasada"),
             (DATOS["limpias"], "abren sin un solo error de consola en un navegador real"),
             (DATOS["lineas_media"], "líneas de media por entrega, todo en un único archivo"),
             (DATOS["empatados"], f"entregas empatadas arriba con {DATOS['cima']}: {lista_nombres(EMPATADOS)}")]
    return '<dl class="estado">' + "".join(f'<div data-reveal><dt>{esc(l)}</dt><dd>{esc(v)}</dd></div>' for v, l in filas) + "</dl>"


def metodo():
    senales = "".join(f'<li data-reveal style="--c:var(--{s["color"]})"><span class="m-n">{esc(s["n"])}</span><h3>{esc(s["nombre"])}</h3><p class="m-que">{esc(s["que"])}</p><p>{esc(s["texto"])}</p></li>'
                      for s in M.ARENA["senales"])
    lectura = dict(M.ARENA["tiers_lectura"])
    filas = "".join(f'<tr><th scope="row"><span class="tier-chip" style="--tc:{TIER_VAR[t]}">Tier {t}</span></th><td>{esc(r)}</td><td>{esc(lectura[t])}</td>'
                    f'<td class="num">{sum(1 for b in BENCH if b["tier"] == t)}</td></tr>' for t, r in TIERS)
    docs = [("methodology.md", "Metodología"), ("rubric.md", "Rúbrica"), ("harness.md", "El arnés"), ("results.md", "Fichas por entrega"),
            ("conclusions.md", "Conclusiones"), ("contributing.md", "Cómo añadir una entrega")]
    enlaces = ('<li><a href="conozca/">Recorrido guiado</a></li>'
               + "".join(f'<li><a href="{GITHUB}/blob/main/docs/{d}" target="_blank" rel="noopener">{esc(n)}<span class="sr"> (GitHub, nueva pestaña)</span></a></li>' for d, n in docs))
    return (f'<ol class="senales">{senales}</ol>'
            '<div class="tabla-envoltura" tabindex="0" role="region" aria-label="Tabla de tiers, desplazable" data-reveal><table class="tiers"><caption class="sr">Tiers y número de entregas</caption>'
            f'<thead><tr><th scope="col">Tier</th><th scope="col">Nota</th><th scope="col">Lectura</th><th scope="col" class="num">Entregas</th></tr></thead><tbody>{filas}</tbody></table></div>'
            f'<ul class="docs" data-reveal>{enlaces}</ul>')


PREGUNTAS = [
    ("¿Qué es Universo-Arena?", f"Un benchmark abierto donde {N} combinaciones de LLM + agente de código implementan el mismo reto: una simulación 3D del Sistema Solar en BabylonJS, como un único index.html autocontenido. Cada entrega se puntúa con una rúbrica de {DATOS['puntos']} puntos y se ejecuta en un navegador real."),
    ("¿Qué combinación obtuvo la mejor puntuación?", f"{lista_nombres(EMPATADOS)} empatan en cabeza con {DATOS['cima']}/100 (tier S). En los empates, las entradas hechas por el mismo sistema que ejecuta el benchmark van por debajo."),
    ("¿Cómo se evalúa cada entrega?", f"Con tres señales: una rúbrica de {len(RUBRICA)} categorías ({DATOS['puntos']} puntos), la ejecución real en Chrome sin pantalla —objetos 3D, FPS y errores de consola— y una calibración que, cuando la lectura del código y la ejecución discrepan, se queda con la ejecución."),
    ("¿El benchmark es reproducible y de código abierto?", "Sí, con licencia MIT: el código de cada entrega y los datos crudos (benchmark.json y runtime.json) están en GitHub, y el arnés de captura está documentado en docs/harness.md. El script del arnés no vive en el repositorio."),
]


def faq():
    return '<div class="faq">' + "".join(f'<details data-reveal><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in PREGUNTAS) + "</div>"


def seguridad():
    """«Seguridad comprobada» (kit «confianza y recorrido», 25-oct-2026). Sin cifras: sc-seguridad.js pinta lo que lee de
    /salud-publica/publico.json (solo lo publicable que mide el servidor). Sin nada publicable, la sección se quita sola
    (data-sc-quitar); por file:// tampoco aparece."""
    return ('<section id="seguridad-comprobada" class="bloque sc" data-sc data-sc-quitar aria-labelledby="sc-titulo">'
            '<div class="envoltura"><p class="eyebrow">Seguridad comprobada</p><h2 id="sc-titulo">No te pedimos que nos creas: compruébalo</h2>'
            '<p class="entrada">Herramientas públicas e independientes revisan este sitio: el cifrado de la conexión, las protecciones del navegador, '
            'el código y la accesibilidad. Aquí está lo que dicen, con la fecha de la medición, una captura real del informe y el enlace para que lo verifiques en la fuente.</p>'
            '<div class="sc-resumen" data-sc-resumen hidden></div><div data-sc-lista></div>'
            '<p class="sc-nota-pie">Aquí solo aparecen las verificaciones con la calificación más alta. Se vuelven a medir de forma automática; '
            'si un resultado deja de cumplir, sale de esta sección hasta que se corrige. En las capturas se omite la dirección del servidor. '
            'Para reportar una vulnerabilidad: <a href="/.well-known/security.txt">security.txt</a>.</p></div></section>')


def json_ld():
    url = SITIO + "/"
    grafo = [
        {"@type": "WebSite", "@id": url + "#website", "url": url, "name": "Universo-Arena", "description": DESCRIPCION, "inLanguage": "es",
         "publisher": {"@type": "Person", "name": "Alexander Oviedo Fadul", "url": "https://alexanderoviedofadul.dev"}},
        {"@type": "Dataset", "@id": url + "#dataset", "name": "Universo-Arena · Benchmark LLM + Agente de Código",
         "description": (f"Benchmark abierto: {N} combinaciones de LLM y agente de código implementan el mismo reto (una simulación 3D del Sistema Solar "
                         f"en BabylonJS, un único index.html autocontenido) y se puntúan con una rúbrica de {DATOS['puntos']} puntos, ejecución real en navegador y calibración."),
         "url": url, "license": "https://opensource.org/licenses/MIT",
         "creator": {"@type": "Person", "name": "Alexander Oviedo Fadul", "url": "https://alexanderoviedofadul.dev"}, "inLanguage": "es", "isAccessibleForFree": True,
         "keywords": ["benchmark LLM", "agentes de código", "BabylonJS", "Sistema Solar 3D", "evaluación de modelos de IA", "WebGL"],
         "variableMeasured": ["puntuación total (0-100)", "tier", "errores de consola", "número de objetos 3D", "FPS"],
         "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITIO}/assets/{n}"} for n in ("benchmark.json", "runtime.json")]},
        {"@type": "ItemList", "name": "Ranking Universo-Arena · LLM + Agente de Código", "description": f"Clasificación de {N} entregas (LLM + agente) por puntuación total.",
         "numberOfItems": N, "itemListOrder": "https://schema.org/ItemListOrderDescending",
         "itemListElement": [{"@type": "ListItem", "position": b["rank"], "name": f"{b['modelo']} · {b['agente']}", "url": f"{SITIO}/{b['folder']}/index.html"} for b in BENCH]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PREGUNTAS]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def datos_ficha():
    """Lo que necesita la ficha (no las tarjetas, que ya están en el HTML)."""
    d = {"cats": [[k, CORTO[k], m] for k, _, m in CATS], "feats": FEATS,
         "entregas": {b["folder"]: {k: b[k] for k in ("modelo", "agente", "color", "total", "tier", "rank", "lineas", "scores", "features", "fortalezas", "debilidades", "veredicto")}
                      | {"objetos": b["runtime"]["meshes"], "errores": b["runtime"]["consoleErrors"], "fps": b["runtime"]["fps"]} for b in BENCH}}
    return json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def pagina():
    logo_neg = "assets/marca/logos/ua-horizontal-negativo.svg"
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', (REPO / logo_neg).read_text(encoding="utf-8"))
    lw = round(float(vb.group(1)) * 30 / float(vb.group(2)))
    nav = [("recorrido", "Cómo se mide"), ("podio", "Podio"), ("galeria", "Galería"), ("hallazgos", "Hallazgos"), ("metodo", "Método")]
    navh = "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in nav)
    tarjetas = "".join(tarjeta(b) for b in BENCH)
    return f"""<!DOCTYPE html>
<!-- GENERADO por scripts/generar_galeria.py desde assets/benchmark.json y el Manual de Marca v1.0 — no editar a mano. -->
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(TITULO)}</title>
<meta name="description" content="{esc(DESCRIPCION)}">
<link rel="canonical" href="{SITIO}/">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta name="author" content="Alexander Oviedo Fadul">
<meta name="theme-color" content="{hexa('ua-vacio')}">
<meta name="color-scheme" content="dark">
<link rel="icon" href="assets/marca/logos/ua-simbolo.svg" type="image/svg+xml">
<link rel="icon" href="assets/marca/logos/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/marca/logos/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Universo-Arena">
<meta property="og:locale" content="es_ES">
<meta property="og:url" content="{SITIO}/">
<meta property="og:title" content="{esc(TITULO)}">
<meta property="og:description" content="{esc(DESCRIPCION)}">
<meta property="og:image" content="{SITIO}/{OG}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Universo-Arena: un prompt, {N} universos. El Sol en el foco de una órbita elíptica y un cometa con la cola lejos del Sol.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITULO)}">
<meta name="twitter:description" content="{esc(DESCRIPCION)}">
<meta name="twitter:image" content="{SITIO}/{OG}">
<link rel="alternate" type="text/plain" href="{SITIO}/llms.txt" title="llms.txt">
<link rel="sitemap" type="application/xml" href="{SITIO}/sitemap.xml">
<link rel="preload" href="assets/marca/fuentes/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/marca/tokens-v1.css">
<link rel="stylesheet" href="assets/hub/galeria.css">
<link rel="stylesheet" href="kit-confianza/sc-seguridad.css">
<script type="application/ld+json">{json_ld()}</script>
<script src="assets/hub/galeria.js" defer></script>
<script src="kit-confianza/sc-seguridad.js" defer></script>
</head>
<body>
<a class="saltar" href="#principal">Saltar al contenido</a>
<header class="cab" data-cab>
  <a class="cab-marca" href="#principal" aria-label="Universo-Arena, inicio"><img src="{logo_neg}" width="{lw}" height="30" alt="Universo-Arena"></a>
  <nav class="cab-nav" aria-label="Principal"><ul>{navh}</ul></nav>
  <a class="cab-gh" href="{GITHUB}" target="_blank" rel="noopener">GitHub<span class="sr"> (nueva pestaña)</span></a>
</header>
<main id="principal" tabindex="-1">
{hero()}
{recorrido()}
<section id="podio" class="bloque" aria-labelledby="podio-tit">
  <div class="envoltura"><p class="eyebrow" data-reveal>El podio</p><h2 id="podio-tit" data-reveal>Los tres mejores universos</h2>
  <p class="entrada" data-reveal>Nota sobre {DATOS['puntos']} con la rúbrica, contrastada con la ejecución real. {esc(lista_nombres(EMPATADOS))} empatan con {DATOS['cima']}; el orden sigue la regla contra el auto-favoritismo.</p>
  {podio()}</div>
</section>
<section id="galeria" class="bloque" aria-labelledby="galeria-tit">
  <div class="envoltura"><p class="eyebrow" data-reveal>La galería</p><h2 id="galeria-tit" data-reveal>Las {N} entregas</h2>
  <p class="entrada" data-reveal>Cada tarjeta es una combinación de modelo y agente, con la captura real de lo que se ve al abrirla. La ficha trae el desglose por categoría, lo que hizo bien y lo que falló.</p>
  {chips()}
  <div class="rejilla" data-rejilla>{tarjetas}</div></div>
</section>
<section id="hallazgos" class="bloque" aria-labelledby="hallazgos-tit">
  <div class="envoltura"><p class="eyebrow" data-reveal>Hallazgos</p><h2 id="hallazgos-tit" data-reveal>Lo que decidió el benchmark</h2>
  {hallazgos()}
  <h3 class="sub" data-reveal>El estado del arte</h3>
  {estado()}
  <div class="prosa" data-reveal><p>Generar en una sola pasada una experiencia 3D web compleja y autocontenida ha dejado de ser una hazaña: es lo esperable de un agente de código de frontera. La pregunta ya no es «¿puede escribir mil quinientas líneas de WebGL sin una excepción?», sino <strong>«¿acierta los detalles difíciles?»</strong>: que el Sol va en el foco, que un vector tiene sentido, que doscientos objetos piden instancing y que una API se verifica antes de usarla.</p>
  <p>Y una lección sobre cómo medir: el juez que solo lee el código es rápido pero falible. Aquí se juzga por ejecución —abrir la app, contar sus objetos, mirar su consola y capturar lo que se ve—.</p></div></div>
</section>
<section id="metodo" class="bloque" aria-labelledby="metodo-tit">
  <div class="envoltura"><p class="eyebrow" data-reveal>Método</p><h2 id="metodo-tit" data-reveal>Tres señales y cinco tiers</h2>
  {metodo()}
  <h3 class="sub" data-reveal>Preguntas frecuentes</h3>
  {faq()}</div>
</section>
{seguridad()}
</main>
<footer class="pie">
  <div class="envoltura">
    <img src="{logo_neg}" width="{lw}" height="30" alt="Universo-Arena" loading="lazy">
    <p>Reto y curación: Alexander Oviedo Fadul · Licencia MIT · Capturas reales tomadas en Chrome sin pantalla · Datos en <a href="assets/benchmark.json">assets/benchmark.json</a></p>
    <ul class="pie-enlaces">
      <li><a href="Prompt-Maestro_v2.txt">El prompt</a></li>
      <li><a href="{GITHUB}" target="_blank" rel="noopener">Repositorio<span class="sr"> (nueva pestaña)</span></a></li>
      <li><a href="llms.txt">llms.txt</a></li>
      <li><a href="docs/Manual_Marca_UniversoArena/v1.0/index.html">Manual de marca</a></li>
      <li><a href="conozca/">Recorrido guiado</a></li>
      <li><a href="#seguridad-comprobada">Seguridad comprobada</a></li>
      <li><a href="/.well-known/security.txt">Reportar una vulnerabilidad</a></li>
    </ul>
  </div>
</footer>
<dialog class="ficha" data-ficha-dialogo aria-label="Ficha de la entrega"></dialog>
</body>
</html>
"""


def main():
    previews()
    cartel_trampas()
    imagen_og()
    (REPO / "assets" / "hub" / "fichas.js").write_text(
        "/* GENERADO por scripts/generar_galeria.py desde assets/benchmark.json — no editar a mano.\n"
        "   Datos de la ficha de cada entrega. galeria.js lo pide cuando la página está ociosa o al abrir\n"
        "   la primera ficha: así el HTML no carga ~95 KB que solo usa quien abre una. */\n"
        "window.UA_FICHAS = " + datos_ficha() + ";\n", encoding="utf-8")
    (REPO / "index.html").write_text(pagina(), encoding="utf-8")
    p = REPO / "index.html"
    print(f"OK → index.html {p.stat().st_size / 1024:.1f} KB · {N} entregas · previews {len(list((REPO / 'assets/hub/previews').glob('*.webp')))} · {OG}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
