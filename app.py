from flask import Flask, render_template, jsonify
from game.enemies import basic_enemies
from game.entities import Player
import random

app = Flask(__name__)

player = Player('Guts', 0, 0, 1, 10)


@app.route('/')
def hello_word():
    return render_template('index.html')


@app.route('/api/player/stats')
def get_player_stats():
    return jsonify({
        'name': player.player_name,
        'blood': player.player_blood,
        'kills': player.player_kills,
        'damage': player.player_damage,
        'health': player.player_health
    })


@app.route('/api/enemies')
def get_enemies():
    enemies_data = []
    for i, enemy in enumerate(basic_enemies):
        enemies_data.append({
            'id': i,
            'name': enemy.name,
            'health': enemy.health,
            'damage': enemy.damage,
            'is_alive': enemy.health > 0
        })
    return jsonify(enemies_data)


@app.route('/api/attack/random', methods=['POST'])
def attack_random():
    for i, enemy in enumerate(basic_enemies):
        print(f'{i}: {enemy.name} - HP: {enemy.health} - Alive: {enemy.health > 0}')

    alive_enemies = [e for e in basic_enemies if e.health > 0]
    print(f"Alive enemies count: {len(alive_enemies)}")

    if not alive_enemies:
        return jsonify({'error': 'All enemies is dead!'})

    enemy = random.choice(alive_enemies)

    enemy.health -= player.player_damage
    player.player_blood += player.player_damage

    result = {
        'message': f'{player.player_name} attack {enemy.name} for {player.player_damage} damage!',
        'enemy_health': enemy.health,
        'player_blood': player.player_blood
    }

    if enemy.health <= 0:
        player.player_kills += 1
        result['message'] = f'You kill {enemy.name}'

    return jsonify(result)


@app.route('/api/upgrade/damage', methods=['POST'])
def upgrade_damage():
    if player.player_blood >= 2:
        player.player_damage += 1
        player.player_blood -= 2
        result = {
            'success': True,
            'message': f'{player.player_name} damage increased by 1 to {player.player_damage}',
            'player_damage': player.player_damage,
            'player_blood': player.player_blood
        }
    else:
        result = {
            'success': False,
            'message': 'Not enough blood, need 2 blood'
        }
    return jsonify(result)


@app.route('/api/upgrade/health', methods=['POST'])
def upgrade_health():
    if player.player_blood >= 5:
        player.player_health += 2
        player.player_blood -= 5
        result = {
            'success': True,
            'message': f'{player.player_name} health increased by 2 to {player.player_health}',
            'player_health': player.player_health,
            'player_blood': player.player_blood
        }
    else:
        result = {
            'success': False,
            'message': 'Not enough blood, need 5 blood'
        }
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
