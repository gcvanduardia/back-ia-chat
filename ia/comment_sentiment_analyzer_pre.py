import re
from transformers import pipeline
from transformers import AutoTokenizer
from tqdm import tqdm
import glob
import pandas as pd
from datetime import datetime

# Cargar la pipeline de análisis de sentimientos, que incluye el modelo y el tokenizador
sentiment_pipeline = pipeline("text-classification", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")
# Cargar el tokenizador
tokenizer = AutoTokenizer.from_pretrained("lxyuan/distilbert-base-multilingual-cased-sentiments-student")

def getInput():
    excel_files = glob.glob(f'input/*.xlsx')
    if excel_files:
        df = pd.read_excel(excel_files[0])
        df_filtered = df.copy()
        return df_filtered
    else:
        print(f"No se encontraron archivos de Excel en la carpeta input")
        return pd.DataFrame()

def normalize_comment(comment):
    # Asegúrate de que comment es una cadena de texto
    if not isinstance(comment, str):
        comment = str(comment)
    # Convierte a minúsculas
    """ comment = comment.lower() """
    # Elimina caracteres especiales (manteniendo espacios y alfanuméricos)
    """ comment = re.sub(r'[^a-z0-9\s]', '', comment) """
    # Reemplaza múltiples espacios con uno solo
    comment = re.sub(r'\s+', ' ', comment).strip()
    # Truncar a 512 tokens
    tokens = tokenizer(comment, truncation=True, max_length=400)
    comment = tokenizer.decode(tokens['input_ids'])
    return comment

def analyze_comments(df):
    df = df.copy()
    df.loc[:, 'Comentarios'] = df['Comentarios'].fillna('').astype(str)
    df.loc[:, 'Asunto'] = df['Asunto'].fillna('').astype(str)
    df.loc[:, 'Asignado'] = df['Asignado'].fillna('').astype(str)
    df.loc[:, 'Resultado'] = df['Resultado'].fillna('').astype(str)
    df.loc[:, 'Concatenado'] = df.apply(lambda row: 
                                    "Vendedor: " + row['Asignado'] + ". "
                                    "Asunto: " + row['Asunto'] 
                                 + (". Comentarios: " + row['Comentarios'] if row['Comentarios'] != '' else "") 
                                 + (". Resultado: " + row['Resultado'] if row['Resultado'] != '' else ""), axis=1)

    # Analizar el sentimiento de cada 'Concatenado' y almacenar los resultados en las nuevas columnas
    tqdm.pandas()  # Habilita la barra de progreso para `progress_apply`
    results = df.progress_apply(lambda row: analyze_if_valid(row['Concatenado'], row['Comentarios'], row['Resultado']), axis=1)

    # Separar los resultados en dos columnas 'label' y 'score'
    df['label'] = results.apply(lambda x: x['label'])
    df['score'] = results.apply(lambda x: x['score'])

    return df

def analyze_if_valid(concatenado, comentario, resultado):
    if (isinstance(comentario, str) and len(comentario) > 3) or (isinstance(resultado, str) and len(resultado) > 3):
        return sentiment_pipeline(normalize_comment(concatenado))[0]
    else:
        return {'label': 'none', 'score': 0}

def main():
    comments = getInput()
    analyzed_comments = analyze_comments(comments)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'input_pos_ia/file_{timestamp}.xlsx'
    analyzed_comments.to_excel(filename, index=False)

if __name__ == "__main__":
    main()