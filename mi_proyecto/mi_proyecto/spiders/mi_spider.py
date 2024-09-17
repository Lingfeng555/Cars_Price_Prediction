import scrapy

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