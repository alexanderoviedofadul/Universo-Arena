# Manual de Marca Universo-Arena v1.0 — «El Sol en el foco»

Primer manual de marca de Universo-Arena. Mide lo que la galería ya tenía —el Sol de la barra
(`.brand .dot`) y los colores de su `:root`— y fija las reglas de la galería nueva. Kit copiado del
Manual de Marca Pentest C360 v1.0 (← Isabella EA v2.0 ← Maloca v2.0 ← ENKI v2.0 ← KANSA v6.0).

Una sola fuente genera todo lo demás: `contenido/*.json` **y los datos del benchmark**
(`assets/benchmark.json`, `docs/rubric.md`, `docs/methodology.md`). **No se editan las salidas a mano.**

| Salida | Qué es |
|---|---|
| `index.html` | Recorrido inmersivo (abre por `file://` y en `/docs/Manual_Marca_UniversoArena/v1.0/`) |
| `UniversoArena_Inmersivo_v1.html` | Portable autocontenido: fuentes, CSS, GSAP y logos en línea, sin red |
| `impresion.html` → `Manual_Marca_UniversoArena_v1.pdf` | 40 páginas A4 apaisadas |
| `assets/logos/` | El Sol, logotipos y favicons (SVG maestros + PNG) |
| `assets/data/tokens-v1.css` · `tokens_v1.json` | Paleta para la web |
| `../../../assets/marca/` | Tokens, woff2 y logos que usa la galería (los copia el build) |

## Flujo

```bash
python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/fuentes_v1.py     # solo si cambian las fuentes
python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/build_v1.py
python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/export_pdf_v1.py
python3 -B scripts/generar_galeria.py                                      # la galería usa la marca
python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/audit_v1.py       # debe terminar en 0 fallos
```

Fuente, salidas, `assets/marca/` y la galería van **en el mismo commit**: el despliegue es un `git pull`.

## Capítulos

00 Portada · 01 Origen y nombre · 02 La arena · 03 Símbolo y logotipo · 04 Color · 05 Tipografía ·
06 Interfaces · 07 Aplicaciones · 08 Tono y voz · 09 Web · 10 Gobernanza y fuentes.

## Reglas que no dan error

1. **Las cifras no se escriben.** Entregas, notas, tiers y categorías salen de `{d:clave}` (calculado por
   `build_v1.py` desde el benchmark). La lista negra del audit falla con cualquier «N entregas» escrito a mano.
2. **El Sol no se rediseña.** Es `radial-gradient(circle at 35% 30%, #fff, #ffd24a 30%, #ff7a3c 65%, #7a1d00)`
   sobre un círculo de 26 px. El audit lo compara con la galería anterior (`git show 8acc8ef:index.html`).
   El radio del degradado es el que usa CSS por defecto (*farthest-corner*): 95,5 u en el viewBox de 100.
3. **El recurso gráfico respeta la física del benchmark**: el Sol en el **foco** de cada elipse (el centro se
   marca y queda vacío) y la cola del cometa en el sentido `cometa − Sol`. Dibujarlo al revés es un uso incorrecto.
4. **Tier = color + letra.** Sobre claro se escribe con la versión profunda del color (AA); el claro no llega.
5. **El PDF recorta en silencio**: la paginación es fija y `overflow:hidden` esconde lo que crece. Solo
   `audit_v1.py` lo ve.
6. **Chromium fijado**: los scripts usan `CHROME_PATH` o `/root/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`.
7. **Versionado e inmutable**: un cambio de fondo abre v1.1 o v2.0 en otra carpeta.

Fuentes y verificación: [`documentacion/FUENTES_Y_VERIFICACION.md`](documentacion/FUENTES_Y_VERIFICACION.md).
