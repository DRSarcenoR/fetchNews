import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import json


if __name__ in "__main__":
    # configuracion inicial de la app
    st.set_page_config(page_title='Scrapping de Noticias', layout='wide')

    # definir función para la busqueda simulada
    def buscar_info(termino):
        time.sleep(2)  # Simula un proceso de carga
        datos = [
            {
                "Sitio": f"Sitio {i}",
                "Título": f"Título del artículo {i}",
                "Resumen": f"Este es un resumen del artículo {i} relacionado con {termino}.",
                "Categoría": "Categoría {i % 3 + 1}",
                "Link": f"https://www.ejemplo.com/articulo-{i}",
                "Fecha": f"2023-01-{i:02d}",
                "Autor": f"Autor {i}"
            }
            for i in range(1, 21)
        ]
        return pd.DataFrame(datos)
        
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
                    df = buscar_info(termino)
                    st.session_state["resultados"] = df
                    st.session_state["busqueda"] = termino
                    st.success("Búsqueda completada. Ve a la pestaña de Resultados.")
    elif pagina == 'Resultados':
        st.title('Resultados de la Búsqueda')

        if 'resultados' not in st.session_state:
            st.warning('No hay datos disponibles. Realiza una búsqueda primero.')
        else:
            st.write(f"Resultados para: **{st.session_state['busqueda']}**")

            # crea una tabla con scroll
            st.dataframe(st.session_state['resultados'], height=400)

            # Convertir datos JSON para descarga
            json_data = st.session_state['resultados'].to_json(orient='records', indent=4, force_ascii=False)

            # Boton de descarga
            st.download_button(
                label='Descargar datos en JSON',
                data=json_data.encode('utf-8'),
                file_name='resultados.json',
                mime='application/json'
            )
    
