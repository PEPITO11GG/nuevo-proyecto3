# Instrucciones Rápidas para Render.com

## ✅ Credenciales Configuradas

Las credenciales ya están configuradas en el código:
- **CLIENT_ID**: `574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665.apps.googleusercontent.com`
- **CLIENT_SECRET**: `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`
- **REDIRECT_URI**: `https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback`

## 🚀 Pasos para Desplegar en Render

### Paso 1: Configurar Variables de Entorno en Render

1. Ve a tu aplicación en Render: https://dashboard.render.com
2. Selecciona tu servicio: **nuevo-proyecto-1-jxln**
3. Ve a la sección **"Environment"**
4. Agrega las siguientes variables de entorno:

```
GOOGLE_CLIENT_ID=574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback
SESSION_SECRET=genera-una-clave-secreta-aleatoria-muy-larga-aqui
FLASK_ENV=production
PORT=5000
```

**Nota**: Para generar un `SESSION_SECRET` seguro, ejecuta:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Paso 2: Verificar Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona el proyecto: **netflix-477503**
3. Ve a **"APIs y servicios"** → **"Credenciales"**
4. Edita tu **OAuth 2.0 Client ID**
5. Verifica que la **URI de redirección autorizada** incluya:
   ```
   https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback
   ```
6. Verifica que los **Orígenes JavaScript autorizados** incluyan:
   ```
   https://nuevo-proyecto-1-jxln.onrender.com
   ```
7. **Guarda los cambios**

### Paso 3: Desplegar la Aplicación

1. En Render, verifica que tu servicio esté configurado:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
2. Si es un nuevo despliegue, haz clic en **"Create Web Service"**
3. Si ya existe, haz clic en **"Manual Deploy"** → **"Deploy latest commit"**
4. Espera a que se complete el despliegue (puede tardar 2-5 minutos)

### Paso 4: Configurar Credenciales del Servidor (IMPORTANTE - Solo una vez)

1. Una vez desplegada, accede a: **https://nuevo-proyecto-1-jxln.onrender.com/setup**
2. Serás redirigido a Google para autorizar
3. **Autoriza el acceso a Gmail** con tu cuenta de Google (la cuenta cuyos correos quieres buscar)
4. Serás redirigido de vuelta y verás un mensaje de éxito
5. Las credenciales se guardarán automáticamente en `server_credentials.json` en el servidor

### Paso 5: Probar la Aplicación

1. Accede a: **https://nuevo-proyecto-1-jxln.onrender.com**
2. Ingresa un correo electrónico de prueba
3. Selecciona el tipo de búsqueda (verificación o hogar)
4. Haz clic en **"Buscar Correo"**
5. Deberías ver los resultados del correo

## ⚠️ Importante

1. **Solo necesitas configurar las credenciales UNA VEZ** en el paso 4
2. **Los usuarios finales NO necesitan autenticarse** - pueden usar la aplicación directamente
3. **El archivo `server_credentials.json` se crea automáticamente** después de autorizar en `/setup`
4. **Las variables de entorno deben estar configuradas en Render**, no solo en el código local

## 🔧 Solución de Problemas

### Error: "redirect_uri_mismatch"
- Verifica que la URI en Google Cloud Console sea exactamente: `https://nuevo-proyecto-1-jxln.onrender.com/setup/oauth2callback`
- No debe haber espacios ni caracteres extra
- Debe usar HTTPS (no HTTP)

### Error: "No hay credenciales válidas"
- Debes completar el Paso 4 primero (acceder a `/setup`)
- Verifica que el archivo `server_credentials.json` exista en el servidor
- Revisa los logs en Render para ver errores específicos

### La aplicación no inicia
- Verifica los logs en Render (sección "Logs")
- Verifica que todas las variables de entorno estén configuradas
- Verifica que `gunicorn` esté en `requirements.txt`
- Verifica que el `Procfile` esté correcto

### Error 500 en la aplicación
- Revisa los logs en Render
- Verifica que las credenciales estén correctas
- Verifica que Gmail API esté habilitada en Google Cloud Console

## 📋 Checklist Final

- [ ] Variables de entorno configuradas en Render
- [ ] URI de redirección actualizada en Google Cloud Console
- [ ] Orígenes JavaScript actualizados en Google Cloud Console
- [ ] Gmail API habilitada en Google Cloud Console
- [ ] Aplicación desplegada en Render
- [ ] Credenciales del servidor configuradas en `/setup`
- [ ] Aplicación funcionando correctamente

## 🎯 URLs Importantes

- **Aplicación**: https://nuevo-proyecto-1-jxln.onrender.com
- **Configuración**: https://nuevo-proyecto-1-jxln.onrender.com/setup
- **API**: https://nuevo-proyecto-1-jxln.onrender.com/api/verify

## 📝 Notas

- El archivo `.env` está en `.gitignore` para seguridad
- Las credenciales están configuradas en el código como valores por defecto
- En producción, siempre usa las variables de entorno en Render
- El `SESSION_SECRET` debe ser único y seguro

¡Todo listo para desplegar! 🚀
