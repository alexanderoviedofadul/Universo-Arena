# «Seguridad comprobada» y recorrido guiado (25-oct-2026)

Universo-Arena entra en la segunda oleada del **kit «confianza y recorrido»** (el mismo que llevan Cédula 360,
Cartera360, Enki, PixelCV y Visores). El kit vive en `Configuraciones_Equipos/VPS_Ubuntu_Hostinger/38-confianza-y-recorrido/`;
aquí va su **copia** (`kit-confianza/`, con `KIT_VERSION` y `SHA256SUMS`): no se edita en este repo, se edita el kit y se
vuelve a sincronizar.

## Qué se añadió

| Pieza | Dónde |
|---|---|
| Recorrido guiado: 7 capítulos en escenas, diapositivas y mapa | `conozca/` → **https://universo-arena.alexanderoviedofadul.dev/conozca/** |
| Contenido del recorrido (una sola fuente) | `docs/recorrido/conozca.json` (Caddy no sirve `/docs/*.json`) |
| Kit (motor, estilos, GSAP 3.15.0 local) | `kit-confianza/` (kit 1.0.4) |
| Sección «Seguridad comprobada» | Generada por `scripts/generar_galeria.py` (`seguridad()`), al final de `<main>`, con `--sc-*` a la marca en `assets/hub/galeria.css` |
| Entradas al recorrido | Portada («¿Primera vez aquí? Haz el recorrido guiado»), Método (primera entrada de la lista de documentos) y pie («Recorrido guiado», «Seguridad comprobada», «Reportar una vulnerabilidad») |
| Inter para el recorrido | `assets/hub/fuentes.css` (la misma `@font-face` de la galería) |

El sitio no tiene acceso ni login: las entradas son las de la portada, la ayuda (Método) y el pie.

**Regenerar** (tras cambiar `docs/recorrido/conozca.json` o la galería):

```bash
node <kit>/generar-conozca.mjs docs/recorrido/conozca.json             # escribe conozca/{index.html,tema.css,marcas.css}
node <kit>/generar-conozca.mjs docs/recorrido/conozca.json --comprobar # falla si lo generado no está al día
bash <kit>/../scripts/sincronizar-kit.sh .                             # copia una versión nueva del kit a kit-confianza/
python3 -B scripts/generar_galeria.py && python3 -B docs/Manual_Marca_UniversoArena/v1.0/scripts/audit_v1.py   # 0 fallos
```

### Reglas

- 🔴 **Ninguna cifra a mano.** La sección lee `/salud-publica/publico.json`, que escribe cada noche
  `/root/scripts/salud-publica-ronda.sh` en el VPS con SOLO lo publicable (la calificación más alta, menos de 45 días,
  enlace a la fuente). Sin nada publicable se quita sola (`data-sc-quitar`); por `file://` tampoco aparece.
- 🔴 **El recorrido no escribe el número de entregas** (regla del manual: las cifras salen del benchmark) y **no muestra a
  nadie**: las figuras son los carteles de las paradas (`assets/hub/carteles/`, revisados en el rediseño: sin personas ni
  texto) y la captura de una simulación (`assets/hub/previews/`).
- Marca: colores del manual v1.0 (Vacío `#05060F`, Cosmos `#0A0D1F`, Sol `#FFD24A`, Estelar `#EAF0FF`), Inter, y tuteo
  como la galería (`"tratamiento": "tu"`).
- El recorrido funciona con una CSP **sin `'unsafe-inline'`** (`script-src 'self'; style-src 'self'`): `@conozca` en el
  Caddyfile.
- `security.txt`: el del repo (`.well-known/security.txt`, RFC 9116, contacto propio del proyecto), servido tal cual.

## Lo corregido para merecer la sección (sin cambiar lo que se ve)

| Herramienta | Antes (24-oct, 21:43) | Corrección |
|---|---|---|
| W3C | 48 errores | 36 `aria-label` en `<span class="t-rank">` → texto oculto `.sr` («Puesto »); 2 `aria-label` en `<p class="chips">` → texto oculto; los 5 carteles diferidos sin `src` y con `sizes` sin `srcset` → GIF transparente de 1 px en `src` y `data-sizes` (lo aplica `galeria.js` al cargar) |
| WAVE | 1 error + 710 «contrastes» | Los 710 eran falsos: WAVE reconstruye la página en `wave.webaim.org` y, con `Cross-Origin-Resource-Policy: same-origin` en todo, no cargaba `galeria.css`. Ahora **CORP por tipo** en Caddy (estáticos `cross-origin` + `Access-Control-Allow-Origin *`; el resto `same-origin`). El error era una «referencia ARIA rota»: el `<dialog>` de la ficha citaba `ficha-tit` antes de existir → `aria-label`, y `galeria.js` pone `aria-labelledby` al pintar la ficha |
| Mozilla Observatory | A+ (135/100) | — |
| securityheaders | A+ | — |
| axe (a11y-100) | — | 0 violaciones (portada; recorrido, índice, mapa y 390 px en el e2e) |

## Vista previa y pruebas

Caddy aislado en `127.0.0.1:18740` con la CSP de producción en la portada y la estricta en `/conozca/`:
`e2e-conozca.mjs` del kit en verde (arranque sin errores de consola ni CSP; axe 0 en índice, recorrido, mapa y 390 px;
teclado; reducir movimiento; sin JS; almacenamiento bloqueado; 390/360/320 px sin desplazamiento horizontal; la sección
en `/` con 2 verificaciones, axe 0 y captura ampliable). W3C del `index.html` y de `conozca/index.html`: 0 errores y 0
avisos. `audit_v1.py`: 0 fallos. Revisión visual de las capturas en escritorio y celular.

## Después

(Se completa tras el despliegue con la misma herramienta pública.)

## Pendiente

- La portada mantiene `style-src 'unsafe-inline'`: el generador pinta `style="--c:…"`, `--tc`, `--p` y `opacity:0` en
  tarjetas, podio y carteles (≈80 atributos). Pasarlos a una hoja generada es posible pero no cambia ninguna nota
  (Observatory ya da A+ 135 y no penaliza `unsafe-inline` solo en estilos).
- Las 36 demos siguen con `'unsafe-inline'` y `'unsafe-eval'` (BabylonJS): son resultados del experimento y no se tocan.
- PageSpeed, SSL Labs, VirusTotal e internet.nl llegan con la ronda nocturna; internet.nl pedirá AAAA y DNSSEC (DNS:
  decisión del operador).
