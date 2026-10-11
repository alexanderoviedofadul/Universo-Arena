# Fuentes y verificación — Manual Universo-Arena v1.0

La bibliografía completa está en `contenido/fuentes.json` y se imprime en el capítulo 10.
Aquí, cómo se comprobó cada tipo de dato el 11-oct-2026.

| Dato | Cómo se verificó |
|---|---|
| El Sol | `.brand .dot` de `git show 8acc8ef:index.html` (la galería anterior), comparado parada por parada por `audit_v1.py` |
| Radio del degradado | CSS Images Level 3: sin tamaño, *farthest-corner* → de (35, 30) a (100, 100) = 95,5 u |
| Proporciones del logotipo | La misma regla: Sol 26 px, `gap: 10px`, nombre a 16 px con `font-weight: 800` y `letter-spacing: -.01em` |
| Colores «CSS» | `:root` de la galería anterior (`--bg`, `--bg2`, `--txt`, `--dim`, `--faint`, `--accent`, `--accent2`, `--S` … `--D`) |
| Contrastes | Calculados por `build_v1.py` con la fórmula de WCAG 2.1 |
| Cifras del benchmark | Leídas de `assets/benchmark.json` en cada build; el audit comprueba totales, tiers, rango, carpetas, capturas, `llms.txt` y `sitemap.xml` |
| Rúbrica y tiers | Tabla de `docs/rubric.md` y cortes de `docs/methodology.md` |
| Fechas | `git log --date=short` y `CHANGELOG.md` |
| Licencias de fuentes | `fuentes/*/OFL.txt` |

## Corregido respecto a la galería anterior

- La FAQ decía que el arnés de captura «está versionado en GitHub»: `CLAUDE.md` y `docs/harness.md` dicen que
  vive fuera del repositorio. La galería nueva lo dice así.
- La imagen para compartir (`assets/og-image.png`) ponía el Sol en el centro de órbitas concéntricas y un lema
  en inglés sin fuente («The Advanced AI Agent Evolution Hub»). La nueva es `assets/og-universo-arena-v1.png`.
- «MiniMax M3 pasa de 79 a 92 al cambiar de agente»: el benchmark ya tenía su 95 con OpenCode. Ahora la cifra
  se calcula.
- El pie enlazaba `README.md`, que Caddy no sirve (404 desde el pentest del 10-oct). Ahora enlaza al repositorio.
