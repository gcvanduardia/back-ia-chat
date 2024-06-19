import glob
import pandas as pd
import unicodedata
import numpy as np
import re 

def comments_analysis_filt(region, week, general):
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
    if not excel_files:
        print("No se encontraron archivos de Excel en la carpeta input_pos_ia")
        return pd.DataFrame()
    df = pd.read_excel(excel_files[0])
    df['Comentarios'] = df['Comentarios'].apply(normalize_comment)
    df['Resultado'] = df['Resultado'].apply(normalize_comment)
    df['Concat'] = df['Comentarios'] + ' ' + df['Resultado']
    
    if not general and region == '':
        df = df[df['SEMANA'] == week]
    elif not general and week == 0:
        df = df[df['REGION'] == region]
    elif not general and region != '' and week != 0:
        df = df[(df['REGION'] == region) & (df['SEMANA'] == week)]
    comments = df[['REGION','SEMANA','Concatenado', 'label', 'score']]
    top_positive_comments, top_negative_comments = filter_top_comments(comments)
    combined_json = create_json(comments, top_positive_comments, top_negative_comments)
    return combined_json

def filter_top_comments(comments):
    comments = comments.drop_duplicates(subset=['Concatenado'])
    positive_comments = comments[comments['label'] == 'positive']
    negative_comments = comments[comments['label'] == 'negative']
    top_positive_comments = positive_comments.sort_values(by='score', ascending=False)[['REGION','SEMANA','Concatenado', 'label', 'score']].head(5)
    top_negative_comments = negative_comments.sort_values(by='score', ascending=False)[['REGION','SEMANA','Concatenado', 'label', 'score']].head(5)
    top_positive_comments['score'] = (top_positive_comments['score'] * 100).round().astype(int).astype(str) + '%'
    top_negative_comments['score'] = (top_negative_comments['score'] * 100).round().astype(int).astype(str) + '%'
    top_positive_comments = top_positive_comments.rename(columns={'Concatenado': 'Comentario'})
    top_negative_comments = top_negative_comments.rename(columns={'Concatenado': 'Comentario'})
    return top_positive_comments, top_negative_comments

def create_json(comments, top_positive_comments, top_negative_comments):
    comments_list = comments.to_dict(orient='records')
    top_positive_comments = top_positive_comments.rename(columns={'Comentario': 'Comentario'})
    top_positive_comments_list = top_positive_comments.to_dict(orient='records')
    top_negative_comments = top_negative_comments.rename(columns={'Comentario': 'Comentario'})
    top_negative_comments_list = top_negative_comments.to_dict(orient='records')
    combined_json = {
        'top_positive_comments': top_positive_comments_list,
        'top_negative_comments': top_negative_comments_list
    }
    return combined_json

def week_report_by_region(week):
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
    if not excel_files:
        print("No se encontraron archivos de Excel en la carpeta input_pos_ia")
        return pd.DataFrame()
    df = pd.read_excel(excel_files[0])
    df['Comentarios'] = df['Comentarios'].apply(normalize_comment)
    df['Resultado'] = df['Resultado'].apply(normalize_comment)
    df['Concat'] = df['Comentarios'] + ' ' + df['Resultado']
    df = df[df['SEMANA'] == week]  # filter by week
    tfv_count = df[df['Asunto'] == 'TFV'].groupby('REGION').size()
    visitas = df[df['Asunto'] != 'TFV']
    visitas_count = visitas.groupby('REGION').size()
    planificada_count = visitas[visitas['Estatus de la visita'] == 'Planificada'].groupby('REGION').size()
    visitas_realizadas = visitas[visitas['Estatus de la visita'] == 'Realizada'].groupby('REGION').size()
    comments = visitas[(visitas['Comentarios'].str.len() > 3) & (visitas['Resultado'].str.len() > 3)]
    comments_count = comments.groupby('REGION').size()
    positive_comments_count = comments[(comments['label'] == 'positive') & (comments['score'] > 0.5)].groupby('REGION').size()
    negative_comments_count = comments[(comments['label'] == 'negative') & (comments['score'] > 0.5)].groupby('REGION').size()
    duplicated_concatenados_count = comments[comments['Concat'].duplicated()].groupby('REGION').size()
    result = pd.DataFrame({
        'TFV': tfv_count,
        'V': visitas_count,
        'VP': planificada_count,
        'VR': visitas_realizadas,
        'C': comments_count,
        'C+': positive_comments_count,
        'C-': negative_comments_count,
        'CD': duplicated_concatenados_count
    })
    result = result.reset_index()
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)
    result['%TFV'] = result['TFV'] / (result['TFV'] + result['V'])
    result['%V'] = result['V'] / (result['TFV'] + result['V'])
    result['%C'] = result['C'] / (result['V'])
    result['%CD'] = result['CD'] / (result['C'])
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)
    result['%TFV'] = (result['%TFV'] * 100).round(0).astype(int).astype(str) + '%'
    result['%V'] = (result['%V'] * 100).round(0).astype(int).astype(str) + '%'
    result['%C'] = (result['%C'] * 100).round(0).astype(int).astype(str) + '%'
    result['%CD'] = (result['%CD'] * 100).round(0).astype(int).astype(str) + '%'
    result = result[['REGION', 'TFV', '%TFV', 'V', '%V', 'VP', 'VR', 'C', '%C', 'C+', 'C-', 'CD', '%CD']]
    result = result.sort_values(['REGION', 'C-'], ascending=[True, False])
    kw = palabras_clave_mas_repetidas(df)
    return [result, kw]

def region_report_by_week(region):
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
    if not excel_files:
        print("No se encontraron archivos de Excel en la carpeta input_pos_ia")
        return pd.DataFrame()
    df = pd.read_excel(excel_files[0])
    df['Comentarios'] = df['Comentarios'].apply(normalize_comment)
    df['Resultado'] = df['Resultado'].apply(normalize_comment)
    df['Concat'] = df['Comentarios'] + ' ' + df['Resultado']
    df = df[df['REGION'] == region]  # filter by region
    tfv_count = df[df['Asunto'] == 'TFV'].groupby('SEMANA').size()
    visitas = df[df['Asunto'] != 'TFV']
    visitas_count = visitas.groupby('SEMANA').size()
    planificada_count = visitas[visitas['Estatus de la visita'] == 'Planificada'].groupby('SEMANA').size()
    visitas_realizadas = visitas[visitas['Estatus de la visita'] == 'Realizada'].groupby('SEMANA').size()
    comments = visitas[(visitas['Comentarios'].str.len() > 3) & (visitas['Resultado'].str.len() > 3)]
    comments_count = comments.groupby('SEMANA').size()
    positive_comments_count = comments[(comments['label'] == 'positive') & (comments['score'] > 0.5)].groupby('SEMANA').size()
    negative_comments_count = comments[(comments['label'] == 'negative') & (comments['score'] > 0.5)].groupby('SEMANA').size()
    duplicated_concatenados_count = comments[comments['Concat'].duplicated()].groupby('SEMANA').size()
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
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)
    result['%TFV'] = result['TFV'] / (result['TFV'] + result['V'])
    result['%V'] = result['V'] / (result['TFV'] + result['V'])
    result['%C'] = result['C'] / (result['V'])
    result['%CD'] = result['CD'] / (result['C'])
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)
    result['%TFV'] = (result['%TFV'] * 100).round(0).astype(int).astype(str) + '%'
    result['%V'] = (result['%V'] * 100).round(0).astype(int).astype(str) + '%'
    result['%C'] = (result['%C'] * 100).round(0).astype(int).astype(str) + '%'
    result['%CD'] = (result['%CD'] * 100).round(0).astype(int).astype(str) + '%'
    result = result[['SEMANA', 'TFV', '%TFV', 'V', '%V', 'VP', 'VR', 'C', '%C', 'C+', 'C-', 'CD', '%CD']]
    result = result.sort_values(['SEMANA', 'C-'], ascending=[True, False])
    kw = palabras_clave_mas_repetidas(df)
    return [result, kw]

def global_report_by_region():
    excel_files = glob.glob(f'input_pos_ia/*.xlsx')
    if not excel_files:
        print("No se encontraron archivos de Excel en la carpeta input_pos_ia")
        return pd.DataFrame()

    df = pd.read_excel(excel_files[0])
    df['Comentarios'] = df['Comentarios'].apply(normalize_comment)
    df['Resultado'] = df['Resultado'].apply(normalize_comment)
    df['Concat'] = df['Comentarios'] + ' ' + df['Resultado']

    tfv_count = df[df['Asunto'] == 'TFV'].groupby('REGION').size()
    visitas = df[df['Asunto'] != 'TFV']
    visitas_count = visitas.groupby('REGION').size()
    planificada_count = visitas[visitas['Estatus de la visita'] == 'Planificada'].groupby('REGION').size()
    visitas_realizadas = visitas[visitas['Estatus de la visita'] == 'Realizada'].groupby('REGION').size()
    comments = visitas[(visitas['Comentarios'].str.len() > 3) & (visitas['Resultado'].str.len() > 3)]
    comments_count = comments.groupby('REGION').size()
    positive_comments_count = comments[(comments['label'] == 'positive') & (comments['score'] > 0.5)].groupby('REGION').size()
    negative_comments_count = comments[(comments['label'] == 'negative') & (comments['score'] > 0.5)].groupby('REGION').size()
    duplicated_concatenados_count = comments[comments['Concat'].duplicated()].groupby('REGION').size()

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
    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)

    result['%TFV'] = result['TFV'] / (result['TFV'] + result['V'])
    result['%V'] = result['V'] / (result['TFV'] + result['V'])
    result['%C'] = result['C'] / (result['V'])
    result['%CD'] = result['CD'] / (result['C'])

    result = result.replace([np.inf, -np.inf], np.nan)
    result = result.fillna(0)

    result['%TFV'] = (result['%TFV'] * 100).round(0).astype(int).astype(str) + '%'
    result['%V'] = (result['%V'] * 100).round(0).astype(int).astype(str) + '%'
    result['%C'] = (result['%C'] * 100).round(0).astype(int).astype(str) + '%'
    result['%CD'] = (result['%CD'] * 100).round(0).astype(int).astype(str) + '%'

    result = result[['REGION', 'TFV', '%TFV', 'V', '%V', 'VP', 'VR', 'C', '%C', 'C+', 'C-', 'CD', '%CD']]
    result = result.sort_values(['REGION', 'C-'], ascending=[True, False])

    kw = palabras_clave_mas_repetidas(df)

    return [result, kw]

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