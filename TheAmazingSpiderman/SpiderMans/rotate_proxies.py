from mitmproxy import http
import random

PROXIES = []

for i in range(50):
    PROXIES.append('http://localhost:808'+ str(i))

def request(flow: http.HTTPFlow) -> None:
    # Selecciona un proxy al azar
    proxy = random.choice(PROXIES)
    flow.request.make(proxy)
    print("Usando proxy:", proxy)