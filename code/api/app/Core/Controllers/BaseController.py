import json
from typing import cast
from flask import request
import logging
from api.app.Data.Enum.http_status_code import HTTPStatusCode

from api.app.Exceptions.APIException import APIException
from api.app.Validators.RequestValidator import RequestValidator

from ...Data.Interfaces.PaginationResult import PaginationResult
from ..Data.BaseModel import BaseModel
from ..Services.BaseService import BaseService
from ...Midlewares.auth import auth_midleware
from ....database.DBConnection import AlchemyEncoder, AlchemyRelationEncoder, get_session
from ....utils.http_utils import build_response, get_paginate_params, get_filter_params, get_relationship_params, get_search_method_param, get_search_params

SUCCESS_STATUS = 200
UNAUTHORIZED_STATUS = 401
ERROR_STATUS = 400

@auth_midleware
def index(service):
    session = get_session()
    (page, per_page) = get_paginate_params(request)
    relationship_retrieve = get_relationship_params(request)
    filter_query = get_filter_params(request)
    filter_keys = filter_query.keys()

    search_query = get_search_params(request)
    search_keys = cast(BaseService, service).get_search_columns()
    search_columns = list(set(search_keys).intersection(search_query.keys()))
    filters_search = []
    for skey in search_columns:
        filters_search.append({
            'column': getattr(cast(BaseService, service).model, skey),
            'value': search_query[skey]
        })
    
    search_method = 'AND'
    if len(filters_search) > 0:
        search_method = get_search_method_param(request)
    
    model_filter_keys = cast(BaseService, service).get_filter_columns()
    filters_model = set(model_filter_keys).intersection(filter_keys)
    
    filters = []
    for f in filters_model:
        filters.append({f: filter_query[f]})
    
    try:
        query, elements = cast(BaseService, service).multiple_filters(session, filters, True, page, per_page, search_filters=filters_search, search_method=search_method)
        total_elements = cast(BaseService, service).count_with_query(query)
        
        encoder = AlchemyEncoder if 'relationships' not in relationship_retrieve else AlchemyRelationEncoder

        body = PaginationResult(elements, page, per_page, total_elements, refType=cast(BaseService, service).model).to_dict()
        body['Data'] = list(map(lambda d: dict(
                **cast(BaseModel, d).to_dict(jsonEncoder=encoder, encoder_extras=relationship_retrieve)
            ), body['Data'])
        )

        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        body = e.to_dict()
        status_code = e.status_code
    except Exception as e:
        logging.exception("Cannot make the request")
        print(str(e))
        body = dict(message=str(e))
        status_code = HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    
    return build_response(status_code, body, jsonEncoder=encoder, encoder_extras=relationship_retrieve)

@auth_midleware
def find(service, id: int):
    session = get_session()
    relationship_retrieve = get_relationship_params(request)
    try:
        encoder = AlchemyEncoder if 'relationships' not in relationship_retrieve else AlchemyRelationEncoder
        element = cast(BaseService, service).get_one(session, id)
        body = element.to_dict(jsonEncoder=encoder, encoder_extras=relationship_retrieve)
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