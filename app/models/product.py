from ..extensions import db
from datetime import datetime
from .category import Category

class Product(db.Model):
    __tablename__ = 'produto'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    originalPrice = db.Column(db.Numeric(10,2), nullable=True)
    imageUrl = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default='Ativo', nullable=False)
    isPromotion = db.Column(db.Boolean, default=False, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = db.relationship('Category', back_populates='products')
    
    def to_dict(self):
        category_data = { 'id': self.category.id, 'name': self.category.name } if self.category else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category': category_data,
            'originalPrice': float(self.originalPrice) if self.originalPrice is not None else None,
            'imageUrl': self.imageUrl,
            'status': self.status,
            'isPromotion': self.isPromotion,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 