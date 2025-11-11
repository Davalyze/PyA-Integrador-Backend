import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.responses import StreamingResponse
from datetime import datetime, date
from decimal import Decimal
import io
def sql_to_df(query_result):
    """
    Convierte el resultado de una consulta SQL (lista de dicts o tuplas)
    en un DataFrame de pandas.
    
    Args:
        query_result (list[dict] | list[tuple]): Resultado devuelto por una query.

    Returns:
        pd.DataFrame: DataFrame con los datos o DataFrame vacío si no hay resultados.
    """
    if not query_result:
        return pd.DataFrame()  # Evita errores si la consulta no trae datos

    # Si es lista de tuplas (sin claves de columnas)
    if isinstance(query_result[0], tuple):
        raise ValueError(" query_result debe ser una lista de diccionarios con nombres de columnas")

    # Convierte normalmente si es lista de dicts
    return pd.DataFrame(query_result)



def df_to_dict(df):
    """
    Convierte un DataFrame en una lista de diccionarios (records).
    """
    if df is None or df.empty:
        return []
    return df.to_dict(orient="records")


def normalize_text(value: str) -> str:
    if not value:
        return ""
    # Limpia solo caracteres invisibles, pero deja los espacios normales
    return (
        str(value)
        .replace("\r", "")
        .replace("\n", "")
        .replace("\t", "")
        .replace("\xa0", " ")  # espacio no rompible
        .replace("\u200b", "")
        .replace("\x0b", "")
        .strip()
        .upper()
    )


def generar_script_insert_zoft(tabla_destino: str, datos: list):
    """
    Genera un script SQL con sentencias INSERT IGNORE INTO a partir de una lista de diccionarios.

    ✅ Soporta correctamente:
        - Strings con comillas simples.
        - Fechas y datetimes.
        - Números decimales.
        - Valores None (los convierte en NULL).

    Args:
        tabla_destino (str): Nombre de la tabla destino.
        datos (list): Lista de diccionarios, donde cada diccionario representa una fila.

    Returns:
        str: Script SQL con sentencias INSERT generadas.
    """

    if not datos or not isinstance(datos, list):
        return ""

    sql_script = ""

    # Extraer las columnas de la primera fila
    columnas_destino = list(datos[0].keys())
    columnas_str = ", ".join(columnas_destino)

    # Construir cada sentencia INSERT
    for fila in datos:
        valores_formateados = []

        for columna in columnas_destino:
            valor = fila.get(columna)

            if isinstance(valor, str):
                # Escapar comillas simples
                valor_escapado = valor.replace("'", "''")
                valores_formateados.append(f"'{valor_escapado}'")

            elif isinstance(valor, (int, float, Decimal)):
                # Convertir números normalmente
                valores_formateados.append(str(valor))

            elif isinstance(valor, (datetime, date)):
                # Fechas y datetimes formateadas a SQL estándar
                valores_formateados.append(f"'{valor.strftime('%Y-%m-%d %H:%M:%S')}'")

            elif valor is None:
                valores_formateados.append("NULL")

            else:
                # Cualquier otro tipo → convertir a string
                valor_escapado = str(valor).replace("'", "''")
                valores_formateados.append(f"'{valor_escapado}'")

        valores_str = ", ".join(valores_formateados)
        sql_script += f"INSERT IGNORE INTO {tabla_destino} ({columnas_str}) VALUES ({valores_str});\n"

    return sql_script

        