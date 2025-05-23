from flask import Blueprint, request, jsonify
from app.controllers.base.main_controller import MainController
from app.utils.decorators import admin_required, get_jwt_identity
from typing import Any

bp = Blueprint('tickets', __name__, url_prefix='/api')
controller = MainController()

@bp.route('/tickets', methods=['POST'])
def create_ticket() -> tuple[Any, int]:
    try:
        data = request.get_json()

        ticket = controller.tickets.create_ticket(
            user_id=data['user_id'],
            data=data
        )

        return jsonify(ticket.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets', methods=['GET'])
def get_all_tickets() -> tuple[Any, int]:
    try:
        tickets = controller.tickets.get_all()
        return jsonify([ticket.to_dict() for ticket in tickets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/user/<int:user_id>', methods=['GET'])
def get_user_tickets(user_id: int) -> tuple[Any, int]:
    try:
        tickets = controller.tickets.get_user_tickets(user_id)
        return jsonify([ticket.to_dict() for ticket in tickets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id: int) -> tuple[Any, int]:
    try:
        ticket = controller.tickets.get_by_id(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket não encontrado'}), 404
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        ticket = controller.tickets.update(ticket_id, data)
        if not ticket:
            return jsonify({'error': 'Ticket não encontrado'}), 404
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id: int) -> tuple[Any, int]:
    try:
        if controller.tickets.delete(ticket_id):
            return jsonify({'message': 'Ticket deletado com sucesso'}), 200
        return jsonify({'error': 'Ticket não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>/assign', methods=['POST'])
def assign_ticket(ticket_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        ticket = controller.tickets.assign_to_agent(ticket_id, data['agent_id'])
        if not ticket:
            return jsonify({'error': 'Ticket não encontrado'}), 404
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>/close', methods=['POST'])
def close_ticket(ticket_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        ticket = controller.tickets.close_ticket(ticket_id, data.get('resolution'))
        if not ticket:
            return jsonify({'error': 'Ticket não encontrado'}), 404
        return jsonify(ticket.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/status/<status>', methods=['GET'])
def get_tickets_by_status(status: str) -> tuple[Any, int]:
    try:
        tickets = controller.tickets.get_by_status(status)
        return jsonify([ticket.to_dict() for ticket in tickets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/priority/<priority>', methods=['GET'])
def get_tickets_by_priority(priority: str) -> tuple[Any, int]:
    try:
        tickets = controller.tickets.get_by_priority(priority)
        return jsonify([ticket.to_dict() for ticket in tickets]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>/messages', methods=['POST'])
def create_message(ticket_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        message = controller.ticket_messages.create_message(ticket_id, data['user_id'], data['message'])
        return jsonify(message.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/tickets/<int:ticket_id>/messages', methods=['GET'])
def get_messages(ticket_id: int) -> tuple[Any, int]:
    messages = controller.ticket_messages.get_ticket_messages(ticket_id)
    return jsonify([message.to_dict() for message in messages]), 200

@bp.route('/tickets/<int:ticket_id>/update-status', methods=['PATCH'])
def update_ticket_status_and_priority(ticket_id: int) -> tuple[Any, int]:
    try:
        data = request.get_json()
        status = data.get('status')
        priority = data.get('priority')

        if not status and not priority:
            return jsonify({'error': 'É necessário fornecer status e/ou prioridade'}), 400

        ticket = controller.tickets.update_ticket_status_and_priority(
            ticket_id=ticket_id,
            status=status,
            priority=priority
        )

        if not ticket:
            return jsonify({'error': 'Ticket não encontrado'}), 404

        return jsonify(ticket.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400