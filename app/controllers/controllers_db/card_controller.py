from typing import List, Optional
from app.models.card import Card
from app.controllers.base.base_controller import BaseController
from app.services.encryption_service import EncryptionService
from ..base.main_controller import MainController

class CardController(BaseController[Card]):
    def __init__(self, encryption_service: EncryptionService, client: MainController) -> None:
        super().__init__(Card, client)
        self.encryption_service = encryption_service

    def create_card(
        self, 
        user_id: int, 
        card_number: str,
        card_holder_name: str,
        card_expiration_date: str,
        card_cvv: str
    ) -> Card:
        try:
            encrypted_number = self.encryption_service.encrypt(card_number)
            encrypted_cvv = self.encryption_service.encrypt(card_cvv)
            
            card = self.create({
                'user_id': user_id,
                'card_number': encrypted_number,
                'card_holder_name': card_holder_name,
                'card_expiration_date': card_expiration_date,
                'card_cvv': encrypted_cvv
            })
            return card
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_user_cards(self, user_id: int) -> List[Card]:
        return self.get_query().filter_by(user_id=user_id).all()

    def get_card_details(self, card_id: int, user_id: int) -> Optional[dict]:
        card = self.get_query().filter_by(id=card_id, user_id=user_id).first()
        if card:
            return {
                'id': card.id,
                'card_holder_name': card.card_holder_name,
                'card_number': self.encryption_service.decrypt(card.card_number)[-4:],
                'expiration_date': card.card_expiration_date.isoformat()
            }
        return None 