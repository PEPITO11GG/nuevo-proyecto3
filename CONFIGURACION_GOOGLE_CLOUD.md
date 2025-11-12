# Configuración de Google Cloud para Gmail API

## IMPORTANTE: Configuración para Desarrollo

**Los usuarios finales NO necesitan autenticarse con Google.** Esta aplicación está diseñada para que solo el desarrollador autentique una vez, y luego los usuarios puedan buscar correos directamente sin autenticación.

## Pasos para obtener las credenciales

1. **Accede a Google Cloud Console**
   - Ve a https://console.cloud.google.com/
   - Inicia sesión con tu cuenta de Google (la cuenta que tiene acceso a Gmail)

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
       - `http://localhost:8080/` (por defecto, el script encontrará un puerto libre)
       - O cualquier puerto localhost que prefieras (ej: `http://localhost:8080/`, `http://localhost:9000/`)

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
     GOOGLE_REDIRECT_URI=http://localhost:8080/
     ```
   - **Nota**: `GOOGLE_REDIRECT_URI` es opcional. Si no se especifica, el script de configuración encontrará un puerto libre automáticamente.

## Autenticación inicial (solo para el desarrollador)

Una vez configuradas las credenciales en el archivo `.env`:

1. **Ejecuta el script de configuración** (solo una vez):
   ```bash
   python setup_auth.py
   ```

2. **Sigue las instrucciones**:
   - El script abrirá automáticamente tu navegador
   - Inicia sesión con tu cuenta de Google (la cuenta que tiene acceso a Gmail)
   - Autoriza el acceso a Gmail
   - El script guardará las credenciales en `token.json`

3. **¡Listo!** Ahora puedes ejecutar la aplicación Flask:
   ```bash
   python app.py
   ```

## Uso de la aplicación

Una vez configurada la autenticación:

1. **Inicia la aplicación**: `python app.py`
2. **Accede a la aplicación**: http://localhost:5000
3. **Los usuarios pueden buscar correos directamente**:
   - Ingresan el correo electrónico de la plataforma (opcional)
   - Seleccionan el tipo de búsqueda (verificación o hogar)
   - Hacen clic en "Buscar Correo"
   - Ven el contenido del correo más reciente y relevante

**Los usuarios NO necesitan autenticarse con Google en ningún momento.**

## Notas importantes

- **Seguridad**: 
  - Nunca compartas tu `CLIENT_SECRET` públicamente
  - El archivo `token.json` contiene credenciales sensibles y está en `.gitignore`
  - Solo el desarrollador necesita ejecutar `setup_auth.py` una vez

- **Archivos protegidos**: 
  - Asegúrate de que los siguientes archivos estén en `.gitignore`:
    - `.env`
    - `token.json`
    - `client_secrets.json`

- **Scopes**: La aplicación usa el scope `https://www.googleapis.com/auth/gmail.readonly` (solo lectura)

- **Renovación de credenciales**: 
  - Las credenciales se renuevan automáticamente cuando expiran
  - Si hay un problema, ejecuta `setup_auth.py` nuevamente para reautenticarte

- **URI de redirección**: 
  - Si el script encuentra un puerto libre automáticamente, asegúrate de agregar ese puerto como URI de redirección autorizada en Google Cloud Console
  - El script te mostrará qué URI usar si encuentra un puerto libre



