# Rediseño de la galería con el kit de marca (11-oct-2026)

Galería nueva en `index.html`, **generada** desde `assets/benchmark.json`, y primer manual de marca
(`docs/Manual_Marca_UniversoArena/v1.0/`). Kit de referencia: KANSA v6.0, en su adaptación de Pentest C360 v1.0.

## 1. Qué había

| | Antes |
|---|---|
| Galería | Un `index.html` de 150 KB hecho a mano, con el `const DATA = [...]` reinyectado a mano tras cada tanda y los contadores del «estado del arte» escritos a mano (se quedaron atrás más de una vez: `c905798`) |
| Scripts | Todo en línea, así que la CSP necesitaba `'unsafe-inline'` para scripts también en la portada |
| Marca | Ninguna escrita. El Sol de la barra (`.brand .dot`) y un `:root` de colores. Inter declarada y **nunca cargada** |
| Imagen social | `assets/og-image.png` (920 KB): el Sol en el **centro** de órbitas concéntricas —justo lo que el benchmark penaliza— y un lema en inglés sin fuente |
| Errores | Un error de consola en producción (Lighthouse «Best Practices» 96) y el pie enlazaba `README.md`, que Caddy responde 404 |
| Datos inexactos | La FAQ decía que el arnés está versionado en GitHub (vive fuera del repositorio); «MiniMax M3 pasa de 79 a 92» (ya tenía 95) |

## 2. Qué hay ahora

- **Manual de Marca v1.0 «El Sol en el foco»** — ver su [README](../Manual_Marca_UniversoArena/v1.0/README.md).
  El Sol no se rediseña: es el `.brand .dot` pasado a vector, y el audit lo compara con la galería anterior.
  Paleta cerrada de 30 colores, PDF de 40 páginas, portable sin red, `audit_v1.py` en **0 fallos**.
- **`scripts/generar_galeria.py`** escribe `index.html`, `assets/hub/fichas.js`, las capturas en WebP
  (`assets/hub/previews/`, 480 y 800 px), el cartel de la parada 04 y `assets/og-universo-arena-v1.png`.
  Ninguna cifra se escribe a mano: entregas, nota media, «sin errores», empates, colas correctas, instancing,
  la dispersión por agente y el número de entregas de cada tier se calculan.
- **Estructura**: hero con la órbita de la marca en capas (paralaje) → recorrido de cinco paradas (patrón
  ScrollWorld): el reto, la rúbrica, la ejecución, las dos trampas, la calibración → podio → galería de 36
  tarjetas con orden y filtro → ficha de cada entrega en un `<dialog>` (radar, barras, requisitos, lo que hizo
  bien y lo que falló, demo y código en GitHub) → hallazgos y estado del arte → método (tres señales, tabla de
  tiers, documentos) → preguntas frecuentes (las mismas del JSON-LD).
- **Sin scripts en línea**: solo `application/ld+json`. GSAP 3.15, ScrollTrigger y Lenis 1.3.26
  (`assets/hub/vendor/`, copias de las de Pentest C360 ← KANSA) se piden en la primera interacción; nunca con
  movimiento reducido ni ahorro de datos.
- **Abre con doble clic**: rutas relativas, y los datos de las fichas en un `<script src>`, no en un `fetch`.
- **Las 36 carpetas de entregas no se tocaron** (`git diff --stat` sobre ellas: vacío).

### Carteles (MiniMax, 11-oct-2026, revisados uno a uno)

| Parada | Cartel | Revisión |
|---|---|---|
| 01 El reto | Un punto de luz que se abre en hilos hacia planetas de colores | Aceptado |
| 02 La rúbrica | Astrolabio y planetario de latón | Aceptado (los grabados no forman texto legible) |
| 03 La ejecución | Observatorio con la cúpula abierta bajo la Vía Láctea | Aceptado |
| 04 Las dos trampas | **La órbita de la marca, dibujada por código** | Se pidieron tres carteles: uno sin Sol (ambiguo), uno con la **cola hacia el Sol** —el error que el benchmark penaliza— y además con bandas negras y una firma, y otro con la cola a 57° de la dirección anti-solar. Una imagen de IA no garantiza la física: esta parada usa `M.portada_html()` del manual |
| 05 La calibración | Balanza de vidrio en equilibrio | Aceptado |

Sin personas, sin texto, sin logotipos. WebP a 640/960/1280 px (3–25 KB).

## 3. Verificación en el ensayo

Caddy local en `127.0.0.1:8197` sirviendo el árbol de trabajo con la CSP propuesta para la portada
(`script-src 'self'`) y la actual para el resto. Chromium 1228 de Playwright.

| Prueba | Resultado |
|---|---|
| Consola (errores y avisos), 1440 y 390 px, recorriendo la página | **0** |
| Violaciones de CSP con `script-src 'self'` | **0** |
| Peticiones a otros dominios al cargar | **0** |
| Desborde horizontal | **0** (scrollWidth = ancho) |
| axe (WCAG 2.1 A/AA + buenas prácticas), página y ficha abierta, 1440 y 390 | **0** (tras hacer enfocable la tabla de tiers en móvil) |
| Sin JavaScript | 0 textos ocultos, 36 tarjetas y 36 enlaces a demo; los botones «Ver ficha» no aparecen |
| Movimiento reducido | GSAP no se carga; 0 elementos sin revelar |
| Orden y filtro | Tier B → 6 tarjetas; «Rendimiento» reordena; la ficha abre con `showModal` y devuelve el foco |
| Enlaces a las 36 demos | 36 × 200 |
| `audit_v1.py` del manual (incluye la galería, `llms.txt` y `sitemap.xml`) | **0 fallos** |

## 4. Medición (Lighthouse 12.6.0 móvil, producción, 3 corridas)

| | Rendimiento | Accesibilidad | Buenas prácticas | SEO | LCP | TBT | Peso |
|---|---|---|---|---|---|---|---|
| Antes | 100 · 100 · 100 | 100 | 96 (error de consola) | 100 | 1,1–1,3 s | 0–50 ms | 615 KiB |
| Después | _ver §8_ | | | | | | |

## 5. Seguridad

- **Webhook** (`/root/webhooks/universo-arena-webhook.js`, fuera de este repositorio): solo verificaba la
  firma **si llegaba la cabecera**, así que un POST sin firma con `ref` de `main` lanzaba un `git pull`; y
  tenía un secreto de respaldo escrito en el código. Ahora la firma es obligatoria (401 sin ella o con una
  falsa) y sin la variable de entorno rechaza todo. Probado: sin firma 401, firma falsa 401, firma válida 200.
  Copia previa en `universo-arena-webhook.js.pre-firma-20261011`. Las entregas de GitHub ya venían firmadas.
- **El secreto del webhook está en la unidad de systemd** (`Environment=` en
  `/etc/systemd/system/universo-arena-webhook.service`, modo 644: legible por cualquier usuario del VPS).
  Recomendado: moverlo a un `EnvironmentFile` en 600 y rotarlo en GitHub. No lo hice: es del operador.

## 6. Caddy (propuesta; este rediseño no lo edita)

La galería ya no ejecuta scripts en línea. Propuesta: en el bloque `universo-arena.alexanderoviedofadul.dev`,
una CSP estricta **solo para la portada**, sin tocar la de las demos (que necesitan `unsafe-eval` y los CDN
de BabylonJS):

```caddy
	@portada path / /index.html
	header @portada Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests"
```

(Un `header` con matcher se aplica después del bloque `header { … }` global y sustituye su CSP para esas rutas.
`style-src` conserva `'unsafe-inline'` por los atributos `style="--c:…"` de las tarjetas.)

## 7. Trampas

- **Un `caddy reload` de ensayo habla con el admin de producción** si la configuración de ensayo lleva
  `admin off`: el comando usa `localhost:2019` por defecto. Pasó durante este trabajo: producción **rechazó**
  la carga (puerto ocupado) y conservó su configuración; se comprobaron 200 en cinco dominios. Para el ensayo,
  parar y volver a lanzar `caddy run`, nunca `caddy reload`.
- **Lenis se queda con el scroll**: en Playwright, `scrollIntoView()` después de mover la rueda no lleva a
  la parada (Lenis vuelve a su objetivo). Probar las paradas con movimiento reducido o sin interacción previa.
- **`preserveAspectRatio="xMidYMid slice"`** en el hero: en móvil el Sol (x = 1230 de 1600) queda fuera
  del encuadre y se ven solo las órbitas. Es decorativo; el titular es el LCP.

## 8. Producción
