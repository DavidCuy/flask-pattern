from flask import Blueprint
from api.app.Controllers.ExampleController import index, find, store, update, delete
from api.app.Services.ExampleService import ExampleService

example = Blueprint('example', __name__)
example_service = ExampleService()

example.route('/', methods=['GET'], defaults={'service': example_service}) (index)
example.route('/', methods=['POST'], defaults={'service': example_service}) (store)
example.route('/<id>', methods=['GET'], defaults={'service': example_service}) (find)
example.route('/<id>', methods=['PUT'], defaults={'service': example_service}) (update)
example.route('/<id>', methods=['DELETE'], defaults={'service': example_service}) (delete)