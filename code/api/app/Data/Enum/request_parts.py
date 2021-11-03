from enum import Enum

class RequestPart(Enum):
    """ Part of the request
    """

    BODY = "body"
    PARAM = "param"
    QUERY = "query"
