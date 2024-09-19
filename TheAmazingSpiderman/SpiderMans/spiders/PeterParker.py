import scrapy
import time
import os
import re
import random
import json
from scrapy.http import Response
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
            time.sleep(random.uniform(15, 20))
            yield scrapy.Request(url, self.parse)
    
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
        
    def _obtener_provincia(self, titulo):
        patron = r'\d+\s€\s*en\s*(.*?)\s*\|'
        resultado = re.search(patron, titulo)
    
        if resultado:
            return resultado.group(1)
        else:
            return "No se encontró el municipio"

    def _parse_ficha_tecnica (self, response):
        
        pass

    def parse(self, response):
        # Extraer el título de la página
        titulo = response.xpath('//title/text()').get()

        self.log(f'Título de la página: {titulo}')
        self.log(f'Precio: {self._getPrice(titulo)} €')
        self.log(f'Provincia: {self._obtener_provincia(titulo)}')

        ficha_tecnica = response.xpath('//a[contains(@class, "sui-AtomButton sui-AtomButton--primary sui-AtomButton--outline sui-AtomButton--center sui-AtomButton--link sui-AtomButton--circular")]/@href').get()
        self.log(f'Ficha tecnica: {ficha_tecnica}')
        if(ficha_tecnica == None): 
            self.saveFile (response, 'data/html')
            return
        yield scrapy.Request(self.base_url + ficha_tecnica, self._parse_ficha_tecnica)

        self.saveFile (response, 'data/html')