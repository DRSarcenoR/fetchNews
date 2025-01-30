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
import streamlit as st
import pandas as pd
import numpy as np
import warnings
# ------------------------------>
#     librerías propias
from CHN.general import Analysis, Scrapping
# ------------------------------>



if __name__ in "__main__":
    warnings.filterwarnings('ignore')

