import scrapy
import os
from datetime import datetime

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

        # Obtener la fecha y hora actual para el nombre del archivo
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Crear la carpeta "data/html" si no existe
        output_dir = 'data/html'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Nombre del archivo basado en la fecha y hora del scraping
        filename = f'{output_dir}/{self.start_urls + current_time}.html'

        # Guardar el contenido HTML de la página en un archivo
        with open(filename, 'wb') as f:
            f.write(response.body)

        self.log(f'Archivo guardado: {filename}')