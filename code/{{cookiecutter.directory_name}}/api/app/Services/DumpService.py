from api.app.Core.Services.BaseService import BaseService
from api.app.Data.Models.models import Dump


class DumpService(BaseService):
    def __init__(self) -> None:
        super().__init__(Dump)