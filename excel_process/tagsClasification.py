import re
from unidecode import unidecode

def encontrar_palabras_clave(texto, palabras_clave):
    coincidencias_reales = set()
    texto = unidecode(texto)

    for palabra in palabras_clave:
        palabra = unidecode(palabra)
        # Escapamos cada palabra para que caracteres especiales sean tratados literalmente
        palabra_escapada = re.escape(palabra)
        # Creamos un patrón regex que busca la palabra exacta, ignorando mayúsculas y minúsculas
        patron = r'\b' + palabra_escapada + r'\b'
        regex = re.compile(patron, re.IGNORECASE)
        
        # Buscamos la palabra en el texto. Si hay una coincidencia, añadimos la palabra original a nuestro conjunto
        if regex.search(texto):
            coincidencias_reales.add(palabra)

    # Convertimos el conjunto a una lista y luego a una cadena de texto separada por comas
    return ', '.join(list(coincidencias_reales))