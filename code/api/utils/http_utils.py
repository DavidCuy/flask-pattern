import json
import decimal
import datetime
from json.encoder import JSONEncoder
from typing import Tuple
from flask import json, render_template, Response, request
from flask.wrappers import Request

class CustomJSONDecoder(json.JSONEncoder):
    """ Clase que ayuda con el manejo de JSON de un blob Storage de Azure
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        if isinstance(o, bytes):
            return o.decode()
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
        return super(CustomJSONDecoder, self).default(o)

def build_response(status: int, body: dict, application_type: str = 'application/json', jsonEncoder: JSONEncoder = CustomJSONDecoder, circular: bool = True, is_body_str: bool = False) -> Response:
    """ Devuelve el formato que acepta azure para una respuesta de HTTP

    Args:
        status (int): Codido http
        body (dict): Contenido del json de respuesta
        application_type (str, optional): Tipo de respuesta. Defaults to 'application/json'.
        jsonEncoder (JSONEncoder, optional): Codificacion el JSON de salida. Defaults to CustomJSONDecoder.
        circular (bool, optional): Inidica si la codificacion la hara por cada parametro del JSON. Defaults to True.

    Returns:
        func.HttpResponse: Respuesta HTTP aceptada por Azure
    """
    return Response(
        status=status,
        response=body if is_body_str else json.dumps(body, cls=jsonEncoder, check_circular=circular),
        mimetype=application_type
    )

def serialize_json(data: dict, jsonEncoder: JSONEncoder = CustomJSONDecoder, circular: bool = True) -> str:
    """ Devuelve una cadena en formato JSON de un objeto

    Args:
        data (dict): Contenido del json de respuesta
        jsonEncoder (JSONEncoder, optional): Codificacion el JSON de salida. Defaults to CustomJSONDecoder.
        circular (bool, optional): Inidica si la codificacion la hara por cada parametro del JSON. Defaults to True.

    Returns:
        str: Cadena con formato JSON del contenido
    """
    return json.dumps(data, cls=jsonEncoder, check_circular=circular)

def get_paginate_params(req: Request) -> Tuple[bool, int, int]:
    """ Devuelve los parametros de paginacion de una peticion http

    Args:
        req (func.HttpRequest): Peticion http

    Returns:
        Tuple[bool, int, int]: Parametros de paginacion (Paginado, num de pagina, elementos por pagina)
    """

    page = request.args.get('offset')
    if page is not None:
        page = int(page)
    else:
        page = 1

    per_page = request.args.get('limit')
    if per_page is not None:
        per_page = int(per_page)
    else:
        per_page = 100
    
    return (page, per_page)
    