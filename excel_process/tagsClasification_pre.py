import re
from tqdm import tqdm
import glob
import pandas as pd
from datetime import datetime
from tagsClasification import encontrar_palabras_clave

productos = [ "Varilux", "Eyezen", "Transition", "Transitions", "Crizal", "Stellest", "Attitude", "Panoramax", "Vx", "Tr", "Shamir", "Kodak", "Alcon", "Autograph", "Intouch", "Mp", "Marca propia", "Futurex", "Easy", "Clarity", "Ovation", "Poli", "Antireflejo", "Luz azul" ]
palabras_negocio = [ "Vision sencilla" ,"Terminados" ,"Tallados" ,"AR" ,"Doble estilo" ,"fulljob" ,"NOW" ,"toricos" ,"stock" ,"LC" ,"promo" ,"promocion" ,"CAMPAÑA" ,"garantia" ,"cortesia" ,"pedido" ,"agencia" ,"cartera" ,"transferencia" ]
competidores = [ "Hoya", "Zeiss", "Labocosta", "Visionlab", "Megalens", "Restrepo" ]
palabras_visita = [ "paciente", "medidas", "formula", "precio", "politica", "LP" ]

def getInput():
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
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
    return comment

def analyze_comments(df, palabras_clave, nueva_columna):
    print('Analizando ', nueva_columna, '...')
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
    
    tqdm.pandas()  # Habilita la barra de progreso para `progress_apply`
    df[nueva_columna] = df['Concatenado'].progress_apply(lambda x: encontrar_palabras_clave(x, palabras_clave))

    return df

def main():
    comments = getInput()
    analyzed_comments = analyze_comments(comments, productos, 'tags_productos')
    analyzed_comments = analyze_comments(analyzed_comments, palabras_negocio, 'tags_negocio')
    analyzed_comments = analyze_comments(analyzed_comments, competidores, 'tags_competidores')
    analyzed_comments = analyze_comments(analyzed_comments, palabras_visita, 'tags_visita')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'input_pos_ia/file_{timestamp}.xlsx'
    analyzed_comments.to_excel(filename, index=False)

if __name__ == "__main__":
    main()