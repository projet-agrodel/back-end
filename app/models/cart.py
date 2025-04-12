from app import db
from datetime import datetime
from typing import List, Optional

class Cart(db.Model):
    __tablename__ = 'carrinho'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True)
    
    # Relacionamentos
    user = db.relationship('User', backref='cart')
    items = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class CartItem(db.Model):
    __tablename__ = 'carrinho_item'
    
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinho.id', ondelete='CASCADE'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relacionamento
    product = db.relationship('Product', backref='cart_items')
    
    def to_dict(self) -> dict:
        return {
            'cart_id': self.carrinho_id,
            'product_id': self.produto_id,
            'quantity': self.quantity,
            'product': self.product.to_dict() if self.product else None
        } 