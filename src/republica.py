# ------------------------------>
#           REPUBLICA GT
# ------------------------------>
# 
# Autor: Diego Sarceño
# Contacto: dsarceno68@gmail.com | diego.sarceno@chn.com.gt
# Tel: (+502) 4204 4629
# 
# 
# ------------------------------>
# paquetes necesarios
import pandas as pd
import time
import random
import json
from datetime import datetime
from pytz import timezone

# scrapping
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import bs4
import requests
from requests.exceptions import RequestException
import warnings
# ------------------------------>
#       PAQUETE PROPIO
from CHN.general import Connections, Scrapping
# ------------------------------>



class Republica:
    def __init__(self, nombre : str) -> None:
        # url y busqueda
        self.url = 'https://republica.gt/'
        self.busqueda = 'buscar/'

        # nombre
        self.nombre = nombre
        self.name = '%20'.join(self.nombre.split())

        # creamos el objeto de scrapping
        self.scrap = Scrapping()

    

    def extraer_articulos(self, soup : bs4.BeautifulSoup) -> dict:
        return {
            "title": soup.select_one(".nota__titulo-item a").get_text(strip=True),
            "url": soup.select_one(".nota__titulo-item a")["href"],
            "category": soup.select_one(".nota__volanta--text").get_text(strip=True),
            "time": soup.select_one(".nota__fecha").get_text(strip=True)
        }

    def max_pages(self, soup : bs4.BeautifulSoup) -> int:
        paginas = soup.find_all('article', class_='number')
        num_pages = [int(element.text.strip()) for element in paginas if element.text.strip().isdigit()]

        return max(num_pages) if num_pages else 1
    

    def all_pages(self, max_page : int) -> json:
        full = []
        print('Inicio...')
        for i in range(1, max_page + 1):
            # agregamos el número de página
            page = f'/{i}/'
            print(f'Solicitando info pag {i}')
            
            try:
                # solicitamos la información de la pag
                response = self.scrap.genRequest(self.url + self.busqueda + self.name + page) 
                print(f'Estado: {response.status_code}')

                # si se recibio respuesta correcta, parseamos
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # extraemos la información de los articulos
                    articulos = soup.find_all("article", class_='nota nota--linea nota')
                    resultado = [self.extraer_articulos(articulo) for articulo in articulos]

                    # juntamos la data en formato json
                    data = {"page": i, "articulos": resultado}
                    full.append(data)
            except RequestException as e:
                print(f'Error al procesar pagina {i}: {e}')
                continue
        return json.dumps({"republica": full}, indent=4, ensure_ascii=False)


if __name__ in "__main__":
    warnings.filterwarnings('ignore')

    # creamos el objeto
    rep = Republica(nombre='bernardo arevalo')
    scrap = Scrapping()

    # realizamos la peticion
    response = scrap.genRequest(rep.url + rep.busqueda + rep.name)

    if response.status_code == 200:
        # parseamos
        soup = BeautifulSoup(response.content, 'html.parser')

        # numero de paginas
        num_pages = rep.max_pages(soup=soup)

        # extraemos la info
        info = rep.all_pages(num_pages)
        


