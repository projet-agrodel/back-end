from ..controllers_db.user_controller import UserController
from ..controllers_db.product_controller import ProductController
from ..controllers_db.ticket_controller import TicketController, TicketMessageController, TicketAttachmentController
from ..controllers_db.card_controller import CardController
from ..controllers_db.cart_controller import CartController
from ..controllers_db.order_controller import OrderController
from ..controllers_db.payment_controller import PaymentController
from app.services.encryption_service import EncryptionService

class MainController:
    
    def __init__(self) -> None:
        self.encryption_service = EncryptionService()
        self._user_controller = UserController()
        self._product_controller = ProductController()
        self._ticket_controller = TicketController()
        self._ticket_message_controller = TicketMessageController()
        self._card_controller = CardController(self.encryption_service)
        self._cart_controller = CartController()
        self._order_controller = OrderController()
        self._payment_controller = PaymentController()

    @property
    def users(self) -> UserController:
        return self._user_controller

    @property
    def products(self) -> ProductController:
        return self._product_controller

    @property
    def tickets(self) -> TicketController:
        return self._ticket_controller

    @property
    def ticket_messages(self) -> TicketMessageController:
        return self._ticket_message_controller

    @property
    def cards(self) -> CardController:
        return self._card_controller

    @property
    def carts(self) -> CartController:
        return self._cart_controller

    @property
    def orders(self) -> OrderController:
        return self._order_controller

    @property
    def payments(self) -> PaymentController:
        return self._payment_controller
