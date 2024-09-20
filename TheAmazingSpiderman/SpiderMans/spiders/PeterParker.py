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
    cars_links = []
    current_url = ""
    current_ficha = ""
    scraped = []
    car = {}
    index = 0

    def __init__(self):
        with open('data/JSON/prueba.js', 'r') as archivo:
            self.cars_links = json.load(archivo)

    def request (self, url, func):
        if self.status:
            yield scrapy.Request(url, callback=func)
        else:
            yield SplashRequest(url, callback=func)

    def start_requests(self):
        self.current_url = self.base_url + self.cars_links[self.index]
        yield from self.request(self.current_url, self.parse)
    
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

        ficha = {}

        titulo = response.xpath('//title/text()').get()
        self.log(f'Título de la página: {titulo}')

        if ( (titulo == None) or (titulo == "Ups! Parece que algo no va bien...") ) : 
            self.changeStatus()
            yield from self.request(self.current_ficha, self._parse_ficha_tecnica)
            return

        values = response.xpath('//p[contains(@class, "mt-ListModelDetails-listItemValue") and contains(@class, "mt-ListModelDetails-listItemValue--blackBold")]/text()').getall()
        key = response.xpath('//p[@class="mt-ListModelDetails-listItemValue"]/text()').getall()

        for i in range(len(key)):
            self.log(f'{key[i]} : {values[i].strip()}')

        ficha["General"] = dict(zip(key, values))

        key_tables = response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " mt-ListModelDetails mt-ListModelDetails--paddingless ")]//span[@class="mt-ListModelDetails-tableItem"]/text()').getall()
        values_tables = response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " mt-ListModelDetails mt-ListModelDetails--paddingless ")]//span[@class="mt-ListModelDetails-tableItem--strong"]/text()').getall()

        for i in range(len(key_tables)):
            self.log(f'{key_tables[i]}: {values_tables[i].strip()}')

        ficha["General_2"] = dict(zip(key_tables, values_tables))

        text = response.xpath('//div[contains(@class, "mt-PanelEquipment-accordion")]//span[contains(@class, "mt-PanelEquipment-tableItem")]/text()').getall()

        for x in text:
            self.log(f'Texto encontrado: {x.strip()}')

        ficha["Descripciones"] = text

        self.car["ficha_tecnica"] = ficha
        #print(self.car)

        url_cleaned = re.sub(r'[^\w\-_]', '_', self.current_url)
        with open('data/JSON/' + url_cleaned + '.json', 'w') as file:
            # Escribir la lista de diccionarios en formato JSON
            json.dump(self.car, file, indent=4)
        
        self.index = self.index + 1
        if(self.index >= len(self.cars_links)): return
        self.current_url = self.base_url + self.cars_links[self.index]
        yield from self.request(self.current_url, self.parse)

    def parse(self, response):
        # Extraer el título de la página
        try:
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
                self.index = self.index + 1
                if(self.index >= len(self.cars_links)): return
                self.current_url = self.base_url + self.cars_links[self.index]
                yield from self.request(self.current_url, self.parse)
                return
            
            self.car['Link'] = self.current_url
            self.car['Nombre'] = Nombre
            self.car['Precio'] = self._getPrice(titulo)
            self.car['Provincia'] = self._obtener_provincia(titulo)
            self.car['Anio'] = datos[0]
            self.car['Kilometraje'] = datos[1]
            self.car['Tipo'] = datos[3]


            self.current_ficha = self.base_url + ficha_tecnica

            yield from self.request(self.current_ficha, self._parse_ficha_tecnica)
            self.scraped.append(self.car.copy())
        except:
            self.log("HA OCURRIDO UN ERROR ")
        
    def closed(self, reason):

        self.log(f'SCRAPEO TERMINADO: {len(self.scraped)} EN TOTAL')
        if hasattr(self, 'scraped'):
            with open('data/JSON/datosPrueba_5.json', 'w') as file:
                # Escribir la lista de diccionarios en formato JSON
                print(self.scraped)
                json.dump(self.scraped, file, indent=4)
        else:
            self.log('No hay datos para escribir.')