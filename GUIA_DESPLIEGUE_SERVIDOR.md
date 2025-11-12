# Guía de Despliegue en Servidor en Línea

Esta guía te ayudará a desplegar tu aplicación Flask en un servidor en línea y configurarla para que funcione al 100%.

## Paso 1: Preparar el Código para Producción

### 1.1 Actualizar la configuración de producción

Asegúrate de que el archivo `.env` tenga las siguientes variables configuradas con los valores correctos para tu servidor:

```env
GOOGLE_CLIENT_ID=tu_client_id_real
GOOGLE_CLIENT_SECRET=tu_client_secret_real
GOOGLE_REDIRECT_URI=https://tu-dominio.com/setup/oauth2callback
SESSION_SECRET=tu_clave_secreta_muy_segura_aqui
FLASK_ENV=production
```

### 1.2 Modificar app.py para producción

El archivo `app.py` actualmente tiene `debug=True` que debe cambiarse para producción. Puedes usar variables de entorno:

```python
if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=debug_mode)
```

## Paso 2: Configurar Google Cloud Console

### 2.1 Actualizar URI de redirección

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto
3. Ve a "APIs y servicios" → "Credenciales"
4. Edita tu OAuth 2.0 Client ID
5. Agrega la URI de redirección de producción:
   - `https://tu-dominio.com/setup/oauth2callback`
   - Si usas un puerto específico: `https://tu-dominio.com:PUERTO/setup/oauth2callback`

### 2.2 Verificar que Gmail API esté habilitada

1. Ve a "APIs y servicios" → "Biblioteca"
2. Busca "Gmail API"
3. Verifica que esté habilitada

## Paso 3: Elegir Plataforma de Despliegue

### Opción A: Render.com (Recomendado para principiantes)

#### 3.1 Crear cuenta en Render
1. Ve a [render.com](https://render.com/)
2. Crea una cuenta (puedes usar GitHub para login)

#### 3.2 Conectar repositorio
1. Conecta tu repositorio de GitHub/GitLab
2. O sube tu código directamente

#### 3.3 Crear servicio Web
1. Haz clic en "New" → "Web Service"
2. Selecciona tu repositorio
3. Configura:
   - **Name**: gmail-bot-flask (o el nombre que prefieras)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` o `python app.py`

#### 3.4 Configurar variables de entorno en Render
1. Ve a la sección "Environment" de tu servicio
2. Agrega las siguientes variables:
   ```
   GOOGLE_CLIENT_ID=tu_client_id
   GOOGLE_CLIENT_SECRET=tu_client_secret
   GOOGLE_REDIRECT_URI=https://tu-app.onrender.com/setup/oauth2callback
   SESSION_SECRET=tu_clave_secreta_aleatoria
   FLASK_ENV=production
   PORT=5000
   ```

#### 3.5 Instalar gunicorn
Agrega `gunicorn` a tu `requirements.txt`:
```
gunicorn==21.2.0
```

#### 3.6 Crear archivo Procfile (opcional)
Crea un archivo `Procfile` en la raíz:
```
web: gunicorn app:app
```

### Opción B: Heroku

#### 3.1 Instalar Heroku CLI
1. Descarga e instala [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

#### 3.2 Login en Heroku
```bash
heroku login
```

#### 3.3 Crear aplicación
```bash
heroku create tu-app-name
```

#### 3.4 Configurar variables de entorno
```bash
heroku config:set GOOGLE_CLIENT_ID=tu_client_id
heroku config:set GOOGLE_CLIENT_SECRET=tu_client_secret
heroku config:set GOOGLE_REDIRECT_URI=https://tu-app-name.herokuapp.com/setup/oauth2callback
heroku config:set SESSION_SECRET=tu_clave_secreta
heroku config:set FLASK_ENV=production
```

#### 3.5 Crear archivos de configuración
Crea `Procfile`:
```
web: gunicorn app:app
```

Crea `runtime.txt`:
```
python-3.11.0
```

#### 3.6 Desplegar
```bash
git add .
git commit -m "Preparar para producción"
git push heroku main
```

### Opción C: DigitalOcean App Platform

#### 3.1 Crear cuenta en DigitalOcean
1. Ve a [digitalocean.com](https://www.digitalocean.com/)

#### 3.2 Crear nueva app
1. Ve a "Apps" → "Create App"
2. Conecta tu repositorio
3. Configura:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn app:app`

#### 3.4 Configurar variables de entorno
Agrega las mismas variables de entorno que en Render

### Opción D: VPS (Ubuntu Server)

#### 3.1 Conectar al servidor
```bash
ssh usuario@tu-servidor.com
```

#### 3.2 Instalar dependencias
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

#### 3.3 Clonar repositorio
```bash
git clone tu-repositorio.git
cd tu-proyecto
```

#### 3.4 Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 3.5 Configurar variables de entorno
Crea archivo `.env`:
```bash
nano .env
```
Agrega las variables de entorno.

#### 3.6 Crear servicio systemd
Crea `/etc/systemd/system/gmail-bot.service`:
```ini
[Unit]
Description=Gmail Bot Flask App
After=network.target

[Service]
User=usuario
WorkingDirectory=/ruta/a/tu/proyecto
Environment="PATH=/ruta/a/tu/proyecto/venv/bin"
ExecStart=/ruta/a/tu/proyecto/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3.7 Iniciar servicio
```bash
sudo systemctl daemon-reload
sudo systemctl start gmail-bot
sudo systemctl enable gmail-bot
```

#### 3.8 Configurar Nginx
Crea `/etc/nginx/sites-available/gmail-bot`:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/gmail-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 3.9 Configurar SSL con Certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

## Paso 4: Configurar Credenciales del Servidor

### 4.1 Acceder a la ruta de setup
Una vez desplegado, accede a:
```
https://tu-dominio.com/setup
```

### 4.2 Autorizar Google
1. Serás redirigido a Google para autorizar
2. Autoriza el acceso a Gmail con tu cuenta
3. Las credenciales se guardarán en `server_credentials.json` en el servidor

### 4.3 Verificar funcionamiento
1. Accede a `https://tu-dominio.com`
2. Ingresa un email de prueba
3. Selecciona el tipo de búsqueda
4. Haz clic en "Buscar Correo"
5. Deberías ver los resultados

## Paso 5: Verificaciones Finales

### 5.1 Verificar que el archivo server_credentials.json existe
En el servidor, verifica que el archivo se haya creado:
```bash
ls -la server_credentials.json
```

### 5.2 Verificar permisos
Asegúrate de que el archivo tenga permisos correctos:
```bash
chmod 600 server_credentials.json
```

### 5.3 Verificar logs
Revisa los logs de la aplicación para ver si hay errores:
```bash
# En Render/Heroku: Ve a la sección "Logs"
# En VPS: 
sudo journalctl -u gmail-bot -f
```

## Paso 6: Configuración de Producción Adicional

### 6.1 Desactivar modo debug
Asegúrate de que `FLASK_ENV=production` en las variables de entorno.

### 6.2 Configurar SESSION_SECRET seguro
Genera una clave secreta segura:
```python
import secrets
print(secrets.token_hex(32))
```

### 6.3 Configurar CORS (si es necesario)
Si necesitas hacer requests desde otros dominios, instala flask-cors:
```bash
pip install flask-cors
```

Y en `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

## Paso 7: Monitoreo y Mantenimiento

### 7.1 Verificar logs regularmente
Revisa los logs para detectar errores:
- En Render/Heroku: Panel de logs
- En VPS: `sudo journalctl -u gmail-bot`

### 7.2 Verificar que las credenciales no expiren
Las credenciales de OAuth se refrescan automáticamente, pero verifica periódicamente.

### 7.3 Actualizar dependencias
Regularmente actualiza las dependencias:
```bash
pip install --upgrade -r requirements.txt
```

## Solución de Problemas Comunes

### Error: "No hay credenciales válidas"
- Verifica que hayas completado el paso 4 (configurar credenciales del servidor)
- Verifica que el archivo `server_credentials.json` existe en el servidor
- Verifica los permisos del archivo

### Error: "redirect_uri_mismatch"
- Verifica que la URI de redirección en Google Cloud Console coincida exactamente con la de tu servidor
- Asegúrate de usar HTTPS en producción

### Error: "Invalid credentials"
- Verifica que las variables de entorno estén configuradas correctamente
- Verifica que GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET sean correctos

### La aplicación no inicia
- Verifica los logs para ver el error específico
- Verifica que todas las dependencias estén instaladas
- Verifica que el puerto esté disponible

### Error 500 en producción
- Verifica que FLASK_ENV=production
- Verifica los logs para ver el error específico
- Verifica que todas las variables de entorno estén configuradas

## Checklist Final

- [ ] Variables de entorno configuradas en el servidor
- [ ] URI de redirección actualizada en Google Cloud Console
- [ ] Gmail API habilitada en Google Cloud Console
- [ ] Credenciales del servidor configuradas (paso 4)
- [ ] Archivo server_credentials.json existe y tiene permisos correctos
- [ ] Modo debug desactivado en producción
- [ ] SESSION_SECRET configurado y seguro
- [ ] Aplicación accesible desde el navegador
- [ ] Búsqueda de correos funciona correctamente
- [ ] Logs revisados y sin errores

## Soporte

Si tienes problemas:
1. Revisa los logs de la aplicación
2. Verifica que todas las variables de entorno estén configuradas
3. Verifica que la configuración de Google Cloud Console sea correcta
4. Verifica que el archivo server_credentials.json exista y tenga permisos correctos

¡Tu aplicación debería estar funcionando al 100% en producción!
