from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Crear la interfaz de usuario
app_ui = ui.page_fluid(
    ui.h2("Aplicación Shiny en Python"),
    ui.input_file("file", "Cargar archivo CSV", accept=".csv"),
    ui.output_table("tabla"),
    ui.output_plot("grafico")
)

# Lógica del servidor
def server(input, output, session):
    @output
    @render.table
    def tabla():
        file = input.file()
        if file is None:
            return None
        # Leer el CSV cargado
        df = pd.read_csv(file["datapath"])
        return df.head()

    @output
    @render.plot
    def grafico():
        file = input.file()
        if file is None:
            return None
        # Leer el CSV y graficar
        df = pd.read_csv(file["datapath"])
        plt.figure(figsize=(8, 4))
        plt.plot(df[df.columns[0]], df[df.columns[1]], label="Datos")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.tight_layout()
        return plt

# Crear la aplicación
app = App(app_ui, server)
