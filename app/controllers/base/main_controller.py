from ..controllers_db.user_controller import UserController
from ..controllers_db.product_controller import ProductController

class MainController:
    
    def __init__(self) -> None:
        self._user_controller: UserController = UserController()
        self._product_controller: ProductController = ProductController()


    @property
    def users(self) -> UserController:
        return self._user_controller

    @property
    def products(self) -> ProductController:
        return self._product_controller
