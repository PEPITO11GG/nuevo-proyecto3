"""
Script de configuración inicial para autenticar con Google Cloud.
Este script debe ejecutarse UNA VEZ por el desarrollador para generar el token.json.

Los usuarios finales NO necesitan ejecutar este script ni autenticarse.
"""

import os
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

load_dotenv()

# Configuración de Google Cloud OAuth2
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080/')

# Scopes necesarios para la API de Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Archivo donde se guardarán las credenciales
TOKEN_FILE = 'token.json'

# Variable global para almacenar la respuesta de autorización
authorization_response = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Manejador HTTP para capturar el callback de OAuth2."""
    
    def __init__(self, *args, redirect_uri=None, **kwargs):
        self.redirect_uri = redirect_uri
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        global authorization_response
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Construir la URL completa
        if self.redirect_uri:
            # Construir la URL completa desde redirect_uri y self.path
            base_url = self.redirect_uri.rstrip('/')
            full_path = self.path
            full_url = f"{base_url}{full_path}"
        else:
            # Fallback: construir desde los headers de la solicitud
            host = self.headers.get('Host', 'localhost')
            full_url = f"http://{host}{self.path}"
        
        if 'code' in query_params:
            # Éxito - recibimos el código de autorización
            authorization_response = full_url
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            success_html = '''
                <html>
                <head><title>Autenticación Exitosa</title></head>
                <body style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
                    <h1 style="color: #2ed573;">✅ Autenticación Exitosa</h1>
                    <p>Puedes cerrar esta ventana y volver al terminal.</p>
                </body>
                </html>
            '''
            self.wfile.write(success_html.encode('utf-8'))
        elif 'error' in query_params:
            # Error en la autorización
            error = query_params['error'][0]
            error_description = query_params.get('error_description', ['Error desconocido'])[0]
            authorization_response = None
            self.send_response(400)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_html = f'''
                <html>
                <head><title>Error de Autenticación</title></head>
                <body style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
                    <h1 style="color: #ff4757;">❌ Error de Autenticación</h1>
                    <p><strong>Error:</strong> {error}</p>
                    <p><strong>Descripción:</strong> {error_description}</p>
                    <p>Por favor, cierra esta ventana e intenta de nuevo.</p>
                </body>
                </html>
            '''
            self.wfile.write(error_html.encode('utf-8'))
        else:
            authorization_response = None
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('Error: Respuesta de autorización no válida'.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suprimir los mensajes de log del servidor HTTP
        pass


def create_handler(redirect_uri):
    """Factory function para crear el handler con redirect_uri."""
    def handler(*args, **kwargs):
        return OAuthCallbackHandler(*args, redirect_uri=redirect_uri, **kwargs)
    return handler


def find_free_port():
    """Encuentra un puerto libre en el sistema."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def main():
    """Ejecuta el flujo de autenticación OAuth2 y guarda las credenciales."""
    
    # Verificar que las credenciales estén configuradas
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Error: Las credenciales de Google Cloud no están configuradas.")
        print("\nPor favor, configura las siguientes variables en tu archivo .env:")
        print("  - GOOGLE_CLIENT_ID")
        print("  - GOOGLE_CLIENT_SECRET")
        print("  - GOOGLE_REDIRECT_URI (opcional)")
        print("\nConsulta el archivo CONFIGURACION_GOOGLE_CLOUD.md para más información.")
        return
    
    # Verificar si ya existe un token
    if os.path.exists(TOKEN_FILE):
        response = input(f"\n⚠️  El archivo {TOKEN_FILE} ya existe. ¿Deseas reautenticarte? (s/n): ")
        if response.lower() != 's':
            print("Operación cancelada.")
            return
    
    print("\n🔐 Iniciando proceso de autenticación con Google Cloud...")
    print("Este proceso solo necesita realizarse UNA VEZ.")
    print("Los usuarios finales NO necesitarán autenticarse.\n")
    
    # Determinar el puerto y la URI de redirección
    if REDIRECT_URI and REDIRECT_URI != 'http://localhost:8080/':
        # Usar la URI configurada
        redirect_uri = REDIRECT_URI
        port = urlparse(redirect_uri).port or 8080
    else:
        # Encontrar un puerto libre
        port = find_free_port()
        redirect_uri = f'http://localhost:{port}/'
        print(f"⚠️  Nota: Asegúrate de que '{redirect_uri}' esté configurado como URI de redirección")
        print(f"    autorizada en Google Cloud Console.\n")
    
    # Crear el flujo de OAuth2
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    # Obtener la URL de autorización
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    print("Por favor, sigue estos pasos:")
    print("1. Se abrirá automáticamente una ventana en tu navegador")
    print("2. Inicia sesión con tu cuenta de Google (la cuenta que tiene acceso a Gmail)")
    print("3. Autoriza el acceso a Gmail")
    print("4. La ventana se cerrará automáticamente cuando termine\n")
    
    # Crear el handler con el redirect_uri
    handler = create_handler(redirect_uri)
    
    # Iniciar el servidor HTTP
    server = HTTPServer(('localhost', port), handler)
    
    import webbrowser
    
    # Abrir el navegador automáticamente
    print(f"Abriendo navegador en: {authorization_url}\n")
    webbrowser.open(authorization_url)
    
    # Esperar por la respuesta de autorización (timeout de 5 minutos)
    print("Esperando respuesta de autorización...")
    server.timeout = 300
    server.handle_request()
    
    if authorization_response is None:
        print("\n❌ Error: No se recibió la respuesta de autorización.")
        print("Por favor, intenta ejecutar el script nuevamente.")
        return
    
    try:
        # Intercambiar el código de autorización por un token
        # authorization_response ya contiene la URL completa
        flow.fetch_token(authorization_response=authorization_response)
        
        # Obtener las credenciales
        credentials = flow.credentials
        
        # Guardar las credenciales en el archivo token.json
        # Usar el mismo formato que la aplicación espera
        token_dict = json.loads(credentials.to_json())
        
        with open(TOKEN_FILE, 'w') as token:
            json.dump(token_dict, token, indent=2)
        
        print(f"\n✅ ¡Autenticación exitosa!")
        print(f"Las credenciales se han guardado en {TOKEN_FILE}")
        print("\nAhora puedes ejecutar la aplicación Flask y los usuarios podrán buscar correos sin autenticarse.")
        print("Las credenciales se refrescarán automáticamente cuando sea necesario.\n")
        
    except Exception as e:
        print(f"\n❌ Error durante la autenticación: {str(e)}")
        print("\nPor favor, verifica que:")
        print("  - Las credenciales de Google Cloud estén correctamente configuradas")
        print("  - La URI de redirección esté autorizada en Google Cloud Console")
        print("  - La API de Gmail esté habilitada en tu proyecto de Google Cloud")
        print("  - Hayas autorizado el acceso correctamente")


if __name__ == '__main__':
    main()

