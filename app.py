from flask import Flask, render_template, jsonify, Response
from game.game_state import game_state
import random

app = Flask(__name__)


@app.route('/')
def hello_word():
    return render_template('index.html')


@app.route('/api/game/reset', methods=['POST'])
def reset_game() -> Response:
    game_state.reset_game()
    return jsonify({
        'success': True,
        'message': 'Game reset successfully'
    })


@app.route('/api/player/stats')
def get_player_stats() -> Response:
    return jsonify({
        'player_name': game_state.player.player_name,
        'player_blood': game_state.player.player_blood,
        'player_kills': game_state.player.player_kills,
        'player_damage': game_state.player.player_damage,
        'player_health': game_state.player.player_health,
        'player_max_health': game_state.player.player_max_health,
        'player_is_alive': game_state.player.player_is_alive
    })


@app.route('/api/game/state')
def get_game_state():
    wave_info = game_state.check_wave_progress()
    wave_info.pop('wave_changed', None)
    return jsonify(wave_info)


@app.route('/api/enemies')
def get_enemies() -> Response:
    enemies_data = []
    for i, enemy in enumerate(game_state.current_enemies):
        enemies_data.append({
            'enemy_id': i,
            'enemy_name': enemy.name,
            'enemy_health': enemy.health,
            'enemy_max_health': enemy.max_health,
            'enemy_damage': enemy.damage,
            'enemy_is_alive': enemy.health > 0
        })
    return jsonify(enemies_data)


@app.route('/api/attack/random', methods=['POST'])
def attack_random() -> Response:

    alive_enemies = game_state.get_alive_enemies()

    if not alive_enemies:
        return jsonify({'error': 'All enemies is dead!'})

    enemy = random.choice(alive_enemies)
    result = game_state.perform_attack(enemy)

    return jsonify(result)


@app.route('/api/attack/<int:enemy_id>', methods=['POST'])
def attack_specific_enemy(enemy_id) -> Response:

    if enemy_id < 0 or enemy_id >= len(game_state.current_enemies):
        return jsonify({'error': 'Invalid enemy ID'})

    enemy = game_state.current_enemies[enemy_id]
    result = game_state.perform_attack(enemy, enemy_id)

    return jsonify(result)


@app.route('/api/upgrade/damage', methods=['POST'])
def upgrade_damage() -> Response:
    cost = 2
    upgrade_type = 'upgrade_damage'
    result = game_state.buy_upgrade(upgrade_type, cost)

    return jsonify(result)


@app.route('/api/upgrade/health', methods=['POST'])
def upgrade_health() -> Response:

    cost = 2
    upgrade_type = 'upgrade_health'
    result = game_state.buy_upgrade(upgrade_type, cost)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
