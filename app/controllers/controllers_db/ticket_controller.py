from typing import List, Optional, Dict
from app.models.ticket import Ticket, TicketMessage
from app.controllers.base.base_controller import BaseController
from app import db
import os
from werkzeug.utils import secure_filename

class TicketController(BaseController[Ticket]):
    def __init__(self) -> None:
        super().__init__(Ticket)

    def create_ticket(self, user_id: int, data: Dict) -> Ticket:
        try:
            ticket = self.create({
                'user_id': user_id,
                'title': data.get('title'),
                'description': data.get('description'),
                'priority': data.get('priority', 'Média')
            })
            return ticket
        except Exception as e:
            self._db.session.rollback()
            raise e

    def update_ticket_status(self, ticket_id: int, status: str) -> Optional[Ticket]:
        try:
            ticket = self.get_by_id(ticket_id)
            if ticket:
                ticket.status = status
                self._db.session.commit()
                return ticket
            return None
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_user_tickets(self, user_id: int) -> List[Ticket]:
        return self.get_query().filter_by(user_id=user_id).all()

    def search_tickets(self, query: str) -> List[Ticket]:
        return self.get_query().filter(
            (Ticket.title.ilike(f'%{query}%')) |
            (Ticket.description.ilike(f'%{query}%'))
        ).all()

class TicketMessageController(BaseController[TicketMessage]):
    def __init__(self) -> None:
        super().__init__(TicketMessage)

    def create_message(self, ticket_id: int, user_id: int, message: str) -> TicketMessage:
        try:
            message = self.create({
                'ticket_id': ticket_id,
                'user_id': user_id,
                'message': message
            })
            return message
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_ticket_messages(self, ticket_id: int) -> List[TicketMessage]:
        return self.get_query().filter_by(ticket_id=ticket_id).all()