/* Universo-Arena — Galería (index.html). Manual de Marca v1.0, cap. 09.
 *
 * Sin scripts en línea: este fichero lo es todo. Los datos de las fichas están en fichas.js (generado),
 * que se pide cuando la página está ociosa o al abrir la primera ficha: un <script>, no un fetch, para
 * que siga abriendo con doble clic. Todo lo que pinta datos usa textContent y createElement: nada de
 * innerHTML con contenido del benchmark.
 *
 * · El recorrido es el patrón ScrollWorld (midudev vía KANSA, portado sin dependencias en Pentest C360):
 *   si GSAP o Lenis no llegan, la página se sigue leyendo y moviendo.
 * · GSAP + ScrollTrigger + Lenis se piden en la PRIMERA interacción, no al cargar, y nunca con
 *   prefers-reduced-motion ni con ahorro de datos. Se cargan desde assets/hub/vendor/ (rutas relativas:
 *   la galería sigue abriendo con doble clic).
 * · Las tarjetas ya están en el HTML; aquí solo se ordenan, se filtran y abren su ficha.
 */
(function () {
  'use strict';
  var d = document, w = window;
  var reducido = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ahorro = !!(navigator.connection && navigator.connection.saveData);
  var BASE = (d.currentScript && d.currentScript.src) ? d.currentScript.src.replace(/galeria\.js(\?.*)?$/, '') : 'assets/hub/';
  var SVGNS = 'http://www.w3.org/2000/svg';

  function clamp(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
  function el(tag, clase, texto) {
    var n = d.createElement(tag);
    if (clase) n.className = clase;
    if (texto !== undefined) n.textContent = texto;
    return n;
  }
  function tramos(y, keys) {
    if (y <= keys[0].y) return keys[0].v;
    for (var i = 1; i < keys.length; i++) {
      var a = keys[i - 1], b = keys[i];
      if (y <= b.y) return a.v + (b.v - a.v) * ((y - a.y) / (b.y - a.y || 1));
    }
    return keys[keys.length - 1].v;
  }

  /* ── Recorrido ─────────────────────────────────────────────────────────── */
  function cargarImg(img) {
    if (!img || !img.dataset.src) return;
    if (img.dataset.srcset) img.srcset = img.dataset.srcset;
    img.src = img.dataset.src;
    delete img.dataset.src;
  }

  function recorrido(world) {
    var stage = world.querySelector('[data-stage]');
    var stops = [].slice.call(world.querySelectorAll('[data-stop]'));
    var frames = [].slice.call(stage.querySelectorAll('[data-frame]'));
    var links = [].slice.call(stage.querySelectorAll('[data-goto]'));
    var fill = stage.querySelector('[data-rail-fill]');
    var hint = d.querySelector('[data-hint]');
    var last = stops.length - 1;
    var focus = stops.map(function (s) { return Number(s.dataset.focus || 50); });
    var actual = -1, marcas = [], fin = 0, pendiente = false;

    function medir() {
      var y0 = w.scrollY;
      marcas = stops.map(function (s) { return s.getBoundingClientRect().top + y0; });
      var r = world.getBoundingClientRect();
      fin = r.bottom + y0 - w.innerHeight;
    }
    function marcar(i) {
      if (i === actual) return;
      actual = i;
      stops.forEach(function (s, k) { s.classList.toggle('is-current', k === i); });
      links.forEach(function (a, k) { a.setAttribute('aria-current', String(k === i)); });
    }
    function pintar() {
      pendiente = false;
      var y = w.scrollY;
      var claves = marcas.map(function (m, i) { return { y: m, v: i }; });
      claves.push({ y: Math.max(fin, marcas[last] + 1), v: stops.length });
      var pos = tramos(y, claves);
      var en = Math.min(pos, last);
      marcar(Math.round(en));
      stage.style.setProperty('--focus-x', tramos(y, marcas.map(function (m, i) { return { y: m, v: focus[i] }; })) + '%');
      if (fill) fill.style.transform = 'scaleY(' + (en / last) + ')';
      if (hint) hint.style.opacity = String(clamp(1 - y / (w.innerHeight * 0.4)));
      frames.forEach(function (f, i) {
        f.style.opacity = String(i === 0 ? 1 : clamp((pos - i + 0.5) / 0.5));
        if (!reducido) f.style.transform = 'scale(' + (1 + 0.06 * clamp(pos - i)) + ')';
      });
    }
    function pedir() { if (!pendiente) { pendiente = true; w.requestAnimationFrame(pintar); } }
    medir(); pintar();
    w.addEventListener('scroll', pedir, { passive: true });
    w.addEventListener('resize', function () { medir(); pedir(); });
    w.addEventListener('load', function () { medir(); pedir(); });

    var cerca = new IntersectionObserver(function (es) {
      if (!es.some(function (e) { return e.isIntersecting; })) return;
      world.querySelectorAll('.frame-diferido').forEach(function (f) { f.classList.remove('frame-diferido'); });
      world.querySelectorAll('img[data-src]').forEach(cargarImg);
      cerca.disconnect();
      medir(); pedir();
    }, { rootMargin: '100% 0px' });
    cerca.observe(world);

    links.forEach(function (a) {
      a.addEventListener('click', function (e) {
        var destino = d.getElementById(a.getAttribute('href').slice(1));
        if (!destino) return;
        e.preventDefault();
        var y = destino.getBoundingClientRect().top + w.scrollY;
        if (w.lenis) w.lenis.scrollTo(y); else w.scrollTo({ top: y, behavior: reducido ? 'auto' : 'smooth' });
      });
    });
  }

  /* ── Entradas: solo se esconde lo que está fuera de la pantalla al cargar ─── */
  function revelar() {
    if (reducido || !('IntersectionObserver' in w)) return;
    // Sin getBoundingClientRect (forzaría la maquetación al cargar): la primera entrega del observador
    // dice qué está fuera de la pantalla, y solo eso se esconde para revelarlo después.
    var vistos = new WeakSet();
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var n = e.target;
        if (!vistos.has(n)) {
          vistos.add(n);
          if (e.isIntersecting || e.boundingClientRect.top < 0) { io.unobserve(n); return; }
          n.classList.add('por-revelar');
          return;
        }
        if (e.isIntersecting) { n.classList.add('is-in'); io.unobserve(n); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    d.querySelectorAll('[data-reveal]').forEach(function (n) { io.observe(n); });
  }

  /* ── Galería: orden, filtro y ficha ─────────────────────────────────────── */
  var pedidoFichas = null;
  function fichas() {
    if (w.UA_FICHAS) return Promise.resolve(w.UA_FICHAS);
    if (!pedidoFichas) pedidoFichas = script('fichas.js').then(function () { return w.UA_FICHAS; });
    return pedidoFichas;
  }

  function galeria() {
    var rejilla = d.querySelector('[data-rejilla]');
    var barra = d.querySelector('[data-barra]');
    var contador = d.querySelector('[data-contador]');
    if (!rejilla || !barra) return;
    var tarjetas = [].slice.call(rejilla.querySelectorAll('.tarjeta'));
    var orden = 'total', filtro = 'todos';
    barra.hidden = false;

    function aplicar(inicial) {
      if (inicial) {  // el HTML ya viene ordenado por puesto y sin filtro: no se toca el DOM al cargar
        if (contador) contador.textContent = tarjetas.length + ' entregas';
        return;
      }
      var vistas = tarjetas.slice().sort(function (a, b) {
        if (orden === 'total') return Number(a.dataset.rank) - Number(b.dataset.rank);
        return (Number(b.dataset[orden]) - Number(a.dataset[orden])) || (Number(a.dataset.rank) - Number(b.dataset.rank));
      });
      var n = 0;
      vistas.forEach(function (t) {
        var ver = filtro === 'todos' || t.dataset.tier === filtro;
        t.hidden = !ver;
        if (ver) n++;
        rejilla.appendChild(t);
      });
      if (contador) contador.textContent = n === tarjetas.length ? n + ' entregas' : n + ' de ' + tarjetas.length + ' entregas';
    }
    barra.addEventListener('click', function (e) {
      var b = e.target.closest('button.chip');
      if (!b) return;
      var grupo = b.dataset.orden !== undefined ? 'orden' : 'filtro';
      barra.querySelectorAll('[data-' + grupo + ']').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      if (grupo === 'orden') orden = b.dataset.orden.toLowerCase(); else filtro = b.dataset.filtro;
      aplicar();
    });
    aplicar(true);
  }

  function radar(e, cats) {
    var N = cats.length, R = 100, cx = 140, cy = 130;
    var svg = d.createElementNS(SVGNS, 'svg');
    svg.setAttribute('viewBox', '0 0 280 270');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Radar de las ' + N + ' categorías');
    function pt(i, r) { var a = -Math.PI / 2 + i * 2 * Math.PI / N; return [cx + Math.cos(a) * r, cy + Math.sin(a) * r]; }
    function poly(puntos, attrs) {
      var p = d.createElementNS(SVGNS, 'polygon');
      p.setAttribute('points', puntos.map(function (q) { return q.join(','); }).join(' '));
      Object.keys(attrs).forEach(function (k) { p.setAttribute(k, attrs[k]); });
      svg.appendChild(p);
    }
    for (var l = 1; l <= 4; l++) poly(cats.map(function (_, i) { return pt(i, R * l / 4); }), { fill: 'none', stroke: 'rgba(124,156,255,.16)' });
    poly(cats.map(function (c, i) { return pt(i, R * e.scores[c[0]] / c[2]); }), { fill: e.color + '40', stroke: e.color, 'stroke-width': '2' });
    cats.forEach(function (c, i) {
      var q = pt(i, R + 18), t = d.createElementNS(SVGNS, 'text');
      t.setAttribute('x', q[0]); t.setAttribute('y', q[1]);
      t.setAttribute('text-anchor', 'middle'); t.setAttribute('dominant-baseline', 'middle');
      t.setAttribute('font-size', '9'); t.setAttribute('fill', '#9AA8D4');
      t.textContent = c[1];
      svg.appendChild(t);
    });
    return svg;
  }

  function ficha() {
    var dlg = d.querySelector('[data-ficha-dialogo]');
    if (!dlg || typeof dlg.showModal !== 'function') return;
    d.querySelectorAll('[data-ficha]').forEach(function (b) { b.hidden = false; });
    var origen = null;

    function abrir(D, folder) {
      var e = D && D.entregas[folder];
      if (!e) return;
      dlg.textContent = '';
      dlg.style.setProperty('--c', e.color);
      var cab = el('div', 'f-cab');
      var img = el('img');
      img.src = 'assets/hub/previews/' + folder + '-800.webp';
      img.alt = 'Captura de la simulación de ' + e.modelo + ' con ' + e.agente;
      img.width = 800; img.height = 350;
      var cerrar = el('button', 'f-cerrar', '×');
      cerrar.type = 'button'; cerrar.setAttribute('aria-label', 'Cerrar la ficha');
      cerrar.addEventListener('click', function () { dlg.close(); });
      cab.appendChild(img); cab.appendChild(cerrar);
      var tit = el('div', 'f-titulo');
      var izq = el('div'); var h = el('h2', '', e.modelo); h.id = 'ficha-tit';
      izq.appendChild(h); izq.appendChild(el('p', 'f-sub', e.agente + ' · tier ' + e.tier + ' · puesto ' + e.rank));
      var nota = el('div', 'f-nota'); nota.appendChild(el('b', '', String(e.total))); nota.appendChild(el('span', '', 'de 100'));
      tit.appendChild(izq); tit.appendChild(nota);
      var cuerpo = el('div', 'f-cuerpo');
      var rad = el('div', 'f-radar'); rad.appendChild(radar(e, D.cats));
      var dat = el('div', 'f-datos');
      [[e.objetos, 'objetos'], [e.errores, 'errores'], [e.lineas, 'líneas']].forEach(function (x) {
        var c = el('div'); c.appendChild(el('b', '', String(x[0]))); c.appendChild(el('span', '', x[1])); dat.appendChild(c);
      });
      rad.appendChild(dat);
      var barras = el('div', 'f-barras');
      D.cats.forEach(function (c) {
        var fila = el('div', 'f-barra');
        var pista = el('span', 'f-pista'); var rel = el('span', 'f-relleno');
        rel.style.width = Math.round(e.scores[c[0]] / c[2] * 100) + '%';
        pista.appendChild(rel);
        fila.appendChild(el('span', '', c[1])); fila.appendChild(pista); fila.appendChild(el('span', '', e.scores[c[0]] + '/' + c[2]));
        barras.appendChild(fila);
      });
      cuerpo.appendChild(rad); cuerpo.appendChild(barras);
      var rasgos = el('ul', 'f-rasgos');
      rasgos.setAttribute('aria-label', 'Requisitos del reto');
      D.feats.forEach(function (f) {
        var si = !!e.features[f[0]];
        var li = el('li', si ? 'si' : 'no', (si ? '✓ ' : '✕ ') + f[1]);
        li.setAttribute('aria-label', f[1] + (si ? ': cumple' : ': no cumple'));
        rasgos.appendChild(li);
      });
      var cols = el('div', 'f-cols');
      [['Lo que hizo bien', e.fortalezas], ['Lo que falló', e.debilidades]].forEach(function (x) {
        var c = el('div'); c.appendChild(el('h3', '', x[0]));
        var ul = el('ul'); x[1].forEach(function (t) { ul.appendChild(el('li', '', t)); });
        c.appendChild(ul); cols.appendChild(c);
      });
      var acc = el('p', 'f-acciones');
      var demo = el('a', 'btn btn-sol', '▶ Abrir la demo');
      demo.href = folder + '/index.html'; demo.target = '_blank'; demo.rel = 'noopener';
      var carpeta = el('a', 'btn btn-borde', 'Ver el código en GitHub');
      carpeta.href = 'https://github.com/alexanderoviedofadul/Universo-Arena/tree/main/' + encodeURIComponent(folder);
      carpeta.target = '_blank'; carpeta.rel = 'noopener';
      acc.appendChild(demo); acc.appendChild(carpeta);
      [cab, tit, cuerpo, rasgos, cols, acc].forEach(function (n) { dlg.appendChild(n); });
      dlg.showModal();
      cerrar.focus();
    }
    d.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-ficha]');
      if (!b) return;
      origen = b;
      fichas().then(function (D) { abrir(D, b.dataset.ficha); }).catch(function () {
        w.open(b.dataset.ficha + '/index.html', '_blank', 'noopener');
      });
    });
    dlg.addEventListener('click', function (ev) { if (ev.target === dlg) dlg.close(); });
    dlg.addEventListener('close', function () { if (origen && origen.focus) origen.focus(); });
    var ocioso = w.requestIdleCallback || function (fn) { return setTimeout(fn, 2500); };
    w.addEventListener('load', function () { ocioso(function () { fichas().catch(function () {}); }); });
  }

  /* ── Movimiento: GSAP + ScrollTrigger + Lenis en la primera interacción ──── */
  function script(src) {
    return new Promise(function (ok, ko) {
      var s = d.createElement('script'); s.src = BASE + src; s.onload = ok; s.onerror = ko; d.head.appendChild(s);
    });
  }
  function movimiento() {
    script('vendor/gsap.min.js')
      .then(function () { return Promise.all([script('vendor/ScrollTrigger.min.js'), script('vendor/lenis.min.js')]); })
      .then(function () {
        var gsap = w.gsap, ST = w.ScrollTrigger;
        if (!gsap || !ST) return;
        gsap.registerPlugin(ST);
        if (w.Lenis) {
          var lenis = new w.Lenis({ autoRaf: false, anchors: true });
          lenis.on('scroll', ST.update);
          gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
          gsap.ticker.lagSmoothing(0);
          w.lenis = lenis;
        }
        // Hero: las capas de la órbita se separan a distinta velocidad (el fondo, la más lenta).
        var hero = d.querySelector('[data-hero]');
        if (hero) {
          hero.querySelectorAll('[data-capa]').forEach(function (c) {
            var z = Number(c.dataset.capa || 0);
            gsap.to(c, { yPercent: z === 0 ? 4 : (5 - z) * 5, ease: 'none',
              scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
          });
          var texto = hero.querySelector('[data-hero-texto]');
          if (texto) gsap.to(texto, { yPercent: -10, opacity: 0, ease: 'none',
            scrollTrigger: { trigger: hero, start: '45% top', end: 'bottom top', scrub: true } });
        }
      })
      .catch(function () { /* sin movimiento: la página sigue igual */ });
  }

  function luego(fn) { setTimeout(fn, 0); }

  function iniciar() {
    d.documentElement.classList.add('js');
    // Cada pieza en su propia tarea: ninguna bloquea el hilo principal más de unos milisegundos.
    var world = d.querySelector('[data-world]');
    if (world) luego(function () { recorrido(world); });
    luego(revelar);
    luego(galeria);
    luego(ficha);
    if (reducido || ahorro) return;
    var hecho = false;
    var eventos = ['scroll', 'keydown', 'pointerdown', 'touchstart', 'wheel'];
    function primera() {
      if (hecho) return;
      hecho = true;
      eventos.forEach(function (ev) { w.removeEventListener(ev, primera); });
      movimiento();
    }
    eventos.forEach(function (ev) { w.addEventListener(ev, primera, { passive: true, once: true }); });
  }

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
