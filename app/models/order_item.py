from app import db

class OrderItem(db.Model):
    __tablename__ = 'pedido_item'
    
    order_item_id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id', ondelete='CASCADE'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relacionamentos
    product = db.relationship('Product', backref='order_items') 