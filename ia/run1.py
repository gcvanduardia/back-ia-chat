import pandas as pd
import os
import re
from datetime import datetime
from transformers import pipeline
from transformers import AutoTokenizer
from tqdm import tqdm

# Cargar la pipeline de análisis de sentimientos, que incluye el modelo y el tokenizador
sentiment_pipeline = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
# Cargar el tokenizador
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

def normalize_comment(comment):
    # Convierte a minúsculas
    """ comment = comment.lower() """
    # Elimina caracteres especiales (manteniendo espacios y alfanuméricos)
    """ comment = re.sub(r'[^a-z0-9\s]', '', comment) """
    # Reemplaza múltiples espacios con uno solo
    comment = re.sub(r'\s+', ' ', comment).strip()
    return comment

now = datetime.now()
time_stamp = now.strftime('%Y-%m-%d_%H-%M-%S')

archivos = os.listdir('input')
archivos_excel = [f for f in archivos if f.endswith('.xlsx') or f.endswith('.xls')]

comentarios = []

for archivo in archivos_excel:
    df = pd.read_excel(os.path.join('input', archivo), sheet_name='BBDD Monitoramiento')
    df = df.dropna(subset=['Comentarios', 'Resultado'], how='all')  # Drop rows where both 'Comentarios' and 'Resultado' are NaN
    df['Comentarios'] = df['Comentarios'].astype(str)
    df['Asunto'] = df['Asunto'].astype(str)
    df['Asignado'] = df['Asignado'].astype(str)
    df['Resultado'] = df['Resultado'].astype(str)
    df['Concatenado'] = df.apply(lambda 
                                    row: 
                                    "Asunto: " + row['Asunto'] 
                                 + (". Comentarios: " + row['Comentarios'] if row['Comentarios'] != 'nan' else "") 
                                 + (". Resultado: " + row['Resultado'] if row['Resultado'] != 'nan' else "")
                                 , axis=1)
    comentarios_filtrados = [normalize_comment(comentario) for comentario in df['Concatenado'].tolist() if pd.notnull(comentario) and str(comentario).strip()]
    comentarios.extend(comentarios_filtrados)

    # Elimina los comentarios duplicados
comentarios = list(set(comentarios))

df_comentarios = pd.DataFrame(comentarios, columns=['Comentarios'])
df_comentarios.to_excel(f'output/comentarios_{time_stamp}.xlsx', index=False)

# Lista de comentarios a analizar
""" comments_to_analyze = comentarios[:800] """
comments_to_analyze = comentarios

# Analizar los comentarios
results = []
for comment in tqdm(comments_to_analyze, desc="Analizando comentarios"):
    # Dividir el comentario en partes de 450 tokens con una superposición de 50 tokens
    parts = [comment[i:i+512] for i in range(0, len(comment), 400)]
    
    # Analizar cada parte por separado y almacenar los resultados
    part_results = []
    for part in parts:
        tokenized_part = tokenizer(part, truncation=True, max_length=450)
        result = sentiment_pipeline(tokenizer.decode(tokenized_part['input_ids']))
        part_results.append(result[0])
    
    # Promediar los resultados de las partes
    avg_score = sum(result['score'] for result in part_results) / len(part_results)
    # Usar la etiqueta del resultado con la puntuación más alta
    label = max(part_results, key=lambda result: result['score'])['label']
    
    # Agregar el resultado promedio a los resultados
    results.append({'comment': comment, 'label': label, 'score': avg_score})

# Convertir los resultados en un DataFrame
df_results = pd.DataFrame(results)

# Reordenar las columnas
df_results = df_results[['comment', 'label', 'score']]

# Guardar los resultados en un archivo de Excel
df_results.to_excel(f'output/resultados_analisis_{time_stamp}.xlsx', index=False)