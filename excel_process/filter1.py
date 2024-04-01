import glob
import pandas as pd
import unicodedata
import numpy as np
import re

def filter_region_week(region, week):
    """ excel_files = glob.glob(f'input/*.xlsx') """
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
    if excel_files:
        df = pd.read_excel(excel_files[0])
        df['REGION'] = df['REGION'].str.lower().apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())
        region = unicodedata.normalize('NFKD', region.lower()).encode('ascii', 'ignore').decode()
        df_filtered = df.query(f'REGION == "{region}" and SEMANA == {week}')
        """ df_filtered = df.copy() """
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
    tfv_count = df[df['Asunto'] == 'TFV'].groupby('Asignado').size()
    visitas = df[df['Asunto'] != 'TFV']
    visitas_count = visitas.groupby('Asignado').size()
    planificada_count = visitas[visitas['Estatus de la visita'] == 'Planificada'].groupby('Asignado').size()
    visitas_realizadas = visitas[visitas['Estatus de la visita'] == 'Realizada'].groupby('Asignado').size()
    comments = visitas[(visitas['Comentarios'].str.len() > 3) & (visitas['Resultado'].str.len() > 3)]
    comments_count = comments.groupby('Asignado').size()
    positive_comments_count = comments[(comments['label'] == 'positive') & (comments['score'] > 0.5)].groupby('Asignado').size()
    negative_comments_count = comments[(comments['label'] == 'negative') & (comments['score'] > 0.5)].groupby('Asignado').size()
    duplicated_concatenados_count = comments[comments['Concat'].duplicated()].groupby('Asignado').size()

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

    result = result[['Asignado', 'TFV', '%TFV', 'V', '%V', 'VP','VR','C', '%C', 'C+', 'C-', 'CD', '%CD']]

    return result