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
    comentarios = []
    df = df.copy()
    df = df.dropna(subset=['Comentarios', 'Resultado'], how='all')  # Drop rows where both 'Comentarios' and 'Resultado' are NaN
    df.loc[:, 'Comentarios'] = df['Comentarios'].astype(str)
    df.loc[:, 'Asunto'] = df['Asunto'].astype(str)
    df.loc[:, 'Asignado'] = df['Asignado'].astype(str)
    df.loc[:, 'Resultado'] = df['Resultado'].astype(str)
    df.loc[:, 'Concatenado'] = df.apply(lambda 
                                    row: 
                                    "Vendedor: " + row['Asignado'] + ". "
                                    "Asunto: " + row['Asunto'] 
                                 + (". Comentarios: " + row['Comentarios'] if row['Comentarios'] != 'nan' else "") 
                                 + (". Resultado: " + row['Resultado'] if row['Resultado'] != 'nan' else "")
                                 , axis=1)
    comentarios_filtrados = [normalize_comment(comentario) for comentario in df['Concatenado'].tolist() if pd.notnull(comentario) and str(comentario).strip()]
    comentarios.extend(comentarios_filtrados)

    # Elimina los comentarios duplicados
    comentarios = list(set(comentarios))

    # Lista de comentarios a analizar
    comments_to_analyze = comentarios

    # Crear una nueva lista para almacenar los comentarios que tienen 512 tokens o menos
    filtered_comments = []
    # Crear una nueva lista para almacenar los comentarios que tienen más de 512 tokens
    long_comments = []

    for comment in comments_to_analyze:
        # Convertir el comentario en tokens
        tokens = tokenizer.encode(comment, truncation=False)
        
        # Verificar si el comentario tiene 512 tokens o menos
        if len(tokens) <= 512:
            # Si el comentario tiene 512 tokens o menos, agregarlo a la nueva lista
            filtered_comments.append(comment)
        else:
            # Si el comentario tiene más de 512 tokens, agregarlo a la lista de comentarios largos
            long_comments.append(comment)

    # Reemplazar comments_to_analyze con la nueva lista de comentarios
    comments_to_analyze = filtered_comments

    # Analizar los comentarios
    print("Analizando comentarios")
    results = sentiment_pipeline(comments_to_analyze)

    # Analizr los comentarios largos
    for comment in tqdm(long_comments, desc="Analizando comentarios largos"):
        # Dividir el comentario en partes de 450 tokens con una superposición de 50 tokens
        parts = [comment[i:i+480] for i in range(0, len(comment), 400)]
        
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

    for i, comment in enumerate(comments_to_analyze):
        results[i]['comment'] = comment

    # Crear un DataFrame con los resultados
    df_results = pd.DataFrame(results)
    df_results = df_results.reindex(columns=['comment', 'label', 'score'])

    # Redondear el 'score' a dos decimales
    df_results['score'] = df_results['score'].apply(lambda x: int(round(x * 100, 0)))

    # Agregar el símbolo de porcentaje
    df_results['score'] = df_results['score'].apply(lambda x: str(x) + '%')

    return df_results

