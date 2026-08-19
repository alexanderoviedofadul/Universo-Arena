# 🆕 Décima tanda — GLM 5.3 (×3) y Gemini 3.7 Flash (×2) (2026-08-07)

Registro de la ampliación del benchmark de **31 → 36 entradas** — el lote más grande
hasta la fecha: **cinco** combinaciones nuevas de dos familias (GLM 5.3 y Gemini 3.7
Flash), integradas con la metodología de siempre (rúbrica + ejecución real +
verificación contra runtime), un jurado por entrega en paralelo.

## Las cinco nuevas

| Carpeta | Modelo | Agente | Nota | Tier | Puesto |
|:--|:--|:--|:--:|:--:|:--:|
| `Opencode-GLM-5.3` | GLM 5.3 | **OpenCode** | **91** | S | #13 |
| `Zcode-GML-5.3-Max` | GLM 5.3 (Max) | **Zcode** | **90** | S | #15 |
| `Antigravity-Gemini-3.7-Flash-High` | Gemini 3.7 Flash (High) | **Antigravity** | **90** | S | #16 |
| `GLM-5.3-Claude-Code` | GLM 5.3 | **Claude Code** | **89** | A | #22 |
| `Agy-Gemini-3.7-Flash-Antigravity-CLI` | Gemini 3.7 Flash | **Antigravity CLI** | **86** | A | #27 |

Las cinco arrancan con **0 errores de consola** y resuelven **las dos trampas**
nucleares (Sol en el foco con `x = a·cosθ − a·e`, `b = a·√(1−e²)`, y cola del cometa
`(cometa − Sol)` recalculada cada frame sin mutación). Ninguna alcanza a su hermana
calibrada ni roza el podio; el triple empate de cabeza (97) y los siete 95 quedan
intactos.

## Datos de ejecución real (Chrome headless, SwiftShader)

| Carpeta | Objetos | FPS | Errores |
|:--|:--:|:--:|:--:|
| `Agy-Gemini-3.7-Flash-Antigravity-CLI` | 361 | 9 | 0 |
| `Opencode-GLM-5.3` | 324 | 5 | 0 |
| `Antigravity-Gemini-3.7-Flash-High` | 322 | 8 | 0 |
| `GLM-5.3-Claude-Code` | 304 | 6 | 0 |
| `Zcode-GML-5.3-Max` | 290 | 8 | 0 |

## Qué distingue a cada una

- **GLM 5.3 · OpenCode (91, S).** La mejor de las cinco: ecuación de Kepler por
  Newton-Raphson con **velocidad orbital variable real**, foco e instancing correctos, y
  el **tercer discriminador levógiro bien resuelto**. Pero **no alcanza a su hermana
  GLM 5.2 · OpenCode (95)**: nebulosas planas y varios planetas sin textura la dejan un
  escalón por debajo del pelotón de 95 en estética y rendimiento.
- **GLM 5.3 (Max) · Zcode (90, S).** Kepler con aceleración en el perihelio, **10 lunas
  reales** (Tritón retrógrada) y cámara sin rebotes; +1 sobre su hermana 5.2 Max (89).
  Se queda por debajo del clúster de 92 por el **panel de solo 3 secciones** (el spec
  pide 4) y el rendimiento débil.
- **Gemini 3.7 Flash (High) · Antigravity (90, S).** Foco y cola correctos, **Venus y
  Urano retrógrados**, post-proceso doble; +1 sobre la 3.6 High (89) pero por debajo de
  la 3.5 High (92) por el rendimiento (8 fps, escena sobrecargada) y velocidad orbital
  sin 2.ª ley.
- **GLM 5.3 · Claude Code (89, A).** Ambas trampas limpias con `normalizeToNew` y
  robustez sobresaliente, pero **el tercer discriminador queda invertido**: la revolución
  usa `z = +b·sinθ` mientras la rotación axial es `rotation.y+`, dejando revolución y giro
  propio en **sentidos opuestos**. Empata a su hermana 5.2 · Claude Code (89).
- **Gemini 3.7 Flash · Antigravity CLI (86, A).** La **más completa** del campo (2370
  líneas, 361 mallas) con ambas trampas e instancing correctos, pero arrastra el mismo
  defecto que costó puntos a la 3.6: **parches blancos en las etiquetas** (`emissiveColor`
  White + bloom sin alpha, visibles en la captura), no corregido pese a los commits. +1
  sobre la 3.6 CLI (85), por debajo de la 3.5 CLI (89).

## Lecturas de la tanda

1. **Generación nueva ≠ mejor entrega.** GLM 5.3 no supera a GLM 5.2 en su mejor agente
   (OpenCode: 95 → 91), y Gemini 3.7 Flash sube solo **+1** sobre la 3.6 en ambos agentes.
   El techo del reto no se mueve por cambiar de versión de modelo.
2. **Los discriminadores siguen siendo los mismos.** Lo que separó a estas cinco de sus
   hermanas y del clúster superior no fue la escena (todas completas y vistosas) sino los
   **detalles físicos**: el tercer discriminador (sentido de giro) en GLM 5.3 · CC, los
   parches de etiquetas en Gemini 3.7 CLI, el panel incompleto en Zcode, el rendimiento
   en las Gemini. Acertar el foco y la cola ya es la base, no el diferenciador.

## Artefactos regenerados

Tras editar la fuente de verdad [`../assets/benchmark.json`](../assets/benchmark.json)
(36 entradas) se regeneraron, derivándolos de ella:

- **Web principal** [`../index.html`](../index.html): 36 fichas, podio, radares;
  contadores dinámicos (36 entregas · 34/36 sin errores · media 87); bloque "estado del
  arte" (36/36 · 34/36); JSON-LD (`ItemList` de 36) y metas a "36 combinaciones".
- [`../assets/runtime.json`](../assets/runtime.json) y 5 capturas en `assets/previews/`.
- [`../README.md`](../README.md): tablas (ranking, categorías, matriz) y badges (36, 34/36).
- [`results.md`](results.md) (36 fichas), [`conclusions.md`](conclusions.md),
  [`methodology.md`](methodology.md).
- SEO/GEO: `sitemap.xml` (36 demos), `llms.txt` y `llms-full.txt`.

## Cómo reproducir / añadir más

Mismo flujo de [`harness.md`](harness.md), [`contributing.md`](contributing.md) y las
tandas anteriores ([7.ª](septima-tanda-2026-07-29.md), [8.ª](octava-tanda-2026-08-07.md),
[9.ª](novena-tanda-2026-08-07.md)): capturar en Chrome headless → puntuar con la
[`rúbrica`](rubric.md) → **verificar contra el runtime** → fusionar en `benchmark.json`
→ regenerar los artefactos derivados (incluida la **re-inyección** de los datos en
`index.html` y el bloque "estado del arte", que es hardcodeado).
