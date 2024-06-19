import glob
import pandas as pd
import unicodedata
import numpy as np
from datetime import datetime
from excel_process.filter1 import filter_region_week, count_tfv_visits, global_report_by_region, region_report_by_week, week_report_by_region, comments_analysis_filt

regional_main = ""
week_main = ""
data_filtered_main = pd.DataFrame()

def comments_analysis(region, week, general):
    combined_json = comments_analysis_filt(region, week, general)
    mensaje = "Te mostraré los comentarios mas relevates negativos y los mas positivos:"
    if general:
        mensaje = "Te mostraré los comentarios mas relevates negativos y los mas positivos a nivel general:"
    elif not general and region == '':
        mensaje = "Te mostraré los comentarios mas relevates negativos y los mas positivos de la semana {}:".format(week)
    elif not general and week == 0:
        mensaje = "Te mostraré los comentarios mas relevates negativos y los mas positivos de la región {}:".format(region)
    elif not general and region != '' and week != 0:
        mensaje = "Te mostraré los comentarios mas relevates negativos y los mas positivos de la región {} y la semana {}:".format(region, week)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
        {} """.format(mensaje),
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [combined_json['top_negative_comments'],combined_json['top_positive_comments']],
        "table_title": ["# Top comentarios negativos", "# Top comentarios positivos"],
        "messageEnd": ""
    }
    return body

def comments_analysiss(region, week, general):
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
        Te mostraré los 10 comentarios mas relevates negativos y los 10 mas positivos:""",
        "date": str(current_date),
        "add_type": "",
        "add_data": "Comentarios negativos y positivos",
        "table_title": ["# Top 10 comentarios negativos", "# Top 10 comentarios positivos"],
        "messageEnd": "¿Quieres ver el resumen de los comentarios negativos mas relevantes?"
    }
    return body

def get_general_report():
    result, kw = global_report_by_region()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
            Te mostraré el resumen general: """,
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [result.to_dict(orient="records"), kw.to_dict(orient="records")],
        "table_title": ["# Resumen General", "# Palabras clave y su frecuencia"],
        "table_legend": [' **TFV**: Tiempo fuera de visita.  **%TFV**: Porcentaje de TFV.  **V**: Visitas sin contar las TFV.  **%V**: Porcentaje de visitas sin contar las TFV.  **VP**: Visitas planificadas sin contar las TFV.  **VR**: Visitas realizadas sin contar las TFV.  **C**: Comentarios.  **%C**: Porcentaje de comentarios sobre V.  **C+**: Comentarios positivos con score mayor al 50%.  **C-**: Comentarios negativos con score mayor al 50%.  **CD**: Comentarios duplicados.  **%CD**: Porcentaje de comentarios duplicados sobre C.',""],
        "messageEnd": ''
    }
    return body

def report_by_week(week):
    result, kw = week_report_by_region(week)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
            Te mostraré el resumen de la semana {}: """.format(week),
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [result.to_dict(orient="records"), kw.to_dict(orient="records")],
        "table_title": ["# Resumen General de la semana {}".format(week), "# Palabras clave y su frecuencia"],
        "table_legend": [' **TFV**: Tiempo fuera de visita.  **%TFV**: Porcentaje de TFV.  **V**: Visitas sin contar las TFV.  **%V**: Porcentaje de visitas sin contar las TFV.  **VP**: Visitas planificadas sin contar las TFV.  **VR**: Visitas realizadas sin contar las TFV.  **C**: Comentarios.  **%C**: Porcentaje de comentarios sobre V.  **C+**: Comentarios positivos con score mayor al 50%.  **C-**: Comentarios negativos con score mayor al 50%.  **CD**: Comentarios duplicados.  **%CD**: Porcentaje de comentarios duplicados sobre C.',""],
        "messageEnd": ''
    }
    return body

def report_by_region(region):
    result, kw = region_report_by_week(region)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
            Te mostraré el resumen de la region {}: """.format(region),
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [result.to_dict(orient="records"), kw.to_dict(orient="records")],
        "table_title": ["# Resumen General de la region {}".format(region), "# Palabras clave y su frecuencia"],
        "table_legend": [' **TFV**: Tiempo fuera de visita.  **%TFV**: Porcentaje de TFV.  **V**: Visitas sin contar las TFV.  **%V**: Porcentaje de visitas sin contar las TFV.  **VP**: Visitas planificadas sin contar las TFV.  **VR**: Visitas realizadas sin contar las TFV.  **C**: Comentarios.  **%C**: Porcentaje de comentarios sobre V.  **C+**: Comentarios positivos con score mayor al 50%.  **C-**: Comentarios negativos con score mayor al 50%.  **CD**: Comentarios duplicados.  **%CD**: Porcentaje de comentarios duplicados sobre C.',""],
        "messageEnd": ''
    }
    return body

def report_by_region_and_week(region, week):
    print(f"Este es el reporte de la región {region} y la semana {week}")
    regional_main = region
    week_main = week
    data_filtered_main = filter_region_week(regional_main, week_main)
    result, kw = count_tfv_visits(data_filtered_main)
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
    body = {
        "user": "Bot",
        "message": """
            Te mostraré el resumen de tu consulta para regional {} y semana {}:""".format(regional_main, week_main),
        "date": str(current_date),
        "add_type": "tables",
        "add_data": [result.to_dict(orient="records"), kw.to_dict(orient="records")],
        "table_title": ["# Resumen de la semana {} para el regional {}".format(week_main, regional_main), "# Palabras clave y su frecuencia"],
        "table_legend": [' **TFV**: Tiempo fuera de visita.  **%TFV**: Porcentaje de TFV.  **V**: Visitas sin contar las TFV.  **%V**: Porcentaje de visitas sin contar las TFV.  **VP**: Visitas planificadas sin contar las TFV.  **VR**: Visitas realizadas sin contar las TFV.  **C**: Comentarios.  **%C**: Porcentaje de comentarios sobre V.  **C+**: Comentarios positivos con score mayor al 50%.  **C-**: Comentarios negativos con score mayor al 50%.  **CD**: Comentarios duplicados.  **%CD**: Porcentaje de comentarios duplicados sobre C.',""],
        "messageEnd": ''
    }
    return body