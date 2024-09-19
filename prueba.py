import re

def obtener_precio(titulo):
    # Usa una expresión regular para buscar el precio en formato numérico seguido de €
    # Ajustamos para capturar precios sin decimales
    patron = r'(\d{1,3}(?:\.\d{3})*|\d+)\s?€'
    resultado = re.findall(patron, titulo)
    
    if resultado:
        # Devuelve el primer precio encontrado
        return resultado[0] + " €"
    else:
        return "No se encontró el precio"
    
def obtener_municipio(titulo):
        patron = r'\d+\s€\s*en\s*(.*?)\s*\|'
        resultado = re.search(patron, titulo)
    
        if resultado:
            return resultado.group(1)
        else:
            return "No se encontró el municipio"

# Ejemplo de uso
titulo = "Título de la página: KIA Rio (2021) - 11.800 € en Castellón | Coches.net"
precio = obtener_municipio(titulo)
print(f"El precio es: {precio}")