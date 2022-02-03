
from typing import List, Tuple, Type, cast

from sqlalchemy.orm.query import Query
from ..Data.BaseModel import BaseModel
from sqlalchemy.orm.session import Session

class BaseService:
    def __init__(self, model: Type) -> None:
        self.model = model
    
    def get_all(self, session: Session, paginate = False, page = 1, per_page = 10) -> Tuple[Query, BaseModel]:
        """ Obtiene todos los elementos del modelo de datos especificado

        Args:
            self (class): Class
            session (Session): Database session
            paginate (bool, optional): Flag to paginate results. Defaults to False.
            page (int, optional): Pagenumber to return. Defaults to 1.
            per_page (int, optional): Number of elements per page. Defaults to 10.

        Returns:
            List: Lista de objectos de base de datos
        """
        if paginate is True:
            return cast(BaseModel, self.model).get_paginated(session, page, per_page)
        return cast(BaseModel, self.model).all(session)
    
    def get_one(self, session: Session, id: int):
        """ Search an element by id

        Args:
            self (class): Class
            session (Session): Database session
            id (int): Database identifier

        Returns:
            ORMClass: Devuelve un objeto de la base de datos
        """
        return cast(BaseModel, self.model).find(session, id)
    
    def filter_by_column(self, session: Session, column_name: str, column_value, paginate = False, page = 1, per_page = 10, first: bool = False):
        return cast(BaseModel, self.model).filter_by(session, column_name, column_value, paginate, page, per_page, first)

    def get_by_column(self, session: Session, column_name: str, column_value):
        """ Get an element according with the specified colum name and value

        Args:
            self (class): Class
            session (Session): Database session
            column_name (str): Column name
            value (Any): Value to mach

        Returns:
            ORMClass: First coincidence of the search
        """
        return cast(BaseModel, self.model).get_one(session, column_name, column_value)
    
    def multiple_filters(self, session: Session, filters: List[dict], paginate = False, page = 1, per_page = 10, first: bool = False, search_filters: dict = {}, search_method='AND'):
        return cast(BaseModel, self.model).filters(session, filters, paginate, page, per_page, first, search_filters, search_method)
    
    def count_with_query(self, query: Query) -> int:
        return query.count()
    
    def count_elements(self, session: Session) -> int:
        return cast(BaseModel, self.model).count(session)
    
    def count_filtered(self, session: Session, filters: List[dict]) -> int:
        return cast(BaseModel, self.model).count_with_filters(session, filters)
    
    def insert_register(self, session: Session, input_data: dict):
        obj = self.model(**input_data)
        return cast(BaseModel, obj).save(session)
    
    def update_register(self, session: Session, id: int, update_data: dict):
        obj = self.get_one(session, id)
        return cast(BaseModel, obj).update(session, update_data)
    
    def delete_register(self, session: Session, id: int):
        obj = self.get_one(session, id)
        return cast(BaseModel, obj).delete(session)
    
    def get_rules_for_store(self):
        return cast(BaseModel, self.model).rules_for_store()

    def get_filter_columns(self) -> List[str]:
        return cast(BaseModel, self.model).filter_columns
    
    def get_search_columns(self) -> List[str]:
        return cast(BaseModel, self.model).search_columns

    def get_relationship_names(self) -> List[str]:
        return cast(BaseModel, self.model).relationship_names
