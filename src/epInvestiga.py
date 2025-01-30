# ------------------------------>
#          EP INVESTIGA
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



class epInvestiga:
    def __init__(self, nombre : str) -> None:
        # url y parte de la busqueda
        self.url = 'https://epinvestiga.com/'
        self.busqueda = '?s='

        # nombre ingresado por el usuario y su forma de link
        self.nombre = nombre
        self.name = '+'.join(self.nombre.split())

        # creamos el objeto para hacer scrapping
        self.scrap = Scrapping()


    def dividir_fecha_hora_iso(self, fecha_iso : str) -> dict:
        # Parsear la fecha ISO
        fecha = datetime.fromisoformat(fecha_iso)
        
        # Asegurar que está en zona horaria de Centroamérica (GMT-6)
        centroamerica_tz = timezone("America/Guatemala")
        fecha_gmt6 = fecha.astimezone(centroamerica_tz)
        
        # Formatear fecha y hora
        fecha_formateada = fecha_gmt6.strftime("%Y-%m-%d")  # YYYY-MM-DD
        hora_formateada = fecha_gmt6.strftime("%H:%M:%S")  # HH:MM:SS
        
        # Retornar el diccionario
        return {
            "fecha": fecha_formateada,
            "hora": hora_formateada
        }
    

    def extraer_info_articulo(self, soup : bs4.BeautifulSoup) -> dict:
        # link del articulo
        link = soup.find("a", class_="element-wrap")["href"]

        # titulo del articulo
        titulo = soup.find("h3", class_="post-title").get_text(strip=True)

        # extraer el resumen
        resumen = soup.find("div", class_="entry-summary").get_text(strip=True)

        # fecha de entrada
        fecha_entrada = soup.find("time", class_="entry-date")["datetime"]

        # fecha actualizacion
        fecha_actualizacion = soup.find("time", class_="modify-date")
        if fecha_actualizacion:
            fecha_actualizacion = fecha_actualizacion["datetime"]
        else:
            fecha_actualizacion = None

        # autor
        autor = soup.find("div", class_="post-footer").find("span").get_text(strip=True)

        return {
            "titulo": titulo,
            "resumen": resumen,
            "link": link,
            "categoria": None,
            "fecha": self.dividir_fecha_hora_iso(fecha_entrada)['fecha'],
            "autor": autor
        }
    

    def max_page_number(self, soup : bs4.BeautifulSoup) -> int:
        # filtramos por etiqueta y clase
        page_numbers = soup.find_all('a', class_='page-numbers')
        page_numbers = [int(element.text.strip()) for element in page_numbers if element.text.strip().isdigit()]

        return max(page_numbers) if page_numbers else 1
    

    def all_pages(self, max_page : int) -> list:
        # lista de todos los articulos
        full = []
        print('Inicio...')

        # loop sobre las páginas
        for i in range(1, max_page + 1):
            # agregamos el número de página
            page = f'page/{i}/'
            print(f'Solicitando info pag {i}')
            
            try:
                # solicitamos la información de la pag
                response = self.scrap.genRequest(self.url + page + self.busqueda + self.name)
                print(f'Estado: {response.status_code}')

                # si se recibio respuesta correcta, parseamos
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # extraemos la información de los articulos
                    articulos = soup.find_all("article", class_="post-item")
                    resultado = [self.extraer_info_articulo(articulo) for articulo in articulos]

                    # juntamos la data en formato json
                    data = {"page": i, "articulos": resultado}
                    full.append(data)
            except RequestException as e:
                print(f'Error al procesar pagina {i}: {e}')
                continue
        
        info = json.dumps({'epInvestiga': full}, indent=4, ensure_ascii=False)
        return info


if __name__ in "__main__":
    warnings.filterwarnings('ignore')

    # creamos el objeto
    scrap = Scrapping()
    ep = epInvestiga(nombre='bernardo arevalo')

    # extraemos el número de páginas
    response = scrap.genRequest(ep.url + ep.busqueda + ep.name)
    if response == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # numero de páginas
        max_page_ep = ep.max_page_number(soup=soup)

        # extraemos toda la información de las páginas
        info = ep.all_pages(max_page=max_page_ep)