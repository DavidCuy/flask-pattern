from api.utils.http_utils import build_response
import json

class APIException(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None) -> None:
        super().__init__(f"[{status_code}] {message}")

        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv