import json
from typing import cast
from flask import request
import logging
from api.app.Data.Enum.http_status_code import HTTPStatusCode

from api.app.Exceptions.APIException import APIException
from api.app.Validators.RequestValidator import RequestValidator

from ...Data.Interfaces.PaginationResult import PaginationResult
from ..Services.BaseService import BaseService
from ...Midlewares.auth import auth_midleware
from ....database.DBConnection import AlchemyEncoder, get_session
from ....utils.http_utils import build_response, get_paginate_params

SUCCESS_STATUS = 200
UNAUTHORIZED_STATUS = 401
ERROR_STATUS = 400

@auth_midleware
def index(service):
    session = get_session()
    (page, per_page) = get_paginate_params(request)
    
    try:
        elements = cast(BaseService, service).get_all(session, True, page, per_page)
        total_elements = cast(BaseService, service).count_elements(session)
        body = PaginationResult(elements, page, per_page, total_elements).to_dict()
        status_code = 200
    except Exception as e:
        print("Cannot make the request")
        print(e)
        body = dict(message="Cannot make the request")
        status_code = 422
    finally:
        session.close()
    return build_response(status_code, body, jsonEncoder=AlchemyEncoder)

@auth_midleware
def find(service, id: int):
    session = get_session()
    
    try:
        body = cast(BaseService, service).get_one(session, id)
        status_code = 200
    except Exception as e:
        print("Cannot make the request")
        print(e)
        body = dict(message="Cannot make the request")
        status_code = 422
    finally:
        session.close()
    return build_response(status_code, body, jsonEncoder=AlchemyEncoder)

def store(service):
    session = get_session()
    
    RequestValidator(session, cast(BaseService, service).get_rules_for_store()).validate()
    input_params = request.get_json()

    try:
        body = cast(BaseService, service).insert_register(session, input_params)
        response = json.dumps(body, cls=AlchemyEncoder)
        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        response = json.dumps(e.to_dict())
        status_code = e.status_code
    except Exception:
        logging.exception("No se pudo realizar la consulta")
        body = dict(message="No se pudo realizar la consulta")
        response = json.dumps(body)
        status_code=HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    
    return build_response(status_code, response, is_body_str=True)

def update(service, id: int):
    session = get_session()

    input_params = request.get_json()
    try:
        body = cast(BaseService, service).update_register(session, id, input_params)
        response = json.dumps(body, cls=AlchemyEncoder)
        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        response = json.dumps(e.to_dict())
        status_code = e.status_code
    except Exception as e:
        logging.exception("Cannot make the request")
        body = dict(message="Cannot make the request")
        response = json.dumps(body)
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    return build_response(status_code, response, is_body_str=True)

def delete(service, id: int):
    session = get_session()

    try:
        body = cast(BaseService, service).delete_register(session, id)
        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        body = e.to_dict()
        status_code = e.status_code
    except Exception as e:
        logging.exception("Cannot make the request")
        body = dict(message="Cannot make the request")
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    return build_response(status_code, body, jsonEncoder=AlchemyEncoder)