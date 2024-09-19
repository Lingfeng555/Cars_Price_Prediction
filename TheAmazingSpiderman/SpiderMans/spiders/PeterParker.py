import scrapy
import time
import os
import re
import random
import json
from scrapy.http import Response
from scrapy_splash import SplashRequest

class MiSpider(scrapy.Spider):
    status = True
    name = 'PeterParker'
    base_url = 'https://www.coches.net'
    start_urls = []
    current_url = ""

    def __init__(self):
        with open('data/JSON/prueba.js', 'r') as archivo:
            cars = json.load(archivo)
        for car in cars:
            self.start_urls.append(self.base_url + car)

    def request (self, url, func):
        if self.status:
            yield scrapy.Request(url, callback=func)
        else:
            yield SplashRequest(url, callback=func)

    def start_requests(self):
        for url in self.start_urls:
            time.sleep(random.uniform(15, 20))
            self.current_url = url
            yield from self.request(url, self.parse)
    
    def changeStatus(self):
        self.status = not self.status
        self.log(f'ERROR AL ACCEDER LA PAGINA =======> SE CAMBIA STATUS A {self.status}')
        time.sleep(random.uniform(15, 20))

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

        titulo = response.xpath('//title/text()').get()
        self.log(f'Título de la página: {titulo}')

        values = response.xpath('//p[contains(@class, "mt-ListModelDetails-listItemValue") and contains(@class, "mt-ListModelDetails-listItemValue--blackBold")]/text()').getall()
        key = response.xpath('//p[@class="mt-ListModelDetails-listItemValue"]/text()').getall()

        for i in range(len(key)):
            self.log(f'{key[i]} : {values[i].strip()}')

        key_tables = response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " mt-ListModelDetails mt-ListModelDetails--paddingless ")]//span[@class="mt-ListModelDetails-tableItem"]/text()').getall()
        values_tables = response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " mt-ListModelDetails mt-ListModelDetails--paddingless ")]//span[@class="mt-ListModelDetails-tableItem--strong"]/text()').getall()

        for i in range(len(key_tables)):
            self.log(f'{key_tables[i]}: {values_tables[i].strip()}')

        text = response.xpath('//div[contains(@class, "mt-PanelEquipment-accordion")]//span[contains(@class, "mt-PanelEquipment-tableItem")]/text()').getall()
    
        # Iterar sobre los textos extraídos y procesarlos
        for x in text:
            self.log(f'Texto encontrado: {x.strip()}')

    def parse(self, response):
        # Extraer el título de la página
        titulo = response.xpath('//title/text()').get()

        self.log(f'Título de la página: {titulo}')

        if ( (titulo == None) or (titulo == "Ups! Parece que algo no va bien...") ) : 
            self.changeStatus()
            yield from self.request(self.current_url, self.parse)
            return
        
        Nombre = response.xpath('//h1[contains(concat(" ", normalize-space(@class), " "), " mt-TitleBasic-title ") and contains(concat(" ", normalize-space(@class), " "), " mt-TitleBasic-title--s ") and contains(concat(" ", normalize-space(@class), " "), " mt-TitleBasic-title--black ")]/text()').get()
        
        self.log(f'Nombre: {Nombre}')
        self.log(f'Precio: {self._getPrice(titulo)} €')
        self.log(f'Provincia: {self._obtener_provincia(titulo)}')

        datos = response.xpath('//li[contains(@class, "mt-PanelAdDetails-dataItem")]//strong/text()').getall()
    
        self.log(f'Anio: {datos[0]}')
        self.log(f'Kilometraje: {datos[1]}')
        self.log(f'Tipo: {datos[3]}')

        ficha_tecnica = response.xpath('//a[contains(@class, "sui-AtomButton sui-AtomButton--primary sui-AtomButton--outline sui-AtomButton--center sui-AtomButton--link sui-AtomButton--circular")]/@href').get()
        self.log(f'Ficha tecnica: {ficha_tecnica}')
        if(ficha_tecnica == None): 
            self.saveFile (response, 'data/html')
            return
        
        yield from self.request(self.base_url + ficha_tecnica, self._parse_ficha_tecnica)