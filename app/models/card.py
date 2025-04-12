from app import db
from datetime import datetime
from typing import Optional

class Card(db.Model):
    __tablename__ = 'cartao'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    card_number = db.Column(db.LargeBinary, nullable=False)
    card_holder_name = db.Column(db.String(255), nullable=False)
    card_expiration_date = db.Column(db.Date, nullable=False)
    card_cvv = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento
    user = db.relationship('User', backref='cards')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'card_holder_name': self.card_holder_name,
            'card_expiration_date': self.card_expiration_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 