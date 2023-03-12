from flask import Blueprint
from api.app.Controllers.ExampleController import index, find, store, update, delete
from api.app.Services.ExampleService import ExampleService

example_router = Blueprint('example', __name__)
example_service = ExampleService()

example_router.route('/', methods=['GET'], defaults={'service': example_service}) (index)
example_router.route('/', methods=['POST'], defaults={'service': example_service}) (store)
example_router.route('/<id>', methods=['GET'], defaults={'service': example_service}) (find)
example_router.route('/<id>', methods=['PUT'], defaults={'service': example_service}) (update)
example_router.route('/<id>', methods=['DELETE'], defaults={'service': example_service}) (delete)