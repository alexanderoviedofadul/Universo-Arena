/* Universo-Arena · Manual de Marca v1.0 — «Órbita viva»: la metáfora de la marca en movimiento.
   Lienzo 2D (sin librerías). Un planeta recorre una elipse con el Sol en el FOCO y su posición sale
   de la ecuación de Kepler (M = E − e·sinE, resuelta por Newton-Raphson): va más deprisa cerca del
   Sol. Un cometa recorre otra elipse muy excéntrica y su cola apunta en el sentido (cometa − Sol),
   recalculado en cada fotograma. Son las dos trampas del benchmark (docs/rubric.md), dibujadas bien.
   La excentricidad está exagerada para que se vea. Una vuelta del planeta dura 8 s; la del cometa, 14 s.
   Usa el bucle ÚNICO (UA.bucle) y solo corre mientras se ve. Movimiento reducido o sin lienzo →
   html[data-orbita="estatico"] y queda el respaldo SVG del build. Decorativo: aria-hidden. */
(function (w, d) {
  'use strict';
  var K = w.UA = w.UA || {};
  var raiz = d.documentElement;
  var VACIO = '#05060F', ORBITA = '#7C9CFF', POLVO = '#9AA8D4', ESTELAR = '#EAF0FF', PLANETA = '#56E0A6';
  var SOL = [[0, '#FFFFFF'], [0.30, '#FFD24A'], [0.65, '#FF7A3C'], [1, '#7A1D00']];

  function estatico(motivo) { raiz.dataset.orbita = 'estatico'; raiz.dataset.orbitaMotivo = motivo; }

  /* Anomalía excéntrica E a partir de la media M (Newton-Raphson, 6 iteraciones bastan con e < 0,9). */
  function kepler(M, e) {
    var E = e < 0.8 ? M : Math.PI;
    for (var i = 0; i < 6; i++) { E = E - (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E)); }
    return E;
  }

  /* Posición respecto al Sol (foco en el origen): x = a·cosE − a·e, y = b·sinE. */
  function posicion(a, e, E, rot) {
    var b = a * Math.sqrt(1 - e * e);
    var x = a * Math.cos(E) - a * e, y = b * Math.sin(E);
    return [x * Math.cos(rot) - y * Math.sin(rot), x * Math.sin(rot) + y * Math.cos(rot)];
  }

  function elipse(ctx, cx, cy, a, e, rot) {
    var b = a * Math.sqrt(1 - e * e), c = a * e;
    ctx.beginPath();
    ctx.ellipse(cx - c * Math.cos(rot), cy - c * Math.sin(rot), a, b, rot, 0, Math.PI * 2);
    ctx.stroke();
  }

  function montar(lienzo, id) {
    var ctx = lienzo.getContext('2d');
    if (!ctx) { return false; }
    var ancho = 0, alto = 0, dpr = Math.min(w.devicePixelRatio || 1, 2);
    function medir() {
      var r = lienzo.getBoundingClientRect();
      ancho = r.width; alto = r.height;
      lienzo.width = Math.round(ancho * dpr); lienzo.height = Math.round(alto * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function pintar(ms) {
      var s = Math.min(ancho / 400, alto / 250);
      var cx = ancho / 2, cy = alto / 2;
      var aP = 120 * s, eP = 0.55, aC = 165 * s, eC = 0.8, rC = 0.5;
      ctx.fillStyle = VACIO; ctx.fillRect(0, 0, ancho, alto);
      // Órbitas: la del planeta, continua; la del cometa, discontinua. El centro de la primera, marcado y vacío.
      ctx.lineWidth = 1.4; ctx.strokeStyle = ORBITA; ctx.globalAlpha = 0.7; ctx.setLineDash([]);
      elipse(ctx, cx, cy, aP, eP, 0);
      ctx.lineWidth = 1; ctx.strokeStyle = POLVO; ctx.globalAlpha = 0.55; ctx.setLineDash([2 * s, 6 * s]);
      elipse(ctx, cx, cy, aC, eC, rC);
      ctx.setLineDash([]); ctx.globalAlpha = 1;
      var ox = cx - aP * eP;
      ctx.strokeStyle = POLVO; ctx.beginPath(); ctx.moveTo(ox - 4 * s, cy); ctx.lineTo(ox + 4 * s, cy); ctx.moveTo(ox, cy - 4 * s); ctx.lineTo(ox, cy + 4 * s); ctx.stroke();
      // Cometa y su cola (cometa − Sol)
      var q = posicion(aC, eC, kepler(((ms % 14000) / 14000) * Math.PI * 2, eC), rC);
      var qx = cx + q[0], qy = cy + q[1], n = Math.hypot(q[0], q[1]) || 1, ux = q[0] / n, uy = q[1] / n;
      var largo = (30 + 4000 * s / Math.max(n, 40)) * s, anchoCola = 6 * s;
      var g = ctx.createLinearGradient(qx, qy, qx + ux * largo, qy + uy * largo);
      g.addColorStop(0, 'rgba(234, 240, 255, .75)'); g.addColorStop(1, 'rgba(124, 156, 255, 0)');
      ctx.fillStyle = g; ctx.beginPath();
      ctx.moveTo(qx - uy * anchoCola, qy + ux * anchoCola); ctx.lineTo(qx + ux * largo, qy + uy * largo); ctx.lineTo(qx + uy * anchoCola, qy - ux * anchoCola);
      ctx.closePath(); ctx.fill();
      ctx.fillStyle = ESTELAR; ctx.beginPath(); ctx.arc(qx, qy, 3 * s, 0, Math.PI * 2); ctx.fill();
      // Planeta: más rápido en el perihelio
      var p = posicion(aP, eP, kepler(((ms % 8000) / 8000) * Math.PI * 2, eP), 0);
      ctx.fillStyle = PLANETA; ctx.beginPath(); ctx.arc(cx + p[0], cy + p[1], 6 * s, 0, Math.PI * 2); ctx.fill();
      // El Sol, en el foco, con su degradado (brillo en 35 % 30 %)
      var r = 9 * s, gs = ctx.createRadialGradient(cx - r + 0.7 * r, cy - r + 0.6 * r, 0, cx - r + 0.7 * r, cy - r + 0.6 * r, 1.91 * r);
      SOL.forEach(function (st) { gs.addColorStop(st[0], st[1]); });
      ctx.fillStyle = gs; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
    }
    medir();
    w.addEventListener('resize', medir);
    K.bucle.registrar(id, pintar);
    if ('IntersectionObserver' in w) {
      new IntersectionObserver(function (es) { es.forEach(function (en) { K.bucle.activar(id, en.isIntersecting); }); }).observe(lienzo);
    } else { K.bucle.activar(id, true); }
    return true;
  }

  K.orbita = {
    iniciar: function () {
      if (w.matchMedia('(prefers-reduced-motion: reduce)').matches) { return estatico('movimiento-reducido'); }
      if (!K.bucle) { return estatico('sin-bucle'); }
      var lienzos = d.querySelectorAll('canvas.orbita-gl'), n = 0;
      Array.prototype.forEach.call(lienzos, function (c, i) { if (montar(c, 'orbita-' + i)) { n++; } });
      if (n) { raiz.dataset.orbita = 'animado'; } else { estatico('sin-lienzo'); }
    }
  };
})(window, document);
