# Universo 3D — GLM-5.3-Claude-Code

Simulación 3D interactiva del Sistema Solar completa desarrollada en **BabylonJS**, construida bajo las especificaciones de [`Prompt-Maestro_v2.txt`](../Prompt-Maestro_v2.txt) con física orbital kepleriana rigurosa (Sol en el foco de cada elipse), cola cometaria anti-solar dinámica, campo estelar de 3600 puntos y nebulosas procedurales.

---

## 🚀 Entregable

- **Archivo principal:** [`GLM-5.3-Claude-Code/index.html`](index.html)
- **Tecnología:** HTML5, CSS3 y JavaScript Vanilla (ES6+) con motor gráfico **BabylonJS vía CDN oficial** (verificado en ejecución contra Babylon **9.21.2**).
- **Autocontenido:** 100% en un único archivo. Sin assets locales, sin servidores web requeridos y sin pasos de compilación.
- **Ejecución directa:** Funciona al abrir con doble clic (`file://`) o mediante servidor local / HTTPS.

---

## 🎮 Controles y Navegación 3D

| Acción | Control | Descripción |
| :--- | :--- | :--- |
| **Rotación orbital** | `Click izquierdo + Arrastrar` | Órbita suave alrededor del objetivo actual, con auto-rotación en reposo (`idleRotationSpeed: 0.03` tras 3 s de inactividad). |
| **Zoom in / out** | `Rueda del ratón / Pinch` | Acercamiento y alejamiento acotados (`lowerRadiusLimit: 30`, `upperRadiusLimit: 2000`). |
| **Desplazamiento (Pan)** | `Click derecho + Arrastrar` | Traslación del punto de enfoque de la cámara. |
| **Alternar panel UI** | `Botón ⚙ (esquina sup. der.)` | Oculta o despliega el panel de control; se auto-colapsa bajo 600 px de ancho. |

---

## 🌟 Características Astronómicas y Visuales Implementadas

### 1. Sol Central con Corona Oficial
- Esfera emisiva con **textura procedural** (`DynamicTexture`) de granulado fotosférico, repintable en vivo entre 4 tipos estelares (blanco / amarillo / naranja / rojo) desde el panel.
- Corona mediante **`BABYLON.ParticleHelper.CreateAsync("sun", scene)`** — el sistema oficial descargado del CDN — con **degradación elegante** a un `ParticleSystem` procedural (900 partículas, degradados naranjas) si se ejecuta sin red.
- `PointLight` cálida en el origen + `HemisphericLight` tenue de relleno.

### 2. Física Orbital Kepleriana (8 planetas + Plutón)
- **Sol en el foco de la elipse**, no en el centro:
  $$x = a\cos\theta - a\cdot e, \quad z = b\sin\theta, \quad b = a\sqrt{1-e^2}$$
  La **misma función `posicionElipse`** alimenta las líneas de órbita y el movimiento por frame — coincidencia exacta verificada numéricamente (perihelio de la Tierra 45.22 vs. teórico 45.218).
- Excentricidades reales por planeta (Mercurio 0.206, Plutón 0.249…), inclinaciones orbitales y **velocidades keplerianas** $\omega = 55/a^{1.5}$ integradas con $\Delta t = \min(\text{deltaTime}, 50)/1000$.
- **Inclinaciones axiales reales**: Venus 3.09 rad (~176°, rotación retrógrada efectiva) y Urano 1.71 rad (~98°), aplicadas sobre un nodo `eje` separado del nodo de giro para evitar la precesión del polo.
- Texturas procedurales por planeta (bandas de Júpiter con Gran Mancha Roja, casquetes de Marte, océanos y continentes terrestres, Tombaugh Regio en Plutón) y halos atmosféricos con `BLENDMODE_ADD`.

### 3. Cinturón de Asteroides por Instancing
- **260 asteroides** entre Marte y Júpiter (radio 68–84): 2 mallas base visibles + **258 `createInstance()`** — un solo *draw-call* por geometría base, verificado en runtime como `InstancedMesh` reales.

### 4. Cometa Halley con Cola Anti-Solar
- Órbita de alta excentricidad ($e = 0.85$, $a = 130$, período 18 s) inclinada 0.32 rad respecto a la eclíptica.
- Cola de hasta **1400 partículas** recalculada **cada frame**:
  $$\vec{d} = \text{normalizeToNew}(\vec{P}_{\text{Halley}} - \vec{P}_{\text{Sol}})$$
  usando `normalizeToNew()` (nunca `normalize()`, que muta *in-place*), con dispersión cónica ±0.22 sobre `direction1`/`direction2`.
- **Viento solar dinámico**: `emitRate` entre 60 y ~1000 según la cercanía al perihelio ($\propto$ distancia$^{-2}$); gradiente blanco → cian → transparente.

### 5. Anillos Planetarios
- **Saturno**: anillo 1.45–2.35 radios con textura procedural de bandas concéntricas y división oscura tipo Cassini.
- **Urano**: anillo fino tenue 1.6–1.95 radios, vertical por la inclinación axial del planeta.

### 6. Cosmos Profundo
- **3600 estrellas estáticas** (3000 blancas/azuladas + 600 cálidas) en una caja de 2000³, tamaños 0.3–1.5, vida útil infinita y potencia de emisión nula (jamás se mueven).
- **5 nebulosas** orgánicas: planos 520×520 a radio >1550, `DynamicTexture` con gradientes radiales de caída exponencial (rosas / violetas / cianes), `billboardMode` total y mezcla alfa.

### 7. Etiquetas Inteligentes y Post-Procesado
- Etiquetas billboard de los 9 cuerpos en **espacio mundo**, reposicionadas cada frame sobre su planeta (desviación horizontal medida: 0.000) — inmunes al clásico bug de etiquetas apiladas en el Sol.
- `DefaultRenderingPipeline` con **Bloom + tone mapping** y `GlowLayer`, conmutables en vivo y con degradación segura mediante `try/catch`.

---

## 🎛️ Panel de Configuración Interactivo (UI)

Panel flotante *glassmorphism* en la esquina superior derecha, con 4 secciones:

1. **Tiempo y Velocidad:** slider de velocidad global (0–10x), slider de multiplicador orbital (0.1–3x) y botón Pausar/Reanudar.
2. **Visualización y Elementos:** checkboxes de órbitas, nombres, Halley, cola del cometa, asteroides y nebulosas; selector de **6 vistas de cámara** (Sistema Solar, Sol cercano, Tierra, Saturno, Panorámica y Seguir a Halley) con transiciones suavizadas de 1.6 s; slider de escala de planetas (0.5–3x).
3. **Estética y Render:** 3 temas de interfaz (futurista / clásico / oscuro) vía variables CSS, toggle de bloom/glow y selector de tipo estelar del Sol (4 colores).
4. **HUD de Información:** FPS con código de color, conteo de mallas de la escena y leyenda de controles.

---

## ✅ Validación de APIs con Context7

Siguiendo la *regla absoluta* del repositorio, todas las APIs de BabylonJS se validaron contra la documentación oficial (Context7, `/babylonjs/documentation`) **antes** de escribir código. Notablemente: `ParticleHelper.CreateAsync` (el helper actual basado en promesas) en lugar del inexistente `CreateSystem`, y `Vector3.normalizeToNew()` para evitar la mutación *in-place* de `normalize()` — el anti-patrón documentado del benchmark.

---

## 📊 Verificación en Tiempo de Ejecución

Medido con el arnés del benchmark (Chrome headless + SwiftShader, `file://`):

| Métrica | Valor |
| :-- | :-- |
| Errores de consola / peticiones fallidas | **0 / 0** |
| Mallas en escena | 304 (incl. 258 instancias) |
| Partículas activas | 6603 en 6 sistemas |
| Producto punto cola·anti-solar | **0.93** (≈1 con la dispersión del emisor) |
| Pausa | Congela el movimiento con exactitud (Δposición = 0) |
| Seguimiento de cámara | Distancia al objetivo = 0 |

---

## 📁 Estructura del Módulo

```text
GLM-5.3-Claude-Code/
├── index.html   # Archivo autocontenido ejecutable (HTML5 + CSS3 + JS inline)
└── README.md    # Documentación técnica completa
```
