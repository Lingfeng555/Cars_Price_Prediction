# bloqueador_js.py
from mitmproxy import http

def response(flow: http.HTTPFlow) -> None:
    # Bloquear cualquier archivo con extensión .js
    if flow.request.path.endswith(".js"):
        flow.response = http.Response.make(
            204,  # Código de estado 204 (sin contenido)
            b"",  # Cuerpo vacío
            {"Content-Type": "text/plain"}  # Tipo de contenido
        )