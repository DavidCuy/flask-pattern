from flask import Blueprint
from api.app.Controllers.DumpController import index, find, store, update, delete
from api.app.Services.DumpService import DumpService

dump_router = Blueprint('dump', __name__)
dump_service = DumpService()

dump_router.route('/', methods=['GET'], defaults={'service': dump_service}) (index)
dump_router.route('/', methods=['POST'], defaults={'service': dump_service}) (store)
dump_router.route('/<id>', methods=['GET'], defaults={'service': dump_service}) (find)
dump_router.route('/<id>', methods=['PUT'], defaults={'service': dump_service}) (update)
dump_router.route('/<id>', methods=['DELETE'], defaults={'service': dump_service}) (delete)