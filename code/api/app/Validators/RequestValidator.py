import re
import logging
from typing import Any, Match, Type, cast
from sqlalchemy.orm.session import Session
from flask import request
from sqlalchemy.sql.elements import literal
from sqlalchemy.sql.schema import Column

from ..Exceptions.APIException import APIException
from ..Data.Enum.request_parts import RequestPart

class DBValidator:
    def __init__(self, type: str, table: Type, column: Column[int]) -> None:
        self.type = type
        self.table = table
        self.column = column
        pass

class RequestValidator():
    """ Validador de peticiones HTTP entrantes
    """

    request = None
    rules = None
    req_part = None
    is_valid = True
    errors = None
    error_code = 422
    session = None

    def __init__(self, session: Session, rules: dict, req_part: str = 'body',):
        self.rules = rules
        self.req_part = req_part
        self.session = session

    def validate(self) -> bool:
        request_parts = [req.value for req in RequestPart]
        if self.rules is None:
            self.is_valid = True
            raise APIException("Validation not pass", status_code=self.error_code, payload=self.errors)
        if not self.req_part in request_parts:
            self.is_valid = False
            self.errors = {"error": f"The section is not in Request Part. [{str(', ').join(request_parts)}]", "field":"req_part"}
            self.error_code = 500
            raise APIException("Validation not pass", status_code=self.error_code, payload=self.errors)
        "Validate all the rules defined with the request"
        try:
            if self.req_part == RequestPart.BODY.value:
                self.request = request.get_json()
            if self.req_part == RequestPart.PARAM.value:
                self.request = request.view_args
            if self.req_part == RequestPart.QUERY.value:
                self.request = request.args
        except ValueError:
            self.is_valid = False
            self.errors = {"error": "Can't proccess the request", "field": self.req_part}
            self.error_code = 422
            raise APIException("Can't proccess the request", status_code=self.error_code, payload=self.errors)

        self.is_valid = True
        for field in self.rules:
            is_none = False
            request_value = self.request.get(field)
            rule_params = self.rules.get(field)
            for rule_param in rule_params:
                if rule_param == 'nullable' and request_value is None:
                    is_none = True
                    break
                if rule_param == 'required' and not field in self.request:
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} is required", "field":field}
                    break
                elif (not is_none) and rule_param == 'string' and not isinstance(request_value, str):
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be text", "field":field}
                    break
                elif (not is_none) and rule_param == 'boolean' and not isinstance(request_value, bool):
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be true/false", "field":field}
                    break
                elif (not is_none) and rule_param == 'numeric' and not isinstance(request_value, (int, float)) and not request_value.isdigit():
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be a number", "field":field}
                    break
                elif (not is_none) and rule_param == 'email' and not self.is_mail(request_value):
                    self.is_valid = False
                    self.errors = {"error": f"The field {field} should be a valid email", "field":field}
                    break
                elif (not is_none) and isinstance(rule_param, DBValidator) and rule_param.type =='exists':
                    if rule_param.table is None or rule_param.column is None:
                        self.is_valid = False
                        self.errors = {"error": "Validator format error", "field":field}
                        self.error_code = 500
                        break
                    if not self.exists(rule_param, request_value):
                        self.is_valid = False
                        self.errors = {"error": f"The value {request_value} doesn't exits in the column {rule_param.column} of the table {rule_param.table}", "field":field}
                        self.error_code = 422
                        break
                elif (not is_none) and isinstance(rule_param, DBValidator) and rule_param.type == 'unique':
                    if rule_param.table is None or rule_param.column is None:
                        self.is_valid = False
                        self.errors = {"error": "Validator format error", "field":field}
                        self.error_code = 500
                        break
                    if self.exists(rule_param, request_value):
                        self.is_valid = False
                        self.errors = {"error": f"The {request_value} already exists in {rule_param.column} of the table {rule_param.table}", "field":field}
                        self.error_code = 422
                        break
            if not self.is_valid:
                break

        if not self.is_valid:
            raise APIException("Can't proccess the request", status_code=self.error_code, payload=self.errors)
        
        return True

    def is_mail(self, text: str) -> Match or None:
        """ Verify if the input string has a email format

        Args:
            text (str): Email string

        Returns:
            Match or None: Indicates if there is a match according with email regex
        """
        email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        return re.search(email_regex, text)
    
    def exists(self, database_params: DBValidator, value: Any) -> bool:
        """ Define if a field exists in database

        Args:
            database_params (dict): Evaluated parameter
            value (Any): Value to verify

        Returns:
            bool: indicate if the value exists
        """
        return self.session.query(literal(True)).filter(database_params.column == value).first() is not None
    