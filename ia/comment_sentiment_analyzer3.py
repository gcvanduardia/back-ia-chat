import pandas as pd
import re
from transformers import pipeline
from transformers import AutoTokenizer
from tqdm import tqdm

# Cargar la pipeline de análisis de sentimientos, que incluye el modelo y el tokenizador
sentiment_pipeline = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
# Cargar el tokenizador
tokenizer = AutoTokenizer.from_pretrained("lxyuan/distilbert-base-multilingual-cased-sentiments-student")

def normalize_comment(comment):
    # Convierte a minúsculas
    """ comment = comment.lower() """
    # Elimina caracteres especiales (manteniendo espacios y alfanuméricos)
    """ comment = re.sub(r'[^a-z0-9\s]', '', comment) """
    # Reemplaza múltiples espacios con uno solo
    comment = re.sub(r'\s+', ' ', comment).strip()
    return comment

def analyze_comments(df):
    df = df.copy()
    df.loc[:, 'Comentarios'] = df['Comentarios'].astype(str)
    df.loc[:, 'Asunto'] = df['Asunto'].astype(str)
    df.loc[:, 'Asignado'] = df['Asignado'].astype(str)
    df.loc[:, 'Resultado'] = df['Resultado'].astype(str)
    df.loc[:, 'Concatenado'] = df.apply(lambda row: 
                                    "Vendedor: " + row['Asignado'] + ". "
                                    "Asunto: " + row['Asunto'] 
                                 + (". Comentarios: " + row['Comentarios'] if row['Comentarios'] != '' else "") 
                                 + (". Resultado: " + row['Resultado'] if row['Resultado'] != '' else ""), axis=1)
    
    # Analizar el sentimiento de cada 'Concatenado' y almacenar los resultados en las nuevas columnas
    tqdm.pandas()  # Habilita la barra de progreso para `progress_apply`
    results = df['Concatenado'].progress_apply(lambda x: sentiment_pipeline(normalize_comment(x))[0])

    # Separar los resultados en dos columnas 'label' y 'score'
    df['label'] = results.apply(lambda x: x['label'])
    df['score'] = results.apply(lambda x: x['score'])

    return df


