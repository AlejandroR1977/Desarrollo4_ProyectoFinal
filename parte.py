import os
import pandas as pd
import json

# Definimos las rutas
ruta_base = 'datos/csv'
ruta_areas = os.path.join(ruta_base, 'areas')
ruta_catalogos = os.path.join(ruta_base, 'catalogos')
ruta_json = 'datos/json'

# Diccionario final
revistas = {
  '4or': {'areas': ['CIENCIASECO', 'CIENCIASEXA'], 'catalogos': ['SCOPUS']},
  'abacus': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'academia': {'areas': ['CIENCIASECO', 'CIENCIASSOC'], 'catalogos': ['SCOPUS']},
  'academia-revista latinoamericana de administracion': {'areas': ['CIENCIASECO', 'ING'], 'catalogos': ['JCR']},
  'academic leadership': {'areas': ['CIENCIASECO', 'CIENCIASSOC'], 'catalogos': ['SCOPUS']},
  'academy of accounting and financial studies journal': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'academy of banking studies journal': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'academy of entrepreneurship journal': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'academy of management annals': {'areas': ['CIENCIASECO', 'ING'], 'catalogos': ['JCR', 'SCOPUS']},
  'academy of management journal': {'areas': ['CIENCIASECO', 'ING'], 'catalogos': ['JCR', 'SCOPUS']},
  #...
  'accounting and business research': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'accounting and finance': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'accounting and the public interest': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'accounting education': {'areas': ['CIENCIASECO', 'CIENCIASSOC'], 'catalogos': ['SCOPUS']},
  'accounting forum': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  #...
  'acta oeconomica': {'areas': ['CIENCIASECO'], 'catalogos': ['JCR', 'SCOPUS']},
  'action learning: research and practice': {'areas': ['CIENCIASECO', 'CIENCIASSOC'], 'catalogos': ['SCOPUS']},
  'action research': {'areas': ['CIENCIASECO', 'ING', 'CIENCIASSOC'], 'catalogos': ['JCR', 'SCOPUS']},
  'actual problems of economics': {'areas': ['CIENCIASECO'], 'catalogos': ['JCR', 'SCOPUS']},
  #...
  'african development review-revue africaine de developpement': {'areas': ['CIENCIASECO', 'ING'], 'catalogos': ['JCR']},
  'african finance journal': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']},
  'african journal of economic and management studies': {'areas': ['CIENCIASECO'], 'catalogos': ['SCOPUS']}
}


# Función para procesar los CSV
def procesar_csv(directorio, clave):
    for archivo in os.listdir(directorio):
        if archivo.endswith('.csv'):
            path = os.path.join(directorio, archivo)
            df = pd.read_csv(path, encoding='latin1')
            
            # Asegurar que los nombres de columnas no tengan espacios
            df.columns = df.columns.str.strip().str.lower()
            
            if 'revista' not in df.columns:
                print(f"Advertencia: El archivo {archivo} no tiene columna 'revista'.")
                print(f"Columnas disponibles: {list(df.columns)}")
                continue
            
            for _, fila in df.iterrows():
                revista = fila['revista']
                valor = fila['area'] if clave == 'areas' else fila['catalogo']
                if revista not in revistas:
                    revistas[revista] = {"areas": [], "catalogos": []}
                revistas[revista][clave].append(valor)

# Procesar áreas
procesar_csv(ruta_areas, 'areas')

# Procesar catálogos
procesar_csv(ruta_catalogos, 'catalogos')

# Asegurarnos que el folder json exista
os.makedirs(ruta_json, exist_ok=True)

# Guardar el diccionario como JSON
output_path = os.path.join(ruta_json, 'revistas.json')
with open(output_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(revistas, jsonfile, indent=4, ensure_ascii=False)

# Verificar que puede leerse correctamente
with open(output_path, 'r', encoding='utf-8') as f:
    revistas_leidas = json.load(f)
    print("JSON leído correctamente:")
    print(json.dumps(revistas_leidas, indent=4, ensure_ascii=False))
