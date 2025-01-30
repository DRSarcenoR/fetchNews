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
                html2 = f"""
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
                """

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

            # crea una tabla con scroll
            #st.dataframe(st.session_state['resultados'], height=400)

            
    
