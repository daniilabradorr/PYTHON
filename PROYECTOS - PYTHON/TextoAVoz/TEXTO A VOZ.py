'''
Proyecto de Texto a Voz

Este proyecto convierte un artículo existente o texto en un archivo de audio reproducible en formato mp3. 
Usando las bibliotecas NLTK, Newspaper3k y gtts.
Aunque el código podría haber sido dividido en módulos para mejorar su organización y reutilización, 
se ha mantenido en un solo archivo por simplicidad y claridad en la presentación. 

Para una implementación más modular y escalable, se recomienda dividir el código en módulos separados, 
cada uno responsable de una funcionalidad específica (por ejemplo, extracción de texto, procesamiento de texto, conversión de texto a voz, etc.). 
Sin embargo, con fines educativos o demostrativos, mantener el código en un solo archivo puede facilitar su comprensión y revisión rápida.

Autor: [Daniel Labrador Benito]
Fecha: [Fecha]
'''

#Importaciones nesarias para la realización del programa:
import nltk  # NLTK es la biblioteca de procesamiento de lenguaje natural para Python.
import requests
from nltk.corpus import stopwords  # Importa stopwords para filtrar palabras como 'the', 'is', etc.
from nltk.tokenize import sent_tokenize, blankline_tokenize, word_tokenize  # Funciones para dividir el texto en oraciones, líneas y palabras.
from nltk import pos_tag  # Función para etiquetado de partes del discurso.
from nltk.stem import WordNetLemmatizer  # Herramienta para lematizar palabras, es decir, reducir palabras a su raíz.
import spacy  # spaCy es una biblioteca avanzada de procesamiento de lenguaje natural.
from langdetect import detect  # Utilizado para detectar el idioma de un texto.
import newspaper  # Newspaper3k es usado para extracción de artículos de noticias de URLs.
from newspaper import Article,ArticleException  # Clase para manejar y procesar artículos obtenidos de URLs.
from gtts import gTTS
import os
# Descargas necesarias de NLTK
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

# REALIZAMOS LA FUNCIÓN DE SOLICITAR EL TEXTO O LA URL AL USUARIO. ADEMÁS DE UN MANEJO DE ERRORES.
def solicitar_texto_o_url():
    print("BIENVENIDO AL PROGRAMA TEXTO A VOZ")
    while True:
        eleccion_usuario = input('Introducir Texto (1) | URL (2): ')
        # Si elige ingresar texto
        if eleccion_usuario == '1':
            texto = input('Por favor, ingrese el texto: ')
            return texto
        # Si elige ingresar una URL
        elif eleccion_usuario == '2':
            url_articulo = input('Por favor, ingrese la URL: ')
            try:
            # Realizamos la solicitud a la URL y obtenemos el texto del artículo
                response = requests.get(url_articulo)
                response.raise_for_status()  # Lanza una excepción si hay un error en la solicitud HTTP
                articulo = Article(url_articulo)
                articulo.download()
                articulo.parse()
                texto = articulo.text
                return texto
    # Manejamos errores relacionados con la solicitud HTTP
            except requests.RequestException as e:
                print(f"ERROR: No se pudo obtener el artículo de la URL: {e}")
    # Manejamos errores relacionados con la descarga y el análisis del artículo
            except ArticleException as e:
                print(f"ERROR: No se pudo descargar el artículo: {e}")

# REALIZAMOS LA SEGMENTACIÓN DE FRASES Y PÁRRAFOS.
# Definimos una función para segmentar párrafos de manera individual.
def Segmentacion_parrafos(texto):
    # Segmentar el texto en párrafos.
    parrafos = blankline_tokenize(texto)
    return parrafos
# Definimos una función para segmentar frases a partir de los párrafos segmentados.
def Segmentacion_frases_parrafos(parrafos):
    frases_por_parrafo = [sent_tokenize(parrafo) for parrafo in parrafos]
    return frases_por_parrafo

#REALIZAMOS LA LEMATIZACIÓN DE FRASES.
# Cargamos el modelo de spaCy para español
nlp_es = spacy.load('es_core_news_sm')
# Preparar el lematizador de NLTK para inglés
lemmatizer_en = WordNetLemmatizer()
#Función para lematizar las frases de cadad parrafo basándose en el idioma detectado.
def lematizar_frases(frases_por_parrafo):
    lematizadas_por_parrafo = []
    for frases in frases_por_parrafo:
        lematizadas_por_frase = []
        for frase in frases:
            try:
                idioma = detect(frase)  # Detectar el idioma de la frase
                if idioma == 'en':
                    # Proceso de lematización para inglés
                    tokens = word_tokenize(frase)
                    lematizadas = ' '.join([lemmatizer_en.lemmatize(token) for token in tokens])
                elif idioma.startswith('es'):
                    # Proceso de lematización para español
                    doc = nlp_es(frase)
                    lematizadas = ' '.join([token.lemma_ for token in doc])
                else:
                    # Sin lematización si no se detecta el idioma
                    lematizadas = frase
                lematizadas_por_frase.append(lematizadas)
            except Exception as e:
                print(f"Error al lematizar la frase: {frase}. Error: {e}")
                # Si hay un error en la lematización, agregamos la frase original sin lematizar
                lematizadas_por_frase.append(frase)
        lematizadas_por_parrafo.append(lematizadas_por_frase)
    return lematizadas_por_parrafo

#REALIZAMOS LA TOKENIZACIÓN DE PALABRAS
# Definimos una función Tokenizacion_palabras ha sido agregada para tokenizar las palabras en cada frase
def Tokenizacion_palabras(frases_por_parrafo):
    palabras_por_frase = [[word_tokenize(frase) for frase in frases] for frases in frases_por_parrafo]
    return palabras_por_frase

#REALIZAMOS EL ETIQUETADO DE PARTES DEL DISCURSO (POS Tagging).
# Función de POS tagging adaptada para manejar correctamente la estructura de las frases tokenizadas
def etiquetar_pos(frases_tokenizadas):
    pos_etiquetado_por_frase = []
    for lista_frases in frases_tokenizadas:  # lista_frases es una lista de frases, donde cada frase es una lista de tokens
        pos_por_frase = []
        for frase in lista_frases:
            # Cada 'frase' es una lista de palabras/tokens
            pos_por_frase.append(pos_tag(frase))
        pos_etiquetado_por_frase.append(pos_por_frase)
    return pos_etiquetado_por_frase

#REALIZAMOS LA IMPLEMENTACIÓN DE GTTs.
#Función para convertir el texto en audio.
def texto_a_voz(texto, nombre_archivo = 'texto_a_voz_mp3'):
    try:
        idioma = detect(texto)
        if idioma.startswith('es'): #Sí el idioma detectado es el español el audio será en español.
            tts = gTTS(texto, lang='es', slow=False)
            if nombre_archivo:
                tts.save(nombre_archivo)
                print(f"El archivo de audio se ha guardado como {nombre_archivo}")
            # Reproducir el audio sin guardar si no se proporciona un nombre de archivo
            else:
                tts.play()
                print("Reproduciendo el audio...")
        elif idioma.startswith('en'): #Sí el idioma detecatdo es el inglés el audio será en inglés
            tts = gTTS(texto, lang='en', slow=False)
            if nombre_archivo:
                tts.save(nombre_archivo)
                print(f"El archivo de audio se ha guardado como {nombre_archivo}")
            # Reproducir el audio sin guardar si no se proporciona un nombre de archivo
            else:
                tts.play()
                print("Reproduciendo el audio...")
        else:
            print(f"idioma {idioma} no soportado pruebe con otro idioma porfavor.")
    except Exception as e: #Manejo de error.
        print(f"Error al convertir el texto en audio: {e}")
    # Reproducir el archivo de audio
    os.system("start texto_a_voz_mp3")   

#MAIN
texto = solicitar_texto_o_url()
# APLICAR LA SEGMENTACIÓN DE PÁRRAFOS AL TEXTO ORIGINAL.
parrafos_ejemplo = Segmentacion_parrafos(texto)
print("\nPárrafos segmentados:")
print(parrafos_ejemplo)
# APLICAR LA SEGMENTACIÑON DE FRASES A LOS PÁRRAFOS SEGMENTADOS.
frases_por_parrafo = Segmentacion_frases_parrafos(parrafos_ejemplo)
print("\nFrases por párrafo:")
for i, frases in enumerate(frases_por_parrafo):
    print(f"Párrafo {i+1}:")
    for frase in frases:
        print(frase)
    print()
# APLICAR LA TOKENIZACIÓN DE PALABRAS.
palabras_por_frase = Tokenizacion_palabras(frases_por_parrafo)
print("\nPalabras por frase:")
for i, palabras in enumerate(palabras_por_frase):
    print(f"Párrafo {i+1}:")
    for frase_num, frase_palabras in enumerate(palabras):
        print(f"Frase {frase_num+1}: {frase_palabras}")
    print()
# APLICAR EL POS TAGGING.
frases_pos_etiquetadas = etiquetar_pos(palabras_por_frase)
print("\nFrases con etiquetas POS:")
for frases in frases_pos_etiquetadas:
    for frase in frases:
        print(frase)
# CONVERTIR EL TEXTO EN AUDIO.
texto_a_voz(texto)