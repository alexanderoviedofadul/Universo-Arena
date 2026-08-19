# 🚀 Despliegue y Automatización (Webhook CD)

Este documento describe la infraestructura de despliegue de **Universo-Arena** y cómo configurar la integración continua (CD) mediante webhooks de GitHub.

---

## 1. Infraestructura de Producción

El sitio web está alojado en un servidor VPS Ubuntu y se expone públicamente bajo la URL:
👉 **[https://universo-arena.alexanderoviedofadul.dev](https://universo-arena.alexanderoviedofadul.dev)**

### Detalles del Servidor Web (Caddy)
El proyecto es puramente estático (HTML, CSS y JS de BabylonJS vía CDN), por lo que es servido de forma eficiente por **Caddy frontend**. La configuración en el `Caddyfile` se encarga de:
* Servir el directorio raíz del proyecto local de forma estática.
* Forzar conexiones seguras HTTPS (con certificados automatizados de Let's Encrypt / ZeroSSL).
* Aplicar cabeceras de ciberseguridad estrictas (Headers OWASP, bloqueo de directorios ocultos como `.git`, y una política de seguridad de contenido **CSP** que permite la carga de las CDNs autorizadas de BabylonJS).
* Intermediar las llamadas de auto-despliegue redirigiendo la subruta `/webhook` al puerto local del servicio webhook.

---

## 2. Flujo de Auto-Despliegue Continuo (CD)

Para evitar despliegues manuales, se configuró un daemon de webhook en NodeJS corriendo localmente en el puerto **`3020`** del servidor, administrado de forma persistente por **Systemd** (`universo-arena-webhook.service`).

```
GitHub Push (main) ──> Caddy HTTPS (Port 443) ──> Webhook NodeJS (Port 3020) ──> Git Pull (Local)
```

### Comportamiento del Webhook
1. Escucha peticiones de tipo `POST` de GitHub.
2. Verifica la autenticidad del remitente comparando la firma `x-hub-signature-256` con el secreto compartido.
3. Al recibir un push en la rama `main`, responde inmediatamente con un código `202 Accepted` a GitHub e inicia de forma asíncrona un:
   ```bash
   git fetch origin
   git pull origin main
   ```
4. El servidor web de Caddy sirve instantáneamente la nueva versión de los archivos sin necesidad de reiniciar servicios ni compilar assets.

---

## 3. Cómo Activar el Webhook en GitHub

Si administras el repositorio en GitHub (`https://github.com/alexanderoviedofadul/Universo-Arena.git`) y deseas reactivar o configurar el webhook ante un cambio o migración de servidor, sigue estos pasos:

1. Ve a la pestaña **Settings** (Configuración) de tu repositorio en GitHub.
2. En la barra lateral izquierda, selecciona **Webhooks**.
3. Haz clic en el botón **Add webhook** (Añadir webhook).
4. Configura los siguientes parámetros obligatorios:
   * **Payload URL:** `https://universo-arena.alexanderoviedofadul.dev/webhook`
   * **Content type:** `application/json`
   * **Secret:** *(Solicitar el secreto de firma criptográfica configurado en el entorno de producción del VPS)*
   * **SSL verification:** Mantener marcado *Enable SSL verification*.
   * **Which events would you like to trigger this webhook?:** Seleccionar *Just the push event* (Solo el evento push).
   * **Active:** Mantener la casilla marcada.
5. Haz clic en **Add webhook** para guardar.

Una vez guardado, GitHub enviará un evento de prueba (`ping`) para verificar la comunicación y confirmar la integración continua con un check verde.
