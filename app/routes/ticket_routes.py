from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.base.main_controller import MainController
from typing import Any

bp = Blueprint('tickets', __name__)
controller = MainController()

@bp.route('/tickets', methods=['POST'])

def create_ticket() -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        ticket = controller.tickets.create_ticket(user_id, data)
        return jsonify(ticket.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets', methods=['GET'])

def get_tickets() -> tuple[Any, int]:
    user_id = get_jwt_identity()
    query = request.args.get('query')
    
    if query:
        tickets = controller.tickets.search_tickets(query)
    else:
        tickets = controller.tickets.get_user_tickets(user_id)
    
    return jsonify([ticket.to_dict() for ticket in tickets]), 200

@bp.route('/tickets/<int:ticket_id>', methods=['GET'])

def get_ticket(ticket_id: int) -> tuple[Any, int]:
    ticket = controller.tickets.get_by_id(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket não encontrado'}), 404
    return jsonify(ticket.to_dict()), 200

@bp.route('/tickets/<int:ticket_id>/status', methods=['PATCH'])

def update_ticket_status(ticket_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        status = data.get('status')
        ticket = controller.tickets.update_ticket_status(ticket_id, status)
        if not ticket:
            return jsonify({'error': 'Ticket não encontrado'}), 404
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>/messages', methods=['POST'])

def create_message(ticket_id: int) -> tuple[Any, int]:
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        message = controller.ticket_messages.create_message(ticket_id, user_id, data['message'])
        return jsonify(message.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>/messages', methods=['GET'])

def get_messages(ticket_id: int) -> tuple[Any, int]:
    messages = controller.ticket_messages.get_ticket_messages(ticket_id)
    return jsonify([message.to_dict() for message in messages]), 200