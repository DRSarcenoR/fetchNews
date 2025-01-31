# /src/__init__.py
# ------------------------------>
#         FETCH NEWS
# ------------------------------>
# 
# script principal del proyecto de 
# web-scrapping en noticias.
# 
# Autor: Diego Sarceño
# Contacto: dsarceno68@gmail.com | diego.sarceno@chn.com.gt
# Tel: (+502) 4204 4629
# 
# ------------------------------>
#     librerias del proyecto
from src.voxPopuli import voxPopuli
from src.epInvestiga import epInvestiga
from src.insightCrime import insightCrime
from src.plazaPublica import plazaPublica
from src.republica import Republica
# ------------------------------>
#     librerías útiles
#import streamlit as st
import pandas as pd
import numpy as np
import warnings
import json
import time
import random
import json
from datetime import datetime
from pytz import timezone
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
# ------------------------------>
#     librerías propias
from CHN.general import Analysis, Scrapping
# ------------------------------>


class scrappedNews:
    def __init__(self, nombre : str) -> None:
        # nombre
        self.nombre = nombre

        # instanciamos todos los objetos de las diferentes paginas
        self.vp = voxPopuli(nombre=nombre)
        self.ep = epInvestiga(nombre=nombre)
        self.ic = insightCrime(nombre=nombre)
        self.pp = plazaPublica(nombre=nombre)
        self.re = Republica(nombre=nombre)

        # paquete scrapping
        self.scrap = Scrapping()


    def voxPopuliInfo(self) -> json:
        # numero de paginas
        max_pages = self.vp.obtener_max_pags()

        mp = max_pages if max_pages else 1

        # todos los articulos
        info = self.vp.all_pages(max_pages=mp)

        return info



    def epInvestigaInfo(self) -> json:
        # extraemos el número de páginas
        response = self.scrap.genRequest(self.ep.url + self.ep.busqueda + self.ep.name)
        if response == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # numero de páginas
            max_page_ep = self.ep.max_page_number(soup=soup)

            # extraemos toda la información de las páginas
            info = self.ep.all_pages(max_page=max_page_ep)

            return info
        

    def insightCrimeInfo(self) -> json:
        try:
            # llamamos a la api y generamos el json
            data = self.scrap.genRequest(self.ic.apiurl)
            
            if isinstance(data, dict):
                # limpiamos la data con la que nos interesa a nostros
                info = self.ic.clean_data(data=data)
                return info
            else:
                print('Error: no se pudo obtener una respuesta válida de la API.')
                return {"insightCrime": []}
        except RequestException as e:
            print(f'Error en la solicitud a la API: {e}')
            info = {'insightCrime': []}
            return info
        except Exception as e:
            print(f'Error inesperado: {e}')
            info = {'insightCrime': []}
            return info
            
    

    def plazaPublicaInfo(self) -> json:
        # entramos a la pagina y extraemos la información de la busqueda
        html_parsed = self.pp.selenium_conection()
        articulos = [self.pp.extraer_articulos(articulo) for articulo in html_parsed.select('div.gsc-webResult')]

        # json
        info = json.dumps({"plazaPublica": [{"page": 1, "articulos": articulos}]}, indent=4, ensure_ascii=False)

        return info
    

    def republicaInfo(self) -> json:
        # realizamos la peticion
        response = self.scrap.genRequest(self.re.url + self.re.busqueda + self.re.name)

        if response.status_code == 200:
            # parseamos
            soup = BeautifulSoup(response.content, 'html.parser')

            # numero de paginas
            num_pages = self.re.max_pages(soup=soup)

            # extraemos la info
            info = self.re.all_pages(num_pages)

            return info
        

    def combine(self) -> json:
        info = json.dumps({
            "voxPopuli": self.voxPopuliInfo()['voxPopuli'],
            "epInvestiga": self.epInvestigaInfo()['epInvestiga'],
            "insightCrime": self.insightCrimeInfo()['insightCrime'],
            "plazaPublica": self.plazaPublicaInfo()['plazaPublica'],
            "republica": self.republicaInfo()['republica']
        }, indent=4, ensure_ascii=False)

        return info
    

    def buscar_info(self) -> pd.DataFrame:
        time.sleep(2)  # Simula un proceso de carga
        datos = [
            {
                "Sitio": f"Sitio {i}",
                "Título": f"Título del artículo {i}",
                "Resumen": f"Este es un resumen del artículo {i} relacionado con {self.nombre}.",
                "Categoría": "Categoría {i % 3 + 1}",
                "Link": f"https://www.ejemplo.com/articulo-{i}",
                "Fecha": f"2023-01-{i:02d}",
                "Autor": f"Autor {i}"
            }
            for i in range(1, 21)
        ]
        return pd.DataFrame(datos)




if __name__ in "__main__":
    warnings.filterwarnings('ignore')

    news = scrappedNews(nombre='bernardo arevalo')

    # toda la busqueda
    info = news.combine()

    with open('data/prueba_general_v1.json', 'w') as gen:
        json.dump(info, gen, indent=4, ensure_ascii=False)


"""
    warnings.filterwarnings('ignore')

    # configuracion inicial de la app
    st.set_page_config(page_title='Scrapping de Noticias', layout='wide')

    # sidebar para navegacion
    pagina = st.sidebar.radio("Navegación", ['Inicio', 'Resultados'])

    if pagina == 'Inicio':
        st.title('Buscador')
        st.write('Ingresa un nombre para realizar la búsqueda...')
        termino = st.text_input('Término de búsqueda', '')
        buscar = st.button('Buscar')

        if buscar:
            if not termino.strip():
                st.error("Por favor, ingresa un término válido para la búsqueda.")
            else:
                with st.spinner("Buscando información..."):
                    # creamos el objeto
                    news = scrappedNews(termino)
                    df = news.buscar_info()
                    st.session_state["resultados"] = df
                    st.session_state["busqueda"] = termino
                    st.success("Búsqueda completada. Ve a la pestaña de Resultados.")
    elif pagina == 'Resultados':
        st.title('Resultados de la Búsqueda')

        if 'resultados' not in st.session_state:
            st.warning('No hay datos disponibles. Realiza una búsqueda primero.')
        else:
            st.write(f"Resultados para: **{st.session_state['busqueda']}**")

            # Convertir datos JSON para descarga
            json_data = st.session_state['resultados'].to_json(orient='records', indent=4, force_ascii=False)

            # Boton de descarga
            st.download_button(
                label='Descargar datos en JSON',
                data=json_data.encode('utf-8'),
                file_name='resultados.json',
                mime='application/json'
            )

            # Generar las tablas personalizadas en HTML
            resultados = st.session_state["resultados"]
            for _, row in resultados.iterrows():
                html2 = f'''
                <div style="border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; padding: 10px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td rowspan="4" style="border: 1px solid #ddd; text-align: center; vertical-align: middle; width: 15%; font-weight: bold;">{row['Sitio']}</td>
                            <td style="border: 1px solid #ddd; font-weight: bold;">Título</td>
                            <td style="border: 1px solid #ddd;">{row['Título']}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; font-weight: bold;">Resumen</td>
                            <td style="border: 1px solid #ddd;">{row['Resumen']}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; font-weight: bold;">Categoría</td>
                            <td style="border: 1px solid #ddd;">{row['Categoría']}</td>
                        </tr>
                        <tr>
                            <td style="border: 1px solid #ddd; font-weight: bold;">Link</td>
                            <td style="border: 1px solid #ddd;"><a href="{row['Link']}" target="_blank">{row['Link']}</a></td>
                        </tr>
                        <tr>
                            <td colspan="2" style="border: 1px solid #ddd; font-weight: bold;">Fecha</td>
                            <td style="border: 1px solid #ddd;">{row['Fecha']}</td>
                            <td style="border: 1px solid #ddd; font-weight: bold;">Autor</td>
                            <td style="border: 1px solid #ddd;">{row['Autor']}</td>
                        </tr>
                    </table>
                </div>
                '''

                html = f'''<div style="border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; padding: 10px;">
                                <table style="width: 100%; border-collapse: collapse;">
                                    <tr>
                                        <td rowspan="6" style="border: 1px solid #ddd; text-align: center; vertical-align: middle; width: 15%; font-weight: bold;">{row['Sitio']}</td>
                                        <td style="border: 1px solid #ddd; font-weight: bold; width: 20%;">Título</td>
                                        <td style="border: 1px solid #ddd; width: 65%;">{row['Título']}</td>
                                    </tr>
                                    <tr>
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Resumen</td>
                                        <td style="border: 1px solid #ddd;">{row['Resumen']}</td>
                                    </tr>
                                    <tr>
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Categoría</td>
                                        <td style="border: 1px solid #ddd;">{row['Categoría']}</td>
                                    </tr>
                                    <tr>
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Link</td>
                                        <td style="border: 1px solid #ddd;"><a href="{row['Link']}" target="_blank">{row['Link']}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Fecha</td>
                                        <td style="border: 1px solid #ddd;">{row['Fecha']}</td>
                                    </tr>
                                    <tr>
                                        <td style="border: 1px solid #ddd; font-weight: bold;">Autor</td>
                                        <td style="border: 1px solid #ddd;">{row['Autor']}</td>
                                    </tr>
                                </table>
                            </div>'''
                st.markdown(html, unsafe_allow_html=True)
"""