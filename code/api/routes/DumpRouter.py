from flask import Blueprint
from api.app.Controllers.DumpController import index, find, store, update, delete
from api.app.Services.DumpService import DumpService

dump = Blueprint('dump', __name__)
example_service = DumpService()

dump.route('/', methods=['GET'], defaults={'service': example_service}) (index)
dump.route('/', methods=['POST'], defaults={'service': example_service}) (store)
dump.route('/<id>', methods=['GET'], defaults={'service': example_service}) (find)
dump.route('/<id>', methods=['PUT'], defaults={'service': example_service}) (update)
dump.route('/<id>', methods=['DELETE'], defaults={'service': example_service}) (delete)