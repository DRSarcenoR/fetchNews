# ------------------------------>
#          PLAZA PUBLICA
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
from selenium.webdriver.common.keys import Keys
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
from CHN.text import text_management
# ------------------------------>



class plazaPublica:
    def __init__(self, nombre : str) -> None:
        # driver y url
        self.__PATH_TO_DRIVER = 'C:/chromedriver-win32/chromedriver-win32/chromedriver.exe'
        self.url = 'https://www.plazapublica.com.gt/'

        # nombre busqueda
        self.nombre = nombre

        # creamos el objeto
        self.tm = text_management()


    def selenium_conection(self) -> bs4.BeautifulSoup:
        # creamos el objeto service
        service = Service(self.__PATH_TO_DRIVER)

        # se inicializa el navegador con el servicio
        driver = webdriver.Chrome(service=service)

        # cargamos la pagina
        driver.get(self.url)

        # esperamos a que cargue la pagina
        WebDriverWait(driver, 10)

        # buscamos el icono de buscar y le damos click
        try:
            buscar_icono = driver.find_element(By.CSS_SELECTOR, '.top-buscar a')
            buscar_icono.click()
            time.sleep(3)
        except:
            print('No fue necesario hacer click')

        # Localizar el campo de búsqueda dentro de Google Custom Search
        search_box = driver.find_element(By.CSS_SELECTOR, "input.gsc-input")

        # Escribir el término de búsqueda y presionar Enter
        search_box.send_keys("bernardo arevalo")
        search_box.send_keys(Keys.RETURN)

        # esperamos un tiempo a que cargue la página
        time.sleep(5) # usamos time sleep para forzar los 5 segundos

        # extramos el html
        html_actual = driver.page_source

        # cerramos el navegador extra
        driver.quit()

        # parseamos el html
        soup = BeautifulSoup(html_actual, 'html.parser')

        return soup

    def extraer_articulos(self, soup : bs4.BeautifulSoup) -> dict:
        title_tag = soup.select_one('.gs-title a')
        url_tag = title_tag['href'] if title_tag else None
        title = title_tag.get_text(strip=True) if title_tag else None

        snippet_tag = soup.select_one('.gs-snippet')
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else None

        source_tag = soup.select_one('.gs-visibleUrl-short')
        source = source_tag.get_text(strip=True) if source_tag else None

        return {
            "titulo": self.tm.remove_unsupported_characters(title),
            "resumen": self.tm.remove_unsupported_characters(snippet),
            "link": self.tm.remove_unsupported_characters(url_tag),
            "categoria": None, 
            "fecha": None,
            "autor": None
        }



if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    # creamos el objeto
    pp = plazaPublica(nombre='bernardo arevalo')

    # entramos a la pagina y extraemos la información de la busqueda
    html_parsed = pp.selenium_conection()
    articulos = [pp.extraer_articulos(articulo) for articulo in html_parsed.select('div.gsc-webResult')]

    # json
    info = json.dumps({"plazaPublica": [{"page": 1, "articulos": articulos}]}, indent=4, ensure_ascii=False)

