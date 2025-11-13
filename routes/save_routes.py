from flask import Blueprint, jsonify
from game.game_state import game_state

save_bp = Blueprint('save', __name__)


@save_bp.route('/api/game/save', methods=['POST'])
def save_game():
    game_state.save_game()
    return jsonify({
        'success': True,
        'message': 'Game saved to PostgreSQL!'
    })


@save_bp.route('/api/game/load', methods=['GET'])
def load_game():
    game_state.load_game()
    return jsonify({
        'success': True,
        'message': 'Game loaded from PostgreSQL!'
    })


@save_bp.route('/api/game/new', methods=['POST'])
def new_game():
    game_state.reset_game()
    return jsonify({
        'success': True,
        'message': 'New game started!'
    })
