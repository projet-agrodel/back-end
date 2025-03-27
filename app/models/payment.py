from app import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'pagamento'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id', ondelete='CASCADE'))
    payment_method = db.Column(db.Enum('Cartão', 'PIX'), nullable=False)
    status = db.Column(db.Enum('Aprovado', 'Pendente', 'Rejeitado'), nullable=False)
    amount = db.Column(db.Decimal(10,2), nullable=False)
    transaction_id = db.Column(db.LargeBinary)  # VARBINARY
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 