class MainController:
    
    def __init__(self):
        from ..controllers_db.user_controller import UserController
        from ..controllers_db.product_controller import ProductController
        from ..controllers_db.ticket_controller import TicketController, TicketMessageController
        from ..controllers_db.card_controller import CardController
        from ..controllers_db.cart_controller import CartController
        from ..controllers_db.order_controller import OrderController
        from ..controllers_db.payment_controller import PaymentController
        from ..controllers_db.category_controller import CategoryController
        from app.services.encryption_service import EncryptionService

        self.encryption_service = EncryptionService()
        self._user_controller = UserController(self)
        self._product_controller = ProductController(self)
        self._ticket_controller = TicketController(self)
        self._ticket_message_controller = TicketMessageController(self)
        self._card_controller = CardController(self.encryption_service, self)
        self._cart_controller = CartController(self)
        self._order_controller = OrderController(self)
        self._payment_controller = PaymentController(self)
        self._category_controller = CategoryController(self)

    @property
    def users(self):
        return self._user_controller

    @property
    def products(self):
        return self._product_controller

    @property
    def tickets(self):
        return self._ticket_controller

    @property
    def ticket_messages(self):
        return self._ticket_message_controller

    @property
    def cards(self):
        return self._card_controller

    @property
    def carts(self):
        return self._cart_controller

    @property
    def orders(self):
        return self._order_controller

    @property
    def payments(self):
        return self._payment_controller

    @property
    def categories(self):
        return self._category_controller
