# Configuración para Render.com

## URL de la Aplicación
**Dominio**: https://nuevo-proyecto-1-jxln.onrender.com

## Variables de Entorno Configuradas

Las siguientes variables de entorno deben estar configuradas en Render:

```
GOOGLE_CLIENT_ID=574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback
SESSION_SECRET=tu_clave_secreta_aleatoria_muy_larga_aqui
FLASK_ENV=production
PORT=5000
```

## Pasos para Configurar en Render

### 1. Configurar Variables de Entorno en Render

1. Ve a tu aplicación en Render: https://dashboard.render.com
2. Selecciona tu servicio (nuevo-proyecto-1-jxln)
3. Ve a la sección "Environment"
4. Agrega las siguientes variables de entorno:

   - **GOOGLE_CLIENT_ID**: `574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665.apps.googleusercontent.com`
   - **GOOGLE_CLIENT_SECRET**: `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`
   - **GOOGLE_REDIRECT_URI**: `https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback`
   - **SESSION_SECRET**: Genera una clave secreta aleatoria (usa `python -c "import secrets; print(secrets.token_hex(32))"`)
   - **FLASK_ENV**: `production`
   - **PORT**: `5000`

### 2. Verificar Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona el proyecto: `netflix-477503`
3. Ve a "APIs y servicios" → "Credenciales"
4. Edita tu OAuth 2.0 Client ID
5. Verifica que la **URI de redirección autorizada** incluya:
   ```
   https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback
   ```
6. Verifica que los **Orígenes JavaScript autorizados** incluyan:
   ```
   https://nuevo-proyecto-1-jxln.onrender.com
   ```

### 3. Configurar Credenciales del Servidor (Primera Vez)

1. Una vez que la aplicación esté desplegada en Render
2. Accede a: https://nuevo-proyecto-1-jxln.onrender.com/setup
3. Serás redirigido a Google para autorizar
4. Autoriza el acceso a Gmail con tu cuenta de Google
5. Las credenciales se guardarán automáticamente en `server_credentials.json` en el servidor
6. Verás un mensaje de éxito

### 4. Verificar que Funciona

1. Accede a: https://nuevo-proyecto-1-jxln.onrender.com
2. Ingresa un correo electrónico de prueba
3. Selecciona el tipo de búsqueda (verificación o hogar)
4. Haz clic en "Buscar Correo"
5. Deberías ver los resultados

## Notas Importantes

1. **Archivo server_credentials.json**: Este archivo se crea automáticamente después de autorizar en `/setup`. El archivo actual contiene la configuración del cliente, pero necesita las credenciales del usuario autorizadas.

2. **Seguridad**: 
   - Nunca compartas `GOOGLE_CLIENT_SECRET` o `SESSION_SECRET`
   - Asegúrate de que `.env` y `server_credentials.json` estén en `.gitignore`
   - En producción, siempre usa `FLASK_ENV=production`

3. **URLs**: Todas las URLs deben usar HTTPS en producción. Render proporciona HTTPS automáticamente.

4. **Credenciales**: Solo necesitas configurar las credenciales del servidor UNA VEZ en `/setup`. Después de eso, los usuarios pueden usar la aplicación sin autenticarse.

## Solución de Problemas

### Error: "redirect_uri_mismatch"
- Verifica que la URI en Google Cloud Console sea exactamente: `https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback`
- Verifica que no haya espacios o caracteres extra

### Error: "No hay credenciales válidas"
- Debes completar el paso 3 (acceder a `/setup`) antes de usar la aplicación
- Verifica que el archivo `server_credentials.json` exista en el servidor

### La aplicación no inicia
- Verifica los logs en Render
- Verifica que todas las variables de entorno estén configuradas
- Verifica que `gunicorn` esté en `requirements.txt`

## Comandos Útiles

### Generar SESSION_SECRET seguro
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Verificar variables de entorno en Render
- Ve a la sección "Environment" de tu servicio en Render
- Verifica que todas las variables estén configuradas

## Checklist

- [ ] Variables de entorno configuradas en Render
- [ ] URI de redirección actualizada en Google Cloud Console
- [ ] Orígenes JavaScript actualizados en Google Cloud Console
- [ ] Gmail API habilitada en Google Cloud Console
- [ ] Aplicación desplegada en Render
- [ ] Credenciales del servidor configuradas en `/setup`
- [ ] Aplicación funcionando correctamente

¡Tu aplicación está lista para usar en Render! 🚀
