# Changelog — Manual de Marca Universo-Arena v1.0

## [1.0.0] — 2026-10-11 · «El Sol en el foco»

Primera versión. Kit copiado del Manual de Marca Pentest C360 v1.0 (← Isabella EA v2.0 ← Maloca v2.0
← ENKI v2.0 ← KANSA v6.0).

- **El Sol, vectorizado y no rediseñado**: el `.brand .dot` de la galería (26 px, degradado radial de cuatro
  paradas con el brillo en 35 % 30 %), con el radio del degradado que usa CSS por defecto. Logotipo con las
  proporciones de la barra: Sol 26 px, 10 px de aire, «Universo-Arena» en Inter 800 a 16 px, en curvas.
- **Paleta cerrada de 30 colores**: 3 del Sol, 10 del `:root` de la galería y 17 derivados para papel y vistas
  claras, con su contraste calculado. Retirados seis colores sueltos de la galería anterior.
- **Inter y JetBrains Mono autoalojadas** (SIL OFL 1.1), con θ y √ para las fórmulas. La galería anterior
  declaraba Inter y no la cargaba.
- **Recurso propio**: la órbita con el Sol en el foco y el cometa con la cola lejos del Sol —las dos trampas
  del benchmark—, en la portada (paralaje) y en la «órbita viva» (ecuación de Kepler por Newton-Raphson).
- **Datos leídos, no copiados**: entregas, notas, tiers y rúbrica salen de `assets/benchmark.json`,
  `docs/rubric.md` y `docs/methodology.md` al construir.
- Salidas: recorrido inmersivo, portable sin red, PDF A4 apaisado de 40 páginas y tokens.
- `audit_v1.py`: **0 fallos**, con el benchmark, la galería, `llms.txt` y `sitemap.xml` comprobados.
