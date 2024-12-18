# Projecto Docker + Mongo DB/Atlas + API CityBikes


# Índice

1. [Introducción](#introducción)  
2. [Estructura del Proyecto](#estructura-del-proyecto)   
3. [Cómo ejecutar los script](#cómo-ejecutar-los-python-scripts-en-tu-dispositivo)  
4. [Cómo ejecutarlo en Docker](#cómo-ejecutar-script_ipy-de-forma-dockerizada)  

## Introducción
El objetivo de este proyecto es utilizar los datos de la API CityBikes con diferentes tecnologías. Con un par de scripts, se recoge información, se procesa y se guarda en una base de datos que podrá
ser en local o en cloud (Mongo ATLAS). Además, se utiliza Docker para dockerizar el proceso y así hacer más fácil el despliegue en cualquier dispositivo.

## Estructura del proyecto

**/**
  - .env: se encuentran variables de entorno para los scripts. En él deberías poner contraseña del cluster, nombre de usuario, nombre de la colección de Mongo...
> [!CAUTION]
> No compartas tus variables de entorno a sitios públicos.
  - LICENSE: este proyecto está bajo una licencia de tipo GNU General Public License v3.0
---

**/ docker**
  - docker-compose.yml: archivo donde se encuentra la configuración de los docker utilizados (mongo y un pequeño contenedor para lanzar un script)
  - dockerfile: archivo para la creación de la imagen de un docker. El objetivo es crear una imagen lo más pequeña posible para que el contenedor
    ejecute un trabajo.
  - requirements.txt: serán las librerías que necesite la imagen a partir de dockerfile.
  - script_I.py: este es el trabajo que ejecutará el contenedor docker 'apibicis'. Es un script para la recogida de datos desde la API, procesamiento de
    sus datos y guardado. Los datos se guardarán en el otro contenedor Mongo.

Con todos estos archivos, el despliegue de los contenedores y sus trabajos es mucho más sencillo, ya que no ahce falta configurar networks, librearias, imágenes... al estar
todo en cada archivo.

---

**/ notebooks**

  En esta carpeta se encuentran a modo de cuaderno Jupyter los scripts que se han hecho. De esta manera, se puede ver un poco más detallado lo que hace cada uno de ellos.
  
---

**/ python_scripts**
  
  En esta carpeta se encuentran los scripts básicos de python:
  
    - script_I.py. Se conecta a la API y a Mongo Atlas y una vez recogidos los datos, los almacena en el cluster de Mongo. Este script está diseñado
      para ejecutarse en bucle hasta que el usuario lo pare.
      
    - script_II.py. Se conecta al cluster de Mongo Atlas y recoge los datos. Depués, exporta los datos procesados (con claves específicas como id, free_bikes, empty_slots...)
      a dos formatos: csv y parquet. La ruta a donde los exporta se puede configurar desde las variables de entorno.

## ¿Cómo ejecutar los python scripts en tu dispositivo?
1. Lo primero que debes tener (sin contar que ya tengas un IDE pre-instalado) será instalar las librerías necesarias para los archivos. Para ello debes
hacer lo siguiente:
```console
conda env create --file apibicis.yml
```

2. En caso de que quieras conecarte a Mongo Atlas con variables de entorno, mira el archivo .env y cambia las variables a tu gusto. Si ya tienes un enlace a Mongo Atlas y no quieres
   utilizar .env, simplemente cámbialo:
   
**Opción 1 con variables de entorno**

.env
```
MONGO_USER=<tu-usuario>
MONGO_PASSWORD=<contraseña-de-cluster>
MONGO_CLUSTER=<nombre-del-cluster>
MONGO_DB=api_data
MONGO_COLLECTION=data_collection
EXPORT_PATH=./exports
```
Script_I.py
```
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
DATABASE_NAME = "api_data"  # Nombre de la base de datos
COLLECTION_NAME = "data_collection"  # Nombre de la colección
```
**Opción 2 con enlace propio**

Script_I.py
```
# Pegas la URL
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.kdeu0.mongodb.net/?retryWrites=true&w=majority&appName={cluster}"
```

3. Por último, simplemente ejecuta los archivos desde los cuadernos Jupyter o desde consola utilizando el siguiente comando:

   ```console
   cd 'python scripts'
   python script_I.py && python script_II.py
   ```

## ¿Cómo ejecutar script_I.py de forma dockerizada?

En principio, el contenedor que ejecutará el trabajo del script está en mi docker hub y, además, a través del docker-compose.yml se configura para que se genere un contenedor desde esa imagen en
docker hub.
Si quieres generar tu propia imagen en tu docker hub deberás ejecutar, en el mismo directorio a dockerfile. esto:
     
       
       docker build -t <nombre-de-usuario-dockerhub>/<nombre-de-imagen>:latest
       docker login
       docker push <nombre-de-usuario-dockerhub>/<nombre-de-imagen>:latest
       
De esta manera, se sube a tu docker hub esa misma imagen.

Lo siguiente será crear las imágenes docker desde docker compose:

```console
docker compose up -d
```

Listo !! 🚀 

Ya tendrías tus dos contenedores corriendo y funcionando. A partir de ahora la máquina 'apibicis' estará continuamente cargando datos en la otra máquina Mongo DB
