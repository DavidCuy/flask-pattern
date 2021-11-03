from typing import List
from flask import request

from api.app.Core.Data.BaseModel import BaseModel
from .ResourceReference import ResourceReference

class PaginationResult:
    def __init__(self, data: List[BaseModel], offset: int = 1, limit: int = 1, total: int = 1, prefix_link: str = "/catalogs") -> None:
        if len(data) > 0:
            self.Data = data
            #self.Links = {
            #    "next": ResourceReference(type(data[0]), prefix_model='/catalog').to_dict(),
            #    "current": ResourceReference(type(data[0]), prefix_model='/catalog').to_dict(),
            #    "prev": ResourceReference(type(data[0]), prefix_model='/catalog').to_dict()
            #}
            self.Links = {
                "current": ResourceReference(
                    type(data[0]),
                    prefix_model=prefix_link,
                    sufix_model=f"?offset={offset}&limit={limit}", action=request.method)
                    .to_dict()
            }
            self.Offset = offset
            self.Limit = limit
            self.Total = total

            if (self.Offset * self.Limit) < self.Total:
                self.Links["next"] = ResourceReference(
                    type(data[0]),
                    prefix_model='/catalog',
                    sufix_model=f"?offset={offset+1}&limit={limit}").to_dict()
            if self.Offset > 1:
                self.Links["prev"] = ResourceReference(
                    type(data[0]),
                    prefix_model='/catalog',
                    sufix_model=f"?offset={offset-1}&limit={limit}").to_dict()
        else:
            self.Data = []
            self.Links = None
            self.Offset = 0
            self.Limit = 0
            self.Total = 0
    
    def to_dict(self) -> dict:
        return {
            "Data": self.Data,
            "Links": self.Links,
            "Offset": self.Offset,
            "Limit": self.Limit,
            "Total": self.Total
        }
    