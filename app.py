from flask import Flask, render_template, jsonify
from game.game_state import game_state
import random

app = Flask(__name__)


@app.route('/')
def hello_word():
    return render_template('index.html')


@app.route('/api/game/reset', methods=['POST'])
def reset_game():
    game_state.reset_game()
    return jsonify({
        'success': True,
        'message': 'Game reset successfully'
    })


@app.route('/api/player/stats')
def get_player_stats():
    return jsonify({
        'player_name': game_state.player.player_name,
        'player_blood': game_state.player.player_blood,
        'player_kills': game_state.player.player_kills,
        'player_damage': game_state.player.player_damage,
        'player_health': game_state.player.player_health,
        'player_max_health': game_state.player.player_max_health,
        'player_is_alive': game_state.player.player_is_alive
    })


@app.route('/api/enemies')
def get_enemies():
    enemies_data = []
    for i, enemy in enumerate(game_state.enemies):
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
def attack_random():
    for i, enemy in enumerate(game_state.enemies):
        print(f'{i}: {enemy.name} - HP: {enemy.health} - Alive: {enemy.health > 0}')

    alive_enemies = [e for e in game_state.enemies if e.health > 0]
    print(f"Alive enemies count: {len(alive_enemies)}")

    if not alive_enemies:
        return jsonify({'error': 'All enemies is dead!'})

    enemy = random.choice(alive_enemies)

    enemy.health -= game_state.player.player_damage
    game_state.player.player_blood += game_state.player.player_damage

    result = {
        'message': f'{game_state.player.player_name} attack {enemy.name} for {game_state.player.player_damage} damage!',
        'enemy_health': enemy.health,
        'player_blood': game_state.player.player_blood
    }

    if enemy.health <= 0:
        game_state.player.player_kills += 1
        result['message'] = f'You kill {enemy.name}'

    return jsonify(result)


@app.route('/api/upgrade/damage', methods=['POST'])
def upgrade_damage():
    if game_state.player.player_blood >= 2:
        game_state.player.player_damage += 1
        game_state.player.player_blood -= 2
        result = {
            'success': True,
            'message': f'{game_state.player.player_name} damage increased by 1 to {game_state.player.player_damage}',
            'player_damage': game_state.player.player_damage,
            'player_blood': game_state.player.player_blood
        }
    else:
        result = {
            'success': False,
            'message': 'Not enough blood, need 2 blood'
        }
    return jsonify(result)


@app.route('/api/upgrade/health', methods=['POST'])
def upgrade_health():
    if game_state.player.player_blood >= 5:
        game_state.player.player_health += 2
        game_state.player.player_blood -= 5
        result = {
            'success': True,
            'message': f'{game_state.player.player_name} health increased by 2 to {game_state.player.player_health}',
            'player_health': game_state.player.player_health,
            'player_blood': game_state.player.player_blood
        }
    else:
        result = {
            'success': False,
            'message': 'Not enough blood, need 5 blood'
        }
    return jsonify(result)


@app.route('/api/attack/<int:enemy_id>', methods=['POST'])
def attack_specific_enemy(enemy_id):

    if enemy_id < 0 or enemy_id >= len(game_state.enemies):
        return jsonify({'error': 'Invalid enemy ID'})

    enemy = game_state.enemies[enemy_id]
    print(f'Id: {enemy_id} Name: {enemy.name} HP: {enemy.health} Alive: {enemy.health > 0}')

    if enemy.health <= 0:
        return jsonify({'error': 'Enemy is dead!'})
    elif game_state.player.player_health <= 0:
        return jsonify({'error': 'You are Dead!'})

    enemy.health -= game_state.player.player_damage
    game_state.player.player_health -= enemy.damage
    game_state.player.player_blood += game_state.player.player_damage

    enemy_is_alive = enemy.health > 0
    player_is_alive = game_state.player.player_is_alive > 0

    result = {
        'success': True,
        'message': f'Player {game_state.player.player_name} attack {enemy.name}',
        'enemy_health': enemy.health,
        'player_health': game_state.player.player_health,
        'player_blood': game_state.player.player_blood,
        'player_kills': game_state.player.player_kills,
        'enemy_is_alive': enemy_is_alive,
        'player_is_alive': player_is_alive
    }

    if enemy.health <= 0:
        game_state.player.player_kills += 1
        result['message'] = f'You kill {enemy.name}'
        result['enemy_is_alive'] = False
        result['player_kills'] = game_state.player.player_kills

    if game_state.player.player_health <= 0:
        result['message'] = f'YOU DIED! GAME OVER'
        result['player_is_alive'] = False
        result['success'] = False

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
