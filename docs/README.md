# 📚 Documentación · Universo-Arena

Documentación completa del benchmark, su metodología y cómo reproducirlo o ampliarlo.

| Documento | Contenido |
|:--|:--|
| **[methodology.md](methodology.md)** | Cómo se evaluó: las tres señales (rúbrica, ejecución real, calibración), por qué y sus límites. |
| **[rubric.md](rubric.md)** | La rúbrica de 100 puntos: las 10 categorías, sus máximos y criterios de puntuación. |
| **[results.md](results.md)** | Ficha detallada de las 36 entregas: desglose, runtime, fortalezas, debilidades y veredicto. |
| **[harness.md](harness.md)** | El arnés técnico: pipeline multi-agente, capturas con Chrome headless y reproducibilidad. |
| **[conclusions.md](conclusions.md)** | Análisis comparativo, conclusiones y estado del arte (versión extendida). |
| **[contributing.md](contributing.md)** | Cómo añadir una nueva entrada y regenerar el benchmark y la galería. |
| **[segunda-tanda-2026-06-17.md](segunda-tanda-2026-06-17.md)** | Ampliación 14→17: las 3 entradas nuevas, su calibración verificada por *runtime* y el hallazgo de la familia GLM 5.2. |
| **[tercera-tanda-2026-06-18.md](tercera-tanda-2026-06-18.md)** | Ampliación 17→19: 2 entradas (OpenCode·MiniMax y Pi·DeepSeek), y cómo Pi·DeepSeek arregla las trampas que otra entrada DeepSeek falló. |
| **[cuarta-tanda-2026-07-05.md](cuarta-tanda-2026-07-05.md)** | Ampliación 20→23: 3 entradas (Fable 5·Ultracode, MiMo·Claude Code, MiMo·OpenCode) y el hallazgo MiMo v2.5 Pro con tres agentes. |
| **[quinta-tanda-2026-07-23.md](quinta-tanda-2026-07-23.md)** | Ampliación 23→25: 2 entradas Gemini 3.6 Flash (Antigravity y Antigravity CLI) y el hallazgo de que 3.6 Flash no supera a 3.5 con el mismo agente. |
| **[sexta-tanda-2026-07-27.md](sexta-tanda-2026-07-27.md)** | Ampliación 25→26: entrada de Claude Opus 5 (Ultracode + Claude Code), con auditoría adversarial y jurado calibrado sobre el archivo final. |
| **[septima-tanda-2026-07-29.md](septima-tanda-2026-07-29.md)** | Ampliación 26→28: 2 entradas Kimi K3 (Claude Code y OpenCode) y el salto generacional de Kimi (K2.7 tier B → K3 tier S/A). |
| **[octava-tanda-2026-08-07.md](octava-tanda-2026-08-07.md)** | Ampliación 28→29: GPT-5.6 Terra · Codex (79, tier B) — regresión frente a GPT-5.5 (97) por fallar el foco pese a acertar la cola. |
| **[novena-tanda-2026-08-07.md](novena-tanda-2026-08-07.md)** | Ampliación 29→31: DeepSeek V4 Flash · OpenCode (92, tier S, re-verificado de 96) y Claude Opus 4.6 · Antigravity (78, tier B, falla ambas trampas). |
| **[decima-tanda-2026-08-07.md](decima-tanda-2026-08-07.md)** | Ampliación 31→36: 3× GLM 5.3 (OpenCode 91, Zcode 90, Claude Code 89) y 2× Gemini 3.7 Flash (High 90, CLI 86); ninguna alcanza a las hermanas 5.2/podio. |
| **[deployment.md](deployment.md)** | Infraestructura de despliegue en producción y webhook de auto-despliegue continuo (CD). |
| **[seo-geo-2026-06-15.md](seo-geo-2026-06-15.md)** | Auditoría y mejora SEO + GEO/AEO: Open Graph/Twitter por red social, `llms.txt`, `sitemap.xml`, `robots.txt` y JSON-LD. |
| **[security-audit-2026-06-15.md](security-audit-2026-06-15.md)** | Auditoría de ciberseguridad (websec-100): redirect HTTP→HTTPS, bloqueo de paths sensibles, headers OWASP, CSP y `security.txt`. |
| **[pagespeed-2026-06-15.md](pagespeed-2026-06-15.md)** | Optimización PageSpeed/Lighthouse a **100/100/100/100** (Performance, Accessibility, Best Practices, SEO). |

## Enlaces rápidos

- 🌐 **Galería interactiva:** [`../index.html`](../index.html)
- 🏆 **Resumen y ranking:** [`../README.md`](../README.md)
- 📜 **El reto:** [`../Prompt-Maestro_v2.txt`](../Prompt-Maestro_v2.txt)
- 🗂️ **Datos crudos:** [`../assets/benchmark.json`](../assets/benchmark.json) · [`../assets/runtime.json`](../assets/runtime.json)

## En una frase

> Un mismo prompt exigente (una simulación 3D del Sistema Solar con BabylonJS en un único `index.html`), 23 combinaciones distintas de **LLM + agente de código**, evaluadas con una rúbrica y, sobre todo, **ejecutándolas de verdad** en un navegador.
