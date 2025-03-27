from app import db

class CartItem(db.Model):
    __tablename__ = 'carrinho_item'
    
    carrinho_id = db.Column(db.Integer, db.ForeignKey('carrinho.id', ondelete='CASCADE'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relacionamento
    product = db.relationship('Product', backref='cart_items') 