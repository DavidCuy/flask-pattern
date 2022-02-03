from typing import Any, Dict, List
from sqlalchemy import Column, Integer, String
from ...Core.Data.BaseModel import BaseModel
from ...Validators.RequestValidator import DBValidator
from datetime import datetime

class Example(BaseModel):
    """ Table Examples Database model

    Args:
        BaseModel (ORMClass): Parent class

    Returns:
        Person: Instance of model
    """

    __tablename__ = 'Examples'
    id = Column("IdExample", Integer, primary_key=True)
    Description = Column("Description", String, nullable=False)
    
    filter_columns = []
    relationship_names = []
    search_columns = ['Description']
    signed_urls = []
    
    # This model path is used to know which path will raise the event
    model_path_name = "example"
    
    def property_map(self) -> Dict:
        return {
            "id": "IdExample"
        }
    
    def display_members(self) -> List[str]:
        return [
            "id", "Description"
        ]
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        return {
            "Description": ["required", DBValidator("unique", Example, Example.Description), "string"]
        }
