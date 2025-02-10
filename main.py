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
#from src.plazaPublica import plazaPublica
from src.republica import Republica
# ------------------------------>
#     librerías útiles
#import streamlit as st
import pandas as pd
import numpy as np
import warnings
import json
import io
import time
import random
import json
import functools
from typing import Callable
from datetime import datetime
from pytz import timezone
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
from bs4 import BeautifulSoup
import bs4
import requests
from requests.exceptions import RequestException
# app
import streamlit as st
# ------------------------------>
#     librerías propias
from CHN.general import Analysis, Scrapping, Decorators
# ------------------------------>



class SDecorators:
    def __init_(self) -> None:
        pass
    
    @staticmethod
    def tiempo_ejecucion(func):
        #@functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            tiempo = end - start
            st.write(f'Tiempo de ejecución de {func.__name__}: {tiempo:.6f} segundos')
            return result
        return wrapper
    
    @staticmethod
    def inicio_y_fin(func):
        #@functools.wraps(func)
        def wrapper(*args, **kwargs):
            st.write(f'Inicio de la función: {func.__name__}')
            result = func(*args, **kwargs)
            st.write(f'Fin de la función: {func.__name__}')
            return result
        return wrapper




class scrappedNews:
    def __init__(self, nombre : str) -> None:
        # nombre
        self.nombre = nombre

        # instanciamos todos los objetos de las diferentes paginas
        self.vp = voxPopuli(nombre=nombre)
        self.ep = epInvestiga(nombre=nombre)
        self.ic = insightCrime(nombre=nombre)
        #self.pp = plazaPublica(nombre=nombre)
        self.re = Republica(nombre=nombre)

        # paquete scrapping
        self.scrap = Scrapping()

    @Decorators.inicio_y_fin
    def voxPopuliInfo(self) -> json:
        try:
            # numero de paginas
            max_pages = self.vp.obtener_max_pags()

            mp = max_pages if max_pages else 1

            # todos los articulos
            info = self.vp.all_pages(max_pages=mp)

            return info
        except Exception as e:
            print(f'Error: {e}')
            return {"voxPopuli": []}
    


    @Decorators.inicio_y_fin
    def epInvestigaInfo(self) -> json:
        # extraemos el número de páginas
        response = self.scrap.genRequest(self.ep.url + self.ep.busqueda + self.ep.name)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # numero de páginas
            max_page_ep = self.ep.max_page_number(soup=soup)

            # extraemos toda la información de las páginas
            info = self.ep.all_pages(max_page=max_page_ep)

            return info
        else:
            return {"epInvestiga": []}
        

    @Decorators.inicio_y_fin
    def insightCrimeInfo(self) -> json:
        try:
            # llamamos a la api y generamos el json
            response = self.scrap.genRequest(self.ic.apiurl)

            # transformamos la response a json
            data = json.loads(response.content.decode('utf-8'))

            if isinstance(data, dict):
                # limpiamos la data con la que nos interesa a nostros
                info = self.ic.clean_data(data=data)
                print('todo ok')
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
            
    '''
    @Decorators.inicio_y_fin
    def plazaPublicaInfo(self) -> json:
        # entramos a la pagina y extraemos la información de la busqueda
        html_parsed = self.pp.selenium_conection()
        articulos = [self.pp.extraer_articulos(articulo) for articulo in html_parsed.select('div.gsc-webResult')]

        # json
        info = json.dumps({"plazaPublica": [{"page": 1, "articulos": articulos}]}, indent=4, ensure_ascii=False)

        return info
    '''


    @Decorators.inicio_y_fin
    def republicaInfo(self) -> json:
        try:
            # realizamos la peticion
            response = self.scrap.genRequest(self.re.url + self.re.busqueda + self.re.name)

            if response.status_code == 200:
                try:
                    # parseamos
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # numero de paginas
                    num_pages = self.re.max_pages(soup=soup)

                    # extraemos la info
                    info = self.re.all_pages(num_pages)

                    return info
                except Exception as parse_error:
                    print(f'Error al parsear el html: {parse_error}')
            else:
                print(f'Respuesta http inesperada: {response.status_code}')
        except requests.exceptions.Timeout:
            print("La solicitud tardó demasiado y fue cancelada.")
        except requests.exceptions.ConnectionError:
            print("Error de conexión. Verifica tu internet o si el sitio está caído.")
        except requests.exceptions.HTTPError as http_err:
            print(f"Error http: {http_err}")
        except Exception as e:
            print(f"Error inesperado {e}")
        
        # si todo falla se retorna lo siguiente
        return {"republica": [{"page": 1, "articulos": []}]}

    def ensure_dict(self, obj : str | dict, news : str) -> dict:
        if isinstance(obj, str):
            try:
                return json.loads(obj)
            except json.JSONDecodeError:
                return {}
        return obj if isinstance(obj, dict) else {news: [{"page": 1, "articulos": []}]}


    def combine(self) -> json:
        vp = self.ensure_dict(self.voxPopuliInfo(), "voxPopuli")
        ep = self.ensure_dict(self.epInvestigaInfo(), "epInvestiga")
        ic = self.ensure_dict(self.insightCrimeInfo(), "insightCrime")
        #pp = self.ensure_dict(self.plazaPublicaInfo(), "plazaPublica")
        re = self.ensure_dict(self.republicaInfo(), "republica")

        #vp = None
        #ep = None
        #ic = None
        #pp = None
        #re = None

        info = {
            "voxPopuli": vp['voxPopuli'] if vp else None,
            "epInvestiga": ep['epInvestiga'] if ep else None,
            "insightCrime": ic['insightCrime'] if ic else None,
            #"plazaPublica": pp['plazaPublica'] if pp else None,
            "republica": re['republica'] if re else None
        }

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

    def extract_json(self, data : dict) -> pd.DataFrame:
        if isinstance(data, dict):
            try:
                articulos = [
                    (diary, articulo['titulo'], articulo['resumen'], articulo['link'], articulo['categoria'], articulo['fecha'], articulo['autor'])
                    for diary, pages in data.items()
                    for page in pages
                    for articulo in page['articulos']
                ]
                df = pd.DataFrame(articulos, columns=['Diario', 'Título', 'Resumen', 'Link', 'Categoría', 'Fecha', 'Autor'])
                return df
            except Exception as e:
                print(f'Error: {e}')
                return pd.DataFrame((np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan), columns=['Diario', 'Título', 'Resumen', 'Link', 'Categoría', 'Fecha', 'Autor'])
        else:
            return pd.DataFrame((np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan), columns=['Diario', 'Título', 'Resumen', 'Link', 'Categoría', 'Fecha', 'Autor'])



if __name__ == "__main__":
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

                    # buscamos
                    #df = news.buscar_info()
                    info = news.combine()

                    # extraemos el dataframe
                    df = news.extract_json(data=info)
                    st.session_state["resultados"] = df
                    st.session_state["busqueda"] = termino
                    st.success("Búsqueda completada. Ve a la pestaña de Resultados.")
    elif pagina == 'Resultados':
        st.title('Resultados de la Búsqueda')

        if 'resultados' not in st.session_state:
            st.warning('No hay datos disponibles. Realiza una búsqueda primero.')
        else:
            st.write(f"Resultados para: **{st.session_state['busqueda']}**")
            # busqueda
            termino = st.session_state['busqueda']
            termino2 = '-'.join(termino.strip().split())

            # dataframe
            resultados = st.session_state["resultados"]

            # Convertir datos #
            # a json
            json_data = st.session_state['resultados'].to_json(orient='records', indent=4, force_ascii=False)
            # a xlsx
            xlsx_buffer = io.BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine='openpyxl') as writer:
                resultados.to_excel(writer, index=False, sheet_name='Datos')
            xlsx_data = xlsx_buffer.getvalue()
            # a csv
            csv_buffer = io.StringIO()
            resultados.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            # mostrar los botons en fila
            col1, col2, col3 = st.columns(3)
            with col1:
                # Boton de descarga
                st.download_button(
                    label='Descargar datos en JSON',
                    data=json_data.encode('utf-8'),
                    file_name=f'resultados_{termino2}.json',
                    mime='application/json'
                )
            
            with col2:
                st.download_button(
                    label='Descargar XLSX',
                    data=xlsx_data,
                    file_name=f'resultados_{termino2}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            with col3:
                st.download_button(
                    label='Descargar CSV',
                    data=csv_data,
                    file_name=f'resultados_{termino2}.csv',
                    mime='text/csv'
                )

            # Generar las tablas personalizadas en HTML
            for _, row in resultados.iterrows():
                html2 = f'''
                <div style="border: 1px solid #ddd; border-radius: 8px; margin-bottom: 10px; padding: 10px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td rowspan="4" style="border: 1px solid #ddd; text-align: center; vertical-align: middle; width: 15%; font-weight: bold;">{row['Diario']}</td>
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
                                        <td rowspan="6" style="border: 1px solid #ddd; text-align: center; vertical-align: middle; width: 15%; font-weight: bold;">{row['Diario']}</td>
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