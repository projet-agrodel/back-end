from typing import Optional, List
from app.models.user import User
from app.controllers.base.base_controller import BaseController
from app import bcrypt
from app import db

class UserController(BaseController[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def create_user(self, data: dict) -> User:
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.generate_password_hash(data['password'] + str(salt))
            
            new_user = self.create({
                'name': data['name'],
                'email': data['email'],
                'password': hashed_password,
                'salt': salt,
                'phone': data.get('phone'),
                'type': data.get('type', 'client')
            })
            return new_user
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_query().filter_by(email=email).first()

    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        try:
            user = self.get_by_id(user_id)
            if not user:
                return None

            if 'password' in data:
                salt = bcrypt.gensalt()
                data['password'] = bcrypt.generate_password_hash(data['password'] + str(salt))
                data['salt'] = salt

            return self.update(user_id, data)
        except Exception as e:
            self._db.session.rollback()
            raise e

    def search_users(self, query: str) -> List[User]:
        return self.get_query().filter(
            (User.name.ilike(f'%{query}%')) |
            (User.email.ilike(f'%{query}%'))
        ).all()

    def get_users_by_type(self, user_type: str) -> List[User]:
        return self.get_query().filter_by(type=user_type).all()

    def get_user_by_id(user_id):
        return User.query.get_or_404(user_id)

    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e 