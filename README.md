# Serverless Pattern
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![SQL SERVER](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)


Muchas veces no es complicado iniciar un proyecto de backend, aun cuando tenemos definido algún framework instalado. Por eso en este proyecto de git se muestra una sugerencia para iniciar un proyecto utilizando el framework flask para python con Docker.

Aunque este ejemplo se centra con su integracion en SQL Server, puede migrarse a cualquier otro gestor de base de datos agregando las dependencias correspondientes en el archivo [code/requirements.txt](code/requirements.txt)

## Para correr este proyecto
Nos tenemos que posicionar en la carpeta [code/serverless-service-name](code/serverless-service-name).

De igual forma se debe copiar y modificar las variables declaradas en el en archivo `.env.example` y renombrarlo a `.env`. Estas serán nuestras variables de entorno, donde queremos guardar la información sensible como base de datos, llaves de acceso, etc.

Creamos un ambiente virtual para mejor manejo del proyecto con los comandos:

```
python -m virutalenv venv
```

En caso de no tener el paquete de virutalenv podemos instalarlo en el sistema con el siguiente comando:
```
pip install virtualenv
```

Finalmente ejecutamos el ambiente virutal.

En windows
```
venv\Scripts\activate
```

En mac o linux
```
source venv/bin/activate
```

## Documentacion de API

De igual manera se deja un [template de la API en OpenAPI3](documentation/api/api_gateway.yml), para integrarse facilmente con swagger o postman

