from app import db
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Enum

class Ticket(db.Model):
    __tablename__ = 'ticket'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(Enum('Aberto', 'Em Andamento', 'Resolvido', 'Fechado', name='ticket_status'), default='Aberto')
    priority = db.Column(Enum('Baixa', 'Média', 'Alta', 'Urgente', name='ticket_priority'), default='Média')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='tickets', foreign_keys=[user_id])
    messages = db.relationship('TicketMessage', backref='ticket', cascade='all, delete-orphan')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'messages': [message.to_dict() for message in self.messages]
        }

class TicketMessage(db.Model):
    __tablename__ = 'ticket_message'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref='ticket_messages')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        } 