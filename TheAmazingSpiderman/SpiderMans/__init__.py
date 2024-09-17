import subprocess

def ejecutar_mitmproxy():
    try:
        # Comando para ejecutar mitmproxy en modo regular y escuchar en el puerto 8080
        comando = ['mitmproxy', '--mode', 'regular', '--listen-port', '8080', '-s', 'bloqueador_js.py']

        # Ejecuta el comando en una subproceso
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("mitmproxy iniciado en el puerto 8080 con bloqueo de JavaScript")

        # Puedes esperar a que el proceso termine o hacer que el script continúe.
        proceso.wait()

    except Exception as e:
        print(f"Error al iniciar mitmproxy: {e}")

ejecutar_mitmproxy()