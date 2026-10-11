#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_v1.py — Barrera de calidad del Manual de Marca Universo-Arena v1.0.
Copiada del audit_v1.py de Pentest C360 v1.0 (← Flyn.sh v1.0 ← Isabella EA v2.0 ← Maloca v2.0 → ENKI v2.0 → KANSA v6.0),
sin audio. Se audita TODO:

  impresión   desborde de cada elemento (incluidos SVG) fuera del cuerpo de la
              página · logos dentro de su caja y dibujo dentro de su viewBox ·
              solape entre líneas de texto · ids duplicados · páginas = total
  ejecución   cero errores de consola, cero excepciones y cero peticiones que no
              sean file:/data: (index.html, portable e impresion.html)
  inmersivo   0 AudioContext (sin audio) · como mucho 1 bucle
              requestAnimationFrame activo · movimiento reducido = órbita estática
              y nada sin revelar · Cmd/Ctrl+tecla no se intercepta · índice con Esc
  fuentes     document.fonts.check de cada familia + cobertura de glifos (fontTools)
  portable    ≤ 2,5 MB, sin recursos externos ni rutas a assets/ · build determinista
  datos       hitos con fuente · benchmark coherente (rúbrica de 10 categorías y 100 puntos, totales =
              suma del desglose, tier = el de su nota, carpetas y capturas, llms.txt y sitemap.xml) ·
              Sol maestro = .brand .dot de la galería anterior (8acc8ef) · lista negra (cifras escritas
              a mano, promesas, CDN) · tokens del CSS = paleta · favicons con su tamaño ·
              copias de assets/marca/ = las del manual

Sale con código 1 si algo falla. Uso: python3 docs/Manual_Marca_UniversoArena/v1.0/scripts/audit_v1.py
"""
import hashlib
import os
import json
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent.parent
REPO = BASE.parents[2]
CHROME = os.environ.get("CHROME_PATH", '/root/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome')
FALLOS, AVISOS = [], []


def fallo(m):
    FALLOS.append(m)
    print("  ✗", m)


def ok(m):
    print("  ✓", m)


JS_PAGINAS = r"""() => {
  const out = { desbordes: [], logos: [], solapes: [], paginas: 0 };
  const T = 1.5;
  const fuera = (r, c) => Math.max(r.bottom - c.bottom, r.right - c.right, c.left - r.left, c.top - r.top);
  const recortados = '.inc-fig, .portada-fondo, .orbita-vivo, .paleta-mini, .captura, .pantalla, .bn-fondo';
  document.querySelectorAll('section.page').forEach(pg => {
    out.paginas++;
    const n = pg.dataset.pagina;
    const cuerpo = (pg.querySelector('.pg-cuerpo') || pg).getBoundingClientRect();
    const limite = pg.classList.contains('plantilla-portada') ? pg.getBoundingClientRect() : cuerpo;
    pg.querySelectorAll('.pg-cuerpo *').forEach(el => {
      if (el.closest(recortados) && !el.matches(recortados)) return;
      const r = el.getBoundingClientRect();
      if (!r.width && !r.height) return;
      const o = fuera(r, limite);
      if (o > T) out.desbordes.push(`p${n} ${el.tagName.toLowerCase()}.${String(el.className.baseVal ?? el.className).split(' ')[0]} sale ${o.toFixed(1)}px: «${(el.textContent || '').trim().slice(0, 40)}»`);
    });
    pg.querySelectorAll('[data-logo]').forEach(caja => {
      const svg = caja.querySelector('svg'); if (!svg) return;
      const rs = svg.getBoundingClientRect(), rc = caja.getBoundingClientRect();
      if (!caja.closest('.inc-fig') && fuera(rs, rc) > T) out.logos.push(`p${n} ${caja.dataset.logo}: el svg sale de su caja`);
      const vb = svg.viewBox.baseVal, bb = svg.getBBox();
      if (bb.x < vb.x - .5 || bb.y < vb.y - .5 || bb.x + bb.width > vb.x + vb.width + .5 || bb.y + bb.height > vb.y + vb.height + .5)
        out.logos.push(`p${n} ${caja.dataset.logo}: dibujo fuera del viewBox (${bb.x.toFixed(0)},${bb.y.toFixed(0)},${(bb.x + bb.width).toFixed(0)},${(bb.y + bb.height).toFixed(0)})`);
      const tarjeta = caja.closest('.var-card, .fondo-card, .lock, .fav, .min-fila, .anat-fig, .evolucion figure');
      if (tarjeta && fuera(rs, tarjeta.getBoundingClientRect()) > T) out.logos.push(`p${n} ${caja.dataset.logo}: el logo se sale de su tarjeta`);
      if (rs.width < 8 || rs.height < 6) out.logos.push(`p${n} ${caja.dataset.logo}: tamaño ${rs.width.toFixed(0)}×${rs.height.toFixed(0)} px demasiado pequeño`);
    });
    // Solapes entre líneas de texto de nodos distintos
    const lineas = [];
    const w = document.createTreeWalker(pg, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const t = w.currentNode;
      if (!t.textContent.trim() || t.parentElement.closest('svg, .inc-fig, [aria-hidden="true"]')) continue;
      const rg = document.createRange(); rg.selectNodeContents(t);
      for (const r of rg.getClientRects()) if (r.width > 1 && r.height > 1) lineas.push({ r, t });
    }
    for (let i = 0; i < lineas.length; i++) for (let j = i + 1; j < lineas.length; j++) {
      const a = lineas[i], b = lineas[j];
      if (a.t === b.t) continue;
      const ix = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
      const iy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
      if (ix > 2 && iy > Math.min(a.r.height, b.r.height) * 0.45)
        out.solapes.push(`p${n} «${a.t.textContent.trim().slice(0, 28)}» × «${b.t.textContent.trim().slice(0, 28)}»`);
    }
  });
  const ids = {}; document.querySelectorAll('[id]').forEach(e => { ids[e.id] = (ids[e.id] || 0) + 1; });
  out.duplicados = Object.entries(ids).filter(([, c]) => c > 1).map(([k, c]) => `${k}×${c}`);
  return out;
}"""

JS_FUENTES = """() => ['800 20px Inter', '400 16px Inter', '400 14px "JetBrains Mono"',
  '700 14px "JetBrains Mono"'].map(f => [f, document.fonts.check(f)])"""

SONDA = """
(() => {
  window.__e2 = { ctx: 0, porFn: new Map(), contar: false };
  for (const n of ['AudioContext', 'webkitAudioContext']) {
    const O = window[n]; if (!O) continue;
    window[n] = function (...a) { window.__e2.ctx++; return new O(...a); };
    window[n].prototype = O.prototype;
  }
  /* Un «bucle» es una función que se vuelve a programar fotograma tras fotograma:
     se cuenta cuántas veces se programa cada función durante la ventana. */
  const raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function (fn) {
    if (window.__e2.contar) window.__e2.porFn.set(fn, (window.__e2.porFn.get(fn) || 0) + 1);
    return raf(fn);
  };
  /* _rafBugFix: bucle interno de ScrollTrigger (sortea un fallo de Chrome); no es de la app. */
  window.__e2bucles = () => [...window.__e2.porFn.entries()].filter(([f, n]) => n >= 20 && f.name !== '_rafBugFix').length;
})();
"""


def abrir(nav, url, movimiento="no-preference", viewport=(1440, 900)):
    ctx = nav.new_context(viewport={"width": viewport[0], "height": viewport[1]}, reduced_motion=movimiento)
    pag = ctx.new_page()
    errores, externas = [], []
    pag.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
    pag.on("pageerror", lambda e: errores.append(str(e)))

    def filtro(route):
        if route.request.url.startswith(("file:", "data:")):
            route.continue_()
        else:
            externas.append(route.request.url)
            route.abort()
    pag.route("**/*", filtro)
    pag.add_init_script(SONDA)
    pag.goto(url)
    return ctx, pag, errores, externas


def auditar_impresion(nav):
    print("\n▸ Impresión (impresion.html)")
    html = (BASE / "impresion.html").read_text(encoding="utf-8")
    total = int(re.search(r'data-total="(\d+)"', html).group(1))
    ctx, pag, errores, externas = abrir(nav, (BASE / "impresion.html").as_uri(), viewport=(1200, 900))
    pag.wait_for_function("window.UA_LISTO === true", timeout=30000)
    pag.emulate_media(media="print")
    r = pag.evaluate(JS_PAGINAS)
    (ok if r["paginas"] == total else fallo)(f"páginas: {r['paginas']} de {total}")
    for k, nombre in [("desbordes", "desbordes"), ("logos", "logos fuera de caja/viewBox"), ("solapes", "solapes de texto"), ("duplicados", "ids duplicados")]:
        if r[k]:
            fallo(f"{nombre}: {len(r[k])}")
            for x in r[k][:25]:
                print("      ·", x)
        else:
            ok(f"{nombre}: 0")
    for f, v in pag.evaluate(JS_FUENTES):
        (ok if v else fallo)(f"fuente {f}: {'cargada' if v else 'NO cargada'}")
    (fallo if errores else ok)(f"errores de consola: {len(errores)} {errores[:3]}")
    (fallo if externas else ok)(f"peticiones externas: {len(externas)} {externas[:3]}")
    ctx.close()


def auditar_inmersivo(nav, archivo):
    print(f"\n▸ Inmersivo ({archivo})")
    url = (BASE / archivo).as_uri()
    ctx, pag, errores, externas = abrir(nav, url)
    pag.wait_for_function("window.UA_V1 && window.UA_V1.listo === true", timeout=30000)
    pag.wait_for_timeout(1200)
    pag.mouse.wheel(0, 2400); pag.wait_for_timeout(600)
    (ok if pag.evaluate("window.__e2.ctx") == 0 else fallo)(f"AudioContext antes del gesto: {pag.evaluate('window.__e2.ctx')}")
    # Bucle único: como mucho 1 rAF en vuelo, medido mientras la órbita viva está visible
    pag.evaluate("document.querySelector('.orbita-vivo').scrollIntoView()"); pag.wait_for_timeout(900)
    pag.evaluate("window.__e2.porFn.clear(); window.__e2.contar = true"); pag.wait_for_timeout(1500)
    raf = pag.evaluate("window.__e2.contar = false, window.__e2bucles()")
    animado = pag.evaluate("document.documentElement.dataset.orbita")
    (ok if raf <= 1 else fallo)(f"bucles de animación activos con la órbita visible ({animado}): {raf}")
    # Atajos: Cmd/Ctrl + tecla no deben interceptarse
    prevenido = pag.evaluate("""() => { const e = new KeyboardEvent('keydown', {key: 'i', metaKey: true, ctrlKey: true, bubbles: true, cancelable: true});
                                document.body.dispatchEvent(e); return e.defaultPrevented; }""")
    (fallo if prevenido else ok)(f"Cmd/Ctrl+I interceptado: {prevenido}")
    abierto = pag.evaluate("!document.querySelector('#indice').hidden")
    (fallo if abierto else ok)(f"el índice NO se abre con Cmd/Ctrl+I: {not abierto}")
    pag.keyboard.press("i"); pag.wait_for_timeout(250)
    abierto = pag.evaluate("!document.querySelector('#indice').hidden")
    foco_dentro = pag.evaluate("document.querySelector('#indice').contains(document.activeElement)")
    (ok if abierto and foco_dentro else fallo)(f"tecla I abre el índice con el foco dentro: {abierto and foco_dentro}")
    pag.keyboard.press("Escape"); pag.wait_for_timeout(250)
    (ok if pag.evaluate("document.querySelector('#indice').hidden") else fallo)("Esc cierra el índice")
    pag.keyboard.press("m"); pag.wait_for_timeout(300)
    n = pag.evaluate("window.__e2.ctx")
    (ok if n == 0 else fallo)(f"AudioContext tras pulsar M (no debe haber audio): {n}")
    for f, v in pag.evaluate(JS_FUENTES):
        (ok if v else fallo)(f"fuente {f}")
    ids = pag.evaluate("() => { const c = {}; document.querySelectorAll('[id]').forEach(e => c[e.id] = (c[e.id] || 0) + 1); return Object.entries(c).filter(([, n]) => n > 1).map(([k]) => k); }")
    (fallo if ids else ok)(f"ids duplicados: {ids[:8]}")
    (fallo if errores else ok)(f"errores de consola: {len(errores)} {errores[:3]}")
    (fallo if externas else ok)(f"peticiones externas: {len(externas)} {externas[:3]}")
    ctx.close()
    # Movimiento reducido: órbita estática y contenido visible sin animar
    ctx, pag, errores, _ = abrir(nav, url, movimiento="reduce")
    pag.wait_for_function("window.UA_V1 && window.UA_V1.listo === true", timeout=30000)
    estado = pag.evaluate("document.documentElement.dataset.orbita")
    (ok if estado == "estatico" else fallo)(f"movimiento reducido → órbita {estado}")
    ocultos = pag.evaluate("[...document.querySelectorAll('[data-revelar]')].filter(e => getComputedStyle(e).opacity < .99).length")
    (ok if ocultos == 0 else fallo)(f"movimiento reducido → elementos sin revelar: {ocultos}")
    (fallo if errores else ok)(f"errores (movimiento reducido): {len(errores)}")
    ctx.close()


def auditar_portable():
    print("\n▸ Portable y determinismo")
    p = BASE / "UniversoArena_Inmersivo_v1.html"
    s = p.read_text(encoding="utf-8")
    mb = p.stat().st_size / 1024 / 1024
    (ok if mb <= 2.5 else fallo)(f"tamaño del portable: {mb:.2f} MB (≤ 2,5)")
    externos = re.findall(r'(?:src|href)="(?:https?:)?//[^"]+"', s)
    (fallo if externos else ok)(f"recursos externos en el portable: {externos[:3]}")
    rutas = re.findall(r'(?:src|href)="assets/[^"]+"', s)
    (fallo if rutas else ok)(f"rutas a assets/ en el portable: {rutas[:3]}")
    salidas = ("index.html", "impresion.html", "UniversoArena_Inmersivo_v1.html", "assets/data/tokens-v1.css", "assets/data/tokens_v1.json",
               "assets/logos/ua-simbolo.svg", "assets/logos/ua-horizontal.svg", "assets/logos/ua-vertical.svg")
    antes = {n: hashlib.sha256((BASE / n).read_bytes()).hexdigest() for n in salidas}
    subprocess.run([sys.executable, "-B", str(BASE / "scripts" / "build_v1.py")], check=True, capture_output=True)
    despues = {n: hashlib.sha256((BASE / n).read_bytes()).hexdigest() for n in antes}
    (ok if antes == despues else fallo)("build determinista (dos ejecuciones = mismos bytes)")


def auditar_datos():
    print("\n▸ Datos del benchmark, marca y lista negra")
    h = json.loads((BASE / "contenido" / "hitos.json").read_text(encoding="utf-8"))["hitos"]
    fuentes = {f["id"] for f in json.loads((BASE / "contenido" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]}
    sin = [x["acto"] for x in h if x["fuente"] not in fuentes]
    (fallo if sin else ok)(f"hitos de la cronología con fuente: {len(h) - len(sin)} de {len(h)}")
    # El benchmark que se cita es coherente: lo que el manual y la galería leen
    bench = json.loads((REPO / "assets/benchmark.json").read_text(encoding="utf-8"))
    rub = re.findall(r"^\|\s*(\d+)\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*(\d+)\s*\|", (REPO / "docs/rubric.md").read_text(encoding="utf-8"), flags=re.M)
    cortes = dict(re.findall(r"\*\*([SABCD])\*\* \(([^)]+)\)", (REPO / "docs/methodology.md").read_text(encoding="utf-8")))
    def tier_de(n):
        for t, r in cortes.items():
            nums = [int(x) for x in re.findall(r"\d+", r)]
            if ("≥" in r and n >= nums[0]) or ("<" in r and n < nums[0]) or (len(nums) == 2 and nums[0] <= n <= nums[1]):
                return t
    reglas = [
        ("la rúbrica tiene 10 categorías y suma 100", len(rub) == 10 and sum(int(x[2]) for x in rub) == 100),
        ("cada entrega puntúa las mismas 10 categorías", all(len(b["scores"]) == len(rub) for b in bench)),
        ("total de cada entrega = suma de su desglose", all(sum(b["scores"].values()) == b["total"] for b in bench)),
        ("tier de cada entrega = el de su nota según methodology.md", all(tier_de(b["total"]) == b["tier"] for b in bench)),
        ("ranking ordenado y sin huecos (rank 1..n)", [b["rank"] for b in bench] == list(range(1, len(bench) + 1)) and all(bench[i]["total"] >= bench[i + 1]["total"] for i in range(len(bench) - 1))),
        ("cada entrega tiene su carpeta con index.html y su captura", all((REPO / b["folder"] / "index.html").exists() and (REPO / b["preview"]).exists() for b in bench)),
    ]
    carpetas = {b["folder"] for b in bench}
    llms = (REPO / "llms.txt").read_text(encoding="utf-8")
    smap = (REPO / "sitemap.xml").read_text(encoding="utf-8")
    reglas.append(("llms.txt enlaza las mismas carpetas que benchmark.json", set(re.findall(r"alexanderoviedofadul\.dev/([^/\s]+)/index\.html", llms)) == carpetas))
    reglas.append(("sitemap.xml lista las mismas carpetas que benchmark.json", set(re.findall(r"<loc>https://universo-arena\.alexanderoviedofadul\.dev/([^/<]+)/index\.html</loc>", smap)) == carpetas))
    # La galería (index.html de la raíz) es la generada desde estos mismos datos
    gal = (REPO / "index.html").read_text(encoding="utf-8")
    scripts_linea = [m for m in re.findall(r"<script(?![^>]*\bsrc=)([^>]*)>", gal) if "application/ld+json" not in m]
    reglas += [
        ("la galería la genera scripts/generar_galeria.py", "GENERADO por scripts/generar_galeria.py" in gal),
        ("la galería no ejecuta scripts en línea (CSP sin unsafe-inline)", not scripts_linea),
        ("la galería tiene una tarjeta y un enlace a la demo por entrega", gal.count('<article class="tarjeta"') == len(bench)
         and all(f'href="{b["folder"]}/index.html"' in gal for b in bench)),
        ("la galería no pide nada a otro dominio al cargar", not re.search(r'(?:src|href)="https?://(?!universo-arena\.alexanderoviedofadul\.dev)[^"]+\.(?:js|css|woff2?)"', gal)),
    ]
    for txt, v in reglas:
        (ok if v else fallo)(txt)
    # El Sol = .brand .dot de la galería anterior (commit 8acc8ef), parada por parada
    try:
        viejo = subprocess.run(["git", "-C", str(REPO), "show", "8acc8ef:index.html"], capture_output=True, text=True, check=True).stdout
        regla = re.search(r"\.brand \.dot\{([^}]+)\}", viejo).group(1)
        grad = re.search(r"radial-gradient\(circle at 35% 30%,([^)]+)\)", regla).group(1)
        paradas = [x.strip().split() for x in grad.split(",")]
        esperado = [["#fff"], ["#ffd24a", "30%"], ["#ff7a3c", "65%"], ["#7a1d00"]]
        sim = (BASE / "assets/logos/ua-simbolo.svg").read_text(encoding="utf-8")
        stops = re.findall(r'<stop offset="([\d.]+)" stop-color="(#[0-9A-F]{6})"/>', sim)
        (ok if paradas == esperado and stops == [("0", "#FFFFFF"), ("0.3", "#FFD24A"), ("0.65", "#FF7A3C"), ("1", "#7A1D00")]
         and 'cx="35" cy="30"' in sim and "width:26px;height:26px;border-radius:50%" in regla else fallo)(
            f"el Sol maestro = .brand .dot de 8acc8ef (4 paradas, brillo en 35 % 30 %, disco): {stops}")
    except (subprocess.CalledProcessError, AttributeError) as e:
        fallo(f"no se pudo leer la galería anterior (8acc8ef): {e}")
    # Copias en assets/marca: idénticas a las del manual (las escribe build_v1.py)
    web = REPO / "assets/marca"
    pares = [(BASE / "assets/data/tokens-v1.css", web / "tokens-v1.css")] + [
        (BASE / "assets/fonts" / f, web / "fuentes" / f) for f in ("inter-var.woff2", "jetbrainsmono-400.woff2")] + [
        (BASE / "assets/logos" / f, web / "logos" / f) for f in ("ua-simbolo.svg", "ua-horizontal-negativo.svg", "ua-horizontal.svg", "favicon-32.png", "apple-touch-icon.png")]
    distintas = [b.name for a, b in pares if not b.exists() or a.read_bytes() != b.read_bytes()]
    (fallo if distintas else ok)(f"tokens, fuentes y logos de assets/marca = los del manual: {distintas or 'ok'}")
    try:
        from PIL import Image
        mal = []
        for nombre, px in [("favicon-16.png", 16), ("favicon-32.png", 32), ("apple-touch-icon.png", 180), ("icono-192.png", 192), ("icono-512.png", 512)]:
            tam = Image.open(BASE / "assets/logos" / nombre).size
            if tam != (px, px):
                mal.append(f"{nombre} {tam}")
        (fallo if mal else ok)(f"favicons e iconos con su tamaño: {mal or 'ok'}")
    except ImportError:
        AVISOS.append("Pillow no disponible: favicons sin medir")
    def sin_notas(o):
        if isinstance(o, dict):
            return {k: sin_notas(v) for k, v in o.items() if not k.startswith("_")}
        if isinstance(o, list):
            return [sin_notas(v) for v in o]
        return o
    def cadenas(o):
        if isinstance(o, dict):
            for v in o.values(): yield from cadenas(v)
        elif isinstance(o, list):
            for v in o: yield from cadenas(v)
        elif isinstance(o, str):
            yield o
    excluidos = {"paleta.json", "fuentes.json", "hitos.json"}  # documentan lo retirado, de dónde sale y cuántas había en cada fecha
    textos = []
    for pth in (BASE / "contenido").glob("*.json"):
        if pth.name in excluidos:
            continue
        textos.extend(cadenas(sin_notas(json.loads(pth.read_text(encoding="utf-8")))))
    textos = "\n".join(textos)
    # «Así no» de la tabla de tono: se cita para retirarlo
    citas = ["El mejor modelo del mundo", "La IA ya programa sola", "GPT gana a Claude", "Evolution Hub"]
    for c in citas:
        textos = textos.replace(c, "", 1)
    negra = {r"\b\d+\s+(entregas|universos|combinaciones|entradas)\b": "las cifras del benchmark se leen con {d:…}, no se escriben",
             r"100 ?%": "sin promesas totales (salvo «100 % K», la tinta de impresión)",
             r"[Ee]volution [Hh]ub|mejor modelo|gana a": "la arena no opina: mide",
             r"bladealex9848": "usuario de GitHub anterior: nombre libre",
             r"fonts\.googleapis|cdn\.jsdelivr|unpkg": "sin CDN ni Google Fonts",
             r"Lorem|ipsum": "sin relleno"}
    textos = re.sub(r"100 % K", "", textos)
    for mal, bien in negra.items():
        (fallo if re.search(mal, textos) else ok)(f"/{mal}/ ausente (→ {bien})")
    html_ = (BASE / "index.html").read_text(encoding="utf-8")
    (fallo if "fonts.googleapis" in html_ or "fonts.gstatic" in html_ else ok)("sin Google Fonts en el recorrido")
    imgs = sorted(p.name for p in (BASE / "assets" / "img").glob("*"))
    usadas = sorted(set(re.findall(r'src="assets/img/([^"]+)"', html_)))
    (ok if imgs == usadas else fallo)(f"imágenes en assets/img = imágenes usadas ({len(imgs)}): {set(imgs) ^ set(usadas) or 'ok'}")
    # Tokens: el :root del CSS base debe coincidir con la paleta generada
    tokens = dict(re.findall(r"--([a-z0-9-]+): (#[0-9A-F]{6});", (BASE / "assets/data/tokens-v1.css").read_text(encoding="utf-8")))
    raiz_css = re.search(r":root \{(.*?)\n\}", (BASE / "assets/css/ua-v1-base.css").read_text(encoding="utf-8"), re.S).group(1)
    css = {k: v.upper() for k, v in re.findall(r"--([a-z0-9-]+): (#[0-9A-Fa-f]{6});", raiz_css)}
    dif = [k for k, v in css.items() if k in tokens and tokens[k] != v] + [k for k in css if k not in tokens and k != "blanco"] + [k for k in tokens if k not in css]
    (fallo if dif else ok)(f"tokens del CSS base = paleta ({len(tokens)}): {dif or 'ok'}")


def auditar_vendor():
    print("\n▸ Copias del kit (GSAP de KANSA v6.0 vía Isabella EA v2.0, VENDOR.sha256)")
    for linea in (BASE / "documentacion" / "VENDOR.sha256").read_text(encoding="utf-8").splitlines():
        if not linea or linea.startswith("#"):
            continue
        h, ruta = linea.split(None, 2)[:2]
        actual = hashlib.sha256((BASE / ruta).read_bytes()).hexdigest()
        (ok if actual == h else fallo)(f"{ruta} idéntico al registrado")


def auditar_glifos():
    print("\n▸ Cobertura de glifos")
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        AVISOS.append("fontTools no disponible"); return
    texto = (BASE / "impresion.html").read_text(encoding="utf-8")
    texto = re.sub(r"<style.*?</style>|<script.*?</script>|<svg.*?</svg>|<[^>]+>", " ", texto, flags=re.S)
    usados = {c for c in texto if ord(c) > 32}
    cubiertos = set()
    for f in (BASE / "assets" / "fonts").glob("*.woff2"):
        cubiertos |= set(TTFont(f).getBestCmap().keys())
    faltan = sorted(c for c in usados if ord(c) not in cubiertos and not c.isspace())
    (fallo if faltan else ok)(f"caracteres sin glifo en ninguna fuente: {''.join(faltan) or 'ninguno'}")


def main():
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=CHROME)
        auditar_impresion(nav)
        for archivo in ("index.html", "UniversoArena_Inmersivo_v1.html"):
            auditar_inmersivo(nav, archivo)
        nav.close()
    auditar_portable()
    auditar_datos()
    auditar_vendor()
    auditar_glifos()
    print(f"\n{'✗' if FALLOS else '✓'} {len(FALLOS)} fallo(s).")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
