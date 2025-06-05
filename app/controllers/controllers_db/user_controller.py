from typing import Optional, List
from ...models.user import User, UserType
from ..base.base_controller import BaseController
from ...extensions import bcrypt, db
from datetime import datetime
from ..base.main_controller import MainController

class UserController(BaseController[User]):
    def __init__(self, client: MainController) -> None:
        super().__init__(User, client)

    def create_user(self, data: dict) -> User:
        try:
            hashed_password = bcrypt.generate_password_hash(data['password'])
            
            user_type_str = data.get('type', 'user')
            try:
                user_type_enum = UserType[user_type_str]
            except KeyError:
                user_type_enum = UserType.user

            new_user = self.create({
                'name': data['name'],
                'email': data['email'],
                'password': hashed_password,
                'phone': data.get('phone'),
                'type': user_type_enum
            })
            return new_user
        except Exception as e:
            self._db.session.rollback()
            raise e

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_query().filter_by(email=email).first()

    def get_by_reset_token(self, token: str) -> Optional[User]:
        return self.get_query().filter_by(reset_password_token=token).filter(User.reset_password_expiration > datetime.utcnow()).first()

    def update_user(self, user_id: int, data: dict) -> Optional[User]:
        try:
            user = self.get_by_id(user_id)
            if not user:
                return None

            if 'password' in data and data['password']:
                hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                data['password'] = hashed_password
                if 'salt' in data:
                    del data['salt']
            elif 'salt' in data:
                del data['salt']

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

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False # Usuário não encontrado

            if not bcrypt.check_password_hash(user.password, current_password):
                return False # Senha atual incorreta

            hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            
            user.password = hashed_new_password
            self._db.session.commit()
            return True
        except Exception as e:
            self._db.session.rollback()
            # Logar o erro e.g., app.logger.error(f"Erro ao alterar senha: {str(e)}")
            return False 