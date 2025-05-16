"""
Imagina que esta API es una biblioteca de películas:   
La función load_movies() es como una biblioteca que carga el catálogo de libros (películas) cuando se abre la biblioteca.
La funcion de get_movies() muestra todo el catálogo cuando alguien lo pide.
La función get_movie(id) es como si alguien preguntara por un libro en específico, es decir, por un código de identificación.
La función chatbot (query) es un asistente que busca películas segun palabras clave y sinónimo.
La función get_movies_by_category(category) ayuda a encontrar películas según su género (acción, comedia, etc...)
"""

# Importamos las herramientas necesarias para continuar nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear la API, HTTPException nos ayuda a manejar errores
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse nos ayuda a manejar respuestas HTML, JSONResponse nos ayuda a manejar respuestas en formato JSON
import pandas as pd # Pandas nos ayuda a manejar datos en tablas como si fuera un Excel
import nltk # nltk es una librería para procesar texto y analizar palabras
from nltk.tokenize import word_tokenize # word_tokenize nos ayuda a tokenizar texto, es decir, a convertirlo en palabras.
from nltk.corpus import wordnet # wordnet es una librería para analizar sinónimos.

# Indicamos la ruta donde nltk buscará los datos descargados en nuestro computador.
nltk.data.path.append ('C:\Users\USUARIO\AppData\Roaming\nltk_data')
nltk.download('punkt')