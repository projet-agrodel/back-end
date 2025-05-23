from ..extensions import db
from datetime import datetime
from enum import Enum

class UserType(Enum):
    admin = "admin"
    user = "user"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    type = db.Column(db.Enum(UserType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reset_password_token = db.Column(db.String(100), nullable=True, unique=True)
    reset_password_expiration = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "type": self.type.value,
            "created_at": self.created_at.isoformat(), 
            "updated_at": self.updated_at.isoformat(),
        }