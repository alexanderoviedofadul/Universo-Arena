# 🌌 Universo-Arena

<p align="center">
  <img src="assets/og-universo-arena-v1.png" alt="Universo-Arena: un prompt, muchos universos. El Sol en el foco de una órbita elíptica y un cometa con la cola lejos del Sol" width="100%">
</p>

### Un mismo prompt. 36 combinaciones de LLM + agente de código. Una sola pasada. ¿Quién construye el mejor universo 3D?

<p align="center">
  <img alt="Entregas" src="https://img.shields.io/badge/entregas-36-7c9cff">
  <img alt="Ganador" src="https://img.shields.io/badge/%F0%9F%A5%87-GPT--5.5%20·%20Codex%20(97)-ffd24a">
  <img alt="Sin errores" src="https://img.shields.io/badge/sin%20errores-34%2F36-56e0a6">
  <img alt="Tecnología" src="https://img.shields.io/badge/BabylonJS-WebGL-bb464b">
  <img alt="Licencia" src="https://img.shields.io/badge/licencia-MIT-blue">
</p>

<p align="center">
  <img alt="PageSpeed" src="https://img.shields.io/badge/PageSpeed-100%2F100%2F100%2F100-56e0a6">
  <img alt="Seguridad" src="https://img.shields.io/badge/headers-HSTS%20·%20CSP%20·%20COOP%2FCORP-ffd24a">
  <img alt="LLM-friendly" src="https://img.shields.io/badge/llms.txt-✓-7c9cff">
  <img alt="Despliegue" src="https://img.shields.io/badge/live-universo--arena.alexanderoviedofadul.dev-c08bff">
</p>


**Universo-Arena** es un *benchmark* abierto que enfrenta a distintos modelos de lenguaje (LLM) y agentes de codificación ante un mismo reto exigente: implementar, en **un único `index.html` autocontenido**, una **simulación 3D del Sistema Solar con BabylonJS** siguiendo al pie de la letra [`Prompt-Maestro_v2.txt`](Prompt-Maestro_v2.txt).

Cada carpeta del repositorio contiene la entrega de una combinación distinta — y su **nombre indica el modelo y el agente usados** (p. ej. `Opus-4.8-Claude-Code` = *Claude Opus 4.8* con *Claude Code*; `codex-gpt-5.5` = *GPT‑5.5* con *Codex*).

> 🔭 **[Ver la galería interactiva con resultados, fichas y demos en vivo →](index.html)**
> *(abre `index.html` en la raíz: ranking, radar por categorías, capturas reales y enlace a cada simulación)*

---

## 🎯 El reto

`Prompt-Maestro_v2.txt` no es un *"hola mundo"*. Pide una escena completa y físicamente plausible en un solo archivo, sin assets locales ni servidor:

- ☀️ **Sol** central emisivo con corona de partículas, pulso de escala y luz puntual.
- 🪐 **8 planetas + Plutón** (enano) con **órbitas elípticas** (Sol en el foco), velocidad orbital tipo **Kepler** (inversa a la distancia), inclinación de plano orbital, eje axial propio y etiquetas billboard.
- ☄️ **Cometa Halley** con órbita excéntrica y **cola que siempre apunta en sentido opuesto al Sol** (recalculada cada frame).
- 🌑 **Cinturón de asteroides** (200+), **anillos de Saturno**, **3000+ estrellas** de fondo y **nebulosas** procedurales.
- 🎬 **Post‑procesado** (bloom + glow + tone mapping), cámara `ArcRotateCamera` con auto‑rotación y **panel de configuración** con 4 secciones y decenas de controles.
- 📜 **Regla absoluta:** consultar la documentación oficial de BabylonJS (vía *context7*) **antes** de escribir código y **no inventar APIs**.

Todo ello generado en **una sola pasada** por cada agente.

---

## 🧪 Metodología

La evaluación combina **tres señales independientes** para evitar tanto la subjetividad como las alucinaciones del juez:

1. **Rúbrica de 100 puntos** sobre 10 categorías (escena, fidelidad orbital, cometa Halley, estética, panel UI, cámara, post‑procesado, rendimiento, robustez y calidad de código). Un jurado‑LLM por implementación leyó el `index.html` completo y el spec, y puntuó **verificando el código, no los comentarios**.
2. **Ejecución real en Chrome *headless*** (WebGL vía SwiftShader) de las 36 entregas: se capturó **captura de pantalla**, número de **mallas en escena**, **FPS** y, sobre todo, **errores de consola y excepciones** reales. Ningún archivo se juzga solo por su código: se juzga por lo que hace al abrirse.
3. **Calibración adversarial + corrección por *runtime*.** Un juez final normalizó las notas entre jurados. Donde la revisión estática contradijo la ejecución real, **mandó la ejecución real** (ver "El caso GLM‑5.2" más abajo).

> Orquestado con un *pipeline* multi‑agente (15+ subagentes): un evaluador por entrega en paralelo, un calibrador, y re‑evaluaciones dirigidas para las contradicciones. Toda la data cruda vive en [`assets/benchmark.json`](assets/benchmark.json) y [`assets/runtime.json`](assets/runtime.json).

---

## 🏆 Resultados

<!-- TABLES:START -->
### 🏆 Ranking global

| # | | Modelo | Agente / Herramienta | Puntuación | Tier | Errores consola | Líneas | Demo |
|--:|:--|:--|:--|:--:|:--:|:--:|--:|:--:|
| 1 | 🥇 | **GPT-5.5** | Codex | **97** | S | ✅ 0 | 1496 | [▶](codex-gpt-5.5/index.html) |
| 2 | 🥈 | **Claude Opus 4.8** | Ultracode + Claude Code | **97** | S | ✅ 0 | 1496 | [▶](Opus-4.8-Ultracode-Extension-Claude-Code/index.html) |
| 3 | 🥉 | **Claude Opus 5** | Ultracode + Claude Code | **97** | S | ✅ 0 | 2432 | [▶](Opus-5-Claude-Code-Ultracode/index.html) |
| 4 |  | **GLM 5.2** | OpenCode | **95** | S | ✅ 0 | 1080 | [▶](Opencode-GLM-5.2/index.html) |
| 5 |  | **MiniMax M3** | OpenCode | **95** | S | ✅ 0 | 1165 | [▶](Opencode-Minimax-M3/index.html) |
| 6 |  | **Claude Opus 4.8** | Claude Code | **95** | S | ✅ 0 | 995 | [▶](Opus-4.8-Claude-Code/index.html) |
| 7 |  | **MiMo v2.5 Pro** | MiMoCode | **95** | S | ✅ 0 | 1151 | [▶](Mimo-V2.5-Pro-MimoCode/index.html) |
| 8 |  | **Claude Fable 5** | Ultracode + Claude Code | **95** | S | ✅ 0 | 1355 | [▶](Fable-5-Claude-Code-Ultracode/index.html) |
| 9 |  | **Gemini 3.5 (High)** | Antigravity | **92** | S | ✅ 0 | 1533 | [▶](Antigravity-Gemini-3.5-High/index.html) |
| 10 |  | **MiniMax M3** | Claude Code | **92** | S | ✅ 0 | 1062 | [▶](Minimax-M3-Claude-Code/index.html) |
| 11 |  | **Kimi K3** | Claude Code | **92** | S | ✅ 0 | 1245 | [▶](Kimi-K3-Claude-Code/index.html) |
| 12 |  | **DeepSeek V4 Flash** | OpenCode | **92** | S | ✅ 0 | 1131 | [▶](Opencode-DeepSeek-V4-Flash/index.html) |
| 13 |  | **GLM 5.3** 🆕 | OpenCode | **91** | S | ✅ 0 | 1041 | [▶](Opencode-GLM-5.3/index.html) |
| 14 |  | **MiMo v2.5 Pro** | Claude Code | **90** | S | ✅ 0 | 1005 | [▶](Mimo-V2.5-Pro-Claude-Code/index.html) |
| 15 |  | **GLM 5.3 (Max)** 🆕 | Zcode | **90** | S | ✅ 0 | 1381 | [▶](Zcode-GML-5.3-Max/index.html) |
| 16 |  | **Gemini 3.7 Flash (High)** 🆕 | Antigravity | **90** | S | ✅ 0 | 1752 | [▶](Antigravity-Gemini-3.7-Flash-High/index.html) |
| 17 |  | **Gemini 3.5 Flash** | Antigravity CLI | **89** | A | ✅ 0 | 1637 | [▶](Agy-Gemini-3.5-Flash-Antigravity-CLI/index.html) |
| 18 |  | **GLM 5.2** | Claude Code | **89** | A | ✅ 0 | 1306 | [▶](GLM-5.2-Claude-Code/index.html) |
| 19 |  | **GLM 5.2 (Max)** | Zcode | **89** | A | ✅ 0 | 1275 | [▶](Zcode-GML-5.2-Max/index.html) |
| 20 |  | **MiMo v2.5 Pro** | OpenCode | **89** | A | ✅ 0 | 1239 | [▶](Mimo-V2.5-Pro-OpenCode/index.html) |
| 21 |  | **Gemini 3.6 Flash (High)** | Antigravity | **89** | A | ✅ 0 | 1249 | [▶](Antigravity-Gemini-3.6-Flash-High/index.html) |
| 22 |  | **GLM 5.3** 🆕 | Claude Code | **89** | A | ✅ 0 | 1567 | [▶](GLM-5.3-Claude-Code/index.html) |
| 23 |  | **DeepSeek V4 Pro** | CodeWhale | **88** | A | ✅ 0 | 1251 | [▶](codewhale-deepseek-v4-pro/index.html) |
| 24 |  | **DeepSeek V4 Pro** | Pi | **88** | A | ✅ 0 | 1575 | [▶](Pi-DeepSeek-v4-pro/index.html) |
| 25 |  | **Kimi K3** | OpenCode | **87** | A | ✅ 0 | 1544 | [▶](Kimi-K3-Open-Code/index.html) |
| 26 |  | **Claude Sonnet 4.6** | Antigravity IDE | **86** | A | ✅ 0 | 1592 | [▶](Claude-Sonnet-4.6-Antigravity-IDE/index.html) |
| 27 |  | **Gemini 3.7 Flash** 🆕 | Antigravity CLI | **86** | A | ✅ 0 | 2370 | [▶](Agy-Gemini-3.7-Flash-Antigravity-CLI/index.html) |
| 28 |  | **Gemini 3.6 Flash** | Antigravity CLI | **85** | A | ✅ 0 | 1510 | [▶](Agy-Gemini-3.6-Flash-Antigravity-CLI/index.html) |
| 29 |  | **Kimi K2.7** | Claude Code | **80** | B | ⚠️ 1 | 696 | [▶](Kimi-k.7-code-Claude-Code/index.html) |
| 30 |  | **Kimi K2.7** | Kimi Code CLI | **79** | B | ⚠️ 1 | 541 | [▶](kimi-k2.7-code-Kimi-Code-CLI/index.html) |
| 31 |  | **MiniMax M3** | mini-agent | **79** | B | ✅ 0 | 1100 | [▶](mini-agent-MiniMax-M3/index.html) |
| 32 |  | **GPT-5.6 Terra** | Codex | **79** | B | ✅ 0 | 120 | [▶](codex-gpt-5.6-terra/index.html) |
| 33 |  | **DeepSeek V4 Pro** | Pi Coding Agent | **78** | B | ✅ 0 | 1276 | [▶](deepseek-v4-pro-Pi-Coding-Agent/index.html) |
| 34 |  | **Claude Opus 4.6** | Antigravity | **78** | B | ✅ 0 | 1824 | [▶](Antigravity-Claude-Opus-4.6/index.html) |
| 35 |  | **Devstral** | Vibe | **70** | C | ✅ 0 | 960 | [▶](vibe-devstral/index.html) |
| 36 |  | **Z.ai GLM 5.2** | Claude Code | **54** | D | ✅ 0 | 624 | [▶](Zai-GLM-5.2-Claude-Code/index.html) |

### 📊 Desglose por categoría

| Modelo (agente) | Escena /20 | Órbitas /12 | Halley /8 | Estética /15 | UI /15 | Cámara /8 | Post-pro /6 | Rend. /6 | Robustez /5 | Código /5 | **Total** |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| GPT-5.5 · Codex | 19 | 12 | 8 | 13 | 15 | 8 | 6 | 6 | 5 | 5 | **97** |
| Claude Opus 4.8 · Ultracode + Claude Code | 19 | 12 | 8 | 13 | 15 | 8 | 6 | 6 | 5 | 5 | **97** |
| Claude Opus 5 · Ultracode + Claude Code | 20 | 12 | 8 | 13 | 15 | 8 | 6 | 6 | 5 | 4 | **97** |
| GLM 5.2 · OpenCode | 19 | 12 | 8 | 13 | 14 | 8 | 6 | 6 | 4 | 5 | **95** |
| MiniMax M3 · OpenCode | 19 | 11 | 8 | 13 | 15 | 8 | 6 | 6 | 5 | 4 | **95** |
| Claude Opus 4.8 · Claude Code | 19 | 10 | 8 | 13 | 15 | 8 | 6 | 6 | 5 | 5 | **95** |
| MiMo v2.5 Pro · MiMoCode | 19 | 11 | 8 | 12 | 15 | 8 | 6 | 6 | 5 | 5 | **95** |
| Claude Fable 5 · Ultracode + Claude Code | 19 | 12 | 8 | 13 | 14 | 7 | 6 | 6 | 5 | 5 | **95** |
| Gemini 3.5 (High) · Antigravity | 18 | 12 | 8 | 11 | 15 | 7 | 6 | 6 | 4 | 5 | **92** |
| MiniMax M3 · Claude Code | 19 | 11 | 8 | 12 | 14 | 8 | 6 | 4 | 5 | 5 | **92** |
| Kimi K3 · Claude Code | 18 | 11 | 8 | 13 | 14 | 7 | 6 | 5 | 5 | 5 | **92** |
| DeepSeek V4 Flash · OpenCode | 18 | 11 | 8 | 12 | 14 | 8 | 6 | 5 | 5 | 5 | **92** |
| GLM 5.3 · OpenCode | 19 | 11 | 7 | 13 | 14 | 7 | 5 | 5 | 5 | 5 | **91** |
| MiMo v2.5 Pro · Claude Code | 18 | 11 | 8 | 11 | 13 | 7 | 6 | 6 | 5 | 5 | **90** |
| GLM 5.3 (Max) · Zcode | 18 | 11 | 8 | 14 | 12 | 7 | 6 | 4 | 5 | 5 | **90** |
| Gemini 3.7 Flash (High) · Antigravity | 19 | 11 | 7 | 14 | 14 | 7 | 5 | 3 | 5 | 5 | **90** |
| Gemini 3.5 Flash · Antigravity CLI | 19 | 9 | 8 | 12 | 14 | 8 | 6 | 5 | 4 | 4 | **89** |
| GLM 5.2 · Claude Code | 20 | 11 | 4 | 13 | 15 | 8 | 6 | 4 | 4 | 4 | **89** |
| GLM 5.2 (Max) · Zcode | 18 | 9 | 8 | 11 | 15 | 7 | 6 | 6 | 4 | 5 | **89** |
| MiMo v2.5 Pro · OpenCode | 17 | 11 | 8 | 11 | 14 | 7 | 6 | 5 | 5 | 5 | **89** |
| Gemini 3.6 Flash (High) · Antigravity | 19 | 11 | 7 | 13 | 14 | 7 | 6 | 4 | 4 | 4 | **89** |
| GLM 5.3 · Claude Code | 19 | 10 | 7 | 13 | 13 | 7 | 6 | 4 | 5 | 5 | **89** |
| DeepSeek V4 Pro · CodeWhale | 19 | 11 | 8 | 11 | 14 | 7 | 6 | 3 | 4 | 5 | **88** |
| DeepSeek V4 Pro · Pi | 19 | 10 | 8 | 12 | 13 | 6 | 6 | 5 | 5 | 4 | **88** |
| Kimi K3 · OpenCode | 18 | 10 | 7 | 12 | 14 | 7 | 6 | 5 | 4 | 4 | **87** |
| Claude Sonnet 4.6 · Antigravity IDE | 18 | 9 | 4 | 12 | 15 | 8 | 6 | 5 | 4 | 5 | **86** |
| Gemini 3.7 Flash · Antigravity CLI | 18 | 11 | 7 | 11 | 14 | 7 | 6 | 4 | 4 | 4 | **86** |
| Gemini 3.6 Flash · Antigravity CLI | 18 | 11 | 7 | 10 | 14 | 7 | 5 | 5 | 4 | 4 | **85** |
| Kimi K2.7 · Claude Code | 17 | 9 | 3 | 11 | 15 | 7 | 6 | 3 | 4 | 5 | **80** |
| Kimi K2.7 · Kimi Code CLI | 18 | 9 | 4 | 11 | 14 | 7 | 6 | 3 | 4 | 3 | **79** |
| MiniMax M3 · mini-agent | 17 | 9 | 3 | 11 | 14 | 7 | 6 | 3 | 4 | 5 | **79** |
| GPT-5.6 Terra · Codex | 17 | 4 | 8 | 12 | 14 | 7 | 6 | 4 | 3 | 4 | **79** |
| DeepSeek V4 Pro · Pi Coding Agent | 19 | 5 | 4 | 12 | 13 | 7 | 6 | 3 | 5 | 4 | **78** |
| Claude Opus 4.6 · Antigravity | 18 | 6 | 5 | 12 | 14 | 7 | 6 | 3 | 3 | 4 | **78** |
| Devstral · Vibe | 15 | 9 | 3 | 10 | 11 | 7 | 6 | 4 | 2 | 3 | **70** |
| Z.ai GLM 5.2 · Claude Code | 9 | 11 | 5 | 7 | 4 | 6 | 0 | 4 | 3 | 5 | **54** |

### ✅ Matriz de cumplimiento

| Modelo (agente) | Órbitas elípticas | Cola Halley correcta | Cinturón | Instancing | Anillos Saturno | Plutón | 3000+ estrellas | Nebulosas | Bloom/Glow | Panel completo | Vistas cámara | deltaTime |
|:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| GPT-5.5 · Codex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Opus 4.8 · Ultracode + Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Opus 5 · Ultracode + Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GLM 5.2 · OpenCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiniMax M3 · OpenCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Opus 4.8 · Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiMo v2.5 Pro · MiMoCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Fable 5 · Ultracode + Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini 3.5 (High) · Antigravity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiniMax M3 · Claude Code | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kimi K3 · Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DeepSeek V4 Flash · OpenCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GLM 5.3 · OpenCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiMo v2.5 Pro · Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GLM 5.3 (Max) · Zcode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| Gemini 3.7 Flash (High) · Antigravity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini 3.5 Flash · Antigravity CLI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GLM 5.2 · Claude Code | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GLM 5.2 (Max) · Zcode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiMo v2.5 Pro · OpenCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini 3.6 Flash (High) · Antigravity | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GLM 5.3 · Claude Code | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DeepSeek V4 Pro · CodeWhale | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DeepSeek V4 Pro · Pi | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kimi K3 · OpenCode | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Sonnet 4.6 · Antigravity IDE | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini 3.7 Flash · Antigravity CLI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gemini 3.6 Flash · Antigravity CLI | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kimi K2.7 · Claude Code | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Kimi K2.7 · Kimi Code CLI | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| MiniMax M3 · mini-agent | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GPT-5.6 Terra · Codex | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| DeepSeek V4 Pro · Pi Coding Agent | — | — | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Claude Opus 4.6 · Antigravity | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Devstral · Vibe | ✅ | — | ✅ | — | — | ✅ | — | ✅ | ✅ | — | ✅ | ✅ |
| Z.ai GLM 5.2 · Claude Code | ✅ | ✅ | — | — | ✅ | — | — | — | — | — | — | ✅ |
<!-- TABLES:END -->

---

## 🔬 Análisis comparativo

**Lo que separó a los mejores: dos trampas de corrección de dominio.** Casi todas las entregas "se ven bien", pero el spec esconde dos detalles que solo se resuelven con razonamiento físico real:

1. **El Sol en el *foco* de la elipse, no en el centro.** Una elipse con el Sol centrado es geométricamente trivial y *parece* correcta; ponerlo en el foco (`x = a·cosθ − a·e`) requiere entender la órbita. El grupo de cabeza (GPT‑5.5, ambos Opus, DeepSeek‑CodeWhale, GLM‑5.2) lo hizo; otros (Gemini, Sonnet 4.6) dejaron el Sol en el centro y perdieron fidelidad. **Fable 5 · Ultracode** fue el primero en ir más allá: resuelve la ecuación de Kepler (`M = E − e·sinE`) por Newton‑Raphson, con aceleración real en el perihelio (2.ª ley) y período ∝ a^1.5 (3.ª ley). **Claude Opus 5 · Ultracode** lleva esa misma mecánica **a cada una de las 250 rocas del cinturón**, donde el resto del campo gira un aro circular en bloque.
2. **La cola del cometa Halley.** Es **el bug más discriminante del benchmark**. El vector "lejos del Sol" es `cometa − Sol`; muchísimas entregas lo invirtieron (`.negate()`, `.scale(-1)` o un `normalize()` mal usado) y **la cola acabó apuntando hacia el Sol** — justo lo contrario de la física. Falló en Sonnet 4.6, ambos Kimi, MiniMax‑mini‑agent, DeepSeek‑Pi, Devstral y, por una mutación *in‑place* de `Vector3.normalize()`, también en GLM‑5.2 y Z.ai‑GLM‑5.2. Acertarlo fue el sello de las entregas de tier S/A altas.

**La trampa de rendimiento: *instancing*.** El cinturón de 200‑260 asteroides es un caso de libro para `createInstance`/*thin instances*. Lo resolvieron GPT‑5.5, los dos Opus 4.8, Gemini, **las tres entradas de la 2.ª tanda** (OpenCode, Antigravity y Zcode) y **las cuatro de MiMo/Fable de la 4.ª**; buena parte del resto creó cientos de mallas y materiales independientes (cientos de *draw calls*), lo que explica los FPS bajos.

**El agente importa tanto como el modelo.** Un mismo LLM rinde distinto según su andamiaje: **MiniMax M3** abarca **95 (OpenCode) · 92 (Claude Code) · 79 (mini‑agent)**, y **MiMo v2.5 Pro** repite el patrón con tres agentes — **95 (MiMoCode) · 90 (Claude Code) · 89 (OpenCode)** —, donde el agente propio del modelo saca su mejor versión. El caso extremo es **GLM 5.2**, con cuatro combinaciones: **95 (OpenCode) · 89 (Claude Code) · 89 (Zcode·Max) · 54 (Z.ai)** — una dispersión de **41 puntos** sobre el mismo modelo base. **OpenCode** repite dos veces en lo más alto (95 con GLM 5.2 y 95 con MiniMax M3): el andamiaje —planificación, consulta de documentación, auto‑verificación— levanta (o hunde) la misma base.

**El mismo modelo, dos veces, distinto resultado.** `Pi-DeepSeek-v4-pro` (**88**) acierta las dos trampas (cola anti‑solar y foco elíptico) que la otra entrada del mismo modelo, `deepseek-v4-pro-Pi-Coding-Agent` (**78**), había fallado — andamiaje y varianza entre ejecuciones, en estado puro.

> **Ampliaciones:** el benchmark creció de 14 a **36 entradas** en diez tandas (14→17 el 2026‑06‑17, 17→19 el 2026‑06‑18, 19→20 el 2026‑07‑04, 20→23 el 2026‑07‑05, 23→25 el 2026‑07‑23, 25→26 el 2026‑07‑27, 26→28 el 2026‑07‑29, 28→29 el 2026‑08‑07, 29→31 el 2026‑08‑07, 31→36 el 2026‑08‑07) con la misma metodología y **verificación contra el *runtime***. El techo sigue en **97** con **triple empate**. Detalle en [`docs/segunda-tanda-2026-06-17.md`](docs/segunda-tanda-2026-06-17.md), [`docs/tercera-tanda-2026-06-18.md`](docs/tercera-tanda-2026-06-18.md), [`docs/cuarta-tanda-2026-07-05.md`](docs/cuarta-tanda-2026-07-05.md), [`docs/quinta-tanda-2026-07-23.md`](docs/quinta-tanda-2026-07-23.md), [`docs/sexta-tanda-2026-07-27.md`](docs/sexta-tanda-2026-07-27.md), [`docs/septima-tanda-2026-07-29.md`](docs/septima-tanda-2026-07-29.md), [`docs/octava-tanda-2026-08-07.md`](docs/octava-tanda-2026-08-07.md), [`docs/novena-tanda-2026-08-07.md`](docs/novena-tanda-2026-08-07.md) y [`docs/decima-tanda-2026-08-07.md`](docs/decima-tanda-2026-08-07.md).

**Una tercera trampa, hallada en la 6.ª tanda: el sentido de giro.** BabylonJS es **levógiro** y una rotación positiva sobre Y lleva **+X → −Z**. Si la elipse se recorre con `z = +b·sinθ` y la rotación propia se aplica con `rotation.y += …`, revolución y rotación van **en sentidos opuestos**: los planetas prógrados giran al revés y Venus, Urano y Plutón acaban prógrados en vez de retrógrados. No lo delata ninguna captura —solo el razonamiento sobre la convención del motor—, y se arregla con un signo. Detalle en [`docs/rubric.md`](docs/rubric.md#un-tercer-discriminador-hallado-en-la-6ª-tanda).

**La regla absoluta predijo los fallos.** Las entregas que ignoraron la consulta de documentación tendieron a **inventar APIs** — `emissionRange`, `mesh.diameter` (Devstral) — que se traducen directamente en bugs visibles (estrellas sin distribuir, anillos en `NaN`). Verificar la documentación no fue burocracia: fue corrección.

### ⚖️ El caso GLM‑5.2: cuando el juez‑LLM alucina y el *runtime* corrige

La revisión estática inicial sentenció a **GLM‑5.2‑Claude‑Code** con un *"bug fatal, pantalla negra"* por unos *strings* de color mal cerrados. **La ejecución real lo desmintió:** 279 mallas en escena, **0 excepciones**, UI completa y bloom activo (ver su captura en la galería). Los *strings* defectuosos existen, pero el navegador los tolera y la escena se construye entera. La nota se corrigió de un injusto 38 a **89**. Moraleja metodológica: **un juez‑LLM sobre código estático sobre‑penaliza; sin ejecución real, un benchmark de agentes no es fiable.**

---

## ✅ Conclusiones

- **El listón base es altísimo.** Las **36** entregas arrancan y renderizan una escena WebGL compleja (1000+ líneas) en una sola pasada, y **34 de 36 con cero errores de consola**. Generar una app 3D autocontenida y funcional ya es terreno resuelto para los agentes frontera.
- **La frontera ya no es "¿funciona?" sino "¿acierta los detalles difíciles?":** foco orbital, signo de un vector, *instancing*, degradación elegante. Ahí se decide todo.
- **Profundidad vs. amplitud.** La mejor mecánica orbital del benchmark (Z.ai‑GLM‑5.2, con Kepler real por Newton‑Raphson) se quedó en el tier D por **entregar una escena incompleta** (sin Plutón, sin asteroides, sin nebulosas, sin post‑procesado). Resolver lo difícil no compensa dejar lo fácil a medias.
- **El andamiaje del agente es un multiplicador**, no un detalle: el mismo modelo gana o pierde un *tier* según su agente.
- **Evaluar agentes exige ejecutarlos.** La corrección de GLM‑5.2 muestra que la revisión estática y la ejecución real discrepan, y que la verdad está en el *runtime*.

---

## 🌐 Estado del arte (junio 2026)

La generación *one‑shot* de una experiencia 3D web compleja y autocontenida ha dejado de ser una hazaña: es el **comportamiento esperable** de un agente de código frontera. Hace poco la pregunta era *"¿puede un LLM escribir 1500 líneas de WebGL que ni siquiera lancen una excepción?"*; hoy la respuesta es *sí, casi siempre*, y el debate se ha desplazado a la **corrección de dominio** y la **disciplina de ingeniería**: entender que el Sol va en el foco, que un vector tiene sentido, que 250 objetos piden *instancing* y que una API debe verificarse antes de usarse.

Los diferenciadores ya no son sintácticos sino **de razonamiento**: física, geometría y arquitectura de rendimiento. Y de forma reveladora, **el agente/andamiaje pesa tanto como el modelo base** — la planificación, la consulta de documentación y los bucles de auto‑verificación convierten a un modelo competente en uno sobresaliente. La cabeza de la tabla la comparten un *GPT‑5.5*, un *Claude Opus 4.8* y un *Claude Opus 5* empatados en 97, con *MiniMax M3* y *Gemini 3.5 Flash* demostrando que el pelotón frontera es ancho y multi‑proveedor.

Por último, este ejercicio deja una lección sobre **cómo se deben medir** los agentes: el *LLM‑as‑judge* sobre código estático es rápido pero falible (llegó a declarar "rota" una entrega que funcionaba perfectamente). El estándar emergente —y el que aquí se aplica— es **juzgar por ejecución**: abrir la app, contar sus objetos, mirar su consola y capturar lo que el usuario realmente ve. El estado del arte de los agentes es excelente; el estado del arte de su *evaluación* apenas empieza a ponerse a su altura.

---

## 📚 Documentación

Toda la documentación vive en [`docs/`](docs/):

| Documento | Contenido |
|:--|:--|
| [docs/methodology.md](docs/methodology.md) | Cómo se evaluó (las tres señales) y sus límites. |
| [docs/rubric.md](docs/rubric.md) | La rúbrica de 100 puntos y las dos "trampas" de corrección. |
| [docs/results.md](docs/results.md) | Ficha detallada de las 36 entregas. |
| [docs/harness.md](docs/harness.md) | El arnés técnico y cómo reproducirlo. |
| [docs/conclusions.md](docs/conclusions.md) | Análisis comparativo y estado del arte (extendido). |
| [docs/contributing.md](docs/contributing.md) | Cómo añadir una nueva entrada. |
| [docs/sexta-tanda-2026-07-27.md](docs/sexta-tanda-2026-07-27.md) | Última ampliación (25→26): Claude Opus 5 · Ultracode, con auditoría adversarial y jurado calibrado sobre el archivo final. |
| [docs/deployment.md](docs/deployment.md) | Infraestructura de despliegue y webhook de auto-deploy (CD). |
| [docs/seo-geo-2026-06-15.md](docs/seo-geo-2026-06-15.md) | SEO + GEO/AEO: Open Graph/Twitter, `llms.txt`, `sitemap.xml`, JSON-LD. |
| [docs/security-audit-2026-06-15.md](docs/security-audit-2026-06-15.md) | Auditoría de ciberseguridad (websec-100): headers OWASP, CSP, `security.txt`. |
| [docs/pagespeed-2026-06-15.md](docs/pagespeed-2026-06-15.md) | PageSpeed/Lighthouse **100/100/100/100**. |

### 🏅 Calidad de producción

El sitio en vivo está auditado y optimizado con la familia de skills `-100`:

- **PageSpeed/Lighthouse**: medición antes/después del rediseño en [`docs/rediseno-2026-10/README.md`](docs/rediseno-2026-10/README.md).
- **Seguridad:** HTTPS forzado (308), HSTS preload-ready, CSP, COOP/CORP, Permissions-Policy, `security.txt` y bloqueo de paths sensibles. **0 violaciones CSP** verificadas en navegador real.
- **SEO + IA:** tarjetas sociales por red (Open Graph/Twitter), `robots.txt`, `sitemap.xml`, datos estructurados JSON-LD y `llms.txt`/`llms-full.txt` para LLMs.

### 🎨 Marca y galería (octubre 2026)

- **[Manual de Marca v1.0 «El Sol en el foco»](docs/Manual_Marca_UniversoArena/v1.0/README.md)**: el Sol de la barra pasado a vector sin rediseñarlo, paleta cerrada de 30 colores con su contraste, Inter y JetBrains Mono autoalojadas, recorrido inmersivo, portable sin red y PDF de 40 páginas. Las cifras del manual se leen del benchmark.
- **La galería se genera**: `python3 -B scripts/generar_galeria.py` escribe `index.html` desde `assets/benchmark.json` (tarjetas, podio, cifras, JSON-LD y metas). Recorrido de cinco paradas por el método, ficha de cada entrega y sin scripts en línea. Las carpetas de las entregas no se tocan.
- Medición y decisiones: [`docs/rediseno-2026-10/README.md`](docs/rediseno-2026-10/README.md).

Historial de cambios en [`CHANGELOG.md`](CHANGELOG.md).

## 📁 Estructura del repositorio

```
Universo-Arena/
├── index.html                  ← 🌐 galería interactiva (GENERADA por scripts/generar_galeria.py; ábrela)
├── scripts/generar_galeria.py  ← genera la galería desde assets/benchmark.json
├── README.md                   ← este documento
├── CHANGELOG.md · CLAUDE.md · LICENSE
├── Prompt-Maestro_v2.txt       ← el reto que todos implementaron
├── docs/                       ← metodología, rúbrica, resultados, arnés, conclusiones
│   └── Manual_Marca_UniversoArena/v1.0/  ← manual de marca (inmersivo, portable, PDF, tokens)
├── assets/
│   ├── benchmark.json          ← fuente de verdad del benchmark (notas, features, runtime)
│   ├── runtime.json            ← datos objetivos de ejecución (meshes, errores)
│   ├── marca/                  ← tokens, fuentes y logos (los copia el build del manual)
│   ├── hub/                    ← CSS, JS, carteles, capturas WebP y fichas de la galería
│   ├── og-universo-arena-v1.png ← imagen para compartir (1200×630)
│   ├── universo_arena_banner.png · og-image.png  ← imágenes anteriores (las citan artículos publicados)
│   └── previews/*.png          ← capturas reales de cada simulación
└── <Modelo>-<Agente>/index.html   ← una carpeta por entrega (36)
```

## ▶️ Cómo usarlo

- **Sitio Web de Producción:** Accede a la galería en vivo en **[https://universo-arena.alexanderoviedofadul.dev](https://universo-arena.alexanderoviedofadul.dev)**.
- **Galería local:** abre [`index.html`](index.html) en la raíz con doble clic.
- **Una simulación concreta:** abre el `index.html` de su carpeta. Requiere conexión a internet (BabylonJS por CDN).
- **Despliegue y Webhook (CD):** El proyecto cuenta con integración y despliegue continuo mediante webhook. Cualquier push en `main` actualiza los archivos automáticamente. Ver detalles en [`docs/deployment.md`](docs/deployment.md).
- **Documentación y reproducibilidad:** ver [`docs/`](docs/).

## 📜 Licencia y créditos

Código bajo licencia [MIT](LICENSE). Reto y curación: **Alexander Oviedo Fadul**. Cada simulación es obra original de la combinación LLM + agente indicada en el nombre de su carpeta. Benchmark, capturas y galería orquestados con un *pipeline* multi‑agente sobre Claude Code.
