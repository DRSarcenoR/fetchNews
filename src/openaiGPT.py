import os 
from dotenv import load_dotenv
#import src.openaiGPT as openaiGPT
import json
import subprocess
from openai import OpenAI
import os
from pathlib import Path

class openaiGPT:
    def __init__(self) -> None:
        # ruta al archivo .env
        dotenv_path = Path(__file__).resolve().parent.parent / ".env"

        # configuramos proxies
        os.environ['HTTP_PROXY'] = "http://DRSarcenoR:Periphery.8@172.31.100.99:8080"
        os.environ['HTTPS_PROXY'] = "http://DRSarcenoR:Periphery.8@172.31.100.99:8080"

        # Cargamos la info del archivo .env (api)
        load_dotenv(dotenv_path)

        # instanciamos el cliente
        self.cliente = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        
        # definimos la key
        #openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def search(self, link: str) -> str:
        prompt = (
            f"Visita este enlace de una noticia pública y extrae solamente el texto del artículo principal, sin anuncios, menús ni información adicional.\n\n"
            f"Enlace: {url}\n\n"
            f"Devuelve solo el texto completo del artículo, en formato de texto plano."
        )
        response = self.cliente.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
        
    def extract(self, text: str) -> list | None:
        prompt = (
            "Extrae todos los nombres de personas mencionadas en el siguiente texto de noticia. "
            "Devuélvelos como una lista de Python sin repetir y solo nombres completos, sin explicaciones ni detalles adicionales. "
            "Texto:\n\n"
            f"{text}\n\n"
            "Lista de nombres:"
        )
        response = self.cliente.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        contenido = response.choices[0].message.content
        try:
            nombres = eval(contenido)
            if isinstance(nombres, list):
                return nombres
        except:
            print("No se pudo convertir la respuesta en lista:", contenido)
        return []


if __name__ == "__main__":
    # creamos el objeto
    oai = openaiGPT()

    url = "https://news.google.com/read/CBMiywJBVV95cUxOSUloRllkZ0JZcGQ1OHRHbHB1RGdqU3k4cmlWZUNQRTFCTjJ4WkFEbnRkLWNld2Q1UHRsY0lwdXp6bzZCYllYY0k2clc3eUpzUHBhZ29WNEozMnNGbzBRTHFzYVhkMUZiMGJRZTNzV3RKQlNsR3hqQzJsY1pBbmFBUWFtaWNNa2NESzFGMjQ5dXJOakhPMnlnSTNzQWxwMlFmWjRza1hQLXg5MW1rdU5UM0dUWjRUaTN4dkludmE4QzBPNDhHaE45T3VidXRmZWR5LWhJeC1ZbHpvcTF6cHJlcFpURGhHQm04cm1EMkU4RU10aHlZbDRhdUhxLWVWTzYtYTVXa09tVjFNUFlCVnoybWRDelctU05PcXhCOW9oNGZpT2xvbkZTdXd0TzZZa09BeTU1bUR3TFdwX1diQXdKbU5ZakFSZmNrZ2FJ?hl=es-419&gl=US&ceid=US%3Aes-419"
    texto = oai.search(link=url)
    nombres = oai.extract(text=texto)
    
    print("Texto: \n", texto[:500], "...\n")
    print("Nombres encontrados: ", nombres)