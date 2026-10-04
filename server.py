#!/usr/bin/env python3
"""
Servidor HTTP Local para la Aplicación Móvil PWA Kimby QC
Permite abrir la app en la PC o en cualquier teléfono celular conectado a la misma red Wi-Fi.
"""
import http.server
import socket
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return '127.0.0.1'

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def run_server():
    ip = get_local_ip()
    url_local = f"http://localhost:{PORT}"
    url_mobile = f"http://{ip}:{PORT}"

    print("=" * 65)
    print("🏭 EMBUTIDOS KIMBY - SISTEMA DE CONTROL DE CALIDAD OCR")
    print("=" * 65)
    print(f"\n[+] Servidor iniciado exitosamente en el puerto {PORT}")
    print(f"\n💻 En tu computadora (navegador):")
    print(f"   -> {url_local}")
    print(f"\n📱 En tu teléfono celular (misma red Wi-Fi):")
    print(f"   -> {url_mobile}")
    print("\n💡 Para usar en el móvil:")
    print("   1. Asegúrate de que el celular esté en la misma red Wi-Fi.")
    print(f"   2. Abre Chrome o Safari en tu celular y entra a {url_mobile}")
    print("   3. Si deseas instalarla como app nativa, pulsa 'Agregar a pantalla de inicio'.")
    print("\nPresiona Ctrl + C para detener el servidor.\n")
    print("-" * 65)

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Servidor detenido por el usuario.")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()
