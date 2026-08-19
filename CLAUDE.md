# CLAUDE.md

Guidance for Claude Code (and other agents) working in this repository.

## What this repo is

**Universo-Arena** is an open benchmark: many combinations of **LLM + coding agent** each implement the *same* prompt — a 3D Solar System simulation in BabylonJS, as a single self-contained `index.html` — and are scored and ranked. The repo also contains a showcase website and full documentation of the benchmark.

- The challenge: [`Prompt-Maestro_v2.txt`](Prompt-Maestro_v2.txt).
- Each entry lives in its own folder; **the folder name encodes the model and agent used** (e.g. `Opus-4.8-Claude-Code`, `codex-gpt-5.5`, `mini-agent-MiniMax-M3`).

## Repository layout

```
Universo-Arena/
├── index.html                  # showcase gallery (data embedded; works on file://)
├── README.md                   # benchmark summary + ranking tables (data-driven)
├── CHANGELOG.md                # Keep a Changelog format
├── CLAUDE.md                   # this file
├── LICENSE                     # MIT
├── Prompt-Maestro_v2.txt       # the challenge every entry implements
├── assets/
│   ├── benchmark.json          # SINGLE SOURCE OF TRUTH for the ranking
│   ├── runtime.json            # objective runtime data (meshes, console errors, webgl)
│   ├── universo_arena_banner.png
│   └── previews/<folder>.png   # real screenshot per entry
├── docs/                       # methodology, rubric, results, harness, conclusions, contributing,
│                               #   + seo-geo / security-audit / pagespeed reports (skills -100)
├── robots.txt · sitemap.xml    # SEO discovery (regenerate from benchmark.json)
├── llms.txt · llms-full.txt    # GEO/AEO: resumen citable + contexto extendido para LLMs
├── humans.txt
├── .well-known/security.txt    # RFC 9116
├── assets/og-image.png         # imagen social 1200×630 (Open Graph / Twitter)
└── <Modelo>-<Agente>/index.html   # one folder per benchmark entry
```

## Conventions (important)

- **Language:** all user-facing text, comments and docs are in **Spanish**.
- **Folder naming = the entry's identity.** Format `<Modelo>-<Agente>`. Don't rename without updating `benchmark.json`, previews and links.
- **Each entry is ONE self-contained `index.html`** (HTML+CSS+JS, BabylonJS via CDN). No local assets, no server, opens with double-click. **Original work per folder** — never copy one entry into another.
- **The showcase `index.html` embeds data inline** (a `const DATA = [...]`), NOT via `fetch`. This is deliberate: `fetch` of a local JSON fails under `file://` (CORS). After editing `assets/benchmark.json`, you MUST re-inject it into `index.html` (replace the `DATA` array).
- **`assets/benchmark.json` is the source of truth.** README tables, `docs/results.md` and the gallery all derive from it. Regenerate downstream artifacts when it changes.
- **Previews are committed** so the gallery looks complete offline; only the live demos need internet (CDN).
- Avoid global-name collisions in the gallery JS (e.g. don't declare `const top`/`const name` at top level — they clash with `window.*`).

## The "regla absoluta" when authoring a new simulation

Before writing BabylonJS code, **consult the official docs** (Context7 library id `/babylonjs/documentation`) and do not invent APIs. In this benchmark, invented APIs (`emissionRange`, `mesh.diameter`) were the direct cause of visible bugs. The two correctness traps that decide the ranking:

1. **Sun at the ellipse focus**, not the center: `x = a·cosθ − a·e`, `z = b·sinθ`, `b = a·√(1−e²)`.
2. **Comet tail points AWAY from the Sun** (`cometa − Sol`), recalculated each frame. Watch out for `Vector3.normalize()` mutating in place.

## How to verify / regenerate

- **Verify a single sim:** `open "<folder>/index.html"` (macOS) and check the browser console.
- **Regenerate screenshots + runtime data:** see [`docs/harness.md`](docs/harness.md) (Puppeteer + system Chrome, headless WebGL via SwiftShader). Outputs `assets/previews/*.png` and `assets/runtime.json`.
- **After changing `benchmark.json`:** regenerate README tables + `docs/results.md`, and re-inject the JSON into the root `index.html`.
- **Add a new entry:** follow [`docs/contributing.md`](docs/contributing.md). The benchmark currently holds **36 entries**. When scoring new ones, **verify each score against the runtime** before integrating: jurors tend to run ~3-4 points generous, so re-check against the actual execution (meshes, console errors, screenshot) and do not let an un-calibrated score leapfrog the calibrated leaders. See the batch records [`docs/segunda-tanda-2026-06-17.md`](docs/segunda-tanda-2026-06-17.md), [`docs/tercera-tanda-2026-06-18.md`](docs/tercera-tanda-2026-06-18.md), [`docs/cuarta-tanda-2026-07-05.md`](docs/cuarta-tanda-2026-07-05.md), [`docs/quinta-tanda-2026-07-23.md`](docs/quinta-tanda-2026-07-23.md), [`docs/sexta-tanda-2026-07-27.md`](docs/sexta-tanda-2026-07-27.md), [`docs/septima-tanda-2026-07-29.md`](docs/septima-tanda-2026-07-29.md), [`docs/octava-tanda-2026-08-07.md`](docs/octava-tanda-2026-08-07.md), [`docs/novena-tanda-2026-08-07.md`](docs/novena-tanda-2026-08-07.md) and [`docs/decima-tanda-2026-08-07.md`](docs/decima-tanda-2026-08-07.md) for the procedure.

## Build / runtime

There is **no build step and no runtime dependencies** for the site — it's vanilla HTML/CSS/JS using modern browser features. The only tooling is the optional benchmark harness (Node + Puppeteer) used to capture screenshots; that lives in a temp dir, not in the repo.

## SEO, GEO/AEO, seguridad y rendimiento (skills `-100`, 2026-06-15)

El sitio en producción está auditado al máximo. Si cambias el `<head>` de la
galería, las metas o el ranking, mantén la coherencia con estos artefactos:

- **SEO/GEO:** el `<head>` de `index.html` lleva Open Graph + Twitter Card +
  JSON-LD (`@graph`: WebSite, Dataset, ItemList, FAQPage). `robots.txt`,
  `sitemap.xml`, `llms.txt` y `llms-full.txt` **se derivan de
  `assets/benchmark.json`** — si cambia el ranking, regenéralos (ver
  [`docs/seo-geo-2026-06-15.md`](docs/seo-geo-2026-06-15.md)). El `ItemList` y el
  `llms.txt` respetan el orden del podio (empate 97: GPT-5.5 🥇, Opus Ultracode 🥈).
- **Imagen social:** `assets/og-image.png` es **1200×630** (no el banner cuadrado).
  Regenérala con ImageMagick si cambia el banner.
- **Seguridad:** los headers (HSTS, CSP, COOP, CORP, Permissions-Policy), el
  redirect HTTP→HTTPS (`308`) y el bloqueo de paths sensibles viven en el
  **`Caddyfile` del VPS** (`/etc/caddy/Caddyfile`, vhost `universo-arena…`), NO en
  el repo. La CSP mantiene `unsafe-eval` a propósito (BabylonJS lo requiere). Ver
  [`docs/security-audit-2026-06-15.md`](docs/security-audit-2026-06-15.md).
- **PageSpeed:** 100/100/100/100. El contraste de textos pequeños depende del token
  CSS `--faint` (debe mantener ≥ 4.5:1 sobre `#0c0f1f`). Ver
  [`docs/pagespeed-2026-06-15.md`](docs/pagespeed-2026-06-15.md).
- **Re-auditar:** `wc360 perf <url>` (PageSpeed) y `wc360 sec <url>` (headers).

## Git

- The project is published at `github.com/alexanderoviedofadul/Universo-Arena`; history is on `main`.
- Commit/push only when the user asks. End commit messages with the required `Co-Authored-By` trailer.
- **Despliegue y CD:** El sitio web se expone en `https://universo-arena.alexanderoviedofadul.dev`. Cuenta con un auto-despliegue continuo (CD) mediante un webhook en Node.js que escucha en el puerto `3020` del VPS y actualiza automáticamente los archivos locales en la rama `main` tras recibir el evento push de GitHub.
