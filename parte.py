import os
import csv
import json

# Definimos las rutas
base_folder = 'datos'
csv_areas_folder = os.path.join(base_folder, 'csv', 'areas')
csv_catalogos_folder = os.path.join(base_folder, 'csv', 'catalogos')
json_folder = os.path.join(base_folder, 'json')
json_output_path = os.path.join(json_folder, 'revistas.json')

# Diccionario final
revistas = {
    "acta geofisica": {
        "areas": ["CIENCIAS_EXA", "ING"],
        "catalogos": ["JCR", "SCOPUS"]
    },
    "acta geofisica sinica": {
        "areas": ["CIENCIAS_EXA"],
        "catalogos": ["SCOPUS"]
    },
    "acta matematica": {
        "areas": ["MATEMÁTICAS", "CIENCIAS_EXA"],
        "catalogos": ["JCR", "SCOPUS", "LATINDEX"]
    },
    "acta biologica colombiana": {
        "areas": ["BIOLOGÍA", "CIENCIAS_NATURALES"],
        "catalogos": ["SCOPUS", "REDALYC"]
    },
    "acta astronomica": {
        "areas": ["ASTRONOMÍA", "CIENCIAS_EXA"],
        "catalogos": ["JCR", "SCIELO", "SCIMAGO"]
    },
    "acta química iberoamericana": {
        "areas": ["QUÍMICA", "CIENCIAS_EXA"],
        "catalogos": ["LATINDEX", "SCIELO", "SCIMAGO"]
    },
    "acta médica peruana": {
        "areas": ["MEDICINA", "SALUD"],
        "catalogos": ["SCIELO", "LILACS"]
    },
    "acta botánica mexicana": {
        "areas": ["BIOLOGÍA", "BOTÁNICA"],
        "catalogos": ["SCOPUS", "REDALYC", "LATINDEX", "SCIMAGO"]
    },
    "acta neurobiología experimental": {
        "areas": ["NEUROCIENCIA", "BIOLOGÍA", "CIENCIAS_NATURALES"],
        "catalogos": ["JCR", "SCOPUS"]
    },
    "acta oceanográfica del pacífico": {
        "areas": ["OCEANOGRAFÍA", "CIENCIAS_NATURALES"],
        "catalogos": ["LATINDEX", "SCOPUS"]
    },
    "acta paleontológica argentina": {
        "areas": ["PALEONTOLOGÍA", "CIENCIAS_NATURALES"],
        "catalogos": ["SCOPUS", "SCIELO", "SCIMAGO"]
    },
    "acta farmacológica sinica": {
        "areas": ["FARMACOLOGÍA", "CIENCIAS_DE_LA_SALUD"],
        "catalogos": ["JCR", "SCOPUS", "SCIMAGO"]
    },
    "acta informática": {
        "areas": ["CIENCIAS_COMPUTACIONALES", "ING"],
        "catalogos": ["SCOPUS", "LATINDEX"]
    },
    "acta física polaca": {
        "areas": ["FÍSICA", "CIENCIAS_EXA"],
        "catalogos": ["JCR", "SCOPUS", "SCIMAGO"]
    },
    "acta materiales": {
        "areas": ["INGENIERÍA_DE_MATERIALES", "ING"],
        "catalogos": ["JCR", "SCOPUS", "SCIMAGO"]
    }
}


# Función para procesar archivos CSV
def procesar_csv(folder, tipo):
    for archivo in os.listdir(folder):
        if archivo.endswith('.csv'):
            ruta = os.path.join(folder, archivo)
            with open(ruta, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Saltar encabezado si existe
                for row in reader:
                    if len(row) >= 2:
                        revista = row[0].strip().lower()
                        valor = row[1].strip()
                        if revista not in revistas:
                            revistas[revista] = {"areas": [], "catalogos": []}
                        if tipo == "areas":
                            if valor not in revistas[revista]["areas"]:
                                revistas[revista]["areas"].append(valor)
                        elif tipo == "catalogos":
                            if valor not in revistas[revista]["catalogos"]:
                                revistas[revista]["catalogos"].append(valor)

# Procesar áreas
procesar_csv(csv_areas_folder, "areas")

# Procesar catálogos
procesar_csv(csv_catalogos_folder, "catalogos")

# Asegurarnos que el folder json exista
os.makedirs(json_folder, exist_ok=True)

# Guardar el diccionario como JSON
with open(json_output_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(revistas, jsonfile, indent=4, ensure_ascii=False)

# Verificar que puede leerse correctamente
with open(json_output_path, 'r', encoding='utf-8') as f:
    revistas_leidas = json.load(f)
    print("JSON leído correctamente:")
    print(json.dumps(revistas_leidas, indent=4, ensure_ascii=False))
