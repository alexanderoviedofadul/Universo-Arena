<!--
  POST LISTO PARA PUBLICAR — LinkedIn · VERSIÓN 2 (≈2.700 caracteres, cabe en el límite de 3.000 de LinkedIn)
  Autor: Alexander Oviedo Fadul
  Imagen: assets/universo_arena_banner.png · Galería: https://universo-arena.alexanderoviedofadul.dev · Repo: https://github.com/alexanderoviedofadul/Universo-Arena
  Copia desde el primer título (🌌). Sube el banner como imagen del post.
-->

![Universo-Arena](../assets/universo_arena_banner.png)

🌌 Le di el mismo reto a 14 inteligencias artificiales. Tres días después, EE. UU. apagó la mejor del mundo.

El 9 de junio Anthropic lanzó Claude Fable 5, su modelo más capaz. El 12, una directiva de control de exportaciones de EE. UU. obligó a suspenderlo para cualquier ciudadano extranjero. Como no se puede filtrar por nacionalidad en tiempo real, lo desactivaron para todo el planeta.

Yo soy colombiano. Soy ese "ciudadano extranjero". El mejor modelo del momento se volvió inaccesible en un fin de semana.

Y esa misma semana terminé un experimento que respondía, sin querer, a una pregunta incómoda: ¿de verdad necesitamos a Fable 5?

🛰️ El experimento
Le di el MISMO prompt exigente —una simulación 3D del Sistema Solar en BabylonJS, en un único index.html— a 14 combinaciones de modelo + agente de código. Una sola pasada cada una. Y no me quedé en leer el código: abrí las 14 en un navegador real y medí objetos, FPS y errores de consola.

📊 Lo que encontré
🔹 14/14 arrancaron. 12/14, sin un solo error de consola.
🥇 Empate en cabeza: GPT-5.5 (Codex) y Claude Opus 4.8, 97/100.
☄️ El bug más común: la cola del cometa apuntando hacia el Sol (signo de vector invertido).
🧰 El mismo modelo cambia de liga según el agente: MiniMax M3 saltó de 79 a 92.

⚠️ La pregunta incómoda
El modelo que se cayó no era imprescindible. Si 12 de 14 ya hacen trabajo excelente —y el que empató primero fue Opus 4.8, justo el modelo que Fable 5 venía a reemplazar—, depender de un único "mejor modelo" es un espejismo. Y caro: quien construyó todo sobre Fable 5 amaneció sin producto.

🛡️ Mi postura
La resiliencia no es tener el mejor modelo. Es no necesitar a ninguno en particular. Por eso construí MALLO, un orquestador multi-agente con fallback. Irónicamente, hasta la API de Fable 5 trae fallback incorporado.

Esto no es anti-Anthropic: todo el experimento lo armé con Opus 4.8 + Claude Code. Bienvenido todo lo nuevo, siempre que no sea mi único punto de fallo.

👀 Míralo tú mismo
🌌 Galería: https://universo-arena.alexanderoviedofadul.dev
💻 Repo: https://github.com/alexanderoviedofadul/Universo-Arena

¿Estás construyendo sobre un solo proveedor? Y tu cometa… ¿apunta para el lado correcto? 👇

#InteligenciaArtificial #MultiAgente #LLM #LegalTech #Colombia
