import os
import json
import base64
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_SECRET', 'dev-secret-key-change-in-production')

# Configuración de Google Cloud OAuth2
# IMPORTANTE: Las credenciales se cargan desde el archivo .env
CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID', '574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665.apps.googleusercontent.com')
CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET', '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')
REDIRECT_URI: str = os.getenv('GOOGLE_REDIRECT_URI', 'https://nuevo-proyecto3.onrender.com/setup/oauth2callback')

# Scopes necesarios para la API de Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Archivo para almacenar credenciales del servidor
CREDENTIALS_FILE = 'server_credentials.json'

NETFLIX_CONFIG = {
    'sender': 'info@account.netflix.com',
    'subjects': {
        'verificacion': 'Código de verificación de Netflix',
        'hogar': 'Actualiza tu Hogar de Netflix'
    }
}


def get_credentials():
    """
    Obtiene las credenciales de OAuth2 de Google Cloud desde el servidor.
    Las credenciales se almacenan en un archivo del servidor, no en la sesión del usuario.
    Si no hay credenciales válidas, retorna None.
    """
    if not os.path.exists(CREDENTIALS_FILE):
        return None
    
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds_dict = json.load(f)
        
        creds = Credentials.from_authorized_user_info(creds_dict)
        
        # Si las credenciales están expiradas y hay un refresh token, refrescar
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Guardar las credenciales actualizadas
            with open(CREDENTIALS_FILE, 'w') as f:
                json.dump(json.loads(creds.to_json()), f, indent=2)
        
        return creds
    except Exception as e:
        print(f"Error al cargar credenciales: {e}")
        return None


def save_credentials(credentials):
    """
    Guarda las credenciales en el archivo del servidor.
    """
    try:
        creds_dict = json.loads(credentials.to_json())
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(creds_dict, f, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar credenciales: {e}")
        return False


def get_gmail_service():
    """
    Crea un cliente de Gmail API usando las credenciales de Google Cloud OAuth2 del servidor.
    """
    creds = get_credentials()
    
    if not creds or not creds.valid:
        raise Exception('No hay credenciales válidas configuradas en el servidor. Por favor, configura las credenciales primero usando la ruta /setup.')
    
    service = build('gmail', 'v1', credentials=creds)
    return service


def extract_message_body(payload):
    """
    Función recursiva para extraer el cuerpo del mensaje de Gmail.
    Navega por la estructura MIME y decodifica text/plain o text/html.
    """
    mime_type = payload.get('mimeType', '')
    
    if mime_type in ['text/plain', 'text/html']:
        body_data = payload.get('body', {}).get('data', '')
        if body_data:
            padding_needed = len(body_data) % 4
            if padding_needed:
                body_data += '=' * (4 - padding_needed)
            decoded_bytes = base64.urlsafe_b64decode(body_data)
            return decoded_bytes.decode('utf-8', errors='ignore')
    
    parts = payload.get('parts', [])
    for part in parts:
        result = extract_message_body(part)
        if result:
            return result
    
    return None


@app.route('/')
def index():
    """Página principal de la aplicación"""
    # Siempre mostrar el formulario de búsqueda sin verificar autenticación del usuario
    return render_template('index.html')


# Rutas administrativas para configurar credenciales (solo para uso interno del administrador)
@app.route('/setup')
def setup():
    """Página de configuración inicial (solo para administrador)"""
    # Verificar que las credenciales estén configuradas
    if (CLIENT_ID == 'TU_CLIENT_ID_AQUI' or 
        CLIENT_SECRET == 'TU_CLIENT_SECRET_AQUI' or 
        not CLIENT_ID or 
        not CLIENT_SECRET):
        error_msg = """
        <html>
        <head><title>Error de Configuración</title></head>
        <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
            <h1 style="color: #ff4757;">⚠️ Error de Configuración</h1>
            <p>Las credenciales de Google Cloud no están configuradas.</p>
            <p>Por favor, configura las siguientes variables en tu archivo <code>.env</code>:</p>
            <ul style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
                <li><strong>GOOGLE_CLIENT_ID</strong> - Tu Client ID de Google Cloud Console</li>
                <li><strong>GOOGLE_CLIENT_SECRET</strong> - Tu Client Secret de Google Cloud Console</li>
                <li><strong>GOOGLE_REDIRECT_URI</strong> - URI de redirección (por defecto: http://localhost:5000/setup/oauth2callback)</li>
            </ul>
            <p>Consulta el archivo <code>CONFIGURACION_GOOGLE_CLOUD.md</code> para más información.</p>
            <a href="/" style="color: #e50914; text-decoration: none;">← Volver al inicio</a>
        </body>
        </html>
        """
        return error_msg, 500
    
    # Verificar si ya hay credenciales configuradas
    creds = get_credentials()
    if creds and creds.valid:
        return """
        <html>
        <head><title>Configuración Completada</title></head>
        <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
            <h1 style="color: #2ed573;">✓ Credenciales ya configuradas</h1>
            <p>Las credenciales del servidor ya están configuradas y son válidas.</p>
            <p>Los usuarios pueden usar la aplicación sin necesidad de autenticarse.</p>
            <a href="/" style="color: #e50914; text-decoration: none;">← Volver al inicio</a>
        </body>
        </html>
        """
    
    # Iniciar el flujo de autorización
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI]
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    session['setup_state'] = state
    return redirect(authorization_url)


@app.route('/setup/oauth2callback')
def setup_oauth2callback():
    """Maneja el callback de OAuth2 de Google para la configuración inicial"""
    try:
        state = session.get('setup_state')
        
        # Verificar si hay un error en la respuesta
        error = request.args.get('error')
        if error:
            error_msg = request.args.get('error_description', 'Error desconocido')
            return f"""
            <html>
            <head><title>Error de Autenticación</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
                <h1 style="color: #ff4757;">⚠️ Error de Autenticación</h1>
                <p>No se pudo completar la configuración con Google.</p>
                <p><strong>Error:</strong> {error}</p>
                <p><strong>Descripción:</strong> {error_msg}</p>
                <a href="/setup" style="color: #e50914; text-decoration: none;">← Intentar de nuevo</a>
            </body>
            </html>
            """, 400
        
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [REDIRECT_URI]
                }
            },
            scopes=SCOPES,
            state=state
        )
        flow.redirect_uri = REDIRECT_URI
        
        authorization_response = request.url
        flow.fetch_token(authorization_response=authorization_response)
        
        credentials = flow.credentials
        
        # Guardar credenciales en el servidor
        if save_credentials(credentials):
            session.pop('setup_state', None)
            return """
            <html>
            <head><title>Configuración Exitosa</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
                <h1 style="color: #2ed573;">✓ Configuración completada</h1>
                <p>Las credenciales se han guardado correctamente en el servidor.</p>
                <p>Ahora los usuarios pueden usar la aplicación sin necesidad de autenticarse.</p>
                <a href="/" style="color: #e50914; text-decoration: none;">← Ir a la aplicación</a>
            </body>
            </html>
            """
        else:
            return """
            <html>
            <head><title>Error al Guardar</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
                <h1 style="color: #ff4757;">⚠️ Error al Guardar Credenciales</h1>
                <p>No se pudieron guardar las credenciales en el servidor.</p>
                <p>Por favor, verifica los permisos del archivo.</p>
                <a href="/setup" style="color: #e50914; text-decoration: none;">← Intentar de nuevo</a>
            </body>
            </html>
            """, 500
        
    except Exception as e:
        return f"""
        <html>
        <head><title>Error de Autenticación</title></head>
        <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
            <h1 style="color: #ff4757;">⚠️ Error de Autenticación</h1>
            <p>Ocurrió un error al procesar la autenticación:</p>
            <p><strong>{str(e)}</strong></p>
            <p>Por favor, verifica que:</p>
            <ul>
                <li>Las credenciales de Google Cloud estén correctamente configuradas</li>
                <li>La URI de redirección esté autorizada en Google Cloud Console</li>
                <li>La API de Gmail esté habilitada en tu proyecto de Google Cloud</li>
            </ul>
            <a href="/setup" style="color: #e50914; text-decoration: none;">← Intentar de nuevo</a>
        </body>
        </html>
        """, 500


@app.route('/api/verify', methods=['POST'])
def verify_email():
    """
    Busca correos de Netflix según el tipo especificado.
    Recibe: {email: str, type: str}
    type puede ser 'verificacion' o 'hogar'
    """
    data = request.json
    if not data:
        return jsonify({'error': 'Datos de solicitud no válidos'}), 400
    
    user_email = data.get('email', '')
    search_type = data.get('type', 'verificacion')
    
    if search_type not in NETFLIX_CONFIG['subjects']:
        return jsonify({'error': f'Tipo de búsqueda no válido: {search_type}'}), 400
    
    try:
        service = get_gmail_service()
        
        sender = NETFLIX_CONFIG['sender']
        subject = NETFLIX_CONFIG['subjects'][search_type]
        
        query = f'from:{sender} subject:"{subject}"'
        if user_email:
            query += f' to:{user_email}'
        
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=1
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return jsonify({
                'status': 'not_found',
                'message': 'No se encontraron correos que coincidan con la búsqueda'
            })
        
        message_id = messages[0]['id']
        
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        subject_header = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'Sin asunto')
        from_header = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Desconocido')
        
        body = extract_message_body(message['payload'])
        
        return jsonify({
            'status': 'success',
            'subject': subject_header,
            'from': from_header,
            'snippet': message.get('snippet', ''),
            'body': body or 'No se pudo extraer el cuerpo del mensaje'
        })
        
    except Exception as e:
        error_message = str(e)
        if 'No hay credenciales válidas' in error_message or 'credenciales' in error_message.lower():
            return jsonify({
                'error': 'Error del servidor al acceder a Gmail. Por favor, intenta más tarde o contacta al soporte técnico.'
            }), 500
        return jsonify({
            'error': f'Error al buscar correos: {error_message}'
        }), 500


if __name__ == '__main__':
    # Configuración para producción
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
