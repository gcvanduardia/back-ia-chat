import re
from tqdm import tqdm
import glob
import pandas as pd
from datetime import datetime
from tagsClasification import encontrar_palabras_clave

palabras_clave = [ "Davivienda", "Nequi", "Banco", "Préstamos", "Aplicaciones", "Intereses", "Problemas técnicos", "Quejas", "Crédito", "Banco de Bogotá", "Intereses altos", "Negado", "Libre inversión", "Préstamo", "Tasas", "Pagos", "Tarjeta de crédito", "Aplicación", "Problemas", "Cliente", "Deuda", "Asesoría", "App", "Banco virtual", "Tasa de interés", "Bancolombia", "Falabella", "Nubank", "Cooperativas", "Compra de cartera", "Coopcentral", "Serfinanza", "Caja social", "Bancolombia", "Occidente", "BBVA", "Popular", "GNB", "AV", "Argrario" ]

def getInput():
    excel_files = glob.glob(f'output_pos_ia_davivienda/*.xlsx')
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
    df.loc[:, 'Comment'] = df['Comment'].fillna('').astype(str)
    df.loc[:, 'titulovideo'] = df['titulovideo'].fillna('').astype(str)
    df.loc[:, 'Likes'] = pd.to_numeric(df['Likes'], errors='coerce')
    df.loc[:, 'Concatenado'] = df.apply(lambda row: 
                                    "Likes: " + str(row['Likes']) + ". "
                                    "Video: " + row['titulovideo'] 
                                 + (". Comentario: " + row['Comment'] if row['Comment'] != '' else ""), axis=1)
    
    tqdm.pandas()  # Habilita la barra de progreso para `progress_apply`
    df[nueva_columna] = df['Concatenado'].progress_apply(lambda x: encontrar_palabras_clave(x, palabras_clave))

    return df

def main():
    comments = getInput()
    analyzed_comments = analyze_comments(comments, palabras_clave, 'palabras_clave')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'input_pos_ia_davivienda/file_{timestamp}.xlsx'
    analyzed_comments.to_excel(filename, index=False)

if __name__ == "__main__":
    main()