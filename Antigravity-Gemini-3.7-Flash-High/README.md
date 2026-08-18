# Universo 3D — Antigravity-Gemini-3.7-Flash-High

Simulación 3D interactiva, inmersiva y de alto rendimiento del Sistema Solar completo desarrollada en **BabylonJS**, construida estrictamente bajo los requerimientos y especificaciones de [`Prompt-Maestro_v2.txt`](../Prompt-Maestro_v2.txt).

---

## 🚀 Entregable

- **Archivo principal:** [`Antigravity-Gemini-3.7-Flash-High/index.html`](index.html)
- **Tecnología:** HTML5, CSS3 Glassmorphism y JavaScript Vanilla (ES6+) con motor gráfico **BabylonJS 7+ vía CDN oficial**.
- **Autocontenido:** 100% autocontenido en un único archivo. Sin assets locales, sin servidores web requeridos y sin pasos de compilación.
- **Ejecución directa:** Funciona inmediatamente al abrir mediante doble clic (`file://`) o mediante servidor local / HTTPS.

---

## 🎮 Controles y Navegación 3D

| Acción | Control | Descripción |
| :--- | :--- | :--- |
| **Rotación orbital** | `Click izquierdo + Arrastrar` | Órbita suave alrededor del objetivo actual con auto-rotación en reposo. |
| **Zoom in / out** | `Rueda del ratón / Pinch` | Acercamiento y alejamiento con límites configurados (`lowerRadiusLimit: 25`, `upperRadiusLimit: 2200`). |
| **Desplazamiento (Pan)** | `Click derecho + Arrastrar` | Traslación del punto de enfoque de la cámara. |
| **Alternar panel UI** | `Botón ⚙️ (Esquina sup. der.)` | Oculta o despliega el panel de control glassmorphism. |

---

## 🌟 Características Astronómicas y Visuales Implementadas

### 1. Sol Central y Dinámica de Fotosfera
- **Núcleo Solar:** Esfera 3D central con material emisivo cálido y textura procedural dinámica generada en memoria con `BABYLON.DynamicTexture` (simulación de turbulencia de plasma solar y granulado fotosférico).
- **Luz Puntual Solar:** `BABYLON.PointLight` en el origen $(0,0,0)$ con intensidad calibrada (2.2) y coloración cálida para iluminar de manera realista los cuerpos del sistema.
- **Pulsación Armónica:** Modulación de escala sinusoidal ($1.0 \leftrightarrow 1.04$) con período de ~3 segundos.
- **Corona Solar Oficial:** Integración con `BABYLON.ParticleHelper.CreateAsync("sun", scene)` y degradación elegante a `BABYLON.ParticleSystem` procedural con emisor esférico en memoria si se ejecuta offline bajo `file://`.

### 2. Sistema Solar Completo (8 Planetas + Plutón Enano)
- **Física Orbital Kepleriana Rigurosa:**
  - Sol situado estrictamente en el **foco de la elipse**:
    $$x = a \cos\theta - a \cdot e$$
    $$z = b \sin\theta \quad \text{donde } b = a \sqrt{1 - e^2}$$
  - Líneas orbitales (`BABYLON.MeshBuilder.CreateLines`) y trayectorias planetarias calculadas con la **misma función matemática unificada** para garantizar alineación absoluta.
  - Velocidades orbitales Keplerianas inversamente proporcionales a la distancia ($v \propto \frac{1}{\sqrt{a}}$).
  - Inclinación de planos orbitales (`orbitTilt`) e inclinación de ejes de rotación propia (`axialTilt`), incluyendo la rotación retrógrada de Venus y la inclinación extrema (~97.8°) de Urano.
- **Texturizado Procedural Planetario:**
  - Superficies detalladas en memoria: Bandas y Gran Mancha Roja en Júpiter, continentes y nubes en la Tierra, casquetes polares en Marte, cráteres en Mercurio y bandas doradas en Saturno.
- **Atmósferas y Anillos:**
  - Atmósferas semitransparentes con resplandor para la Tierra, Venus y Marte.
  - Sistemas de anillos concéntricos con textura de división de Cassini para Saturno y Urano.
- **Etiquetas Flotantes:** Nombres identificativos con `BABYLON.TransformNode.BILLBOARDMODE_ALL`.

### 3. Cinturón de Asteroides Optimizado (Instanced Meshes)
- Más de **280 asteroides rocosos** distribuidos elípticamente entre Marte ($a=72$) y Júpiter ($a=120$).
- Renderizado ultra-optimizado mediante `baseAsteroid.createInstance()` (1 solo *draw-call* de geometría base), manteniendo 60 FPS estables.

### 4. Cometa Halley y Cola Vectorial Anti-Solar
- **Órbita Excéntrica:** Alta excentricidad ($e = 0.85$, $a = 150$, período visible de ~18s).
- **Cálculo Anti-Solar por Frame:**
  $$\vec{d}_{\text{anti-solar}} = \text{normalize}(\vec{P}_{\text{Halley}} - \vec{P}_{\text{Sol}})$$
- Emisión de partículas (`BABYLON.ParticleSystem`) dirigida estrictamente en la dirección opuesta al Sol con gradiente de color cromático (blanco brillante a azul cian y fadeout transparente).

### 5. Cosmos Profundo y Nebulosas
- **Campo Estelar:** Más de 3600 estrellas estáticas distribuidas tridimensionalmente en un volumen cúbico profundo de $2800^3$ unidades.
- **Nebulosas Lejanas:** 5 planos gigantes de nebulosas a radio $1500+$ con gradientes radiales procedurales, billboard activo y mezcla aditiva `ALPHA_ADD`.

### 6. Pipeline de Post-Procesado
- `BABYLON.DefaultRenderingPipeline` con Bloom, Glow Layer y mapeo de tonos ACES habilitados.
- Conmutador en tiempo real desde la interfaz de usuario con degradación controlada mediante `try/catch`.

---

## 🎛️ Panel de Configuración Interactivo (UI)

El panel flotante en la esquina superior derecha cuenta con diseño **Glassmorphism** (`backdrop-filter: blur(16px)`):

1. **Sección 1 — Tiempo y Velocidad:**
   - Slider de velocidad global ($0.0\text{x} \leftrightarrow 10.0\text{x}$).
   - Slider de multiplicador orbital ($0.1\text{x} \leftrightarrow 3.0\text{x}$).
   - Botón toggle de Pausar / Reanudar simulación.
2. **Sección 2 — Visualización y Elementos:**
   - Checkboxes independientes para órbitas, nombres, cometa Halley, cola vectorial, cinturón de asteroides y nebulosas.
   - Selector cinemático de vistas de cámara: Sistema Solar, Sol Cercano, Tierra, Saturno, Panorámica Lejana y Seguir a Halley.
   - Slider de escala relativa de planetas ($0.5\text{x} \leftrightarrow 3.0\text{x}$).
3. **Sección 3 — Estética y Render:**
   - Temas visuales de la interfaz: *Futurista Neón*, *Clásico Dorado* y *Oscuro Profundo*.
   - Toggle de resplandor post-procesado (Bloom/Glow).
   - Selector dinámico de tipo de estrella: Amarillo Estándar (G2V), Gigante Naranja (K), Enana Blanca (A) y Supergigante Roja (M).
4. **Sección 4 — HUD de Métricas e Información:**
   - Contador de FPS en tiempo real con código de color dinámico.
   - Conteo total de mallas en escena.
   - Leyenda de controles interactivos.

---

## 📋 Validación de APIs de BabylonJS

Cumpliendo con la **Regla Absoluta** de [`Prompt-Maestro_v2.txt`](../Prompt-Maestro_v2.txt), todas las firmas y métodos de BabylonJS fueron rigurosamente validados:

- `BABYLON.Engine` / `BABYLON.Scene`: Configuración de render loop y manejo de eventos `webglcontextlost` y `webglcontextrestored`.
- `BABYLON.ArcRotateCamera`: `attachControl`, `useAutoRotationBehavior`, `lowerRadiusLimit`, `upperRadiusLimit`, `wheelPrecision`.
- `BABYLON.HemisphericLight` / `BABYLON.PointLight`: Gestión precisa de intensidades difusas y especulares.
- `BABYLON.MeshBuilder.CreateSphere`, `CreateLines`, `CreatePlane`, `CreateDisc`: Parámetros de geometría y generación procedural.
- `BABYLON.ParticleSystem` & `BABYLON.ParticleHelper`: Capacidades, emisores de caja/esféricos, `blendMode`, gradientes de color y control de emisión por frame.
- `BABYLON.DynamicTexture`: Creación en memoria de mapas de textura, gradientes radiales, etiquetas y anillos.
- `BABYLON.DefaultRenderingPipeline` / `BABYLON.GlowLayer`: Post-procesado con bloom, kernel y mapeo de tonos.

---

## 📁 Estructura del Módulo

```text
Antigravity-Gemini-3.7-Flash-High/
├── index.html   # Archivo autocontenido ejecutable (HTML5 + CSS3 + JS Inline)
└── README.md    # Documentación técnica completa
```
