from functools import wraps
from typing import cast
import requests
from flask import request

from api.app.Exceptions.APIException import APIException
from api.app.Data.Enum.http_status_code import HTTPStatusCode


def auth_midleware(func):
    @wraps(func)
    def decorator_func(*args, **kwargs):
        auth_header = cast(str, request.headers.get('Authorization'))
        if auth_header:
            auth_token = auth_header.split(" ")
            if len(auth_token) < 2:
                raise APIException("Bad token", HTTPStatusCode.UNAUTHORIZED.value)
            auth_token = auth_token[1]
        else:
            auth_token = None

        if auth_token:
            pass

            ## TODO: TBD endpoint to verify if the user is already logged
            url = f"https://postman-echo.com/post"

            headers = {
                "content-type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {auth_token}"
            }
            resp = requests.post(url, headers=headers)
            
            if resp.status_code == 200:
                return func(*args, **kwargs)
            
            if not resp.text:
                raise APIException("Unauthorized", resp.status_code)
            raise APIException(resp.text, resp.status_code, resp.json())
        
        raise APIException("There is no token in headers", HTTPStatusCode.UNAUTHORIZED.value)
    return decorator_func

