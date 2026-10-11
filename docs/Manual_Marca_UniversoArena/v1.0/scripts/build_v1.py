#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_v1.py — Manual de Marca Universo-Arena v1.0 «El Sol en el foco».

Kit copiado del Manual de Marca Pentest C360 v1.0 (← Isabella EA v2.0 ← Maloca v2.0 ← ENKI v2.0
← KANSA v6.0). Una sola fuente (contenido/*.json + los datos del benchmark) → salidas GENERADAS:

  assets/logos/ua-*.svg|png        el Sol, logotipos y favicons (geometría única, aquí)
  index.html                       recorrido inmersivo (enlaza assets/, abre por file://)
  impresion.html                   páginas A4 apaisadas (fuente del PDF)
  UniversoArena_Inmersivo_v1.html  portable autocontenido (fuentes, CSS, JS e imágenes en línea)
  assets/data/tokens-v1.css · tokens_v1.json   tokens para la web
  ../../../assets/marca/           tokens, woff2 y logos que usa la galería (los copia este build)

El símbolo NO se rediseña: es el Sol de la barra de la galería (`.brand .dot` del index.html
anterior), un círculo con su degradado radial de cuatro paradas, pasado a SVG cota por cota.
El nombre va en Inter 800 con las proporciones de esa barra, en curvas.

Las cifras (entregas, notas, tiers, categorías de la rúbrica) NO se escriben aquí: se leen de
assets/benchmark.json, de docs/rubric.md y de docs/methodology.md. Si cambia el benchmark,
se vuelve a construir y el manual dice lo nuevo.

No editar las salidas a mano. La salida es determinista (semilla fija, sin fechas).
Uso:  python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/build_v1.py   (desde cualquier carpeta)
"""
import base64
import hashlib
import html
import json
import math
import random
import re
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

BASE = Path(__file__).resolve().parent.parent            # .../v1.0
REPO = BASE.parents[2]                                   # raíz del repositorio Universo-Arena
CONTENIDO = BASE / "contenido"
VERSION = "1.0.0"
SELLO_PIE = "Universo-Arena · Manual de Marca v1.0"
PORTABLE = "UniversoArena_Inmersivo_v1.html"

# ─────────────────────────────────────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────────────────────────────────────

def leer(rel):
    return (BASE / rel).read_text(encoding="utf-8")


def esc(s):
    return html.escape(str(s), quote=True)


FUENTES = json.loads(leer("contenido/fuentes.json"))["fuentes"]
NUM_FUENTE = {f["id"]: i + 1 for i, f in enumerate(FUENTES)}
HITOS = json.loads(leer("contenido/hitos.json"))
ARENA = json.loads(leer("contenido/arena.json"))


def inline(s):
    """Texto de contenido → HTML. Admite HTML en línea simple, marcas {f:id} y {d:clave}
    (un dato del benchmark, calculado: ver DATOS)."""
    def cita(m):
        ids = [x.strip() for x in m.group(1).split(",")]
        partes = []
        for i in ids:
            if i not in NUM_FUENTE:
                raise SystemExit(f"Fuente desconocida en el contenido: {i}")
            partes.append(f'<a href="#fuente-{i}">{NUM_FUENTE[i]}</a>')
        return '<sup class="cita">[' + ", ".join(partes) + "]</sup>"

    def dato(m):
        k = m.group(1)
        if k not in DATOS:
            raise SystemExit(f"Dato desconocido en el contenido: {k}")
        return esc(DATOS[k])
    s = re.sub(r"\{d:([a-z0-9_]+)\}", dato, s)
    return re.sub(r"\{f:([a-z0-9,\- ]+)\}", cita, s)


# ─────────────────────────────────────────────────────────────────────────────
# Datos del benchmark: se leen, no se copian
# ─────────────────────────────────────────────────────────────────────────────

BENCH = json.loads((REPO / "assets" / "benchmark.json").read_text(encoding="utf-8"))


def _rubrica():
    """Las 10 categorías y su máximo, de la tabla de docs/rubric.md («| 1 | **Nombre** | 20 | …»)."""
    filas = re.findall(r"^\|\s*(\d+)\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*$",
                       (REPO / "docs" / "rubric.md").read_text(encoding="utf-8"), flags=re.M)
    return [{"n": int(n), "nombre": nom.strip(), "max": int(mx), "que": que.strip()} for n, nom, mx, que in filas]


def _tiers():
    """Los cortes de cada tier, de docs/methodology.md («**S** (≥90) · **A** (82–89) · …»)."""
    txt = (REPO / "docs" / "methodology.md").read_text(encoding="utf-8")
    return re.findall(r"\*\*([SABCD])\*\* \(([^)]+)\)", txt)


RUBRICA = _rubrica()
TIERS = _tiers()


def _base_modelo(m):
    """«GLM 5.2 (Max)» y «Z.ai GLM 5.2» son el mismo modelo base que «GLM 5.2» (así los agrupa el README)."""
    m = re.sub(r"\s*\(.*?\)", "", m)
    return re.sub(r"^Z\.ai\s+", "", m).strip()


def _datos():
    n = len(BENCH)
    totales = [b["total"] for b in BENCH]
    limpias = sum(1 for b in BENCH if b["runtime"]["consoleErrors"] == 0)
    arrancan = sum(1 for b in BENCH if b["runtime"].get("webgl"))
    cima = max(totales)
    empatados = [b for b in BENCH if b["total"] == cima]
    grupos = {}
    for b in BENCH:
        grupos.setdefault(_base_modelo(b["modelo"]), []).append(b["total"])
    amplio = max(((k, v) for k, v in grupos.items() if len(v) > 1), key=lambda kv: max(kv[1]) - min(kv[1]))
    agentes = sorted({b["agente"] for b in BENCH})
    return {
        "entregas": str(n),
        "limpias": f"{limpias}/{n}",
        "arrancan": f"{arrancan}/{n}",
        "media": str(round(sum(totales) / n)),
        "lineas_media": f"{round(sum(b['lineas'] for b in BENCH) / n):,}".replace(",", "."),
        "cima": str(cima),
        "empatados": str(len(empatados)),
        "podio": " · ".join(f"{b['modelo']} ({b['agente']})" for b in BENCH[:3]),
        "categorias": str(len(RUBRICA)),
        "puntos": str(sum(c["max"] for c in RUBRICA)),
        "modelos_base": str(len(grupos)),
        "agentes": str(len(agentes)),
        "dispersion_modelo": amplio[0],
        "dispersion": str(max(amplio[1]) - min(amplio[1])),
        "dispersion_rango": f"{min(amplio[1])}–{max(amplio[1])}",
        "dispersion_n": str(len(amplio[1])),
        "minimo": str(min(totales)),
    }


DATOS = _datos()


# ─────────────────────────────────────────────────────────────────────────────
# Color: una paleta cerrada, cada color con su origen; contraste WCAG calculado
# ─────────────────────────────────────────────────────────────────────────────

PALETA = json.loads(leer("contenido/paleta.json"))
COLORES = {k: {"nombre": c["nombre"], "hex": c["hex"].upper(), "uso": c["uso"], "origen": c["origen"]}
           for k, c in PALETA["colores"].items()}
RETIRADOS = PALETA["retirados"]
ORIGENES = {"logo": "logo", "css": "CSS", "deriv": "v1.0"}
SOL = [("#FFFFFF", 0), ("ua-sol", .30), ("ua-fulgor", .65), ("ua-brasa", 1)]     # radial-gradient de .brand .dot
TIER_COLOR = {"S": "ua-sol", "A": "ua-esmeralda", "B": "ua-celeste", "C": "ua-nebulosa", "D": "ua-coral"}
TIER_CLARO = {"S": "ua-ambar-profundo", "A": "ua-verde-profundo", "B": "ua-azul-profundo", "C": "ua-nebulosa-profunda", "D": "ua-rojo-texto"}


def hexa(i):
    return i if i.startswith("#") else COLORES[i]["hex"]


def _lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contraste(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def nivel_wcag(r):
    if r >= 7: return "AAA"
    if r >= 4.5: return "AA"
    if r >= 3: return "AA grande"
    return "No apto"


def exportar_tokens():
    """Tokens para la web (assets/marca/) y para el CSS del manual. GENERADOS."""
    filas = [f"  --{k}: {c['hex']};  /* {c['nombre']} · {ORIGENES[c['origen']]} */" for k, c in COLORES.items()]
    sol = ", ".join(f"{hexa(c)} {p * 100:g}%" for c, p in SOL)
    css = ("/* GENERADO por docs/Manual_Marca_UniversoArena/v1.0/scripts/build_v1.py — no editar a mano.\n"
           f"   Paleta cerrada de Universo-Arena v1.0: {len(COLORES)} colores. Los del logo se leyeron en el Sol de la\n"
           "   barra de la galería anterior (.brand .dot); los de CSS, en su :root; el resto se deriva con su\n"
           "   contraste calculado (contenido/paleta.json). */\n:root {\n"
           + "\n".join(filas)
           + f"\n  --ua-sol-radial: radial-gradient(circle at 35% 30%, {sol});"
           + "\n  --f-display: 'Inter', system-ui, sans-serif;\n  --f-mono: 'JetBrains Mono', ui-monospace, monospace;\n}\n")
    (BASE / "assets/data/tokens-v1.css").write_text(css, encoding="utf-8")
    datos = {"marca": "Universo-Arena", "version": VERSION, "colores": COLORES,
             "degradado": {"sol": [[hexa(c), p] for c, p in SOL]},
             "tiers": {t: {"oscuro": hexa(TIER_COLOR[t]), "claro": hexa(TIER_CLARO[t])} for t in TIER_COLOR},
             "tipografia": {"display": "Inter", "texto": "Inter", "codigo": "JetBrains Mono"}}
    (BASE / "assets/data/tokens_v1.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# Símbolo: el Sol de la barra, sin tocar una cota.
#   .brand .dot { width:26px; height:26px; border-radius:50%;
#                 background: radial-gradient(circle at 35% 30%, #fff, #ffd24a 30%, #ff7a3c 65%, #7a1d00) }
# En un viewBox de 100 u: círculo de radio 50 centrado; el foco del brillo en (35, 30). El tamaño del
# degradado es el de CSS por defecto (farthest-corner): la esquina más lejana, (100, 100), a 95,5 u.
# El halo (box-shadow 0 0 18px) es un efecto de pantalla: no forma parte del símbolo.
# ─────────────────────────────────────────────────────────────────────────────

LADO = 100
BRILLO = (35, 30)
R_GRAD = math.hypot(LADO - BRILLO[0], LADO - BRILLO[1])
INTER = BASE / "fuentes" / "inter" / "Inter[opsz,wght].ttf"


def degradado_sol(id_, cx=50, cy=50, r=50):
    """El degradado del Sol para un disco de radio r centrado en (cx, cy): las cotas del viewBox de
    100 u escaladas. Con los valores por defecto es el del maestro."""
    k = r / 50
    pasos = "".join(f'<stop offset="{p:g}" stop-color="{hexa(c)}"/>' for c, p in SOL)
    return (f'<radialGradient id="{id_}" cx="{cx - r + BRILLO[0] * k:g}" cy="{cy - r + BRILLO[1] * k:g}" r="{R_GRAD * k:.2f}" '
            f'gradientUnits="userSpaceOnUse">{pasos}</radialGradient>')


@lru_cache(maxsize=None)
def _inter(peso, opsz):
    f = TTFont(INTER)
    instantiateVariableFont(f, {"wght": peso, "opsz": opsz}, inplace=True)
    return f


def texto_trazado(cad, peso, cuerpo, tracking=0.0, x0=0.0, y0=0.0, opsz=14):
    """Trazado SVG de `cad` en Inter con cuerpo `cuerpo` (u), línea base en y0. Son curvas:
    el logotipo no depende de que la fuente esté instalada."""
    f = _inter(peso, opsz)
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    k = cuerpo / f["head"].unitsPerEm
    x = x0
    d = []
    for ch in cad:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, y0)))
        d.append(pen.getCommands())
        x += gs[g].width * k + tracking
    cap = f["OS/2"].sCapHeight * k
    return " ".join(d), x - tracking - x0, cap


# Proporciones de la barra: Sol de 26 px, 10 px de aire, «Universo-Arena» en Inter 800 a 16 px y -0,01 em.
ESC_CAB = LADO / 26
CUERPO = 16 * ESC_CAB
AIRE = 10 * ESC_CAB
TRACK = -0.01 * CUERPO
NOMBRE = "Universo-Arena"


def simbolo_cuerpo(modo, dx=0, dy=0, k=1.0):
    """modo: «color» (el degradado radial) o un hex (una sola tinta: disco plano)."""
    t = f' transform="translate({dx:g} {dy:g}) scale({k:g})"' if (dx or dy or k != 1) else ""
    relleno = "url(#sol)" if modo == "color" else modo
    return f'<g{t}><circle cx="50" cy="50" r="50" fill="{relleno}"/></g>'


def defs_simbolo(modo):
    return degradado_sol("sol") if modo == "color" else ""


def svg_simbolo(modo="color", titulo="Universo-Arena"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LADO} {LADO}" role="img" aria-label="{esc(titulo)}">'
            f'<defs>{defs_simbolo(modo)}</defs>{simbolo_cuerpo(modo)}</svg>\n')


def svg_horizontal(modo_sim, color_txt):
    x = LADO + AIRE
    _, w, cap = texto_trazado(NOMBRE, 800, CUERPO, TRACK)
    base = LADO / 2 + cap / 2
    d, w, _ = texto_trazado(NOMBRE, 800, CUERPO, TRACK, x, base)
    ancho = round(x + w + 2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {LADO}" role="img" aria-label="Universo-Arena">'
            f'<defs>{defs_simbolo(modo_sim)}</defs>{simbolo_cuerpo(modo_sim)}<path d="{d}" fill="{color_txt}"/></svg>\n'), ancho


def svg_vertical(modo_sim, color_txt):
    _, w, cap = texto_trazado(NOMBRE, 800, CUERPO, TRACK)
    ancho = round(max(w, LADO) + 8)
    base = LADO + 22 + cap
    alto = round(base + CUERPO * 0.26 + 3)
    x = (ancho - w) / 2
    d, _, _ = texto_trazado(NOMBRE, 800, CUERPO, TRACK, x, base)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" role="img" aria-label="Universo-Arena">'
            f'<defs>{defs_simbolo(modo_sim)}</defs>{simbolo_cuerpo(modo_sim, (ancho - LADO) / 2)}<path d="{d}" fill="{color_txt}"/></svg>\n'), ancho


ANCHOS = {}


def generar_logos():
    """Maestros de la marca. Todo sale de simbolo_cuerpo() y texto_trazado()."""
    tinta, estelar = hexa("ua-tinta"), hexa("ua-estelar")
    L = BASE / "assets" / "logos"
    L.mkdir(parents=True, exist_ok=True)
    archivos = {
        "ua-simbolo.svg": svg_simbolo("color"),
        "ua-simbolo-tinta.svg": svg_simbolo(tinta),
        "ua-simbolo-blanco.svg": svg_simbolo("#FFFFFF"),
        "ua-simbolo-negro.svg": svg_simbolo("#000000"),
    }
    for nombre, (s, t) in {
        "ua-horizontal.svg": ("color", tinta),
        "ua-horizontal-negativo.svg": ("color", estelar),
        "ua-horizontal-blanco.svg": ("#FFFFFF", "#FFFFFF"),
        "ua-horizontal-tinta.svg": (tinta, tinta),
    }.items():
        archivos[nombre], ANCHOS[nombre] = svg_horizontal(s, t)
    for nombre, (s, t) in {
        "ua-vertical.svg": ("color", tinta),
        "ua-vertical-negativo.svg": ("color", estelar),
    }.items():
        archivos[nombre], ANCHOS[nombre] = svg_vertical(s, t)
    for nombre, s in archivos.items():
        (L / nombre).write_text(s, encoding="utf-8")
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        raise SystemExit("Falta rsvg-convert (paquete librsvg2-bin) para los PNG de favicon")
    for salida, px in [("favicon-16.png", 16), ("favicon-32.png", 32), ("apple-touch-icon.png", 180),
                       ("icono-192.png", 192), ("icono-512.png", 512)]:
        subprocess.run([rsvg, "-w", str(px), "-h", str(px), "-o", str(L / salida), str(L / "ua-simbolo.svg")], check=True)


_contador_svg = {"n": 0}


def svg_en_linea(nombre, extra_attr=""):
    """SVG listo para incrustar varias veces: los maestros llevan id de degradado («sol») y dos
    copias en la misma página chocarían (trampa 26 de KANSA)."""
    _contador_svg["n"] += 1
    p = f"m{_contador_svg['n']}-"
    s = (BASE / "assets" / "logos" / nombre).read_text(encoding="utf-8")
    s = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', s)
    s = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{p}{m.group(1)})", s)
    s = re.sub(r'\s(role="img"|aria-label="[^"]*")', "", s)
    s = s.strip()
    return s.replace("<svg ", f'<svg width="100%" height="100%" focusable="false" aria-hidden="true" {extra_attr} ', 1)


def ratio(nombre):
    vb = re.search(r'viewBox="([\d.\- ]+)"', (BASE / "assets" / "logos" / nombre).read_text(encoding="utf-8")).group(1).split()
    return f"{float(vb[2]):g} / {float(vb[3]):g}"


def logo(nombre="ua-simbolo.svg", clase="", estilo=""):
    est = f"aspect-ratio:{ratio(nombre)};" + estilo
    return (f'<div class="logo {clase}" data-logo="{esc(nombre)}" style="{est}">' + svg_en_linea(nombre) + "</div>")


def imago(vertical=False, oscuro=False, mono=None):
    """El logotipo completo es un SVG maestro (texto en curvas), no HTML + fuente."""
    if mono:
        nombre = f"ua-horizontal-{mono}.svg"
    elif vertical:
        nombre = "ua-vertical-negativo.svg" if oscuro else "ua-vertical.svg"
    else:
        nombre = "ua-horizontal-negativo.svg" if oscuro else "ua-horizontal.svg"
    clases = "imago" + (" vertical" if vertical else "") + (" sobre-oscuro" if oscuro else "")
    return (f'<div class="{clases}" role="img" aria-label="Universo-Arena">' + logo(nombre, "imago-svg") + "</div>")


IMAGENES = {}


def imagen(rel, alt, clase=""):
    """<img> a assets/; el portable las sustituye por data: URI."""
    IMAGENES[rel] = True
    return f'<img src="assets/{rel}" alt="{esc(alt)}" class="{clase}" loading="lazy" decoding="async">'


# ─────────────────────────────────────────────────────────────────────────────
# El recurso gráfico: una elipse con el Sol en el FOCO (no en el centro) y un cometa cuya cola
# apunta lejos del Sol. Son las dos trampas que deciden el ranking (docs/rubric.md); la marca las
# dibuja bien. Geometría: x = a·cosθ − c, y = b·sinθ con c = a·e y b = a·√(1−e²), Sol en el origen.
# ─────────────────────────────────────────────────────────────────────────────

def elipse(a, e, cx, cy, rot=0.0):
    """Atributos de una <ellipse> con el foco en (cx, cy): su centro se desplaza c = a·e."""
    b = a * math.sqrt(1 - e * e)
    c = a * e
    ox, oy = cx - c * math.cos(rot), cy - c * math.sin(rot)
    return ox, oy, b, c


def punto_en(a, e, cx, cy, theta, rot=0.0):
    b = a * math.sqrt(1 - e * e)
    x, y = a * math.cos(theta) - a * e, b * math.sin(theta)
    return (cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot))


def cola(px, py, sx, sy, largo, ancho):
    """Cola del cometa: un triángulo que sale del núcleo en el sentido (cometa − Sol)."""
    dx, dy = px - sx, py - sy
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    nx, ny = -uy, ux
    fx, fy = px + ux * largo, py + uy * largo
    return (f"M{px + nx * ancho / 2:.1f} {py + ny * ancho / 2:.1f} L{fx:.1f} {fy:.1f} "
            f"L{px - nx * ancho / 2:.1f} {py - ny * ancho / 2:.1f}Z"), (fx, fy)


CENTRO = (1230, 610)      # el Sol (foco común): abajo a la derecha, lejos del título


def capas_portada():
    rng = random.Random(20260615)          # el día del primer commit del repositorio
    VACIO, COSMOS = hexa("ua-vacio"), hexa("ua-cosmos")
    cx, cy = CENTRO
    capas = []
    estrellas = "".join(
        f'<circle cx="{rng.uniform(0, 1600):.0f}" cy="{rng.uniform(0, 900):.0f}" r="{rng.choice((0.8, 1, 1.2, 1.6, 2))}" '
        f'fill="#FFFFFF" opacity="{rng.uniform(.25, .9):.2f}"/>' for _ in range(220))
    capas.append(("fondo", 0,
        '<defs><linearGradient id="PORT-g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{COSMOS}"/><stop offset=".7" stop-color="{VACIO}"/><stop offset="1" stop-color="{VACIO}"/></linearGradient>'
        + "".join(f'<radialGradient id="PORT-{n}" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{c}" stop-opacity="{o}"/>'
                  f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
                  for n, c, o in (("o", hexa("ua-orbita"), ".30"), ("n", hexa("ua-nebulosa"), ".26"), ("s", hexa("ua-sol"), ".55")))
        + '</defs>'
        f'<rect width="1600" height="900" fill="url(#PORT-g)"/>{estrellas}'
        '<ellipse cx="300" cy="140" rx="620" ry="320" fill="url(#PORT-o)"/>'
        '<ellipse cx="1400" cy="820" rx="560" ry="300" fill="url(#PORT-n)"/>'))
    # Órbitas: elipses con el Sol en el foco común, cada una con su planeta
    orbitas = []
    for a, e, rot, theta, r, color in ((150, .18, -.15, 2.4, 9, "ua-celeste"), (250, .22, -.15, 3.3, 13, "ua-esmeralda"),
                                       (360, .28, -.15, 1.7, 17, "ua-nebulosa")):
        ox, oy, b, _ = elipse(a, e, cx, cy, rot)
        orbitas.append(f'<ellipse cx="{ox:.1f}" cy="{oy:.1f}" rx="{a}" ry="{b:.1f}" transform="rotate({math.degrees(rot):.2f} {ox:.1f} {oy:.1f})" '
                       f'fill="none" stroke="{hexa("ua-orbita")}" stroke-width="1.6" opacity=".55"/>')
        px, py = punto_en(a, e, cx, cy, theta, rot)
        orbitas.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{hexa(color)}"/>')
    # El centro geométrico de la elipse mayor, marcado y vacío: el Sol NO va ahí
    ox, oy, _, _ = elipse(360, .28, cx, cy, -.15)
    orbitas.append(f'<g opacity=".7"><path d="M{ox - 7:.1f} {oy:.1f} H{ox + 7:.1f} M{ox:.1f} {oy - 7:.1f} V{oy + 7:.1f}" '
                   f'stroke="{hexa("ua-polvo")}" stroke-width="1.5"/></g>')
    capas.append(("orbitas", 3, "".join(orbitas)))
    # Cometa en órbita muy excéntrica, cola en el sentido (cometa − Sol)
    a, e, rot = 560, .82, .4
    ox, oy, b, _ = elipse(a, e, cx, cy, rot)
    px, py = punto_en(a, e, cx, cy, 2.7, rot)
    d_cola, _ = cola(px, py, cx, cy, 230, 34)
    capas.append(("cometa", 2,
        f'<defs><linearGradient id="PORT-c" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{hexa("ua-estelar")}" stop-opacity=".85"/>'
        f'<stop offset="1" stop-color="{hexa("ua-orbita")}" stop-opacity="0"/></linearGradient></defs>'
        f'<ellipse cx="{ox:.1f}" cy="{oy:.1f}" rx="{a}" ry="{b:.1f}" transform="rotate({math.degrees(rot):.2f} {ox:.1f} {oy:.1f})" '
        f'fill="none" stroke="{hexa("ua-polvo")}" stroke-width="1.2" stroke-dasharray="3 9" opacity=".5"/>'
        f'<path d="{d_cola}" fill="{hexa("ua-estelar")}" opacity=".55"/>'
        f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="#FFFFFF"/>'))
    # El Sol, en el foco
    capas.append(("sol", 1,
        f'<defs>{degradado_sol("PORT-sol", cx, cy, 54)}</defs>'
        f'<circle cx="{cx}" cy="{cy}" r="150" fill="url(#PORT-s)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="54" fill="url(#PORT-sol)"/>'))
    return capas


_contador_port = {"n": 0}


def portada_html(en_capas=False):
    _contador_port["n"] += 1
    pre = f"p{_contador_port['n']}-"
    capas = [(n, z, c.replace("PORT-", pre)) for n, z, c in capas_portada()]
    if not en_capas:
        cuerpo = "".join(f'<g class="capa-{n}">{c}</g>' for n, _, c in capas)
        return ('<svg class="grafica" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice"'
                f' width="100%" height="100%" aria-hidden="true">{cuerpo}</svg>')
    out = []
    for n, z, c in capas:
        out.append(f'<div class="capa capa-{n}" data-z="{z}" aria-hidden="true">'
                   f'<svg viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" width="100%" height="100%">{c}</svg></div>')
    return '<div class="grafica-capas">' + "".join(out) + "</div>"


# ─────────────────────────────────────────────────────────────────────────────
# «Órbita viva»: respaldo estático del lienzo animado (assets/js/ua-v1-orbita.js)
# ─────────────────────────────────────────────────────────────────────────────

_contador_ov = {"n": 0}


def orbita_respaldo_svg():
    _contador_ov["n"] += 1
    p = f"ov{_contador_ov['n']}-"
    cx, cy = 200, 125
    ox, oy, b, _ = elipse(120, .55, cx, cy)
    px, py = punto_en(120, .55, cx, cy, 2.2)
    oxc, oyc, bc, _ = elipse(165, .8, cx, cy, .5)
    qx, qy = punto_en(165, .8, cx, cy, 2.6, .5)
    d_cola, _ = cola(qx, qy, cx, cy, 60, 12)
    return (f'<svg class="orbita-respaldo" viewBox="0 0 400 250" preserveAspectRatio="xMidYMid slice" width="100%" height="100%" aria-hidden="true">'
            f'<defs>{degradado_sol(p + "s", cx, cy, 9)}</defs>'
            f'<rect width="400" height="250" fill="{hexa("ua-vacio")}"/>'
            f'<ellipse cx="{ox:.1f}" cy="{oy:.1f}" rx="120" ry="{b:.1f}" fill="none" stroke="{hexa("ua-orbita")}" stroke-width="1.4" opacity=".7"/>'
            f'<ellipse cx="{oxc:.1f}" cy="{oyc:.1f}" rx="165" ry="{bc:.1f}" transform="rotate({math.degrees(.5):.2f} {oxc:.1f} {oyc:.1f})" fill="none" '
            f'stroke="{hexa("ua-polvo")}" stroke-width="1" stroke-dasharray="2 6" opacity=".55"/>'
            f'<path d="M{ox - 4:.1f} {oy:.1f} H{ox + 4:.1f} M{ox:.1f} {oy - 4:.1f} V{oy + 4:.1f}" stroke="{hexa("ua-polvo")}" stroke-width="1"/>'
            f'<path d="{d_cola}" fill="{hexa("ua-estelar")}" opacity=".5"/><circle cx="{qx:.1f}" cy="{qy:.1f}" r="3" fill="#FFFFFF"/>'
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{hexa("ua-esmeralda")}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="url(#{p}s)"/></svg>')


# ─────────────────────────────────────────────────────────────────────────────
# Componentes (usados por ambas salidas)
# ─────────────────────────────────────────────────────────────────────────────

def comp_indice(caps, **_):
    filas = []
    for c in caps:
        if c["num"] == "00":
            continue
        filas.append(f'<li><a href="#cap-{c["id"]}"><span class="ind-num">{c["num"]}</span>'
                     f'<span class="ind-tit">{esc(c["titulo"])}</span>'
                     f'<span class="ind-pag">{c["_pag_ini"]:02d}</span></a></li>')
    return '<ol class="indice">' + "".join(filas) + "</ol>"


def comp_portada(modo, **_):
    fondo = portada_html(en_capas=(modo == "inmersivo"))
    return (f'<div class="portada"><div class="portada-fondo">{fondo}</div>'
            '<div class="portada-texto">'
            f'<div class="portada-marca">{imago(oscuro=True)}</div>'
            '<p class="portada-lema">El Sol en el foco</p>'
            '<p class="portada-sub">Manual de Marca v1.0</p>'
            f'<p class="portada-pie">Un prompt · {esc(DATOS["entregas"])} universos · universo-arena.alexanderoviedofadul.dev · Octubre de 2026</p>'
            "</div></div>")


def comp_contraportada(modo, **_):
    return ('<div class="portada contra"><div class="portada-fondo">' + portada_html() + "</div>"
            '<div class="portada-texto"><div class="contra-marca">' + imago(vertical=True) + "</div>"
            '<p class="contra-frase">Casi todas las entregas se ven bien. La diferencia está en los detalles que solo resuelve quien entiende la física: el Sol en el foco y la cola lejos del Sol.</p>'
            '<p class="portada-pie">universo-arena.alexanderoviedofadul.dev · Manual de Marca v1.0 · Octubre de 2026 · '
            'Generado desde una sola fuente por scripts/build_v1.py</p></div></div>')


def comp_isotipo(variante="ua-simbolo.svg", fondo="claro", **_):
    return f'<figure class="fig-logo fondo-{fondo}">' + logo(variante, "logo-fig") + "</figure>"


def comp_isotipo_oscuro(**_):
    return comp_isotipo("ua-simbolo.svg", fondo="oscuro")


def comp_lema(**_):
    return ('<div class="lema"><p class="lema-txt">Un prompt. Muchos universos.</p>'
            '<p class="lema-pie">Juzgado por lo que hace al abrirse</p></div>')


def comp_anatomia(**_):
    partes = [("1", "El disco · el Sol", "Un círculo lleno: el Sol de la barra de la galería, de 26 px. Es el favicon y el icono."),
              ("2", "El brillo · arriba a la izquierda", "El degradado nace en (35 %, 30 %): la luz llega de arriba a la izquierda, como en la galería."),
              ("3", "Cuatro paradas · del blanco a la brasa", "Blanco, Sol (30 %), Fulgor (65 %) y Brasa (100 %). Son las del radial-gradient original."),
              ("4", "«Universo-Arena» · el nombre", "Inter 800 con el guion, como en la barra. Tinta sobre claro, Estelar sobre oscuro."),
              ("5", "Sin rediseño", "Todo lo anterior ya estaba en la galería. Esta versión lo mide y lo pasa a vector; no lo cambia.")]
    return ('<div class="anatomia"><div class="anat-fig">' + imago(vertical=True) + "</div><ol class=\"anat-lista\">"
            + "".join(f'<li><span class="anat-n">{n}</span><div><strong>{esc(t)}</strong><p>{esc(d)}</p></div></li>' for n, t, d in partes)
            + "</ol></div>")


def comp_construccion(**_):
    """Retícula de construcción del Sol, con las cotas del CSS original."""
    tinta, borde, azul = hexa("ua-tinta"), hexa("ua-borde"), hexa("ua-orbita-profunda")
    rej = "".join(f'<path d="M{v} 0 V100 M0 {v} H100" stroke="{borde}" stroke-width=".25"/>' for v in range(0, 101, 5))
    cotas = (f'<g font-family="JetBrains Mono, monospace" font-size="3.6" fill="{azul}">'
             f'<text x="37" y="27">brillo 35 · 30</text><text x="52" y="54">r 50</text><text x="58" y="74">r grad {R_GRAD:.1f}</text></g>')
    return ('<figure class="construccion"><svg viewBox="-3 -3 106 106" width="100%" height="100%" aria-hidden="true">'
            f'<defs>{degradado_sol("cons-s")}</defs>{rej}<circle cx="50" cy="50" r="50" fill="url(#cons-s)" opacity=".35"/>'
            f'<circle cx="50" cy="50" r="50" fill="none" stroke="{tinta}" stroke-width=".6"/>'
            f'<path d="M50 50 H100" stroke="{tinta}" stroke-width=".5"/>'
            f'<circle cx="35" cy="30" r="1.6" fill="{hexa("ua-nebulosa-profunda")}"/>'
            f'<path d="M35 30 L100 100" stroke="{hexa("ua-nebulosa-profunda")}" stroke-width=".5" stroke-dasharray="1.5 1.5"/>'
            f'{cotas}</svg>'
            '<figcaption>Retícula de 5 u sobre el viewBox 0 0 100 100 · disco de radio 50 · brillo en (35, 30) · '
            'radio del degradado hasta la esquina más lejana, como hace CSS</figcaption></figure>')


VARIANTES = [("ua-simbolo.svg", "Principal", "El Sol con su degradado. Sobre oscuro y sobre claro", "claro"),
             ("ua-simbolo-tinta.svg", "Una tinta", "Tinta #0B1024: sellos y documentos", "claro"),
             ("ua-simbolo-blanco.svg", "Blanco", "Sobre fotografía o fondos oscuros de una sola tinta", "oscuro"),
             ("ua-simbolo-negro.svg", "100 % K", "Fotocopia, fax y grabado", "claro")]


def comp_variantes(**_):
    return ('<div class="variantes" style="grid-template-columns:repeat(4,minmax(0,1fr))">' + "".join(
        f'<div class="var-card fondo-{f}"><div class="var-logo">{logo(n)}</div><div class="var-txt"><strong>{esc(t)}</strong><span>{esc(d)}</span></div></div>'
        for n, t, d, f in VARIANTES) + "</div>")


def comp_lockups(**_):
    return ('<div class="lockups">'
            f'<div class="lock lock-oscuro"><div class="lock-fig">{imago(oscuro=True)}</div><span>Horizontal negativo · la versión principal: galería, imagen para compartir y README</span></div>'
            f'<div class="lock"><div class="lock-fig">{imago()}</div><span>Horizontal sobre claro · documentos y PDF</span></div>'
            "</div>")


def comp_proteccion(**_):
    return ('<figure class="fig-proteccion"><div class="prot-caja">'
            '<span class="prot-x prot-x-t">X</span><span class="prot-x prot-x-b">X</span>'
            '<span class="prot-x prot-x-l">X</span><span class="prot-x prot-x-r">X</span>'
            + imago() + "</div>"
            '<figcaption>X = la mitad del diámetro del Sol: ese aire libre alrededor</figcaption></figure>')


def comp_minimos(**_):
    filas = [("Pantalla", "logotipo horizontal 140 px de ancho · Sol 16 px", "height:24px"),
             ("Impresión", "logotipo horizontal 35 mm · Sol 5 mm", "height:8mm"),
             ("Favicon 16 px", "el Sol entero, sin el nombre", "height:16px")]
    out = ['<div class="minimos">']
    for a, b, e in filas:
        n = "ua-simbolo.svg" if "Favicon" in a else "ua-horizontal.svg"
        out.append(f'<div class="min-fila"><div class="min-logo">{logo(n, estilo=e + ";width:auto")}</div>'
                   f'<div><strong>{esc(a)}</strong><br><span class="mono">{esc(b)}</span></div></div>')
    out.append("</div>")
    return "".join(out)


def comp_incorrectos(**_):
    casos = [("transform:scaleX(1.45)", "", "No estirar ni comprimir el logotipo"),
             ("filter:hue-rotate(160deg)", "", "No cambiar los colores del Sol"),
             ("", "centro", "No dibujar el Sol en el centro de una órbita elíptica"),
             ("", "cola", "No dibujar la cola del cometa hacia el Sol"),
             ("", "fondo", "No usar la versión negativa sobre claro"),
             ("filter:drop-shadow(4px 4px 0 #0B1024)", "", "No aplicar sombras duras, biseles ni 3D"),
             ("", "texto", "No escribir «UNIVERSO ARENA», «UniversoArena» ni «Universe Arena»"),
             ("", "rayos", "No añadir rayos, caras ni anillos al Sol")]
    out = ['<div class="incorrectos">']
    for estilo, tipo, texto in casos:
        if tipo == "texto":
            fig = '<span class="inc-texto">UNIVERSE<i> ARENA</i></span>'
        elif tipo in ("centro", "cola"):
            cx, cy = 50, 40
            if tipo == "centro":
                cuerpo = (f'<ellipse cx="{cx}" cy="{cy}" rx="38" ry="22" fill="none" stroke="{hexa("ua-orbita-profunda")}" stroke-width="1.5"/>'
                          f'<circle cx="{cx}" cy="{cy}" r="7" fill="{hexa("ua-sol")}"/>')
            else:
                d_cola, _ = cola(78, 22, cx, cy, -22, 7)
                cuerpo = (f'<circle cx="{cx}" cy="{cy}" r="7" fill="{hexa("ua-sol")}"/>'
                          f'<path d="{d_cola}" fill="{hexa("ua-gris-texto")}" opacity=".7"/><circle cx="78" cy="22" r="3" fill="{hexa("ua-tinta")}"/>')
            fig = f'<svg class="inc-emoji" viewBox="0 0 100 80" aria-hidden="true">{cuerpo}</svg>'
        elif tipo == "rayos":
            rayos = "".join(f'<path d="M{50 + math.cos(k * math.pi / 4) * 22:.1f} {40 + math.sin(k * math.pi / 4) * 22:.1f} L{50 + math.cos(k * math.pi / 4) * 32:.1f} {40 + math.sin(k * math.pi / 4) * 32:.1f}" stroke="{hexa("ua-fulgor")}" stroke-width="4" stroke-linecap="round"/>' for k in range(8))
            fig = (f'<svg class="inc-emoji" viewBox="0 0 100 80" aria-hidden="true"><defs>{degradado_sol("inc-s", 50, 40, 16)}</defs>{rayos}'
                   f'<circle cx="50" cy="40" r="16" fill="url(#inc-s)"/></svg>')
        elif tipo == "fondo":
            fig = f'<div class="inc-logo">{logo("ua-horizontal-negativo.svg")}</div>'
        else:
            fig = f'<div class="inc-logo" style="{estilo}">{logo("ua-horizontal.svg")}</div>'
        clase = " inc-fondo" if tipo == "fondo" else ""
        out.append(f'<div class="inc-card"><div class="inc-fig{clase}">{fig}<span class="inc-x" aria-hidden="true">×</span></div><p>{esc(texto)}</p></div>')
    out.append("</div>")
    return "".join(out)


def comp_favicon(**_):
    tams = [(64, "512 · 192 (Android)"), (48, "180 (Apple)"), (32, "32"), (24, "24"), (16, "16")]
    celdas = "".join(f'<div class="fav"><div style="width:{p}px;height:{p}px">{logo("ua-simbolo.svg")}</div><span class="mono">{esc(t)}</span></div>' for p, t in tams)
    return f'<div class="favicons">{celdas}</div>'


def comp_orbita(modo, **_):
    canvas = '<canvas class="orbita-gl" aria-hidden="true" data-solo-inmersivo></canvas>' if modo == "inmersivo" else ""
    return f'<div class="orbita-vivo">{canvas}{orbita_respaldo_svg()}</div>'


def comp_paleta(ids, grande=False, **_):
    out = [f'<div class="paleta{" grande" if grande else ""}">']
    for i in ids:
        c = COLORES[i]
        h = c["hex"]
        r, g, b = (int(h[k:k + 2], 16) for k in (1, 3, 5))
        texto = "#FFFFFF" if contraste(h, "#FFFFFF") >= contraste(h, hexa("ua-vacio")) else hexa("ua-vacio")
        out.append(f'<button type="button" class="swatch" data-copiar="{h}" style="--sw:{h};--sw-t:{texto}">'
                   f'<span class="sw-color"><span class="sw-hex">{h}</span></span>'
                   f'<span class="sw-info"><strong>{esc(c["nombre"])} <span class="sw-origen">{ORIGENES[c["origen"]]}</span></strong><span class="mono">RGB {r} {g} {b} · --{esc(i)}</span>'
                   f'<span class="sw-rol">{esc(c["uso"])}</span></span></button>')
    out.append("</div>")
    return "".join(out)


def comp_degradados(**_):
    sol = ", ".join(f"{hexa(c)} {p * 100:g}%" for c, p in SOL)
    tiers = "".join(f'<span style="background:{hexa(TIER_COLOR[t])};color:{hexa("ua-vacio")}">{t} · {esc(r)}</span>' for t, r in TIERS)
    return ('<div class="degradados">'
            f'<div class="grad-card"><span class="grad-barra" style="background:radial-gradient(circle at 35% 30%,{sol})"></span>'
            f'<strong>El Sol</strong><span class="mono">radial · 35 % 30 % · {esc(sol)}</span><p>Solo para el símbolo y su halo. No es un fondo: sobre él no se escribe.</p></div>'
            f'<div class="grad-card"><span class="grad-barra escala-sev">{tiers}</span>'
            '<strong>La escala de tiers</strong><span class="mono">--ua-sol · --ua-esmeralda · --ua-celeste · --ua-nebulosa · --ua-coral</span>'
            '<p>Solo para notas. Color y letra siempre juntos: nunca un tier solo por su color.</p></div>'
            "</div>")


def comp_contraste(pares, **_):
    filas = []
    for fg, bg, uso in pares:
        fgh, bgh = hexa(fg), hexa(bg)
        r = contraste(fgh, bgh)
        n = nivel_wcag(r)
        filas.append(f'<tr><td><span class="ct-muestra" style="color:{fgh};background:{bgh}">Aa</span></td>'
                     f'<td class="mono">{fgh} / {bgh}</td><td class="mono">{r:.2f} : 1</td>'
                     f'<td><span class="ct-nivel nivel-{n.split()[0].lower()}">{n}</span></td><td>{inline(uso)}</td></tr>')
    return ('<table class="tabla compacta"><thead><tr><th>Muestra</th><th>Texto / fondo</th><th>Contraste</th>'
            '<th>WCAG 2.1</th><th>Uso</th></tr></thead><tbody>' + "".join(filas) + "</tbody></table>")


def comp_retirados(**_):
    filas = "".join(
        f'<tr><td><span class="ct-muestra" style="background:{r["hex"]};color:#fff">&nbsp;&nbsp;</span></td><td class="mono">{esc(r["hex"])}</td>'
        f'<td>{esc(r["nombre"])}</td><td>{inline(r["motivo"])}</td><td>{esc(r["sustituto"])}</td></tr>' for r in RETIRADOS)
    return ('<table class="tabla compacta"><thead><tr><th></th><th>Hex</th><th>Nombre</th><th>Por qué sale</th><th>Lo sustituye</th></tr></thead>'
            f'<tbody>{filas}</tbody></table>')


def comp_paleta_mini(**_):
    ids = ["ua-vacio", "ua-cosmos", "ua-orbita", "ua-nebulosa", "ua-sol", "ua-fulgor", "ua-esmeralda", "ua-estelar"]
    return '<div class="paleta-mini" aria-hidden="true">' + "".join(
        f'<span style="background:{hexa(i)}"><em>{hexa(i)}</em></span>' for i in ids) + "</div>"


ICONOS = {  # trazos de 24 × 24 al estilo Lucide (lineal, extremos redondeados)
    "doc": '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
    "play": '<path d="M7 4v16l13-8z"/>',
    "balanza": '<path d="M12 3v18M5 21h14M6 8l-3 7h6zM18 8l-3 7h6zM6 8h12"/>',
    "orbita": '<ellipse cx="12" cy="12" rx="10" ry="6"/><circle cx="8" cy="12" r="2"/>',
    "ok": '<path d="M20 6 9 17l-5-5"/>',
}


def ico(n):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONOS[n]}</svg>'


def comp_fondos(**_):
    casos = [(hexa("ua-vacio"), "ua-horizontal-negativo.svg", "Vacío #05060F: la galería y el manual en oscuro"),
             (hexa("ua-cosmos"), "ua-horizontal-negativo.svg", "Cosmos #0A0D1F: fichas, paneles y pie"),
             ("#FFFFFF", "ua-horizontal.svg", "Blanco o Niebla: documentos y PDF"),
             (hexa("ua-orbita-profunda"), "ua-horizontal-blanco.svg", "Sobre un color de marca: solo la versión blanca")]
    return '<div class="fondos">' + "".join(
        f'<div class="fondo-card"><div class="fondo-muestra" style="background:{bg}">{logo(n)}</div><p>{esc(t)}</p></div>'
        for bg, n, t in casos) + "</div>"


def comp_especimen(familia, rol, muestra, pesos, **_):
    clases = {"Inter": "ff-display", "JetBrains Mono": "ff-mono"}
    return (f'<div class="especimen"><div class="esp-cab"><strong>{esc(familia)}</strong><span>{esc(rol)}</span></div>'
            f'<div class="esp-muestra {clases[familia]}">{esc(muestra)}</div>'
            f'<div class="esp-abc {clases[familia]}">Aa Bb Cc Ññ Áé 0123456789 ¿? «» · θ √ −</div>'
            f'<div class="esp-pesos mono">{esc(pesos)}</div></div>')


def comp_escala(**_):
    filas = [("Portada", "ff-display", "Inter 800", "56 px", f"Un prompt. {DATOS['entregas']} universos.", "font-size:2.2em;font-weight:800;letter-spacing:-.02em"),
             ("H2", "ff-display", "Inter 800", "36 px", "Los tres mejores universos", "font-size:1.5em;font-weight:800"),
             ("H3", "ff-display", "Inter 700", "18 px", "La cola del cometa", "font-size:1.1em;font-weight:700"),
             ("Cuerpo", "ff-sans", "Inter 400", "16 px / 1,55", "Cada entrega se juzga por lo que hace al abrirse.", "font-size:.95em;font-weight:400"),
             ("Fórmula", "ff-mono", "JetBrains Mono 400", "14 px", "x = a·cosθ − a·e", "font-size:.86em"),
             ("Nota", "ff-sans", "Inter 800 tabular", "28 px", f"{DATOS['cima']}/100", "font-size:1.3em;font-weight:800;font-variant-numeric:tabular-nums")]
    return ('<table class="tabla escala"><thead><tr><th>Nivel</th><th>Familia</th><th>Tamaño</th><th>Muestra</th></tr></thead><tbody>'
            + "".join(f'<tr><td>{a}</td><td class="mono">{c}</td><td class="mono">{d}</td><td class="{b}" style="{s};color:var(--ua-tinta)">{esc(e)}</td></tr>' for a, b, c, d, e, s in filas)
            + "</tbody></table>")


def comp_tipo_mini(**_):
    return ('<div class="tipo-mini" aria-hidden="true"><span class="ff-display" style="font-weight:800">Aa</span><span class="ff-display" style="font-weight:400">Aa</span>'
            '<span class="ff-mono" style="font-weight:700">θ</span><span class="ff-mono" style="font-weight:400">a·e</span></div>')


def comp_tokens(**_):
    grupos = [("EL SOL · .brand .dot", [c for c, _ in SOL if not c.startswith("#")]),
              ("SUPERFICIES Y TEXTO", ["ua-vacio", "ua-cosmos", "ua-estelar", "ua-polvo", "ua-tenue"]),
              ("ACENTOS", ["ua-orbita", "ua-nebulosa"]),
              ("TIERS", [TIER_COLOR[t] for t in "SABCD"])]
    lineas = []
    for g, ids in grupos:
        lineas.append(f'<span class="c-com">/* {g} */</span>')
        for i in dict.fromkeys(ids):
            lineas.append(f'<span class="c-var">--{i}</span>: {hexa(i)};')
    return '<pre class="codigo">' + "\n".join(lineas) + "</pre>"


def comp_pantalla(**_):
    return ('<div class="pantalla" aria-label="Arquitectura de la galería">'
            '<div class="pt-logo">Universo-Arena</div><div class="pt-nav">Recorrido · Podio · Galería · Hallazgos · Método</div>'
            '<div class="pt-side">Hero<br>Recorrido<br>Podio<br>Galería<br>Hallazgos<br>Método</div>'
            f'<div class="pt-main"><div>El Sol en el foco y el cometa · titular «Un prompt. {esc(DATOS["entregas"])} universos.»</div>'
            '<div class="pt-kpis"><span>Entregas</span><span>Criterios</span><span>Sin errores</span><span>Nota media</span></div>'
            f'<div>{esc(DATOS["entregas"])} tarjetas: captura real · nota · tier · objetos · líneas · errores</div><div>Ficha: radar · barras · fortalezas · demo</div></div></div>')


def comp_componentes(**_):
    tiers = "".join(f'<span class="sev-demo" style="background:{hexa(TIER_COLOR[t])};color:{hexa("ua-vacio")}">Tier {t}</span>' for t in "SABCD")
    b = BENCH[0]
    return ('<div class="comp-fila"><span class="btn-demo btn-marca">' + ico("orbita") + ' Ver el ranking</span><small>.btn-marca</small>'
            '<span class="btn-demo btn-claro">Explorar las entregas</span><small>.btn-claro</small>'
            '<span class="btn-demo btn-outline">▶ Abrir demo</span><small>.btn-outline</small></div>'
            f'<div class="comp-fila">{tiers}<small>Tier: color + letra</small></div>'
            '<div class="tarjeta card3d card-viva"><div class="c3-cab">Tarjeta de entrega <span class="muted-oscuro">(datos reales del #1)</span></div><div class="c3-cuerpo">'
            f'<p class="small" style="margin:0 0 .4em"><strong>{esc(b["modelo"])}</strong> · {esc(b["agente"])} · <strong>{b["total"]}</strong>/100 · tier {esc(b["tier"])}</p>'
            f'<p class="small muted" style="margin:0">{b["runtime"]["meshes"]} objetos · {b["lineas"]} líneas · {b["runtime"]["consoleErrors"]} errores de consola. '
            'Todo sale de assets/benchmark.json: la galería no escribe una cifra a mano.</p></div></div>')


def comp_senales(**_):
    return ('<div class="capas-op">' + "".join(
        f'<div class="capa-op" style="--capa:{hexa(s["color"])}"><span class="capa-letra">{esc(s["n"])}</span>'
        f'<div><strong>{esc(s["nombre"])}</strong><span class="mono">{esc(s["que"])}</span>'
        f'<p>{inline(esc(s["texto"]) + " {f:" + s["fuente"] + "}")}</p></div></div>' for s in ARENA["senales"]) + "</div>")


def comp_rubrica(**_):
    return ('<div class="modulos-op cinco">' + "".join(
        f'<div class="mod-op"><strong>{esc(c["nombre"])}</strong><span class="mono">{c["max"]} puntos · categoría {c["n"]}</span></div>'
        for c in RUBRICA) + "</div>"
        f'<p class="small muted">{len(RUBRICA)} categorías, {DATOS["puntos"]} puntos: leídas de la tabla de docs/rubric.md al construir {inline("{f:rubrica}")}.</p>')


def comp_tiers(**_):
    lectura = dict(ARENA["tiers_lectura"])
    return ('<div class="modulos-op cinco">' + "".join(
        f'<div class="mod-op" style="border-top:.3em solid {hexa(TIER_COLOR[t])}"><strong>Tier {t}</strong>'
        f'<span class="mono">{esc(r)} · {sum(1 for b in BENCH if b["tier"] == t)} entregas</span><p>{esc(lectura[t])}</p></div>'
        for t, r in TIERS) + "</div>")


def comp_artefactos(**_):
    return ('<div class="modulos-op dos">' + "".join(
        f'<div class="mod-op"><strong>{esc(e["nombre"])}</strong><span class="mono">{esc(e["id"])}</span><p>{esc(e["texto"])}</p></div>'
        for e in ARENA["artefactos"]) + "</div>")


def comp_cronologia(modo, **_):
    hitos = HITOS["hitos"]
    celdas = "".join(
        f'<div class="cr-hito{" creacion" if h["papel"] == "marca" else ""}"><span class="cr-fecha">{esc(h["fecha"])}</span>'
        f'<span class="cr-acto">{esc(h["acto"])}</span><p>{inline(h["resumen"] + " {f:" + h["fuente"] + "}")}</p></div>'
        for h in hitos)
    n = len(hitos) if modo == "inmersivo" else 4
    crono = f'<div class="crono" style="--n:{n};min-width:{len(hitos) * 11 if modo == "inmersivo" else 0}em">{celdas}</div>'
    if modo == "inmersivo":
        crono = f'<div class="crono-scroll" tabindex="0" role="region" aria-label="Cronología de Universo-Arena, desplazable">{crono}</div>'
    ley = ('<p class="crono-ley"><span><i style="background:var(--ua-orbita)"></i>Hito de marca</span>'
           '<span><i style="background:var(--ua-tinta)"></i>Hito del benchmark</span></p>')
    return crono + ley


def comp_og(**_):
    return ('<div class="og-tarjeta"><div class="og-cab">' + imago(oscuro=True) + '</div>'
            f'<p class="og-tit">Un prompt. {esc(DATOS["entregas"])} universos.</p>'
            '<p class="og-sub">Benchmark abierto de LLM + agente de código, juzgado por ejecución real.</p>'
            f'<p class="og-pie"><span>{esc(DATOS["categorias"])} criterios</span><span>{esc(DATOS["limpias"])} sin errores</span><b>universo-arena.alexanderoviedofadul.dev</b></p></div>')


def comp_ficha(**_):
    b = BENCH[0]
    return ('<div class="cab-informe"><span class="ci-firma"></span><div class="ci-cuerpo">' + imago(oscuro=True)
            + f'<p class="ci-tit">{esc(b["modelo"])} · {esc(b["agente"])}</p><p class="ci-meta mono">#{b["rank"]} · {b["total"]}/100 · {b["runtime"]["meshes"]} objetos · {b["lineas"]} líneas</p>'
            + "".join(f'<span class="sev-demo" style="background:{hexa(TIER_COLOR[t])};color:{hexa("ua-vacio")}">Tier {t}</span>' for t in b["tier"])
            + "</div></div>")


def comp_kpis(items, **_):
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><span class="kpi-v">{inline(esc(i["v"]))}</span><span class="kpi-l">{inline(esc(i["l"]))}</span></div>' for i in items) + "</div>"


def comp_bibliografia(desde=0, hasta=None, **_):
    out = ['<ol class="biblio" start="' + str(desde + 1) + '">']
    for f in FUENTES[desde:hasta]:
        url = f'<span class="mono biblio-url">{esc(f["url"])}</span>' if f.get("url") else ""
        out.append(f'<li id="fuente-{f["id"]}"><strong>{esc(f["autor"])}</strong>. <em>{esc(f["titulo"])}</em>. {esc(f["detalle"])}. {url}</li>')
    out.append("</ol>")
    return "".join(out)


COMPONENTES = {
    "portada": comp_portada, "contraportada": comp_contraportada, "indice": comp_indice,
    "isotipo": comp_isotipo, "isotipo-oscuro": comp_isotipo_oscuro, "lema": comp_lema,
    "anatomia": comp_anatomia, "construccion": comp_construccion, "variantes": comp_variantes,
    "lockups": comp_lockups, "proteccion": comp_proteccion, "minimos": comp_minimos,
    "incorrectos": comp_incorrectos, "favicon": comp_favicon, "orbita": comp_orbita,
    "paleta": comp_paleta, "degradados": comp_degradados, "contraste": comp_contraste, "retirados": comp_retirados,
    "paleta-mini": comp_paleta_mini, "fondos": comp_fondos,
    "especimen": comp_especimen, "escala": comp_escala, "tipo-mini": comp_tipo_mini, "tokens": comp_tokens,
    "pantalla": comp_pantalla, "componentes": comp_componentes, "senales": comp_senales, "rubrica": comp_rubrica,
    "tiers": comp_tiers, "artefactos": comp_artefactos, "cronologia": comp_cronologia,
    "og": comp_og, "ficha": comp_ficha, "kpis": comp_kpis, "bibliografia": comp_bibliografia,
}

# ─────────────────────────────────────────────────────────────────────────────
# Bloques de contenido (mismo vocabulario que KANSA v6, ENKI v2, Maloca v2, Isabella v2 y Pentest v1)
# ─────────────────────────────────────────────────────────────────────────────


def bloque(b, ctx):
    t = b["t"]
    if t == "eyebrow":
        return f'<p class="eyebrow">{inline(b["x"])}</p>'
    if t in ("h2", "h3"):
        return f'<{t} data-revelar>{inline(b["x"])}</{t}>'
    if t == "p":
        return f'<p class="{b.get("c", "")}" data-revelar>{inline(b["x"])}</p>'
    if t == "lista":
        tag = "ol" if b.get("c") == "num" else "ul"
        return f'<{tag} class="lista {b.get("c", "")}" data-revelar>' + "".join(f"<li>{inline(i)}</li>" for i in b["items"]) + f"</{tag}>"
    if t == "nota":
        tit = f'<strong class="nota-tit">{inline(b["titulo"])}</strong>' if b.get("titulo") else ""
        return f'<aside class="nota nota-{b.get("tono", "azul")}" data-revelar>{tit}<p>{inline(b["x"])}</p></aside>'
    if t == "tabla":
        cab = "".join(f"<th>{inline(c)}</th>" for c in b["cab"])
        filas = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in f) + "</tr>" for f in b["filas"])
        return f'<table class="tabla {b.get("c", "")}" data-revelar><thead><tr>{cab}</tr></thead><tbody>{filas}</tbody></table>'
    if t == "cols":
        cols = "".join(f'<div class="col">{"".join(bloque(x, ctx) for x in c)}</div>' for c in b["cols"])
        return f'<div class="cols" style="--cols:{b.get("r", "1fr 1fr")}">{cols}</div>'
    if t == "grid":
        items = "".join(
            (bloque(it, ctx) if isinstance(it, dict) else
             '<div class="celda">' + "".join(bloque(x, ctx) for x in it) + "</div>")
            for it in b["items"])
        return f'<div class="grid g{b.get("n", 3)}">{items}</div>'
    if t == "tarjeta":
        sub = f'<span class="tar-sub">{inline(b["sub"])}</span>' if b.get("sub") else ""
        viva = " card-viva" if ctx["modo"] == "inmersivo" else ""
        return (f'<div class="tarjeta tono-{b.get("tono", "neutro")}{viva}" data-revelar><strong class="tar-tit">{inline(b["titulo"])}</strong>'
                f'{sub}<p>{inline(b["x"])}</p></div>')
    if t == "comp":
        args = {k: v for k, v in b.items() if k not in ("t", "n")}
        return COMPONENTES[b["n"]](modo=ctx["modo"], caps=ctx["caps"], **args)
    if t == "sep":
        return '<hr class="sep">'
    raise SystemExit(f"Tipo de bloque desconocido: {t}")


# ─────────────────────────────────────────────────────────────────────────────
# Capítulos y páginas
# ─────────────────────────────────────────────────────────────────────────────

def cargar_capitulos():
    caps = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CONTENIDO.glob("[0-9][0-9]_*.json"))]
    pag = 1
    for c in caps:
        c["_pag_ini"] = pag
        pag += len(c["paginas"])
    return caps, pag - 1


def portadilla(c, pg, ctx):
    fig = ""
    if pg.get("fig"):
        fig = f'<div class="porta-fig">{bloque({"t": "comp", "n": pg["fig"]}, ctx)}</div>'
    lead = f'<p class="porta-lead">{inline(c["lead"])}</p>' if c.get("lead") else ""
    extra = "".join(bloque(b, ctx) for b in pg.get("bloques", []))
    return (f'<div class="porta"><div class="porta-texto"><p class="porta-num">{esc(c["num"])}</p>'
            f'<p class="eyebrow">{esc(c["kicker"])}</p><h2 class="porta-tit" data-titulo>{esc(c["titulo"])}</h2>'
            f'{lead}{extra}</div>{fig}</div>')


def render_impresion(caps, total):
    ctx = {"modo": "impresion", "caps": caps}
    out = []
    n = 0
    for c in caps:
        for i, pg in enumerate(c["paginas"]):
            n += 1
            plantilla_ = pg.get("plantilla", "libre")
            tono = pg.get("tono", "claro" if plantilla_ == "libre" else "noche")
            ancla = f' id="cap-{c["id"]}"' if i == 0 else ""
            cuerpo = portadilla(c, pg, ctx) if plantilla_ == "portadilla" else "".join(bloque(b, ctx) for b in pg["bloques"])
            cabecera = ("" if plantilla_ == "portada" else
                        f'<header class="pg-cab"><span>{SELLO_PIE}</span>'
                        f'<span>{esc(c["num"])} · {esc(c["corto"])}</span></header>')
            pie = "" if plantilla_ == "portada" else f'<footer class="pg-pie"><span class="pg-n">{n:02d}</span></footer>'
            densa = " densa" if pg.get("densa") else (" amplia" if pg.get("amplia") else "")
            out.append(f'<section class="page plantilla-{plantilla_} sup-{tono}{densa}"{ancla} data-pagina="{n}">'
                       f'{cabecera}<div class="pg-cuerpo">{cuerpo}</div>{pie}</section>')
    assert n == total
    return "\n".join(out)


def render_inmersivo(caps):
    ctx = {"modo": "inmersivo", "caps": caps}
    out = []
    for c in caps:
        laminas = []
        for pg in c["paginas"]:
            plantilla_ = pg.get("plantilla", "libre")
            tono = pg.get("tono", "claro" if plantilla_ == "libre" else "noche")
            cuerpo = portadilla(c, pg, ctx) if plantilla_ == "portadilla" else "".join(bloque(b, ctx) for b in pg["bloques"])
            laminas.append(f'<div class="lamina plantilla-{plantilla_} sup-{tono}">{cuerpo}</div>')
        out.append(f'<section class="escena" id="cap-{c["id"]}" data-escena="{esc(c["num"])}"'
                   f' data-titulo-escena="{esc(c["corto"])}" aria-label="{esc(c["num"])} · {esc(c["titulo"])}">'
                   + "".join(laminas) + "</section>")
    return "\n".join(out)


def nav_items(caps):
    return "".join(
        f'<li><a href="#cap-{c["id"]}" data-ir="cap-{c["id"]}"><span class="rail-num">{esc(c["num"])}</span>'
        f'<span class="rail-tit">{esc(c["corto"])}</span></a></li>' for c in caps)


# ─────────────────────────────────────────────────────────────────────────────
# Ensamblado de salidas
# ─────────────────────────────────────────────────────────────────────────────

SCRIPTS_INMERSIVO = [
    "assets/js/vendor/gsap.min.js", "assets/js/vendor/ScrollTrigger.min.js",
    "assets/js/vendor/ScrollToPlugin.min.js", "assets/js/vendor/SplitText.min.js",
    "assets/js/ua-v1-bucle.js", "assets/js/ua-v1-orbita.js", "assets/js/ua-v1-nucleo.js",
]
TIPOS_IMG = {".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".webp": "image/webp"}


def css_con_fuentes_inline(css_rel, dir_fuentes):
    css = leer(css_rel)

    def rep(m):
        b64 = base64.b64encode((BASE / dir_fuentes / m.group(1)).read_bytes()).decode("ascii")
        return f"url(data:font/woff2;base64,{b64}) format('woff2')"
    return re.sub(r"url\('([^']+\.woff2)'\)\s*format\('woff2'\)", rep, css)


def js_seguro(s):
    return s.replace("</script", "<\\/script")


def plantilla(nombre, **vals):
    s = leer(f"plantillas/{nombre}")
    for k, v in vals.items():
        s = s.replace("{{" + k + "}}", v)
    resto = re.findall(r"\{\{[A-Z_]+\}\}", s)
    if resto:
        raise SystemExit(f"Marcadores sin rellenar en {nombre}: {resto}")
    return s


WEB = REPO / "assets" / "marca"


def exportar_web():
    """Lo que la galería usa de la marca, copiado desde aquí (no editar allí): tokens, woff2 y logos."""
    (WEB / "fuentes").mkdir(parents=True, exist_ok=True)
    (WEB / "logos").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(BASE / "assets/data/tokens-v1.css", WEB / "tokens-v1.css")
    for f in ("inter-var.woff2", "jetbrainsmono-400.woff2"):
        shutil.copyfile(BASE / "assets/fonts" / f, WEB / "fuentes" / f)
    for f in ("ua-simbolo.svg", "ua-horizontal-negativo.svg", "ua-horizontal.svg", "favicon-32.png", "apple-touch-icon.png"):
        shutil.copyfile(BASE / "assets/logos" / f, WEB / "logos" / f)


def raiz_css():
    """El :root del CSS base se reescribe desde la paleta: el audit lo compara con los tokens."""
    p = BASE / "assets/css/ua-v1-base.css"
    css = p.read_text(encoding="utf-8")
    ids = list(COLORES)
    lineas = []
    for i in range(0, len(ids), 4):
        lineas.append("  " + " ".join(f"--{k}: {COLORES[k]['hex']};" for k in ids[i:i + 4]))
    bloque_ = "  /* Paleta cerrada: contenido/paleta.json (la escribe build_v1.py). */\n" + "\n".join(lineas) + "\n"
    nuevo = re.sub(r"(:root \{\n)(.*?)(  --blanco: #FFFFFF;)", lambda m: m.group(1) + bloque_ + m.group(3), css, count=1, flags=re.S)
    if nuevo != css:
        p.write_text(nuevo, encoding="utf-8")


def main():
    generar_logos()
    exportar_tokens()
    raiz_css()
    exportar_web()
    caps, total = cargar_capitulos()

    _contador_svg["n"] = _contador_port["n"] = _contador_ov["n"] = 0
    imp = plantilla("impresion.html.tpl", PAGINAS=render_impresion(caps, total), TOTAL=str(total), VERSION=VERSION)
    (BASE / "impresion.html").write_text(imp, encoding="utf-8")

    _contador_svg["n"] = _contador_port["n"] = _contador_ov["n"] = 0
    escenas = render_inmersivo(caps)
    scripts = "\n".join(f'<script src="{s}"></script>' for s in SCRIPTS_INMERSIVO)
    idx = plantilla("inmersivo.html.tpl", ESCENAS=escenas, NAV=nav_items(caps), SCRIPTS=scripts,
                    ISOTIPO_CAB=svg_en_linea("ua-simbolo.svg"), VERSION=VERSION, TOTAL=str(total))
    (BASE / "index.html").write_text(idx, encoding="utf-8")

    port = idx.replace('<link rel="stylesheet" href="assets/fonts/fonts.css">',
                       "<style>\n" + css_con_fuentes_inline("assets/fonts/fonts.css", "assets/fonts") + "\n</style>")
    for css in ["assets/css/ua-v1-base.css", "assets/css/ua-v1-inmersivo.css"]:
        etiqueta = f'<link rel="stylesheet" href="{css}">'
        if etiqueta not in port:
            raise SystemExit(f"Falta {etiqueta} en la plantilla")
        port = port.replace(etiqueta, "<style>\n" + leer(css) + "\n</style>")
    for s in SCRIPTS_INMERSIVO:
        port = port.replace(f'<script src="{s}"></script>', "<script>\n" + js_seguro(leer(s)) + "\n</script>")
    for rel in sorted(IMAGENES):
        datos = base64.b64encode((BASE / "assets" / rel).read_bytes()).decode("ascii")
        port = port.replace(f'src="assets/{rel}"', f'src="data:{TIPOS_IMG[Path(rel).suffix]};base64,{datos}"')
    port = re.sub(r'\s*<link rel="icon"[^>]*>', "", port)
    port = port.replace('href="impresion.html"', 'href="Manual_Marca_UniversoArena_v1.pdf"')
    sello = ("<!-- ═══ Universo-Arena v1.0 · PORTABLE AUTOCONTENIDO ═══\n"
             "     GENERADO por scripts/build_v1.py desde contenido/ + plantillas/ + assets/ + assets/benchmark.json.\n"
             "     No editar a mano. Tipografías, estilos, librerías (GSAP), logos e imágenes incrustados. -->\n")
    port = port.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + sello, 1)
    (BASE / PORTABLE).write_text(port, encoding="utf-8")

    for n in ("impresion.html", "index.html", PORTABLE, "assets/data/tokens-v1.css", "assets/logos/ua-simbolo.svg"):
        p = BASE / n
        print(f"OK → {n:34s} {p.stat().st_size / 1024:8.1f} KB  sha256 {hashlib.sha256(p.read_bytes()).hexdigest()[:12]}")
    print(f"Páginas: {total} · Capítulos: {len(caps)} · Colores: {len(COLORES)} · Entregas leídas: {len(BENCH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
