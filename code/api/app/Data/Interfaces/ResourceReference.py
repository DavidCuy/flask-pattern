from typing import Dict, Type
from api.app.Core.Data.BaseModel import BaseModel
import Environment as env

class ResourceReference:
    def __init__(self, model: Type[BaseModel], prefix_model: str = "", sufix_model: str = "", action: str = "GET", api_version = "v1") -> None:
        self.Name = model.__name__
        self.Action = action
        self.Ref = f"{env.APP_URL}/api/{api_version}{prefix_model}/{model.model_path_name}{sufix_model}"
    
    def to_dict(self) -> Dict:
        return {
            "Name": self.Name,
            "Action": self.Action,
            "Ref": self.Ref
        }