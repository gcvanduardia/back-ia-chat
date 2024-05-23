import glob
import pandas as pd
import unicodedata
import numpy as np
import re

def filter_by_main_option(option):
    excel_files = glob.glob(f'input_pos_ia_davivienda/*.xlsx')
    if excel_files:
        df = pd.read_excel(excel_files[0])
        df['titulovideo'] = df['titulovideo'].str.lower().str.strip().apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())
        option = unicodedata.normalize('NFKD', option.lower().strip()).encode('ascii', 'ignore').decode()
        query = []
        if option != "todas":
            query.append(f'titulovideo == "{option}"')

        df_filtered = df.query(" and ".join(query)) if query else df.copy()
        return df_filtered
    else:
        print(f"No se encontraron archivos de Excel en la carpeta input")
        return pd.DataFrame()
    
def summary_comments(df):
    df['score'] = df['score'].astype(float)
    total_comentarios = df['Comment'].count()
    comentarios_negativos_relevantes = df[(df['score'] > 0.5) & (df['label'] == 'negative')]['Comment'].count()
    comentarios_positivos_relevantes = df[(df['score'] > 0.5) & (df['label'] == 'positive')]['Comment'].count()
    summary_df = pd.DataFrame({
        'total_comentarios': [total_comentarios],
        'comentarios_negativos_relevantes': [comentarios_negativos_relevantes],
        'comentarios_positivos_relevantes': [comentarios_positivos_relevantes]
    })

    print('summary_df: ')
    print(summary_df)

    kw = palabras_clave_mas_repetidas2(df)

    return [summary_df, kw]


def palabras_clave_mas_repetidas2(df):
    columnas = ['palabras_clave']
    palabras_clave_mas_repetidas = []

    for columna in columnas:
        # Separamos las palabras clave en cada celda
        palabras_clave = df[columna].str.split(', ').explode()
        # Obtenemos todas las palabras clave junto con su frecuencia
        palabras_clave_con_frecuencia = ', '.join([f'{palabra} ({frecuencia})' for palabra, frecuencia in palabras_clave.value_counts().items()])
        palabras_clave_mas_repetidas.append([columna, palabras_clave_con_frecuencia])

    # Convertimos la lista de listas en un DataFrame
    df_resultado = pd.DataFrame(palabras_clave_mas_repetidas, columns=['Categoría', 'Palabra clave (Frecuencia)'])

    return df_resultado



def filter_region_week(region, week):
    """ excel_files = glob.glob(f'input/*.xlsx') """
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
    if excel_files:
        df = pd.read_excel(excel_files[0])
        df['REGION'] = df['REGION'].str.lower().apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())
        region = unicodedata.normalize('NFKD', region.lower()).encode('ascii', 'ignore').decode()

        query = []
        if region != "todas":
            query.append(f'REGION == "{region}"')
        if week != "todas":
            query.append(f'SEMANA == {week}')

        df_filtered = df.query(" and ".join(query)) if query else df.copy()

        return df_filtered
    else:
        print(f"No se encontraron archivos de Excel en la carpeta input")
        return pd.DataFrame()

def normalize_comment(comment):
    if pd.isna(comment):
        return ''
    # Convierte a minúsculas
    """ comment = comment.lower() """
    # Elimina caracteres especiales (manteniendo espacios y alfanuméricos)
    """ comment = re.sub(r'[^a-z0-9\s]', '', comment) """
    # Reemplaza múltiples espacios con uno solo
    comment = re.sub(r'\s+', ' ', comment).strip()
    return comment

def count_tfv_visits(df):
    df['Comentarios'] = df['Comentarios'].apply(normalize_comment)
    df['Resultado'] = df['Resultado'].apply(normalize_comment)
    df['Concat'] = df['Comentarios'] + ' ' + df['Resultado']

    # Crear una nueva columna 'Semanas' con los valores únicos de 'SEMANA' separados por comas y agrupados por 'Asignado'
    df['Semanas'] = df.groupby('Asignado')['SEMANA'].transform(lambda x: ','.join(map(str, x.unique())))

    tfv_count = df[df['Asunto'] == 'TFV'].groupby(['Asignado', 'REGION']).size()
    visitas = df[df['Asunto'] != 'TFV']
    visitas_count = visitas.groupby(['Asignado', 'REGION']).size()
    planificada_count = visitas[visitas['Estatus de la visita'] == 'Planificada'].groupby(['Asignado', 'REGION']).size()
    visitas_realizadas = visitas[visitas['Estatus de la visita'] == 'Realizada'].groupby(['Asignado', 'REGION']).size()
    comments = visitas[(visitas['Comentarios'].str.len() > 3) & (visitas['Resultado'].str.len() > 3)]
    comments_count = comments.groupby(['Asignado', 'REGION']).size()
    positive_comments_count = comments[(comments['label'] == 'positive') & (comments['score'] > 0.5)].groupby(['Asignado', 'REGION']).size()
    negative_comments_count = comments[(comments['label'] == 'negative') & (comments['score'] > 0.5)].groupby(['Asignado', 'REGION']).size()
    duplicated_concatenados_count = comments[comments['Concat'].duplicated()].groupby(['Asignado', 'REGION']).size()

    result = pd.DataFrame({
        'TFV': tfv_count,
        'V': visitas_count,
        'VP': planificada_count,
        'C': comments_count,
        'VR': visitas_realizadas,
        'C+': positive_comments_count,
        'C-': negative_comments_count,
        'CD': duplicated_concatenados_count
    })

    result = result.reset_index()

    # Agregar la columna 'Semanas' a 'result'
    result = result.merge(df[['Asignado', 'Semanas']].drop_duplicates(), on='Asignado', how='left')

    # Reemplazar NaN e inf con 0
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)

    # Calcular el porcentaje
    result['%TFV'] = result['TFV'] / (result['TFV'] + result['V'])
    result['%V'] = result['V'] / (result['TFV'] + result['V'])
    result['%C'] = result['C'] / (result['V'])
    result['%CD'] = result['CD'] / (result['C'])

    # Reemplazar NaN e inf con 0
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)

    # Convertir a porcentaje y redondear
    result['%TFV'] = (result['%TFV'] * 100).round(0).astype(int).astype(str) + '%'
    result['%V'] = (result['%V'] * 100).round(0).astype(int).astype(str) + '%'
    result['%C'] = (result['%C'] * 100).round(0).astype(int).astype(str) + '%'
    result['%CD'] = (result['%CD'] * 100).round(0).astype(int).astype(str) + '%'

    result = result[['Asignado', 'REGION', 'Semanas', 'TFV', '%TFV', 'V', '%V', 'VP', 'VR', 'C', '%C', 'C+', 'C-', 'CD', '%CD']]

    # Cambiar el nombre de la columna 'REGION' a 'REGION__'
    result = result.rename(columns={'REGION': 'REGION__'})
    # Ordenar 'result' por 'REGION__' y 'C-' en orden descendente
    result = result.sort_values(['REGION__', 'C-'], ascending=[True, False])

    kw = palabras_clave_mas_repetidas(df)
    print('palabras_clave_mas_repetidas: ')
    print(kw)

    return [result, kw]

def palabras_clave_mas_repetidas(df):
    columnas = ['tags_productos', 'tags_negocio', 'tags_competidores', 'tags_visita']
    palabras_clave_mas_repetidas = []

    for columna in columnas:
        # Separamos las palabras clave en cada celda
        palabras_clave = df[columna].str.split(', ').explode()
        # Obtenemos todas las palabras clave junto con su frecuencia
        palabras_clave_con_frecuencia = ', '.join([f'{palabra} ({frecuencia})' for palabra, frecuencia in palabras_clave.value_counts().items()])
        palabras_clave_mas_repetidas.append([columna, palabras_clave_con_frecuencia])

    # Convertimos la lista de listas en un DataFrame
    df_resultado = pd.DataFrame(palabras_clave_mas_repetidas, columns=['Categoría', 'Palabra clave (Frecuencia)'])

    return df_resultado