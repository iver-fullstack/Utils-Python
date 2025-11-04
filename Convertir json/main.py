import re
import json

def parse_user_data(texto):
    # Extrae el contenido dentro de UserData(...)
    match = re.search(r'UserData\((.*?)\)', texto)
    if not match:
        return {}

    contenido = match.group(1)
    campos = re.split(r', (?=\w+=)', contenido)
    resultado = {}
    for campo in campos:
        if '=' in campo:
            clave, valor = campo.split('=', 1)
            resultado[clave.strip()] = valor.strip()
    return resultado

def convertir_response(texto):
    # Elimina "Response{" y "}"
    contenido = texto.strip().removeprefix("Response{").removesuffix("}")
    partes = re.split(r', (?=\w+=)', contenido)
    resultado = {}
    for parte in partes:
        if '=' in parte:
            clave, valor = parte.split('=', 1)
            resultado[clave.strip()] = valor.strip()
    return resultado

def convertir_linea(texto):
    texto = texto.strip()

    # Caso 1: línea tipo Response{...}
    if texto.startswith("Response{"):
        return convertir_response(texto)

    # Caso 2: línea tipo UserData(...)
    if texto.startswith("UserData("):
        return parse_user_data(texto)

    # Caso 3: línea tipo (status=..., data=[UserData(...)], ...)
    resultado = {}

    # Extraer bloque data=[UserData(...)]
    match_data = re.search(r'data=\[UserData\((.*?)\)\]', texto)
    if match_data:
        resultado["data"] = [parse_user_data(match_data.group(0))]
        texto = texto.replace(match_data.group(0), '').strip(', ()')

    # Extraer el resto de campos
    partes = re.split(r', (?=\w+=)', texto)
    for parte in partes:
        if '=' in parte:
            clave, valor = parte.split('=', 1)
            resultado[clave.strip()] = valor.strip()

    return resultado

def leer_archivo_convertir(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                if not linea.strip():
                    continue
                try:
                    convertido = convertir_linea(linea)
                    print(json.dumps(convertido, indent=4, ensure_ascii=False))
                    print("-" * 40)
                except Exception as e:
                    print(f"❌ Error al convertir línea: {e}")
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta}")

# Ejemplo de uso
leer_archivo_convertir("datos.txt")
