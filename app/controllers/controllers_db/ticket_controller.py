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

    def update_ticket_status_and_priority(self, ticket_id: int, status: Optional[str] = None, priority: Optional[str] = None) -> Optional[Ticket]:
        try:
            ticket = self.get_by_id(ticket_id)
            if not ticket:
                return None

            if status:
                if status not in ['Aberto', 'Em Andamento', 'Resolvido', 'Fechado']:
                    raise ValueError('Status inválido')
                ticket.status = status

            if priority:
                if priority not in ['Baixa', 'Média', 'Alta', 'Urgente']:
                    raise ValueError('Prioridade inválida')
                ticket.priority = priority

            self._db.session.commit()
            return ticket
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

    def assign_to_agent(self, ticket_id: int, agent_id: int) -> Optional[Ticket]:
        try:
            ticket = self.get_by_id(ticket_id)
            if ticket:
                ticket.agent_id = agent_id
                ticket.status = 'Em Andamento'
                self._db.session.commit()
                return ticket
            return None
        except Exception as e:
            self._db.session.rollback()
            raise e

    def close_ticket(self, ticket_id: int, resolution: Optional[str] = None) -> Optional[Ticket]:
        try:
            ticket = self.get_by_id(ticket_id)
            if ticket:
                ticket.status = 'Fechado'
                if resolution:
                    # Criar uma mensagem final com a resolução
                    message = TicketMessage(
                        ticket_id=ticket_id,
                        user_id=ticket.user_id,
                        message=f"Ticket fechado. Resolução: {resolution}"
                    )
                    self._db.session.add(message)
                self._db.session.commit()
                return ticket
            return None
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_by_status(self, status: str) -> List[Ticket]:
        return self.get_query().filter_by(status=status).all()

    def get_by_priority(self, priority: str) -> List[Ticket]:
        return self.get_query().filter_by(priority=priority).all()

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