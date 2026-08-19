# Universo 3D — Agy-Gemini-3.7-Flash-Antigravity-CLI

Simulación 3D interactiva, inmersiva y de alto rendimiento del Sistema Solar completo desarrollada en **BabylonJS**, construida bajo las especificaciones de [`Prompt-Maestro_v2.txt`](../Prompt-Maestro_v2.txt) con mejoras integrales en nebulosas orgánicas, zoom cinemático y sistema completo de lunas satelitales.

---

## 🚀 Entregable

- **Archivo principal:** [`Agy-Gemini-3.7-Flash-Antigravity-CLI/index.html`](index.html)
- **Tecnología:** HTML5, CSS3 Glassmorphism y JavaScript Vanilla (ES6+) con motor gráfico **BabylonJS 7+ vía CDN oficial**.
- **Autocontenido:** 100% autocontenido en un único archivo. Sin assets locales, sin servidores web requeridos y sin pasos de compilación.
- **Ejecución directa:** Funciona inmediatamente al abrir mediante doble clic (`file://`) o mediante servidor local / HTTPS.

---

## 🎮 Controles y Navegación 3D

| Acción | Control | Descripción |
| :--- | :--- | :--- |
| **Rotación orbital** | `Click izquierdo + Arrastrar` | Órbita suave alrededor del objetivo actual con auto-rotación en reposo (`idleRotationSpeed: 0.03`). |
| **Zoom in / out fluido** | `Rueda del ratón / Pinch` | Acercamiento y alejamiento continuo sin bloqueos ni retornos forzados (`lowerRadiusLimit: 4`, `upperRadiusLimit: 2800`, `wheelPrecision: 2.0`). |
| **Desplazamiento (Pan)** | `Click derecho + Arrastrar` | Traslación del punto de enfoque de la cámara. |
| **Alternar panel UI** | `Botón ⚙️ (Esquina sup. der.)` | Oculta o despliega el panel de control glassmorphism. |

---

## 🌟 Características Astronómicas y Visuales Implementadas

### 1. Sol Central y Dinámica de Fotosfera
- **Núcleo Solar:** Esfera 3D central con material emisivo cálido y textura procedural dinámica generada en memoria con `BABYLON.DynamicTexture` (simulación de turbulencia de plasma solar y granulado fotosférico).
- **Luz Puntual Solar:** `BABYLON.PointLight` en el origen $(0,0,0)$ con intensidad calibrada (2.2) y coloración cálida para iluminar de manera realista los cuerpos del sistema.
- **Pulsación Armónica:** Modulación de escala sinusoidal ($1.0 \leftrightarrow 1.04$) con período de ~3 segundos.
- **Corona Solar Oficial:** Integración con `BABYLON.ParticleHelper.CreateAsync("sun", scene)` y degradación elegante a `BABYLON.ParticleSystem` procedural con emisor en memoria si se ejecuta offline bajo `file://`.

### 2. Sistema Solar Completo (8 Planetas + Plutón Enano)
- **Física Orbital Kepleriana Rigurosa:**
  - Sol situado estrictamente en el **foco de la elipse**:
    $$x = a \cos\theta - a \cdot e$$
    $$z = b \sin\theta \quad \text{donde } b = a \sqrt{1 - e^2}$$
  - Líneas orbitales (`BABYLON.MeshBuilder.CreateLines`) y trayectorias planetarias calculadas con la **misma función matemática unificada** para garantizar alineación absoluta.
  - Velocidades orbitales Keplerianas inversamente proporcionales a la distancia ($v \propto \frac{1}{\sqrt{a}}$).
  - Inclinación de planos orbitales (`orbitTilt`) e inclinación de ejes de rotación propia (`axialTilt`), incluyendo la rotación retrógrada de Venus y la inclinación extrema (~97.8°) de Urano.
- **Texturizado Procedural Planetario:**
  - Superficies detalladas generadas en memoria: Bandas y Gran Mancha Roja en Júpiter, continentes y nubes en la Tierra, casquetes marcianos y cráteres en Mercurio y bandas doradas en Saturno.
- **Atmósferas y Anillos:**
  - Atmósferas semitransparentes con resplandor para la Tierra, Venus y Marte.
  - Sistemas de anillos concéntricos con textura de división de Cassini para Saturno y Urano.
- **Etiquetas Flotantes:** Nombres identificativos con `BABYLON.TransformNode.BILLBOARDMODE_ALL`.

### 3. Sistema Completo de Lunas y Satélites Naturales
- 🌍 **Tierra:** **La Luna** con textura de maria y cráteres, orbitando a escala visual ajustada.
- 🔴 **Marte:** **Fobos** y **Deimos** (satélites irregulares y veloces).
- 🪐 **Júpiter (Lunas Galileanas):**
  - **Ío:** Terreno volcánico de azufre amarillo-anaranjado.
  - **Europa:** Corteza de hielo brillante con líneas de fractura.
  - **Ganimedes:** El satélite más grande, con terreno helado y cráteres.
  - **Calisto:** Superficie oscura ancestral fuertemente craterizada.
- 🪐 **Saturno:** **Titán** (atmósfera densa anaranjada con hidrocarburos) y **Encélado** (hielo blanco puro).
- 🔵 **Urano:** **Titania** y **Oberón**.
- 🌀 **Neptuno:** **Tritón** (órbita retrógrada y criovulcanismo rosáceo).
- ⚪ **Plutón:** **Caronte** (sistema binario).
- Cada luna cuenta con su propia órbita, etiqueta identificativa y renderizado sincronizado al planeta padre.

### 4. Cinturón de Asteroides Optimizado (Instanced Meshes)
- Más de **280 asteroides rocosos** distribuidos elípticamente entre Marte y Júpiter.
- Renderizado ultra-optimizado mediante `baseAsteroid.createInstance()` (1 solo *draw-call* de geometría base), manteniendo 60 FPS estables.

### 5. Cometa Halley y Cola Vectorial Anti-Solar
- **Órbita Excéntrica:** Alta excentricidad ($e = 0.85$, $a = 155$, período visible de ~18s).
- **Cálculo Anti-Solar por Frame:**
  $$\vec{d}_{\text{anti-solar}} = \text{normalize}(\vec{P}_{\text{Halley}} - \vec{P}_{\text{Sol}})$$
- Emisión de partículas (`BABYLON.ParticleSystem`) dirigida estrictamente en la dirección opuesta al Sol con gradiente de color cromático (blanco brillante a azul cian y fadeout transparente).

### 6. Cosmos Profundo y Nebulosas Orgánicas
- **Campo Estelar:** Más de 3800 estrellas estáticas distribuidas tridimensionalmente en un volumen cúbico profundo de $3600^3$ unidades.
- **Nebulosas Orgánicas Sin Bordes Cuadrados:** Planos gigantes con texturas generadas mediante múltiples fuentes gaussianas suaves con caída exponencial a cero estricto (Orión, Velo, Carina, Laguna y Águila).

### 7. Pipeline de Post-Procesado
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
   - Checkboxes independientes para órbitas, nombres, lunas/satélites, cometa Halley, cola vectorial, cinturón de asteroides y nebulosas.
   - Selector cinemático de vistas de cámara: Sistema Solar, Sol Cercano, Tierra y Luna, Marte y Lunas, Júpiter y Galileanas, Saturno y Titán, Panorámica Cósmica y Seguir a Halley.
   - Slider de escala relativa de planetas ($0.5\text{x} \leftrightarrow 3.0\text{x}$).
3. **Sección 3 — Estética y Render:**
   - Temas visuales de la interfaz: *Futurista Neón*, *Clásico Dorado* y *Oscuro Profundo*.
   - Toggle de resplandor post-procesado (Bloom/Glow).
   - Selector dinámico de tipo de estrella: Amarillo Estándar (G2V), Enana Blanca (A), Gigante Naranja (K) y Supergigante Roja (M).
4. **Sección 4 — HUD de Métricas e Información:**
   - Contador de FPS en tiempo real con código de color dinámico.
   - Conteo total de mallas en escena.
   - Leyenda de controles interactivos.

---

## 📁 Estructura del Módulo

```text
Agy-Gemini-3.7-Flash-Antigravity-CLI/
├── index.html   # Archivo autocontenido ejecutable (HTML5 + CSS3 + JS Inline)
└── README.md    # Documentación técnica completa
```
