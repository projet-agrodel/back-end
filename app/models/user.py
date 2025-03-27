from app import db
from datetime import datetime
from enum import Enum

class UserType(Enum):
    admin = "admin"
    client = "client"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    type = db.Column(db.Enum(UserType), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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