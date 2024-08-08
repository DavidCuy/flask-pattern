import json
import decimal
import datetime
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.session import Session as ORMSession
import Environment as env
from ..config.database import config
from isiflask_core.database.DBConnection import connect_to_main_app

## Database connection string
connect_url = config[env.DB_DRIVER]['conn_string']
db: SQLAlchemy = SQLAlchemy()
connect_to_main_app({"db": db})


def get_session() -> ORMSession:
    """ Return a new database session from engine to data access

    Returns:
        ORMSession: Database session
    """
    return db.session

def get_engine() -> Engine:
    """ Return the database engine

    Returns:
        Engine: Database Engines
    """
    return db.engine


class AlchemyEncoder(json.JSONEncoder):
    """ Based on: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json/41204271 """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            prop_map_obj = obj.__class__.property_map()
            for field in [x for x in obj.attrs]:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
                        data = data.isoformat()
                    else:
                        json.dumps(data)
                    fields[prop_map_obj[field] if field in prop_map_obj else field] = data
                except TypeError:
                    fields[field] = None
            return fields
        if isinstance(obj, decimal.Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class AlchemyRelationEncoder(json.JSONEncoder):
    def __init__(self, relationships: List[str], **kwargs) -> None:
        super().__init__(**kwargs)
        self.relationships = relationships
        
    """ Based on: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json/41204271 """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            prop_map_obj = obj.__class__.property_map()
            
            relation_names = [attr for attr, relation in obj.__mapper__.relationships.items()]
            filters_model = list(set(self.relationships).intersection(relation_names))
            attributes = [x for x in obj.attrs]
            
            if type(filters_model) is list:
                attributes.extend(filters_model)
            
            for field in attributes:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
                        data = data.isoformat()
                    else:
                        json.dumps(data, cls=self.__class__, check_circular=self.check_circular, relationships=self.relationships)
                    fields[prop_map_obj[field] if field in prop_map_obj else field] = data
                except TypeError as e:
                    fields[field] = None
            return fields
        if isinstance(obj, decimal.Decimal):
            if obj % 1 > 0:
                return float(obj)
            else:
                return int(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

