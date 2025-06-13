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
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
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
            db.session.add(new_user)
            db.session.commit()
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
        search_term = f"%{query}%"
        return self.get_query().filter(
            (User.name.ilike(search_term)) |
            (User.email.ilike(search_term))
        ).all()

    def get_users_by_type(self, user_type: str) -> List[User]:
        return self.get_query().filter_by(type=user_type).all()

    def get_user_by_id(self, user_id):
        return self.get_query().get(user_id)

    def delete_user(self, user_id):
        user = self.get_query().get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

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

    def update_user_status(self, user_id: int, status: str) -> Optional[User]:
        if status not in ['ativo', 'bloqueado']:
            raise ValueError("Status inválido. Use 'ativo' ou 'bloqueado'.")

        user = self.get_by_id(user_id)
        if not user:
            return None

        user.status = status
        self._db.session.commit()
        return user

    def update_notification_settings(self, user_id: int, settings: dict) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        if 'notify_new_order' in settings:
            user.notify_new_order = bool(settings['notify_new_order'])
        
        if 'notify_stock_alert' in settings:
            user.notify_stock_alert = bool(settings['notify_stock_alert'])

        self._db.session.commit()
        return user 