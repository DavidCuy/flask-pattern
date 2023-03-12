from api.app.Core.Services.BaseService import BaseService
from api.app.Data.Models.models import Example


class ExampleService(BaseService):
    def __init__(self) -> None:
        super().__init__(Example)