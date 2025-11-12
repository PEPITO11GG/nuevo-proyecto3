# Configuración de Google Cloud para Gmail API

## Pasos para obtener las credenciales

1. **Accede a Google Cloud Console**
   - Ve a https://console.cloud.google.com/
   - Inicia sesión con tu cuenta de Google

2. **Crea o selecciona un proyecto**
   - Crea un nuevo proyecto o selecciona uno existente
   - Anota el ID del proyecto

3. **Habilita la API de Gmail**
   - Ve a "APIs y servicios" → "Biblioteca"
   - Busca "Gmail API"
   - Haz clic en "Habilitar"

4. **Crea credenciales OAuth 2.0**
   - Ve a "APIs y servicios" → "Credenciales"
   - Haz clic en "Crear credenciales" → "ID de cliente OAuth 2.0"
   - Selecciona "Aplicación web" como tipo de aplicación
   - Configura los siguientes valores:
     - **Nombre**: Gmail Bot Flask (o el nombre que prefieras)
     - **URI de redirección autorizadas**: 
       - `http://localhost:5000/setup/oauth2callback` (para desarrollo local)
       - `https://tu-dominio.com/setup/oauth2callback` (para producción)

5. **Copia las credenciales**
   - Después de crear las credenciales, se mostrarán:
     - **CLIENT_ID**: Un string largo que termina en `.apps.googleusercontent.com`
     - **CLIENT_SECRET**: Un string secreto

6. **Configura las variables de entorno**
   - Crea un archivo `.env` en la raíz del proyecto
   - Agrega las siguientes variables:
     ```
     GOOGLE_CLIENT_ID=tu_client_id_aquí
     GOOGLE_CLIENT_SECRET=tu_client_secret_aquí
     GOOGLE_REDIRECT_URI=http://localhost:5000/setup/oauth2callback
     SESSION_SECRET=tu_clave_secreta_aleatoria_aquí
     ```

## Notas importantes

- **Seguridad**: Nunca compartas tu CLIENT_SECRET públicamente
- **Archivo .env**: Asegúrate de que el archivo `.env` esté en `.gitignore`
- **Archivo server_credentials.json**: Este archivo contiene las credenciales del servidor y debe estar en `.gitignore`
- **Producción**: Cambia el `GOOGLE_REDIRECT_URI` cuando despliegues en producción
- **Scopes**: La aplicación usa el scope `https://www.googleapis.com/auth/gmail.readonly` (solo lectura)
- **Configuración única**: Las credenciales solo se configuran UNA VEZ en el servidor usando la ruta `/setup`
- **Usuarios finales**: Los usuarios finales NO necesitan autenticarse con Google. Solo el administrador necesita configurar las credenciales del servidor una vez.

## Configuración inicial (solo una vez)

Una vez configuradas las credenciales en el archivo `.env`:

1. Inicia la aplicación: `python app.py`
2. Ve a http://localhost:5000/setup
3. Serás redirigido a Google para autorizar el acceso a Gmail
4. Autoriza el acceso a Gmail con tu cuenta de Google (la cuenta cuyos correos quieres buscar)
5. Las credenciales se guardarán en el servidor en `server_credentials.json`
6. Una vez completado, los usuarios finales pueden usar la aplicación sin autenticarse

## Uso de la aplicación (usuarios finales)

Una vez configuradas las credenciales del servidor:

1. Los usuarios finales acceden a http://localhost:5000
2. Ingresan el correo electrónico de la plataforma
3. Seleccionan el tipo de búsqueda (verificación o hogar)
4. Hacen clic en "Buscar Correo"
5. Ven el contenido del correo más reciente y relevante

**Nota**: Los usuarios finales NO necesitan autenticarse con Google. La aplicación usa las credenciales del servidor para acceder a Gmail.



