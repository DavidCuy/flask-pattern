# Flask Pattern

Para utilizar este template, se necesitat install el paquetet cookiecutter. Para lograrlo ejecute los siguientes comandos en una terminal:

````shell
pip install virtualenv
````

y

````shell
pip install cookiecutter
````

Cuando el paquete se haya instalado correctamente en tu equipo, ejecute el siguiente comando:

````shell
cookiecutter https://github.com/DavidCuy/flask-pattern --directory code
````

Con esto, tendrá un proyecto básico de flask con ciertos patrones implementados, para finalizar ejecute lo siguiente en la carpeta que se genenre del proyecto
````shell
python -m venv venv
pip install -r requirements.txt
````
### Debugger
Para vscode, se puede revisar la configuración de los debugger (flask y docker) por si se quiere implementar, esto se encuentran [aquí](documentation/vscode_flask_debuger.md)

## Documentacion de API

De igual manera se deja un [template de la API en OpenAPI3](documentation/api/api_gateway.yml), para integrarse facilmente con swagger o postman

