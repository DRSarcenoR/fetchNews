# ------------------------------>
#          INSIGHT CRIMES
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


class insightCrime:
    def __init__(self, nombre: str) -> None:
        # url
        self.url = 'https://insightcrime.org/es/'
        self.busqueda = '?s='
        

        # nombre
        self.nombre = nombre
        self.name = '%2520'.join(self.nombre.split())
        self.apiurl = f'https://public-api.wordpress.com/rest/v1.3/sites/216560024/search?fields%5B0%5D=date&fields%5B1%5D=permalink.url.raw&fields%5B2%5D=tag.name.default&fields%5B3%5D=category.name.default&fields%5B4%5D=post_type&fields%5B5%5D=shortcode_types&fields%5B6%5D=forum.topic_resolved&fields%5B7%5D=has.image&fields%5B8%5D=image.url.raw&fields%5B9%5D=image.alt_text&highlight_fields%5B0%5D=title&highlight_fields%5B1%5D=content&highlight_fields%5B2%5D=comments&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B0%5D%5Bterm%5D%5Bpost_type%5D=attachment&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B1%5D%5Bterm%5D%5Bpost_type%5D=product&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B2%5D%5Bterm%5D%5Bpost_type%5D=newspack_lst_event&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B3%5D%5Bterm%5D%5Bpost_type%5D=tribe_events&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B4%5D%5Bterm%5D%5Bpost_type%5D=newspack_lst_mktplce&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B5%5D%5Bterm%5D%5Bpost_type%5D=newspack_lst_place&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B6%5D%5Bterm%5D%5Bpost_type%5D=newspack_nl_list&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B7%5D%5Bterm%5D%5Bpost_type%5D=newspack_nl_cpt&filter%5Bbool%5D%5Bmust%5D%5B0%5D%5Bbool%5D%5Bmust_not%5D%5B8%5D%5Bterm%5D%5Bpost_type%5D=newspack_lst_generic&query={self.name}&sort=score_default&size=12'


    def clean_data(self, data: json) -> json:
        # almacenamos cada artiuclo
        articulos = []

        # extraemos unicamente la info que nos interesa
        for articulo in data['results']:
            articulos.append(
                {
                    "titulo": articulo['fields']['title.default'],
                    "resumen": articulo['fields']['excerpt.default'],
                    "link": articulo['fields']['permalink.url.raw'],
                    "categoria": articulo['fields']['category.name.default'],
                    "fecha": datetime.strptime(articulo['fields']['date'], "%Y-%m-%d %H:%M:%S").date(),
                    "autor": None
                }
            )
        
        return {
            'insightCrime': [
                {
                    "page": 1,
                    "articulos": articulos
                }
            ]
        }
            


    


if __name__ in "__main__":
    warnings.filterwarnings('ignore')

    # creamos los obetos
    ic = insightCrime(nombre='bernardo arevalo')
    scrap = Scrapping()

    # llamamos a la api y generamos el json
    data = scrap.genRequest(ic.apiurl)

    # limpiamos la data con la que nos interesa a nostros
    info = ic.clean_data(data=data)