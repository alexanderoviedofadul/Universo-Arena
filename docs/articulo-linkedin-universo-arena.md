<!--
  ARTÍCULO LISTO PARA PUBLICAR — LinkedIn (formato artículo largo)
  Autor: Alexander Oviedo Fadul
  Imagen de portada: assets/universo_arena_banner.png
  URL del proyecto (galería): https://universo-arena.alexanderoviedofadul.dev
  Repositorio público: https://github.com/alexanderoviedofadul/Universo-Arena
  Idioma: Español
-->

![Universo-Arena](../assets/universo_arena_banner.png)

# Le di el mismo reto a 14 inteligencias artificiales. Tres días después, el gobierno de EE. UU. apagó la mejor del mundo.

Tres días. Eso fue lo que duró Claude Fable 5 disponible antes de que dejara de existir para mí.

El 9 de junio Anthropic presentó su modelo más capaz hasta la fecha. El 12 de junio, una directiva de control de exportaciones del gobierno estadounidense obligó a la compañía a suspender el acceso a Fable 5 y a su gemelo Mythos 5 para **cualquier ciudadano extranjero**, dentro o fuera de Estados Unidos. Como Anthropic no puede filtrar a sus usuarios por nacionalidad en tiempo real, hizo lo único que podía hacer para cumplir: lo desactivó para todo el planeta.

Yo soy colombiano. Soy, literalmente, ese "ciudadano extranjero". El mejor modelo del momento pasó de titular a inaccesible en un fin de semana.

Voy a ser honesto: mi primera reacción no fue técnica. Fue de impotencia. Y justo esa semana yo venía de terminar un experimento que, sin proponérmelo, respondía a la pregunta que la noticia dejaba en el aire: **¿de verdad necesitamos a Fable 5?**

## El experimento: un prompt, 14 universos

Soy ingeniero de sistemas y abogado. Llevo años construyendo herramientas para la Rama Judicial colombiana, y una de las cosas que aprendí por las malas es que casarse con un solo proveedor de IA es una mala idea. Por eso, hace tiempo, construí MALLO: un orquestador que reparte el trabajo entre varios modelos. Universo-Arena nació de esa misma obsesión, pero llevada al banco de pruebas.

La idea es sencilla de explicar y brutal de ejecutar. Tomé un mismo prompt —exigente de verdad: una simulación 3D del Sistema Solar con BabylonJS, en un único archivo `index.html`, con sol, ocho planetas más Plutón, órbitas elípticas, cinturón de asteroides, el cometa Halley con su cola, miles de estrellas, nebulosas, bloom, y un panel de control completo— y se lo pasé a **14 combinaciones distintas de modelo + agente de código**. Una sola pasada cada una. Sin retoques míos.

GPT‑5.5 con Codex. Claude Opus 4.8 con Claude Code. Gemini 3.5 Flash. MiniMax M3. DeepSeek V4 Pro. Kimi K2.7. GLM 5.2. Devstral. Cada carpeta del repositorio lleva en el nombre el modelo y el agente que la produjeron.

Y aquí viene lo que de verdad importa: no me quedé en leer el código y opinar. **Abrí las 14 simulaciones en un navegador de verdad**, conté cuántos objetos renderizaba cada una, medí sus FPS y, sobre todo, registré sus errores de consola. Una rúbrica de 100 puntos para el criterio; la ejecución real para la verdad.

## Lo que encontré

Lo primero me sorprendió incluso a mí, que soy optimista con esto: **las 14 arrancaron y renderizaron una escena 3D compleja**. Doce de las catorce, sin un solo error en consola. Generar mil quinientas líneas de WebGL que ni siquiera lancen una excepción ya no es una proeza; es el comportamiento esperable de un agente serio en 2026.

La frontera, entonces, ya no está en "¿funciona?". Está en los detalles difíciles. Dos, en concreto, separaron a los mejores del resto:

- **El Sol en el foco de la elipse, no en el centro.** Centrar el Sol parece correcto y es física falsa. Solo el grupo de cabeza lo entendió.
- **La cola del cometa Halley.** El vector "lejos del Sol" es `cometa − Sol`. Suena trivial. No lo es: media tabla invirtió el signo y terminó con la cola apuntando *hacia* el Sol, justo al revés de como se comporta un cometa real. Fue el error más común y más revelador de todo el experimento.

En lo más alto, un empate que dice mucho: **GPT‑5.5 (Codex) y Claude Opus 4.8, los dos con 97 sobre 100**. Dos laboratorios distintos, calidad indistinguible.

Hubo un episodio que me dejó pensando más que cualquier ranking. Uno de mis jurados —un modelo revisando el código de otro— sentenció que una de las entregas estaba "rota, pantalla negra". Cuando la abrí en el navegador, funcionaba perfecta: 279 objetos en pantalla, cero errores, interfaz completa. El juez había alucinado un bug que no existía. Solo ejecutarla de verdad lo desmintió. Le subí la nota de un injusto 38 a un merecido 89. Lección que me llevo: **evaluar agentes de IA sin ejecutarlos no es fiable.** Y como gremio, apenas estamos aprendiendo a medirlos bien.

No quiero vender humo, así que lo digo claro: esto no es ciencia. Es una sola pasada por modelo, sin medir varianza, con FPS tomados por software. Es un pulso, una foto. Pero es una foto tomada con el navegador abierto, no leyendo el código por encima. Y esa foto cuenta una historia.

## La pregunta incómoda

Volvamos a Fable 5.

Anthropic lo presentó como su modelo más capaz, sucesor directo de Opus 4.8. La razón oficial del apagón, según se ha reportado, es que el gobierno cree haber detectado una forma de "jailbreak" del modelo. La propia Anthropic discrepó en público: argumentó que retirar un modelo comercial por un *jailbreak* puntual, si se aplicara como estándar a toda la industria, paralizaría el lanzamiento de cualquier modelo nuevo de cualquier laboratorio.

Tiene razón en eso. Pero no es mi punto. Mi punto es otro, y es el que mi propio benchmark me grita: **el modelo que se cayó no era imprescindible.**

Porque si doce de catorce combinaciones distintas ya producen trabajo excelente —y porque el que empató en el primer puesto fue precisamente Opus 4.8, el modelo que Fable 5 venía a reemplazar—, entonces la indispensabilidad de un único "mejor modelo" es, en buena medida, un espejismo. Un espejismo caro, además. Quien construyó su producto entero sobre Fable 5 amaneció el día 13 sin producto. Quien diversificó, ni se enteró.

*Legal IT Insider* tituló la noticia hablando de "riesgo geopolítico en la cadena de suministro de la IA legal". Como persona que construye tecnología para un sistema de justicia, esa frase me quita el sueño más que cualquier benchmark. Si una herramienta que ayuda a un juez a resolver un habeas corpus depende de un modelo que un gobierno extranjero puede apagar el martes por la tarde, eso no es una arquitectura. Es una apuesta.

## Lo que sí hago (y por qué)

No diversifico por moda. Diversifico porque ya me quemé. Por eso MALLO reparte cada consulta entre varios modelos según sus fortalezas. Por eso en este benchmark hay catorce competidores y no un favorito. Y noten la ironía más fina de toda esta historia: **la propia API de Fable 5 trae un mecanismo de *fallback*** para reintentar en otro modelo de Claude cuando este rechaza una solicitud. Hasta Anthropic asume, dentro de su producto estrella, que no debes depender de un solo modelo.

La resiliencia no es tener el mejor modelo. Es no necesitar a ninguno en particular.

Que quede claro, porque sé cómo se leen estas cosas: **esto no es un ataque a Anthropic.** Todo Universo-Arena —el código, la galería, el sistema multi-agente que juzgó a los catorce— lo construí con Opus 4.8 y Claude Code. Y Opus 4.8 ganó, empatado en el primer lugar. Sería absurdo morder la mano que armó el experimento. Las nuevas actualizaciones y los nuevos LLMs son bienvenidísimos; ojalá Fable 5 vuelva pronto y mejor. Lo que defiendo no es un modelo: es una postura. Bienvenido todo lo nuevo, siempre que no se convierta en mi único punto de fallo.

## Míralo tú mismo

Dejé el experimento completo abierto para que cualquiera lo audite, lo critique o le añada su propia entrada.

- 🌌 **Galería interactiva** (ranking, fichas, radares y demos en vivo de las 14): **https://universo-arena.alexanderoviedofadul.dev**
- 💻 **Repositorio público** (código, datos crudos, metodología): **https://github.com/alexanderoviedofadul/Universo-Arena**

Si trabajas con estos modelos, me encantaría saber tu opinión sobre dos cosas: ¿estás construyendo sobre un solo proveedor? Y la cola de tu cometa… ¿apunta para el lado correcto?

---

### Fuentes sobre la suspensión de Claude Fable 5 / Mythos 5

- Anthropic — *Statement on the US government directive to suspend access to Fable 5 and Mythos 5*: https://www.anthropic.com/news/fable-mythos-access
- MarkTechPost — *Anthropic Disables Claude Fable 5 and Mythos 5 After US Government Order* (13/06/2026): https://www.marktechpost.com/2026/06/13/anthropic-disables-claude-fable-5-and-mythos-5-after-us-government-order/
- The Conversation — *Why the US government shut down Anthropic's latest Claude AI model*: https://theconversation.com/why-the-us-government-shut-down-anthropics-latest-claude-ai-model-285223
- Legal IT Insider — *Anthropic's Claude Fable 5 withdrawal highlights geopolitical risk in legal AI supply chain*: https://legaltechnology.com/anthropics-claude-fable-5-withdrawal-highlights-geopolitical-risk-in-legal-ai-supply-chain/
- Documentación oficial — *Presentamos Claude Fable 5 y Claude Mythos 5*: https://platform.claude.com/docs/es/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5

---

## Post corto para el feed de LinkedIn

> Para acompañar la publicación del artículo, o como post independiente que enlaza a la galería. Dos variantes; elige una. Sube la imagen `assets/universo_arena_banner.png` como adjunto del post.

### Variante A — narrativa

El lunes 9 de junio Anthropic lanzó Claude Fable 5, el modelo más capaz que han publicado.

El jueves 12 ya no existía para mí.

Una directiva de control de exportaciones del gobierno de EE. UU. obligó a Anthropic a suspender el acceso para ciudadanos extranjeros. Como no podían filtrar por nacionalidad en tiempo real, lo desactivaron para todo el mundo. Tres días de vida.

Yo soy ese "ciudadano extranjero". Colombiano. Jurista tecnológico que trabaja a diario con estos modelos.

Y lo curioso es que la semana anterior acababa de publicar justo lo contrario a la urgencia de tener "el mejor modelo único".

Le di el mismo prompt exigente a 14 combinaciones de LLM + agente de código: una simulación 3D del Sistema Solar en BabylonJS, un solo index.html, una sola pasada. Sin correcciones.

Los evalué con rúbrica de 100 puntos y ejecutándolos de verdad en el navegador.

Resultado: GPT-5.5 (Codex) y Claude Opus 4.8 empataron en cabeza con 97/100. Los 14 arrancaron. 12 de 14 sin un solo error de consola.

Dato que me dejó pensando: Opus 4.8, el modelo que Fable 5 venía a reemplazar, está en el primer puesto. No necesitaba al sucesor para hacer trabajo de primer nivel.

La lección no es técnica. Es de resiliencia.

Depender de un solo modelo es hoy un riesgo geopolítico. Un cambio regulatorio un jueves por la tarde puede apagarte el flujo de trabajo sin avisar.

Por eso construí MALLO, un orquestador multi-agente con fallback entre proveedores. Lo gracioso: la propia API de Fable 5 trae su "fallback" incorporado. Hasta Anthropic sabe que la redundancia no es opcional.

No es un benchmark científico —es una sola pasada por modelo— pero la foto es clara: el frontier es ancho. La diversificación no es el plan B; es el plan A.

Galería con las 14 entregas en vivo 👉 https://universo-arena.alexanderoviedofadul.dev
Repo público 👉 https://github.com/alexanderoviedofadul/Universo-Arena

¿Cuántos proveedores distintos usas hoy en tus flujos críticos?

\#InteligenciaArtificial #MultiAgente #LLM #LegalTech #BuildInPublic #InnovaciónJudicial

### Variante B — directa / datos

14 modelos. El mismo prompt. Una sola pasada. Resultados que no esperaba.

Publiqué Universo-Arena: le di a 14 combinaciones de LLM + agente de código exactamente el mismo encargo, sin repeticiones ni correcciones. Una simulación 3D del Sistema Solar en BabylonJS, todo en un único index.html.

Los evalué con rúbrica de 100 puntos y, sobre todo, ejecutándolos de verdad en el navegador.

Los números:

— 14/14 arrancaron sin error fatal
— 12/14 sin un solo error de consola
— Empate en cabeza: GPT-5.5 (Codex) y Claude Opus 4.8, 97/100
— Bug más frecuente: la cola del cometa apuntando hacia el Sol (vector invertido)
— Dato incómodo: un juez-LLM declaró "rota" una entrega que funcionaba perfecto; solo la ejecución real lo desmintió

No es un benchmark científico. Es una sola pasada por modelo, en condiciones reales de trabajo.

Pero esta semana pasó algo que le da otro peso a esos datos.

El 9 de junio Anthropic lanzó Claude Fable 5. El 12 lo suspendieron para ciudadanos extranjeros por una directiva de exportaciones de EE. UU. Como no podían filtrar por nacionalidad en tiempo real, lo bloquearon para todos. Tres días de vida.

Yo soy colombiano. Soy ese ciudadano extranjero.

Mi conclusión es la misma de antes del bloqueo: el frontier ya no es un pico, es una meseta ancha. Depender de un único proveedor es un riesgo de cadena de suministro, ahora también geopolítico.

Por eso construí MALLO: orquestador multi-agente con fallback. Irónicamente, la propia API de Fable 5 incluía un mecanismo de fallback. Hasta Anthropic lo sabe.

Opus 4.8, el modelo que Fable 5 venía a reemplazar, lidera mi ranking. No hizo falta esperar al sucesor.

Las nuevas actualizaciones son bienvenidas. Como punto único de fallo, no.

Galería en vivo 👉 https://universo-arena.alexanderoviedofadul.dev
Repo 👉 https://github.com/alexanderoviedofadul/Universo-Arena

¿Tu stack de IA tiene fallback real o es un single point of failure disfrazado de estrategia?

\#IA #LLM #MultiAgente #ArquitecturaIA #BuildInPublic #Colombia

---

## ✅ Metadatos de publicación

| Campo | Valor |
|:--|:--|
| **Autor** | Alexander Oviedo Fadul |
| **Imagen de portada** | `assets/universo_arena_banner.png` |
| **URL del proyecto (galería)** | https://universo-arena.alexanderoviedofadul.dev |
| **Repositorio público** | https://github.com/alexanderoviedofadul/Universo-Arena |
| **Formato** | Artículo largo de LinkedIn + post de feed (2 variantes) |
| **Idioma** | Español |
| **Hashtags sugeridos** | #InteligenciaArtificial #MultiAgente #LLM #LegalTech #BuildInPublic #InnovaciónJudicial #Colombia |

**Checklist antes de publicar:**

- [ ] Subir `assets/universo_arena_banner.png` como imagen de portada del artículo.
- [ ] Confirmar que el subdominio `universo-arena.alexanderoviedofadul.dev` ya apunta a la galería (ver nota abajo).
- [ ] Publicar el artículo largo y, por separado, uno de los dos posts de feed enlazándolo.
- [ ] Etiquetar a quien aparezca mencionado y responder comentarios las primeras 2 horas (mejor alcance).

> **Sobre el subdominio:** la URL recomendada es **`universo-arena.alexanderoviedofadul.dev`** (coincide con el nombre del repo y es autoexplicativa). Alternativa más corta: `arena.alexanderoviedofadul.dev`. Para activarla, basta con un registro CNAME del subdominio hacia GitHub Pages (`alexanderoviedofadul.github.io`) y añadir ese dominio en *Settings → Pages → Custom domain* del repositorio.
