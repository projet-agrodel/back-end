from typing import TypeVar, Generic, Optional, List, Any
from app import db
from sqlalchemy.orm import Query
from ..base.main_controller import MainController

T = TypeVar('T')

class BaseController(Generic[T]):
    def __init__(self, model: T, client: MainController) -> None:
        self.model = model
        self._db = db
        self.client = client

    def create(self, data: dict) -> T:
        try:
            instance = self.model(**data)
            self._db.session.add(instance)
            self._db.session.commit()
            return instance
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_by_id(self, id: int) -> Optional[T]:
        return self.model.query.get(id)

    def get_all(self) -> List[T]:
        return self.model.query.all()

    def update(self, id: int, data: dict) -> Optional[T]:
        instance = self.get_by_id(id)
        if instance:
            try:
                for key, value in data.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                self._db.session.commit()
                return instance
            except Exception as e:
                self._db.session.rollback()
                raise e
        return None

    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            try:
                self._db.session.delete(instance)
                self._db.session.commit()
                return True
            except Exception as e:
                self._db.session.rollback()
                raise e
        return False

    def get_query(self) -> Query:
        return self.model.query 