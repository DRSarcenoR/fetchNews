# ------------------------------>
#          VOX POPULI
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

class voxPopuli:
    def __init__(self, nombre: str) -> None:
        # url
        self.url = 'https://voxpopuliguate.com/'
        self.busqueda = '?s='

        # nombre
        self.nombre = nombre
        self.name = '+'.join(self.nombre.split())

        # scrap
        self.scrap = Scrapping()


    def obtener_max_pags(self) -> int:
        try:
            # solicitamos la info
            response = self.scrap.genRequest(self.url + self.busqueda + self.name)

            # verificamos que se haya extraido bien
            if response == 200:
                # parseamos el html
                soup = BeautifulSoup(response.content, 'html.parser')

                # segmentamos las paginas
                paginas = soup.find_all('a', class_='page-numbers')

                # extramos todos los números de página
                numeros_paginas = [int(element.text.strip()) for element in paginas if element.text.strip().isdigit()]

                # maximo
                if numeros_paginas:
                    return max(numeros_paginas)
                else:
                    return 1
        except RequestException as e:
            print(f'Error en la solicitud de paginas: {e}')
            return 1
        except Exception as e:
            print(f'Error inesperado: {e}')
            return 1
    
    def extraer_info_articulo(self, soup: BeautifulSoup) -> dict:
        try:
            link_tag = soup.find("a", class_="image-link")
            link = link_tag["href"] if link_tag else None
            title_tag = soup.find("h2", class_="is-title post-title")
            title = title_tag.get_text(strip=True) if title_tag else None
            
            fecha_entrada_tag = soup.find("time", class_="post-date")
            fecha_entrada = fecha_entrada_tag["datetime"] if fecha_entrada_tag else None

            
            return {
                "titulo": title,
                "resumen": None, 
                "link": link,
                "categoria": None, 
                "fecha": datetime.fromisoformat(fecha_entrada).date(),
                "autor": None
            }
        except Exception as e:
            print(f'Error extrayendo información del articulo: {e}')
            return {}

    def all_pages(self, max_pages : int) -> list:
        full = []
        print('Inicio...')
        for i in range(1, max_pages + 1):
            # agregamos el número de página
            page = f'page/{i}/'
            print(f'Solicitando info pag {i}')
            
            try:
                # headers
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
                # solicitamos la información de la pag
                response = self.scrap.genRequest(self.url + page + self.busqueda + self.name, headers=headers)
                print(f'Estado: {response.status_code}')

                # si se recibio respuesta correcta, parseamos
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # extraemos la información de los articulos
                    articles = [self.extraer_info_articulo(article) for article in soup.select("div.loop article.l-post")]

                    # juntamos la data en formato json
                    data = {"page": i, "articulos": articles}
                    full.append(data)
            except RequestException as e:
                print(f'Error al procesar pagina {i}: {e}')
                continue
            except Exception as e:
                print(f'Error inesperado en la pagina {i}: {e}')
                continue
        
        return {
            'voxPopuli': full
        }





if __name__ in "__main__":
    warnings.filterwarnings('ignore')

    # creamos el objeto
    vp = voxPopuli(nombre='bernardo arevalo')

    # numeor de paginas
    max_pages = vp.obtener_max_pags()

    # todos los articulos
    info = vp.all_pages(max_pages=max_pages)