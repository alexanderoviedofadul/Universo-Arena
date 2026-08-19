# Changelog

Todos los cambios notables de **Universo-Arena**. El formato sigue
[Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y el proyecto usa
[Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Añadido — Décima tanda: 31 → 36 entradas (2026-08-07)

- **5 entradas nuevas** (3× GLM 5.3, 2× Gemini 3.7 Flash), todas con **0 errores de
  consola** y ambas trampas resueltas:
  - `Opencode-GLM-5.3` (GLM 5.3 · OpenCode, **91**, #13, tier S): Kepler por
    Newton-Raphson con velocidad variable real, foco e instancing correctos.
  - `Zcode-GML-5.3-Max` (GLM 5.3 (Max) · Zcode, **90**, #15, tier S): Kepler con
    aceleración en perihelio y 10 lunas reales; panel de solo 3 secciones.
  - `Antigravity-Gemini-3.7-Flash-High` (Gemini 3.7 Flash (High) · Antigravity, **90**,
    #16, tier S): foco y cola correctos, Venus/Urano retrógrados; rendimiento pobre.
  - `GLM-5.3-Claude-Code` (GLM 5.3 · Claude Code, **89**, #22, tier A): ambas trampas
    limpias pero **tercer discriminador invertido** (revolución vs rotación).
  - `Agy-Gemini-3.7-Flash-Antigravity-CLI` (Gemini 3.7 Flash · Antigravity CLI, **86**,
    #27, tier A): la más completa (361 mallas) pero **parches blancos en etiquetas
    persisten** (defecto de la 3.6 no corregido).
- **Hallazgos:** ninguna de las 5 alcanza a su hermana calibrada ni al podio. GLM 5.3
  no supera a GLM 5.2 · OpenCode (95); Gemini 3.7 Flash sube solo +1 sobre la 3.6 en
  ambos agentes. El foco elíptico, el tercer discriminador y los parches de etiquetas
  siguen siendo los discriminadores que separan generaciones. Detalle en
  [`docs/decima-tanda-2026-08-07.md`](docs/decima-tanda-2026-08-07.md).
- **Re-ranking completo a 36 entradas** preservando el triple empate de cabeza (97) y
  los siete 95. Ahora **34/36** sin errores y media 87.
- Regenerados todos los artefactos derivados de `assets/benchmark.json`: galería
  `index.html` (DATA, contadores dinámicos, bloque "estado del arte" 36/36·34/36,
  JSON-LD `ItemList` de 36, metas), `README.md` (tablas + badges), `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `docs/README.md`, `sitemap.xml`,
  `llms.txt`, `llms-full.txt` y `assets/runtime.json`.

### Añadido — Novena tanda: 29 → 31 entradas (2026-08-07)

- **2 entradas nuevas**:
  - `Opencode-DeepSeek-V4-Flash` (DeepSeek V4 Flash · OpenCode, **92**, #12, tier S).
    Resuelve **las dos trampas** verificadas en runtime (elipses con el Sol en el foco con
    el signo levógiro `z = −b·sinθ`, y cola del cometa `(cometa − Sol)` con `normalizeToNew`
    sin mutación), el **tercer discriminador** (Venus retrógrado por quaternion) y usa la
    **corona oficial real `ParticleHelper.CreateAsync("sun")`** con fallback, 3600 estrellas
    en caja 2000³ e instancing (240). **Nota re-verificada de 96 a 92:** iguala a los líderes
    en corrección pero arrastra un **bug visible** —las etiquetas de planetas se cuelgan del
    pivot y quedan apiladas sobre el Sol— que los siete 95 limpios no tienen, así que queda
    por debajo de los 95, no en #4. 281 objetos, 0 errores.
  - `Antigravity-Claude-Opus-4.6` (Claude Opus 4.6 · Antigravity, **78**, #29, tier B).
    Escena completa, panel y post-procesado sobresalientes (295 objetos, 0 errores), pero
    **falla las dos trampas**: los 8 planetas orbitan elipses **centradas en el Sol** (sin
    offset `−c`; solo el Halley usa el foco) y la cola del cometa usa `position.normalize()`
    que **muta el núcleo in-place** cada frame. Además sin instancing (250 esferas sueltas).
- **Hallazgos:** (1) la re-verificación evitó que un 96 sin calibrar adelantara a los siete
  95 (DeepSeek queda #12, en el clúster de 92, por un bug de etiquetas). (2) Opus 4.6, pese
  a ser modelo grande, cae a tier B por fallar el foco y mutar la posición del cometa: el
  acabado visual no compensa los discriminadores físicos. Detalle en
  [`docs/novena-tanda-2026-08-07.md`](docs/novena-tanda-2026-08-07.md).
- **Re-ranking completo a 31 entradas** preservando el triple empate de cabeza (97):
  🥇 GPT-5.5 · Codex, 🥈 Claude Opus 4.8 · Ultracode y 🥉 Claude Opus 5 · Ultracode.
  Ahora **29/31** sin errores y media 87.
- Regenerados todos los artefactos derivados de `assets/benchmark.json`: galería
  `index.html` (DATA, contadores dinámicos, bloque "estado del arte" 31/31·29/31, JSON-LD
  `ItemList` de 31, metas), `README.md` (tablas + badges), `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `docs/README.md`, `sitemap.xml`,
  `llms.txt`, `llms-full.txt` y `assets/runtime.json`.

### Añadido — Octava tanda: 28 → 29 entradas (2026-08-07)

- **1 entrada nueva**: `codex-gpt-5.6-terra` (GPT-5.6 Terra · Codex, **79**, #26, tier B).
  Escena completa y vistosa (282 mallas, 0 errores, cinturón por `createInstance`, panel
  de 4 secciones, post-procesado) con la **cola del cometa correcta** (opuesta al Sol,
  `clone().normalize()` sin mutación), pero **falla la trampa del foco**: los planetas
  orbitan en círculos centrados en el Sol (`pivot.rotation.y` con malla a radio fijo), no
  en elipses con el Sol en el foco.
- **Hallazgo:** GPT-5.6 Terra **regresa frente a GPT-5.5** (97 → 79, −18) con el mismo
  agente Codex, por fallar el foco que la generación anterior clavó. Detalle en
  [`docs/octava-tanda-2026-08-07.md`](docs/octava-tanda-2026-08-07.md).
- **Re-ranking completo a 29 entradas** preservando el triple empate de cabeza (97):
  🥇 GPT-5.5 · Codex, 🥈 Claude Opus 4.8 · Ultracode y 🥉 Claude Opus 5 · Ultracode. La
  nueva entra en #26 (tras los 79 ya calibrados). Ahora **27/29** sin errores y media 87.
- Regenerados todos los artefactos derivados de `assets/benchmark.json`: galería
  `index.html` (DATA, contadores dinámicos, bloque "estado del arte" 29/29·27/29, JSON-LD
  `ItemList` de 29, metas), `README.md` (tablas + badges), `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `docs/README.md`, `sitemap.xml`,
  `llms.txt`, `llms-full.txt` y `assets/runtime.json`.

### Añadido — Séptima tanda: 26 → 28 entradas (2026-07-29)

- **2 entradas nuevas** de **Kimi K3**: `Kimi-K3-Claude-Code` (Kimi K3 · Claude Code,
  **92**, #11, tier S) y `Kimi-K3-Open-Code` (Kimi K3 · OpenCode, **87**, #20, tier A).
  Ambas resuelven las dos trampas (cola opuesta al Sol sin mutación, elipses con el Sol
  en el foco) y usan instancing real, con **0 errores de consola** (279 y 302 objetos).
- **Hallazgo:** Kimi salta de **tier B** (K2.7: 80/79) a **S/A** con K3 — salto
  generacional claro. Y el agente vuelve a pesar: la misma base K3 rinde 92 (Claude Code)
  vs. 87 (OpenCode), esta última con el **sentido de giro invertido** confirmado (el
  tercer discriminador) y la cola sin normalizar. Detalle en
  [`docs/septima-tanda-2026-07-29.md`](docs/septima-tanda-2026-07-29.md).
- **Re-ranking completo a 28 entradas** preservando el triple empate de cabeza (97):
  🥇 GPT-5.5 · Codex, 🥈 Claude Opus 4.8 · Ultracode y 🥉 Claude Opus 5 · Ultracode.
  Ahora **26/28** sin errores y **media 88** (subió de 87).
- Regenerados todos los artefactos derivados de `assets/benchmark.json`: galería
  `index.html` (DATA, contadores dinámicos, bloque "estado del arte" 28/28·26/28,
  JSON-LD `ItemList` de 28, metas), `README.md` (tablas + badges), `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `docs/README.md`, `sitemap.xml`,
  `llms.txt`, `llms-full.txt` y `assets/runtime.json`.

### Añadido — Sexta tanda: 25 → 26 entradas (2026-07-27)

- **1 entrada nueva**: `Opus-5-Claude-Code-Ultracode` (Claude Opus 5 · Ultracode +
  Claude Code, **97**, #3, tier S), que **empata en cabeza** con GPT-5.5 · Codex y
  Claude Opus 4.8 · Ultracode. Verificada en ejecución: **305 mallas**, 250
  instancias de asteroide, ~7 100 partículas, **0 errores de consola** y cola del
  cometa con **producto escalar 1.000** frente a (cometa − Sol).
- **Novedades técnicas que no había en el campo:** ecuación de Kepler resuelta por
  Newton-Raphson (2.ª ley) con `n ∝ a^(−3/2)` (3.ª ley) aplicada también a las 250
  rocas del cinturón; límites de cámara del spec (`lowerRadiusLimit = 30`) tratados
  como invariantes usando **teleobjetivo** (`camera.fov`) para los primeros planos;
  cero reservas de memoria en el bucle de render; y el preset **oficial**
  `ParticleHelper.CreateAsync("sun")` cargando de verdad (el spec lo pedía bajo un
  nombre inexistente, `CreateSystem`).
- **Metodología ampliada:** documentación oficial (context7) → verificación de APIs
  por introspección en el runtime real → **auditoría adversarial** (5 auditores +
  escépticos, 38 hallazgos) → **jurado calibrado dos veces**, repuntuando sobre el
  archivo final. Detalle en [`docs/sexta-tanda-2026-07-27.md`](docs/sexta-tanda-2026-07-27.md).
- **Re-ranking completo a 26 entradas**: triple empate de cabeza en 97 y ahora
  **24/26** entregas sin un solo error de consola.
- **Documentación ampliada** con lo aprendido en esta tanda:
  - [`docs/methodology.md`](docs/methodology.md): nueva sección *Ampliación del
    método* (documentación → runtime → auditoría adversarial → jurado calibrado y
    repuntuación), su límite conocido y un **conflicto de interés declarado** para
    las dos entradas producidas por el propio sistema evaluador.
  - [`docs/harness.md`](docs/harness.md): señales nuevas del arnés (instancias,
    partículas vivas, peticiones fallidas, versión del CDN y el **producto escalar**
    que convierte la trampa del cometa en un número), verificación automática del
    panel y las 6 vistas, comprobación en móvil y sondas de introspección de API.
  - [`docs/rubric.md`](docs/rubric.md): documentado un **tercer discriminador**, el
    sentido de giro en el sistema levógiro de Babylon (+X → −Z), que ninguna captura
    delata.
  - [`docs/conclusions.md`](docs/conclusions.md): nueva sección *Fidelidad literal
    vs. impacto visual* y actualización del podio a triple empate.
  - [`docs/contributing.md`](docs/contributing.md): cuándo aplicar el método ampliado.
- Regenerados todos los artefactos derivados de `assets/benchmark.json`: galería
  `index.html` (DATA, contadores, JSON-LD `ItemList` de 26, FAQ y metas),
  `README.md` (tablas + badges), `docs/results.md`, `sitemap.xml`, `llms.txt`,
  `llms-full.txt` y `assets/runtime.json`.

### Añadido — Quinta tanda: 23 → 25 entradas (2026-07-23)

- **2 entradas nuevas** integradas en el benchmark y la galería:
  `Antigravity-Gemini-3.6-Flash-High` (Gemini 3.6 Flash (High) · Antigravity, **89**, #15)
  y `Agy-Gemini-3.6-Flash-Antigravity-CLI` (Gemini 3.6 Flash · Antigravity CLI, **85**, #19).
  Ambas aciertan los puntos críticos (cola opuesta al Sol sin mutación, elipses con el
  Sol en el foco) con **0 errores de consola** (259 y 320 objetos en escena).
- **Hallazgo:** Gemini 3.6 Flash **no supera a Gemini 3.5** con el mismo agente
  (Antigravity 92→89, Antigravity CLI 89→85). El detalle en
  [`docs/quinta-tanda-2026-07-23.md`](docs/quinta-tanda-2026-07-23.md).
- **Higiene:** regenerado el preview faltante de `Mimo-V2.5-Pro-MimoCode` (#6), cuyo PNG
  nunca se había commiteado; su nota y datos no cambian.
- **Re-ranking completo a 25 entradas** preservando el empate de cabeza (97):
  🥇 GPT-5.5 · Codex y 🥈 Claude Opus 4.8 · Ultracode. Ahora **23/25** sin errores.
- Regenerados todos los artefactos derivados de `assets/benchmark.json`: galería
  `index.html` (DATA, contadores, JSON-LD `ItemList` de 25, metas), `README.md`
  (tablas + badges), `docs/results.md`, `docs/conclusions.md`, `docs/methodology.md`,
  `sitemap.xml`, `llms.txt` y `llms-full.txt`.

### Añadido — Cuarta tanda: 19 → 23 entradas (2026-07-05)

- **4 entradas nuevas** integradas en el benchmark y la galería:
  `Mimo-V2.5-Pro-MimoCode` (MiMo v2.5 Pro · MiMoCode, **95**, #6, integrada al pasar
  de 19→20) y las tres de esta tanda —`Fable-5-Claude-Code-Ultracode`
  (Claude Fable 5 · Ultracode + Claude Code, **95**, #7),
  `Mimo-V2.5-Pro-Claude-Code` (MiMo v2.5 Pro · Claude Code, **90**, #10) y
  `Mimo-V2.5-Pro-OpenCode` (MiMo v2.5 Pro · OpenCode, **89**, #14). Todas aciertan los
  puntos críticos (cola opuesta al Sol, elipses al foco, *instancing*) con
  **0 errores de consola**.
- **Re-ranking completo a 23 entradas** preservando el empate de cabeza (97):
  🥇 GPT-5.5 · Codex y 🥈 Claude Opus 4.8 · Ultracode. Ahora **21/23** sin errores y
  **media 87** (subió de 86).
- **Calibración estricta verificada por *runtime***: las notas (95, 90, 89) quedaron
  confirmadas por la ejecución real (310, 260, 263 objetos; 0 errores) sin
  contradicciones. Ninguna nota nueva alcanza el 97 calibrado. Registro en
  [`docs/cuarta-tanda-2026-07-05.md`](docs/cuarta-tanda-2026-07-05.md).
- **Hallazgos:** **Fable 5 · Ultracode** aporta la **mejor mecánica orbital del campo**
  (Kepler 1ª+2ª+3ª ley por Newton-Raphson, aceleración real en perihelio), única en el
  benchmark; no llega al 97 porque las vistas de cámara de seguimiento no hacen *zoom*.
  Y **MiMo v2.5 Pro** queda representado por 3 agentes con dispersión de 6 puntos
  (MiMoCode 95 · Claude Code 90 · OpenCode 89): el andamiaje decide de nuevo.
- **Artefactos regenerados** desde `assets/benchmark.json`: `index.html` (23 fichas,
  contadores dinámicos, JSON-LD `ItemList`/metas), `README.md`, `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `docs/README.md`, `sitemap.xml`,
  `llms.txt`, `llms-full.txt`, `assets/runtime.json` y 3 capturas en `assets/previews/`.

### Añadido — Tercera tanda: 17 → 19 entradas (2026-06-18)

- **2 entradas nuevas** integradas en el benchmark y la galería:
  `Opencode-Minimax-M3` (MiniMax M3 · OpenCode, **95**, #4) y `Pi-DeepSeek-v4-pro`
  (DeepSeek V4 Pro · Pi, **88**, #12). Ambas aciertan los puntos críticos
  (cola opuesta al Sol, elipses al foco, *instancing*) con **0 errores de consola**.
- **Re-ranking completo a 19 entradas**; se mantiene el empate de cabeza (97):
  🥇 GPT-5.5 · Codex y 🥈 Claude Opus 4.8 · Ultracode. Ahora **17/19** sin errores.
- **Calibración sin recortes:** los jurados se instruyeron estrictos desde el inicio
  y sus notas (95, 88) quedaron confirmadas por la ejecución real (264 y 301 objetos),
  sin contradicciones. Registro en
  [`docs/tercera-tanda-2026-06-18.md`](docs/tercera-tanda-2026-06-18.md).
- **Hallazgos:** **OpenCode** suma dos 95 (GLM 5.2 y MiniMax M3) — agente muy fuerte;
  y `Pi-DeepSeek-v4-pro` (88) **resuelve** las trampas (cola anti-solar + foco elíptico)
  que `deepseek-v4-pro-Pi-Coding-Agent` (78) había fallado.
- **Artefactos regenerados** desde `assets/benchmark.json`: `index.html` (19 fichas,
  contadores dinámicos, JSON-LD/metas), `README.md`, `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `sitemap.xml`, `llms.txt`,
  `llms-full.txt` y 2 capturas en `assets/previews/`.

### Añadido — Segunda tanda: 14 → 17 entradas (2026-06-17)

- **3 entradas nuevas** integradas en el benchmark y la galería:
  `Opencode-GLM-5.2` (GLM 5.2 · OpenCode, **95**, 🥉 #3), `Antigravity-Gemini-3.5-High`
  (Gemini 3.5 High · Antigravity, **92**, #5) y `Zcode-GML-5.2-Max`
  (GLM 5.2 Max · Zcode, **89**, #9). Las tres aciertan los puntos críticos
  (cola opuesta al Sol, elipses al foco, *instancing*) con **0 errores de consola**.
- **Re-ranking completo a 17 entradas** preservando el empate de cabeza (97):
  🥇 GPT-5.5 · Codex y 🥈 Claude Opus 4.8 · Ultracode. Ahora **15/17** sin errores.
- **Calibración verificada por *runtime***: los jurados de esta tanda puntuaban
  ~3-4 pts generoso; tras verificación adversarial se ajustaron 99→95, 95→92, 92→89,
  para no destronar el 97 calibrado sin re-baremar. Registro en
  [`docs/segunda-tanda-2026-06-17.md`](docs/segunda-tanda-2026-06-17.md).
- **Hallazgo:** **GLM 5.2** queda representado por 4 combinaciones con dispersión
  de **41 puntos** según el agente (OpenCode 95 · Claude Code 89 · Zcode 89 · Z.ai 54):
  el andamiaje del agente pesa tanto como el modelo base.
- **Artefactos regenerados** desde `assets/benchmark.json`: `index.html` (17 fichas,
  contadores dinámicos, JSON-LD/metas), `README.md`, `docs/results.md`,
  `docs/conclusions.md`, `docs/methodology.md`, `sitemap.xml`, `llms.txt`,
  `llms-full.txt` y 3 capturas en `assets/previews/`.

### Añadido — SEO + GEO/AEO (2026-06-15)

- **Compartición social por red:** `<head>` con **Open Graph** completo
  (Facebook, LinkedIn, WhatsApp, Telegram, Slack, Discord) y **Twitter/X Card**
  `summary_large_image`, con imagen social dedicada `assets/og-image.png` (1200×630).
- **Amigable con buscadores:** `robots.txt`, `sitemap.xml` (home + 14 demos, con
  imágenes), `canonical` y `meta robots`.
- **Amigable con LLMs:** `llms.txt` (resumen citable < 2 000 tokens) y
  `llms-full.txt` (contexto extendido), más política explícita de bots de
  búsqueda/citación de IA en `robots.txt`.
- **Datos estructurados** JSON-LD `@graph`: `WebSite`, `Dataset`, `ItemList`
  (ranking) y `FAQPage`.
- **`humans.txt`** y documento de auditoría [`docs/seo-geo-2026-06-15.md`](docs/seo-geo-2026-06-15.md)
  con before/after, comandos de validación y pendientes (alta en Search Console / Bing).

### Seguridad — websec-100 (2026-06-15)

- **Redirect HTTP→HTTPS** explícito (`308`): el bloque `:80` global de Caddy
  anulaba el auto-redirect y servía HTTP plano sin headers.
- **Bloqueo de paths sensibles** (`404`): `CLAUDE.md`, `commit-simple.sh`,
  `/.claude/*` y backups `*.bak/*.old/*.swp/*.swo/*.orig/*.rej`.
- **Headers de seguridad** añadidos: `Permissions-Policy`,
  `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`; CSP endurecida
  (`form-action`, `frame-src`, `worker-src`, `manifest-src`, `media-src`,
  `upgrade-insecure-requests`). Se conserva `unsafe-eval` (BabylonJS lo requiere).
- **`/.well-known/security.txt`** (RFC 9116) publicado.
- Verificado en navegador headless real: **0 violaciones CSP** en galería y demos.
- Informe: [`docs/security-audit-2026-06-15.md`](docs/security-audit-2026-06-15.md) + snapshots `docs/websec-2026-06-15/`.

### Rendimiento y accesibilidad — pagespeed-100 (2026-06-15)

- **PageSpeed/Lighthouse 100/100/100/100** (Performance, Accessibility, Best
  Practices, SEO; PSI mobile). LCP 1.1 s · CLS 0 · TBT 0 ms.
- **Corregido contraste WCAG AA:** token CSS `--faint` `#6b78a8` → `#7884b5`
  (4.41:1 → 5.22:1), que subió Accessibility de 91 a 100. Audit `color-contrast`
  sin ítems pendientes.
- Informe: [`docs/pagespeed-2026-06-15.md`](docs/pagespeed-2026-06-15.md) + snapshots `docs/pagespeed-2026-06-15/`.

## [1.0.0] — 2026-06-15

Primera versión pública del benchmark, con galería web y documentación completa.

### Añadido

- **Benchmark de 14 entregas** (combinaciones LLM + agente de código) del reto
  `Prompt-Maestro_v2.txt`, cada una en su carpeta `<Modelo>-<Agente>/index.html`.
- **Metodología de tres señales:** rúbrica de 100 puntos (10 categorías), ejecución
  real en Chrome headless (capturas, nº de objetos, FPS y errores de consola) y
  calibración adversarial con corrección por *runtime*.
- **Galería interactiva** ([`index.html`](index.html)) con UI moderna: hero animado,
  podio, 14 fichas con captura real y anillo de puntuación, modal con radar SVG de
  10 categorías, fortalezas/debilidades, datos de ejecución y demos en vivo. Datos
  embebidos para funcionar en `file://`.
- **README** con ranking global, desglose por categoría y matriz de cumplimiento.
- **Documentación** en [`docs/`](docs/): metodología, rúbrica, resultados detallados
  por entrega, arnés técnico/reproducibilidad, conclusiones y guía de contribución.
- **Datos crudos** versionados: [`assets/benchmark.json`](assets/benchmark.json) y
  [`assets/runtime.json`](assets/runtime.json), más capturas en `assets/previews/`.
- **Despliegue y auto-despliegue continuo (CD):** Publicado el benchmark en producción en `https://universo-arena.alexanderoviedofadul.dev` mediante el servidor web Caddy e implementado un webhook en NodeJS (puerto 3020) con firma criptográfica de seguridad en GitHub para actualizaciones automáticas en caliente.
- **Documentación de despliegue:** Creado [`docs/deployment.md`](docs/deployment.md) detallando la infraestructura y pasos para configurar el webhook de integración continua.
- **Banner** del proyecto y scaffolding GitHub (`LICENSE` MIT, `.gitignore`, `CLAUDE.md`).

### Resultados destacados

- 🥇 **GPT-5.5 · Codex** y 🥈 **Claude Opus 4.8 · Ultracode** empatan en cabeza (97/100).
- **14/14** entregas arrancan y renderizan; **12/14** sin un solo error de consola.
- El bug más discriminante: la **cola del cometa Halley apuntando hacia el Sol**.

### Corregido

- **Caso GLM-5.2:** una revisión estática inicial declaró erróneamente "pantalla
  negra / no arranca" a `GLM-5.2-Claude-Code`. La ejecución real (279 objetos, 0
  errores, UI completa) lo desmintió; su nota se corrigió de 38 a **89** mediante
  re-evaluación con contexto de *runtime*. Documentado como lección metodológica.

### Notas

- Las puntuaciones reflejan **una sola ejecución** por entrega (no se mide varianza).
- Los FPS se miden bajo SwiftShader (software) y son solo una señal cualitativa.

[1.0.0]: https://github.com/alexanderoviedofadul/Universo-Arena/releases/tag/v1.0.0
