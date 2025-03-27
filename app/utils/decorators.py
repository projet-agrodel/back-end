from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            from app.controllers.controllers_db.user_controller import UserController
            
            current_user = UserController.get_user_by_id(get_jwt_identity())
            if current_user.type != 'admin':
                return jsonify({'error': 'Acesso negado'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper 