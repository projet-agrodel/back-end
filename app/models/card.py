from app import db
from datetime import datetime

class Card(db.Model):
    __tablename__ = 'cartao'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    card_number = db.Column(db.LargeBinary, nullable=False)  # VARBINARY
    card_holder_name = db.Column(db.String(255), nullable=False)
    card_expiration_date = db.Column(db.Date, nullable=False)
    card_cvv = db.Column(db.LargeBinary, nullable=False)  # VARBINARY
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(datetime.UTC), onupdate=datetime.now(datetime.UTC))
    
    # Relacionamento
    user = db.relationship('User', backref='cards') 