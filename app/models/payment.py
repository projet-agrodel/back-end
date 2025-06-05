from app import db
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Payment(db.Model):
    __tablename__ = 'pagamento'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id', ondelete='CASCADE'))
    payment_method = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('Aprovado', 'Pendente', 'Rejeitado', name='payment_status'), default='Pendente', nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    transaction_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'order_id': self.pedido_id,
            'payment_method': self.payment_method,
            'status': self.status,
            'amount': float(self.amount),
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 