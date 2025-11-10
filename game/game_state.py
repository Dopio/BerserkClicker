from game.entities import Player
from game.enemies import basic_enemies
from game.config import GameConfig


class GameState:
    def __init__(self):
        self.player = None
        self.enemies = basic_enemies
        self.reset_game()

    def reset_game(self):
        self.player = Player(
            GameConfig.PLAYER_NAME,
            GameConfig.STARTING_PLAYER_BLOOD,
            GameConfig.STARTING_PLAYER_KILLS,
            GameConfig.STARTING_PLAYER_DAMAGE,
            GameConfig.STARTING_PLAYER_HEALTH,
            GameConfig.STARTING_PLAYER_MAX_HEALTH,
            True
        )

        for enemy in self.enemies:
            enemy.health = enemy.max_health

    def get_alive_enemies(self):
        return [enemy for enemy in self.enemies if enemy.health > 0]


game_state = GameState()
