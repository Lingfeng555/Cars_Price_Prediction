import scrapy
import time
import os
import re
from scrapy_splash import SplashRequest

class MiSpider(scrapy.Spider):
    name = 'PeterParker'
    start_urls = ['https://www.coches.net/fichas_tecnicas/ford/focus/berlina/5-puertas/10_ecoboost_92kw_trend_125cv_gasolina/84821/637923020181107/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 7})
    
    def saveFile (self, response, output_dir):
        url_cleaned = re.sub(r'[^\w\-_]', '_', response.url)
        if not os.path.exists(output_dir):os.makedirs(output_dir)
        #Define the name of the file
        filename = f'{output_dir}/{url_cleaned}.html'
        with open(filename, 'wb') as f: f.write(response.body)
        self.log(f'Archivo guardado: {filename}')
        f.close()
    
    def parse(self, response):
        # Espera 5 segundos
        time.sleep(3)
        # Extraer el título de la página
        titulo = response.xpath('//title/text()').get()
        self.log(f'Título de la página: {titulo}')

        # Ejemplo: extraer todos los enlaces de la página
        for enlace in response.xpath('//a/@href').getall():
            self.log(f'Enlace encontrado: {enlace}')
            #if(enlace == '/segunda-mano/') : 
                #time.sleep(15)
                #self.log(f'Entrando {self.start_urls[0] + 'segunda-mano/'}')
                #yield SplashRequest(self.start_urls[0] + 'segunda-mano/', self.parse, args={'wait': 7})

        #Save the html File
        self.saveFile (response, 'data/html')