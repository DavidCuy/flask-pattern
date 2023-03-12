# Flask Pattern

For use this template you need to instatll cookiecutter package. To achieve this, execute the following commands in a terminal:

````shell
pip install virtualenv
````

and

````shell
pip install cookiecutter
````

When the package already installed in your system, execute the following command:

````shell
cookiecutter https://github.com/DavidCuy/flask-pattern --directory code
````


With this you'll have a basic project and for finish run the next inside the project:
````shell
python -m venv venv
pip install -r requirements.txt
````
### Debugger
Para vscode, se puede revisar la configuración de los debugger (flask y docker) por si se quiere implementar, esto se encuentran [aquí](documentation/vscode_flask_debuger.md)

## Documentacion de API

De igual manera se deja un [template de la API en OpenAPI3](documentation/api/api_gateway.yml), para integrarse facilmente con swagger o postman

