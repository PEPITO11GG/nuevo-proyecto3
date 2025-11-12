# Soporte Automatizado - Netflix Email Finder

## Descripción General
Aplicación web desarrollada en Python con Flask que funciona como herramienta de soporte automatizado para buscar correos electrónicos específicos de Netflix mediante la API de Gmail. La aplicación utiliza la **integración nativa de Gmail de Replit** para una autenticación simplificada y sin configuración manual.

## Estado del Proyecto
**Fecha de última actualización:** 8 de noviembre de 2025

### Cambios Recientes
- **IMPORTANTE**: Migración a integración nativa de Gmail de Replit (eliminado OAuth manual)
- Sistema simplificado que usa la API de Conexiones de Replit para obtener access tokens
- Creación de endpoints para búsqueda de correos de Netflix
- Frontend dark mode con interfaz interactiva actualizada
- Función recursiva para extraer cuerpo de mensajes MIME complejos con padding normalizado
- Eliminadas dependencias de google-auth-oauthlib (ya no necesarias)

## Arquitectura del Proyecto

### Stack Tecnológico
**Backend:**
- Flask (framework web)
- requests (peticiones HTTP a API de Replit)
- google-api-python-client (Gmail API v1)
- google-auth (credenciales OAuth para Gmail API)
- python-dotenv (variables de entorno)
- **Integración nativa de Gmail de Replit** (gestión automática de credenciales)

**Frontend:**
- HTML5, CSS3, JavaScript vanilla
- Diseño dark mode embebido
- Sanitización XSS con escapeHtml

### Estructura de Archivos
```
.
├── app.py                 # Aplicación principal Flask
├── templates/
│   └── index.html        # Frontend con estilos y JS embebidos
├── .gitignore            # Archivos excluidos de git
├── token.json            # Credenciales del usuario (generado)
├── client_secrets.json   # Credenciales OAuth (generado)
└── replit.md            # Esta documentación
```

## Funcionalidades Principales

### Autenticación con Integración de Replit
- **Sistema automatizado**: Utiliza la integración de Gmail de Replit (conn_google-mail_01K9GCJWC6D4AT8DP9THPV8YMM)
- **get_gmail_access_token()**: Función que obtiene access tokens desde la API de Conexiones de Replit
- **get_gmail_service()**: Crea el cliente de Gmail API usando el access token
- **Sin configuración manual**: No requiere client_secrets.json ni OAuth manual

### Búsqueda de Correos
- **Endpoint `/api/verify`** (POST): Busca correos de Netflix
  - Parámetros: `email` (opcional), `type` (verificacion/hogar)
  - Remitente fijo: `info@account.netflix.com`
  - Tipos de búsqueda:
    - `verificacion`: "Código de verificación de Netflix"
    - `hogar`: "Actualiza tu Hogar de Netflix"

### Procesamiento de Mensajes
- Función recursiva `extract_message_body()` para navegar estructura MIME
- Decodificación base64url de contenido
- Soporte para text/plain y text/html

## Configuración

### Variables de Entorno Necesarias
- `SESSION_SECRET`: Clave secreta para sesiones Flask
- `CLIENT_SECRETS_JSON`: Contenido JSON de credenciales OAuth (opcional)
- `BASE_URL`: URL base de la aplicación (para OAuth redirect_uri)

### Configuración de Google OAuth
1. Crear proyecto en Google Cloud Console
2. Habilitar Gmail API
3. Crear credenciales OAuth 2.0
4. Configurar `CLIENT_SECRETS_JSON` o crear archivo `client_secrets.json`

### Permisos de Gmail
- Scope: `https://www.googleapis.com/auth/gmail.readonly` (solo lectura)

## Seguridad

### Características de Seguridad
- Sanitización XSS en frontend con función `escapeHtml()`
- Validación de estado OAuth para prevenir CSRF
- Credenciales almacenadas localmente (no en código)
- Permisos mínimos de Gmail (solo lectura)
- Archivos sensibles excluidos en .gitignore

### Archivos Sensibles Protegidos
- `token.json` (credenciales de usuario)
- `client_secrets.json` (credenciales OAuth)
- `.env` (variables de entorno)

## Uso de la Aplicación

### Flujo de Usuario
1. Acceder a la aplicación
2. Hacer clic en "Autenticar con Google"
3. Autorizar acceso a Gmail (solo lectura)
4. Seleccionar tipo de búsqueda (verificación o hogar)
5. Hacer clic en "Buscar"
6. Visualizar resultados con remitente, asunto y cuerpo del mensaje

### Interfaz Dark Mode
- Gradiente de fondo oscuro
- Elementos con glassmorphism
- Botones con animaciones hover
- Indicadores de estado visuales (success, error, info)
- Código de mensaje en bloque monoespaciado

## Integración con Replit

### Integración Gmail
- ID: `conn_google-mail_01K9GCJWC6D4AT8DP9THPV8YMM`
- Estado: Configurada y autorizada
- Gestión automática de credenciales OAuth

### Workflow Configurado
- Nombre: `flask-app`
- Comando: `python app.py`
- Puerto: 5000
- Tipo: webview

## Próximas Mejoras Sugeridas
- Soporte para múltiples plataformas (Amazon, HBO, Disney+)
- Dashboard de historial de búsquedas
- Filtros por fecha y rango temporal
- Sistema de notificaciones para nuevos correos
- Exportación de resultados (PDF, CSV)

## Notas de Desarrollo
- La aplicación crea automáticamente `client_secrets.json` desde `CLIENT_SECRETS_JSON`
- Se utiliza Flask en modo debug (cambiar para producción)
- El servidor escucha en todas las interfaces (0.0.0.0:5000)
- La función recursiva maneja estructuras MIME complejas de Gmail

## Preferencias del Usuario
- Idioma: Español
- Estilo de interfaz: Dark mode
- Framework: Flask con plantillas Jinja2
- Gestión de dependencias: UV (Replit)
