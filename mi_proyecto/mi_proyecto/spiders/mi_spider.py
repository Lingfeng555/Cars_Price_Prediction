import scrapy
import os
import re

class MiSpider(scrapy.Spider):
    name = 'mi_spider'
    
    # URL que deseas comenzar a rastrear
    start_urls = ['https://www.coches.net/']

    def parse(self, response):
        # Extraer el título de la página
        titulo = response.xpath('//title/text()').get()
        self.log(f'Título de la página: {titulo}')

        # Ejemplo: extraer todos los enlaces de la página
        for enlace in response.xpath('//a/@href').getall():
            self.log(f'Enlace encontrado: {enlace}')

        # Limpieza de la URL para que sea un nombre de archivo válido
        url_cleaned = re.sub(r'[^\w\-_]', '_', response.url)  # Reemplazar caracteres no válidos

        # Crear la carpeta "data/html" si no existe
        output_dir = 'data/html'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Nombre del archivo basado en la URL limpia
        filename = f'{output_dir}/{url_cleaned}.html'

        # Guardar el contenido HTML de la página en un archivo
        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log(f'Archivo guardado: {filename}')