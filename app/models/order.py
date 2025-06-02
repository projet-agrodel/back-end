from enum import Enum
from app import db
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

class OrderStatus(str, Enum):
    EM_PROCESSAMENTO = 'Em Processamento'
    NAO_AUTORIZADO = 'Não autorizado'
    CONCLUIDO = 'Concluido'

class Order(db.Model):
    __tablename__ = 'pedido'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(20))
    status = db.Column(db.String(40), nullable=False, default=OrderStatus.EM_PROCESSAMENTO)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    
    # Relacionamentos
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', cascade='all, delete-orphan')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'description': self.description.decode() if self.description else None,
            'status': self.status,
            'amount': float(self.amount),
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'payments': [payment.to_dict() for payment in self.payments],
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'pedido_item'
    
    order_item_id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id', ondelete='CASCADE'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'))
    product_name = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relacionamento
    product = db.relationship('Product', backref='order_items')
    
    def to_dict(self) -> dict:
        return {
            'id': self.order_item_id,
            'order_id': self.pedido_id,
            'product_id': self.produto_id,
            'product_name': self.product.name if self.product else None,
            'price': float(self.price),
            'quantity': self.quantity,
        } 