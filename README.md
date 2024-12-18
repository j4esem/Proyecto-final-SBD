# Projecto Docker + Mongo DB/Atlas + API CityBikes

## Introducción
El objetivo de este proyecto es utilizar los datos de la API CityBikes con diferentes tecnologías. Con un par de scripts, se recoge información, se procesa y se guarda en una base de datos que podrá
ser en local o en cloud (Mongo ATLAS). Además, se utiliza Docker para dockerizar el proceso y así hacer más fácil el despliegue en cualquier dispositivo.

## Estructura del proyecto

/
  - .env: se encuentran variables de entorno para los scripts. En él deberías poner contraseña del cluster, nombre de usuario, nombre de la colección de Mongo...
> [!CAUTION]
> No compartas tus variables de entorno a sitios públicos.
  - LICENSE: este proyecto está bajo una licencia de tipo GNU General Public License v3.0
---

/docker
  - docker-compose.yml: archivo donde se encuentra la configuración de los docker utilizados (mongo y un pequeño contenedor para lanzar un script)
  - dockerfile: archivo para la creación de la imagen de un docker. El objetivo es crear una imagen lo más pequeña posible para que el contenedor
    ejecute un trabajo.
  - requirements.txt: serán las librerías que necesite la imagen a partir de dockerfile.
  - script_I.py: este es el trabajo que ejecutará el contenedor docker 'apibicis'. Es un script para la recogida de datos desde la API, procesamiento de
    sus datos y guardado. Los datos se guardarán en el otro contenedor Mongo.

Con todos estos archivos, el despliegue de los contenedores y sus trabajos es mucho más sencillo, ya que no ahce falta configurar networks, librearias, imágenes... al estar
todo en cada archivo.
