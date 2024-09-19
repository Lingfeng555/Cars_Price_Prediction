import scrapy
import time
import os
import re
import random
import json
from scrapy_splash import SplashRequest

class MiSpider(scrapy.Spider):
    name = 'PeterParker'
    base_url = 'https://www.coches.net'
    start_urls = []

    def __init__(self):
        with open('data/JSON/prueba.js', 'r') as archivo:
            cars = json.load(archivo)
        for car in cars:
            self.start_urls.append(self.base_url + car)

    def start_requests(self):
        for url in self.start_urls:
            time.sleep(random.uniform(5, 10))
            yield SplashRequest(url, self.parse)
    
    def saveFile (self, response, output_dir):
        url_cleaned = re.sub(r'[^\w\-_]', '_', response.url)
        if not os.path.exists(output_dir):os.makedirs(output_dir)
        #Define the name of the file
        filename = f'{output_dir}/{url_cleaned}.html'
        with open(filename, 'wb') as f: f.write(response.body)
        self.log(f'Archivo guardado: {filename}')
        f.close()
    
    def _getPrice(self, title):
        patron = r'(\d{1,3}(?:\.\d{3})*|\d+)\s?€'
        resultado = re.findall(patron, title)
    
        if resultado:
            return resultado[0]
        else:
            return "No se encontró el precio"
    
    def parse(self, response):
        # Extraer el título de la página
        titulo = response.xpath('//title/text()').get()
        
        self.log(f'Título de la página: {titulo}')
        self.log(f'Precio: {self._getPrice(titulo)} €')

        enlace = response.xpath('//a[contains(@class, "sui-AtomButton sui-AtomButton--primary sui-AtomButton--outline sui-AtomButton--center sui-AtomButton--link sui-AtomButton--circular")]/@href').get()
        self.log(f'Ficha tecnica: {enlace}')
        if(enlace == None): return

        #self.saveFile (response, 'data/html') _getPrice("Título de la página: KIA Rio (2021) - 11.800 € en Castellón | Coches.net")