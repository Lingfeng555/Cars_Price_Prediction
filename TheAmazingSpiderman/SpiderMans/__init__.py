import subprocess

def ejecutar_mitmproxy():
    try:
        # Comando para ejecutar mitmproxy en modo regular y escuchar en el puerto 8080
        comando = ['mitmproxy', '--mode', 'regular', '--listen-port', '8080']

        # Ejecuta el comando en una subproceso
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print("mitmproxy iniciado en el puerto 8080")

        # Puedes esperar a que el proceso termine o hacer que el script continúe.
        proceso.wait()

    except Exception as e:
        print(f"Error al iniciar mitmproxy: {e}")

if __name__ == "__main__":
    ejecutar_mitmproxy()