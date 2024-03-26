import glob
import pandas as pd
import unicodedata
import numpy as np

def filter_region_week(region, week):
    excel_files = glob.glob(f'input/*.xlsx')
    if excel_files:
        df = pd.read_excel(excel_files[0])
        df['REGION'] = df['REGION'].str.lower().apply(lambda val: unicodedata.normalize('NFKD', val).encode('ascii', 'ignore').decode())
        region = unicodedata.normalize('NFKD', region.lower()).encode('ascii', 'ignore').decode()
        df_filtered = df.query(f'REGION == "{region}" and SEMANA == {week}')
        return df_filtered
    else:
        print(f"No se encontraron archivos de Excel en la carpeta input")
        return pd.DataFrame()

""" def count_tfv_visits(df):
    tfv_count = df[df['Asunto'] == 'TFV'].shape[0]
    not_tfv_count = df[df['Asunto'] != 'TFV'].shape[0]
    result = pd.DataFrame({
        'Asunto': ['TFV', 'Visitas'],
        'Visitas': [tfv_count, not_tfv_count]
    })

    return result """

def count_tfv_visits(df):
    tfv_count = df[df['Asunto'] == 'TFV'].groupby('Asignado').size()
    not_tfv_count = df[df['Asunto'] != 'TFV'].groupby('Asignado').size()
    planificada_count = df[df['Estatus de la visita'] == 'Planificada'].groupby('Asignado').size()
    comments_count = df[(df['Estatus de la visita'] == 'Realizada') & ((df['Comentarios'].notnull()) | (df['Resultado'].notnull()))].groupby('Asignado').size()
    visitas_realizadas = df[df['Estatus de la visita'] == 'Realizada'].groupby('Asignado').size()
    positive_comments_count = df[(df['label'] == 'positive') & (df['score'] > 0.5) & (df['Estatus de la visita'] == 'Realizada')].groupby('Asignado').size()
    negative_comments_count = df[(df['label'] == 'negative') & (df['score'] > 0.5) & (df['Estatus de la visita'] == 'Realizada')].groupby('Asignado').size()
    duplicated_concatenados_count = df[df.duplicated(['Asignado', 'Comentarios', 'Resultado']) & (df['Estatus de la visita'] == 'Realizada') & (df['Comentarios'] != '') & (df['Resultado'] != '') ].groupby('Asignado').size()

    result = pd.DataFrame({
        'TFV': tfv_count,
        'Visitas': not_tfv_count,
        'VP': planificada_count,
        'Coment.': comments_count,
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
    result['%TFV'] = result['TFV'] / (result['TFV'] + result['Visitas'])
    result['%V'] = result['Visitas'] / (result['TFV'] + result['Visitas'])
    result['%VP'] = result['VP'] / (result['TFV'] + result['Visitas'] + result['VP'])
    result['%C'] = result['Coment.'] / result['VR']

    # Reemplazar NaN e inf con 0
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)

    # Convertir a porcentaje y redondear
    result['%TFV'] = (result['%TFV'] * 100).round(0).astype(int).astype(str) + '%'
    result['%V'] = (result['%V'] * 100).round(0).astype(int).astype(str) + '%'
    result['%VP'] = (result['%VP'] * 100).round(0).astype(int).astype(str) + '%'
    result['%C'] = (result['%C'] * 100).round(0).astype(int).astype(str) + '%'

    result = result[['Asignado', 'TFV', '%TFV', 'Visitas', '%V', 'VP', '%VP','VR','Coment.', '%C', 'C+', 'C-', 'CD']]

    return result