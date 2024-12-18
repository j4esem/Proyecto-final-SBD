import time
import requests
import pymongo
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de MongoDB Atlas
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
DATABASE_NAME = "api_data"  # Nombre de la base de datos
COLLECTION_NAME = "data_collection"  # Nombre de la colección

# Escapar el usuario y la contraseña

# Construcción segura de la URI
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.kdeu0.mongodb.net/?retryWrites=true&w=majority&appName={cluster}"

# Configuración de la API
API_URL = "https://api.citybik.es/v2/networks/bicicorunha"  # Ejemplo de API pública (cámbiala por la API deseada)
INTERVAL_SECONDS = 60  # Intervalo entre peticiones (en segundos)

def connect_to_mongodb():
    """
    Conecta a MongoDB Atlas y devuelve la colección de trabajo.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        print("✅ Conexión exitosa a MongoDB Atlas")
        return collection
    except Exception as e:
        print(f"❌ Error al conectar a MongoDB: {e}")
        exit()

def fetch_api_data():
    """
    Realiza una petición GET a la API y devuelve los datos obtenidos.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        print("✅ Datos obtenidos exitosamente de la API")
        return response.json()  # Devuelve la respuesta en formato JSON
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al obtener datos de la API: {e}")
        return None

def store_data_to_mongo(collection, data):
    """
    Almacena los datos en la colección de MongoDB.
    """
    if data:
        try:
            # Almacenar el JSON en MongoDB
            collection.insert_one({"data": data, "timestamp": time.time()})
            print("✅ Datos almacenados correctamente en MongoDB")
        except Exception as e:
            print(f"❌ Error al almacenar los datos en MongoDB: {e}")

def main():
    """
    Bucle principal: obtiene datos de la API y los guarda en MongoDB a intervalos regulares.
    """
    print("🚀 Iniciando el script...")
    collection = connect_to_mongodb()

    try:
        while True:
            # Obtener datos de la API
            data = fetch_api_data()

            # Almacenar los datos en MongoDB
            store_data_to_mongo(collection, data['network']['stations'])

            # Esperar el intervalo definido antes de la próxima iteración
            print(f"⏳ Esperando {INTERVAL_SECONDS} segundos...")
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("🛑 Script detenido por el usuario.")

if __name__ == "__main__":
    main()
