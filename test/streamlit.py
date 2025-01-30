import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__ in "__main__":
    # Título de la aplicación
    st.title("PRUEBAS")


    st.write('### DATOS ALEATORIOS')
    # Generar datos aleatorios
    np.random.seed(42)
    data = pd.DataFrame({
        'x': np.random.rand(100),
        'y': np.random.rand(100)
    })

    # Mostrar el DataFrame en la aplicación
    st.write("### Datos Generados")
    st.dataframe(data)

    # Crear scatter plot con Matplotlib
    fig, ax = plt.subplots()
    ax.scatter(data['x'], data['y'], alpha=0.6)
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.set_title("Gráfico de Dispersión de Datos Aleatorios")

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    
    st.write('### MAPA')
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )

    st.map(map_data)


    st.write('### SESSION STATE')
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    st.session_state.counter += 1

    st.header(f"This page has run {st.session_state.counter} times.")
    st.button("Run it again")
