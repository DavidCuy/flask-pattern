from __future__ import annotations
import json
from json.encoder import JSONEncoder
from typing import Any, Dict, List, Type, cast
from operator import and_, or_
from sqlalchemy import Column, Integer, orm
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from typing import List

from ....database.DBConnection import db, AlchemyEncoder

class BaseModel(db.Model):
    """ Base model for a child classes implementations

    Args:
        Base (Any): SQLAlchemy declarative base

    Raises:
        e: Exceptions for not implemented functions

    Returns:
        BaseModel: Instace of BaseModel class
    """

    ## Indicate it is an abstract class (not 100% completed y going to be done in child classes)
    __abstract__ = True
    ## Model identifier. All tables from database should have
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_path_name = ""
    
    filter_columns = []
    relationship_names = []
    search_columns = []

    # for this project
    signed_urls = []

    @property
    def attrs(self) -> List[str]:
        """ Returns a list of the attributes of an object

        Returns:
            List[str]: Attributes
        """
        preliminar = list(filter(lambda prop: not str(prop).startswith('_'), type(self).__dict__.keys()))
        display_member = self.display_members()
        return list(set(preliminar) & set(display_member)) if len(display_member) > 0 else display_member

    @classmethod
    def all(cls_, session: Session):
        """ Get all rows from a table

        Args:
            cls_ (cls): Type of class
            session (Session): Database session

        Returns:
            List[Type[BaseModel]]: List of elements mapped from database table
        """
        query = session.query(cls_)
        return query, session.query(cls_).all()
    
    @classmethod
    def get_paginated(cls_, session: Session, page: int = 1, per_page: int = 10):
        page = page - 1
        query = session.query(cls_).order_by(cls_.id.desc()).limit(per_page).offset(page*per_page)
        return query.all()
    
    @classmethod
    def find(cls_, session: Session, id: int):
        """ Search a row by id

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            id (int): Row identifier

        Returns:
            Type[BaseModel]: The row that have a coincidence with the identifier
        """
        if int(id) > 0:
            return session.query(cls_).get(id)
    
    @classmethod
    def filter_by(cls_, session: Session, column_name: str, value, paginated: bool = False, page: int = 1, per_page: int = 10, first = False):
        """ Gets all rows that match with the specified filter

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            List[Type[BaseModel]]: List of elements that match with filter
        """
        filter_dict = {
            column_name: value
        }
        query = session.query(cls_).filter_by(**filter_dict).order_by(cls_.id.desc())

        if first:
            return query, query.first()

        if paginated:
            page = page - 1
            return query, query.limit(per_page).offset(page*per_page).all()
        return query, query.all()
    
    @classmethod
    def get_one(cls_, session: Session, column_name: str, value):
        """ Gets the first row that matches the filter

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            Type[BaseModel]: First register that match with filter
        """
        filter_dict = {
            column_name: value
        }
        return session.query(cls_).filter_by(**filter_dict).first()
    
    @classmethod
    def filters(cls_, session: Session, filters: List[dict], paginated: bool = False, page: int = 1, per_page: int = 10, first: bool = False, search_filters: dict = {}, search_method = 'AND'):
        """ Gets all rows that match with the multiple filters specified in dict (and logic)

        Args:
            cls_ (class): Child class method
            session (Session): Database session

        Returns:
            List[Type[BaseModel]]: List of elements that match with the multiple filters
        """
        query = session.query(cls_)
        
        search_query = None
        first_run = True
        for ksearch in search_filters:
            if first_run:
                search_query = cast(Column, ksearch['column']).ilike(ksearch['value'])
                first_run = False
            else:
                if search_method == 'OR':
                    search_query = or_(search_query, cast(Column, ksearch['column']).ilike(ksearch['value']))
                else:
                    search_query = and_(search_query, cast(Column, ksearch['column']).ilike(ksearch['value']))
        
        if search_query is not None:
            query = query.filter(search_query)

        for filter in filters:
            query = query.filter_by(**filter)
        
        query = query.order_by(cls_.id.desc())

        if first:
            return query, query.first()
        
        if paginated:
            page = page - 1
            return query, query.limit(per_page).offset(page*per_page).all()
        return query, query.all()

    def before_save(self, sesion: Session, *args, **kwargs):
        """ Method to execute before save a row in database (polimorfism)
        """
        pass

    def after_save(self, sesion: Session, *args, **kwargs):
        """ Method to execute after save a row in database (polimorfismo)
        """
        pass
    
    def save(self, session: Session, commit=True, *args, **kwargs):
        """ Save a register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.

        Raises:
            e: In case of error, the register will be erased and raise an Exception
        """
        self.before_save(session, *args, **kwargs)
        session.add(self)
        if commit:
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

        self.after_save(session, *args, **kwargs)
        return self

    def before_update(self, sesion: Session, *args, **kwargs):
        """ Method to execute before update a row in database (polimorfism)
        """
        pass

    def after_update(self, sesion: Session, *args, **kwargs):
        """ Method to execute after update a row in database (polimorfism)
        """
        pass

    def update(self, session: Session, object: dict, *args, **kwargs):
        """ Update a specified register in database

        Args:
            session (Session): Database session
            object (dict): Dictionary with only the field to update
        """
        self.before_update(session, *args, **kwargs, **object)
        keys = self.get_keys()
        for key in keys:
            if key in object:
                self.__setattr__(key, object[key])
                pass

        session.commit()
        self.after_update(session, *args, **kwargs)
        return self
    
    def before_delete(self, sesion: Session, *args, **kwargs):
        """ Method to execute before update a row in database (polimorfism)
        """
        pass

    def after_delete(self, sesion: Session, *args, **kwargs):
        """ Method to execute after update a row in database (polimorfism)
        """
        pass

    def delete(self, session: Session, commit=True, *args, **kwargs):
        """ Delete a specified register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.
        """
        self.before_delete(session, *args, **kwargs)
        session.delete(self)
        if commit:
            session.commit()
        self.after_delete(session, *args, **kwargs)

    @classmethod
    def eager(cls_: Type[BaseModel], session: Session, *args) -> Query:
        """ Execute in one load all joins

        Returns:
            Type[BaseModel]: Database query
        """
        cols = [orm.joinedload(arg) for arg in args]
        return session.query(cls_).options(*cols)
    
    @classmethod
    def count(cls_: Type[BaseModel], session: Session) -> int:
        """ Execute in one load all joins

        Returns:
            Type[BaseModel]: Database query
        """
        return session.query(cls_.id).count()
    
    @classmethod
    def count_with_filters(cls_: Type[BaseModel], session: Session, filters: List[dict]) -> int:
        query = session.query(cls_)

        for filter in filters:
            query = query.filter_by(**filter)
        
        return query.count()
    
    @classmethod
    def get_keys(cls_: Type[BaseModel]) -> List[str]:
        """ Get all attributes of class

        Args:
            cls_ (Type[BaseModel]): Child class method

        Returns:
            List[str]:  Attributes
        """
        return list(filter(lambda prop: not str(prop).startswith('_'), cls_.__dict__.keys()))
    
    @classmethod
    def rules_for_store(cls_) -> Dict[str, List[Any]]:
        """Define a dictionary with the rules for each property defined

        Returns:
            Dict[str, List[Any]]: List of rules for each property
        """
        return {}
    
    def property_map(self) -> Dict[str, str]:
        """Remap property with display value

        Returns:
            Dict[str, str]: Dict of string with key as class property name and value as display
        """
        return {}
    
    @classmethod
    def display_members(cls_) -> List[str]:
        """Get only de properties to display to end user

        Returns:
            List[str]: List of properties
        """
        return []
    
    def to_dict(self, jsonEncoder: JSONEncoder = AlchemyEncoder, circular: bool = True, encoder_extras: dict = {}) -> dict:
        return json.loads(json.dumps(self, cls=jsonEncoder, check_circular=circular, **encoder_extras))


    def __repr__(self) -> str:
        """ Model representation

        Returns:
            str: Model output string formatted
        """
        attr_array = [f"{attr}={self.__getattribute__(attr)}" for attr in self.attrs]
        args_format = ",".join(attr_array)
        return f"<{type(self).__name__}({args_format})>"


