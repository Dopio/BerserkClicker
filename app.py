from flask import Flask, render_template, jsonify
from game.enemies import basic_enemies
from game.entities import Player
import random
import json

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


if __name__ == '__main__':
    app.run(debug=True)
