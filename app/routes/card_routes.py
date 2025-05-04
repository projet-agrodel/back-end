from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any

bp = Blueprint('cards', __name__)
controller = MainController()

@bp.route('/cards', methods=['POST'])
def create_card() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        card = controller.cards.create_card(
            user_id=user_id,
            card_number=data.get('card_number'),
            card_holder_name=data.get('card_holder_name'),
            card_expiration_date=data.get('card_expiration_date'),
            card_cvv=data.get('card_cvv')
        )
        
        return jsonify({'message': 'Cartão adicionado com sucesso', 'id': card.id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cards', methods=['GET'])
def get_user_cards() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        cards = controller.cards.get_user_cards(user_id)
        return jsonify([{
            'id': card.id,
            'card_holder_name': card.card_holder_name,
            'card_number_last_digits': card.card_number[-4:] if card.card_number else '',
            'card_expiration_date': card.card_expiration_date
        } for card in cards]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@bp.route('/cards/<int:card_id>', methods=['GET'])
def get_card_details(card_id: int) -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        card_details = controller.cards.get_card_details(card_id, user_id)
        
        if not card_details:
            return jsonify({'message': 'Cartão não encontrado'}), 404
            
        return jsonify(card_details), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500 