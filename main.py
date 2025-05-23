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
nltk.download('punkt_tab')

# Indicamos la ruta donde nltk buscará los datos descargados en nuestro computador.
nltk.data.path.append (r"C:\Users\USUARIO\AppData\Roaming\nltk_data")
nltk.download('punkt') # Es un paquete para dividir frases en palabras
nltk.download('wordnet') # Paquete para encontrar sinónimos en palabras

# Función para cargar las películas desde un archivo csv

def load_movies():
    # Leemos el archivo que contiene información de peliculas y seleccionamos las columnas más importantes
    df = pd.read_csv(r"./Dataset/netflix_titles.csv")[['show_id','title','release_year','listed_in','rating','description']]
    
# Renombramos las columnas para que sean más fáciles de entender
    df.columns = ['id','title','year','category','rating','overview']
    
# Llenamis los espacios vacíos con texto vacío y convertimos los datos en una lista de diccionarios
    return df.fillna('').to_dict(orient='records')

# Cargamos las películas al inicial la API para no leer el archivo cada vez que alguien pregunte por ellas
movies_list = load_movies()

# Función para encontrar sinonimos de una palabra
def get_synonyms(word): 
    # Usamos wordnet para encontrar distintas palabras que significan lo mismo
    return{lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# Creamos la aplicación FastAPI, que será el motor de nuestra API
# Esto inicializa la API con un nombre y una versión 
app = FastAPI(title='Mi aplicación de películas', version='1.0.0')

@app.get('/', tags=['Home'])
def home():
    # Cuando entremos en el navegador a http://127.0.0.1:8000 veremos un mensaje de bienvenida
    return HTMLResponse('<h1> Bienvenido a la API de peliculas </h1>')

# Obteniendo la lista de películas
# Creamos una ruta para obtener todas las películas
# Ruta para obtener todas las películas
@app.get('/movies', tags=['Movies'])
def get_movies():
    # Si hay películas, las enviamos, si no mostramos un error
    return movies_list or HTMLResponse(status_code=500, detail="No hay datos de películas disponibles")

# Ruta para obtener una película específica por su ID
@app.get('/movies/{id}', tags=['Movies'])
def get_movies(id: str):
    # Buscamos en la lista de películas la que tenga el mismo ID
    return next((m for m in movies_list if m['id'] == id), {"Detalle": "Película no encontrada"})

# Ruta del chatbot que responde con películas según palabras clave de la categoría
@app.get('/chatbot', tags=['chatbot'])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intención del usuario
    query_words = word_tokenize(query.lower())
    # Buscamos sinónimos de las palabras clave para ampliar la búsqueda
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words) 
    
    # Filtramos la lista de películas buscando coincidencias en la categoria
    results =[m for m in movies_list if any (s in m ['category'].lower() for s in synonyms)]
    
    # Si encontramos las películas, enviamos la lista de películas ; si no, mostramos un mensaje de que no se encontraron coincidencias
    
    return JSONResponse (content={
        "respuesta": "Aquí tienes algunas películas relacionadas." if results else "No encontré películas en esa categoría.",
        "películas": results
    })

# Ruta para buscar películas por categoría específica
@app.get ('/movies/by_category/', tags=['Movies'])
def get_movies_by_category(category: str):
    # Filtramos la lista de películas según la categoría ingresada
    return [m for m in movies_list if category.lower() in m['category'].lower()]
