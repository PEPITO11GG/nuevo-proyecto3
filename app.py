import os
import json
import base64
from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

<<<<<<< HEAD
# Token file donde se almacenan las credenciales del desarrollador
TOKEN_FILE = 'token.json'
=======
# Configuración de Google Cloud OAuth2
# IMPORTANTE: Rellena estos valores con tus credenciales de Google Cloud Console
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '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')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'https://proyecto-1-jxln.onrender.com/oauth2callback')
>>>>>>> 661fa8d6892714c9b9625706d92402ada5e0a076

# Scopes necesarios para la API de Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

NETFLIX_CONFIG = {
    'sender': 'info@account.netflix.com',
    'subjects': {
        'verificacion': 'Código de verificación de Netflix',
        'hogar': 'Actualiza tu Hogar de Netflix'
    }
}


def get_credentials():
    """
    Obtiene las credenciales almacenadas del desarrollador desde token.json.
    Si las credenciales están expiradas, las refresca automáticamente.
    """
    if not os.path.exists(TOKEN_FILE):
        raise Exception(
            f'No se encontró el archivo {TOKEN_FILE}. '
            'Por favor, ejecuta el script setup_auth.py primero para autenticarte.'
        )
    
    creds = None
    with open(TOKEN_FILE, 'r') as token:
        creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)
    
    # Si las credenciales están expiradas y hay un refresh token, refrescar
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Guardar las credenciales actualizadas
        token_dict = json.loads(creds.to_json())
        with open(TOKEN_FILE, 'w') as token:
            json.dump(token_dict, token, indent=2)
    
    if not creds or not creds.valid:
        raise Exception(
            'Las credenciales no son válidas. '
            'Por favor, ejecuta el script setup_auth.py para reautenticarte.'
        )
    
    return creds


def get_gmail_service():
    """
    Crea un cliente de Gmail API usando las credenciales almacenadas del desarrollador.
    """
    creds = get_credentials()
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
<<<<<<< HEAD
    return render_template('index.html')
=======
    creds = get_credentials()
    authenticated = creds is not None and creds.valid
    
    return render_template('index.html', authenticated=authenticated)


@app.route('/authorize')
def authorize():
    """Inicia el flujo de autorización OAuth2 de Google"""
    # Verificar que las credenciales estén configuradas
    if CLIENT_ID == '574970530991-5r06jcnqo5ic4mk65uovgav3s3vil665' or CLIENT_SECRET == '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' or not CLIENT_ID or not CLIENT_SECRET:
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
                <li><strong>GOOGLE_REDIRECT_URI</strong> - URI de redirección (por defecto: http://localhost:5000/oauth2callback)</li>
            </ul>
            <p>Consulta el archivo <code>CONFIGURACION_GOOGLE_CLOUD.md</code> para más información.</p>
            <a href="/" style="color: #e50914; text-decoration: none;">← Volver al inicio</a>
        </body>
        </html>
        """
        return error_msg, 500
    
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
    
    session['state'] = state
    return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    """Maneja el callback de OAuth2 de Google"""
    try:
        state = session.get('state')
        
        # Verificar si hay un error en la respuesta
        error = request.args.get('error')
        if error:
            error_msg = request.args.get('error_description', 'Error desconocido')
            return f"""
            <html>
            <head><title>Error de Autenticación</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a2e; color: #e6e6e6;">
                <h1 style="color: #ff4757;">⚠️ Error de Autenticación</h1>
                <p>No se pudo completar la autenticación con Google.</p>
                <p><strong>Error:</strong> {error}</p>
                <p><strong>Descripción:</strong> {error_msg}</p>
                <a href="/" style="color: #e50914; text-decoration: none;">← Volver al inicio</a>
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
        session['credentials'] = credentials.to_json()
        
        return redirect(url_for('index'))
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
            <a href="/" style="color: #e50914; text-decoration: none;">← Volver al inicio</a>
        </body>
        </html>
        """, 500


@app.route('/logout')
def logout():
    """Cierra la sesión y elimina las credenciales"""
    session.pop('credentials', None)
    session.pop('state', None)
    return redirect(url_for('index'))
>>>>>>> 661fa8d6892714c9b9625706d92402ada5e0a076


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
        return jsonify({
            'error': f'Error al buscar correos: {error_message}'
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
