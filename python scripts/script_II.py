import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
from pandas import json_normalize

# Cargar variables del archivo .env
load_dotenv()

# Configuración de MongoDB
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
database_name = os.getenv("MONGO_DB")
collection_name = os.getenv("MONGO_COLLECTION")


# Construcción de la URI segura de MongoDB
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.kdeu0.mongodb.net/?retryWrites=true&w=majority&appName={cluster}"

# Configuración de exportación
EXPORT_PATH = os.getenv("EXPORT_PATH", "./exports")  # Directorio de exportación
os.makedirs(EXPORT_PATH, exist_ok=True)  # Crear la carpeta si no existe


def connect_to_mongodb():
    """
    Conecta a MongoDB Atlas y devuelve la colección.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[database_name]
        collection = db[collection_name]
        print(" Conexión exitosa a MongoDB Atlas")
        return collection
    except Exception as e:
        print(f" Error al conectar a MongoDB: {e}")
        exit()

def fetch_data_from_mongo(collection):
    """
    Lee todos los documentos de la base de datos y devuelve una lista de datos.
    """
    pipeline = [
    {"$unwind": "$data"},
    {"$project": {
        "_id": 0,
        "id": "$data.id",
        "name": "$data.name",
        "timestamp": "$data.timestamp",
        "free_bikes": "$data.free_bikes",
        "empty_slots": "$data.empty_slots",
        "uid": "$data.extra.uid",
        "last_updated": "$data.extra.last_updated",
        "slots": "$data.extra.slots",
        "normal_bikes": "$data.extra.normal_bikes",
        "ebikes": "$data.extra.ebikes"
    }}
    ]
    
    # Ejecuta el pipeline y convierte a lista
    data = list(collection.aggregate(pipeline))
    return data

def export_to_csv(dataframe, path):
    """
    Exporta el DataFrame a formato CSV.
    """
    csv_path = os.path.join(path, "exported_data.csv")
    dataframe.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Datos exportados a CSV: {csv_path}")

def export_to_parquet(dataframe, path):
    """
    Exporta el DataFrame a formato Parquet.
    """
    parquet_path = os.path.join(path, "exported_data.parquet")
    dataframe.to_parquet(parquet_path, index=False, engine="pyarrow")
    print(f"✅ Datos exportados a Parquet: {parquet_path}")

def main():
    """
    Ejecuta el script para leer datos de MongoDB y exportarlos.
    """
    print("🚀 Iniciando la exportación de datos...")
    collection = connect_to_mongodb()

    # Obtener datos de MongoDB
    documents = fetch_data_from_mongo(collection)

    # Convertir los datos a un DataFrame de pandas
    df = pd.DataFrame(documents)

    # # Reemplazar el campo '_id' con su representación en string (para CSV/Parquet)
    # if "_id" in df.columns:
    #     df["_id"] = df["_id"].astype(str)

    print("✅ Datos convertidos a DataFrame de pandas")

    # Exportar a CSV y Parquet
    export_to_csv(df, EXPORT_PATH)
    export_to_parquet(df, EXPORT_PATH)

if __name__ == "__main__":
    main()