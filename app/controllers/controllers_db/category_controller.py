from typing import List, Optional
from app.models.category import Category
from app.controllers.base.base_controller import BaseController

class CategoryController(BaseController[Category]):
    def __init__(self) -> None:
        super().__init__(Category)

    def create_category(self, name: str) -> Category:
        try:
            category = self.create({'name': name})
            return category
        except Exception as e:
            self._db.session.rollback()
            raise e

    def search_by_name(self, name: str) -> List[Category]:
        return self.get_query().filter(Category.name.ilike(f'%{name}%')).all()

    def get_by_name(self, name: str) -> Optional[Category]:
        return self.get_query().filter_by(name=name).first() 