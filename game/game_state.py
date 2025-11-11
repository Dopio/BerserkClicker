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

    def perform_attack(self, enemy, enemy_id: int | None = None) -> dict:

        if enemy_id is not None:
            print(f'{self.player.player_name}'
                  f'attack enemy {enemy_id}: {enemy.name}'
                  f'HP: {enemy.health}')

        if enemy.health <= 0:
            return {
                'success': False,
                'message': f'{enemy.name} is Dead!',
            }
        elif self.player.player_health <= 0:
            return {
                'success': False,
                'message': ' You are Dead!',
            }

        enemy.health -= self.player.player_damage
        self.player.player_health -= enemy.damage
        self.player.player_blood += self.player.player_damage

        enemy_is_alive = enemy.health > 0
        player_is_alive = self.player.player_is_alive > 0

        result = {
            'success': True,
            'message': f'Player {self.player.player_name} attack {enemy.name}',
            'enemy_health': enemy.health,
            'player_health': self.player.player_health,
            'player_blood': self.player.player_blood,
            'player_kills': self.player.player_kills,
            'enemy_is_alive': enemy_is_alive,
            'player_is_alive': player_is_alive
        }

        if enemy.health <= 0:
            self.player.player_kills += 1
            result['message'] = f'You kill {enemy.name}'
            result['enemy_is_alive'] = False
            result['player_kills'] = self.player.player_kills

        if self.player.player_health <= 0:
            result['message'] = f'YOU DIED! GAME OVER'
            result['player_is_alive'] = False
            result['success'] = False

        return result

    def buy_upgrade(self, upgrade_type: str, cost: int) -> dict:
        if self.player.player_blood < cost:
            return {
                'success': False,
                'message': f'Not enough blood, need {cost} blood'
            }
        upgrades = {
            'upgrade_damage': {
                'action': lambda: setattr(self.player, 'player_damage', self.player.player_damage + 1),
                'message': f'{self.player.player_name} damage increased by 1 to {self.player.player_damage}'
            },
            'upgrade_health': {
                'action': lambda: setattr(self.player, 'player_health', self.player.player_health + 5),
                'message': f'{self.player.player_name} health increased by 5 to {self.player.player_health}'
            }
        }

        if upgrade_type not in upgrades:
            return {
                'success': False,
                'message': f'Unknown upgrade type: {upgrade_type} ',
            }

        upgrade = upgrades[upgrade_type]
        upgrade['action']()
        self.player.player_blood -= cost

        result = {
            'success': True,
            'message': f'{game_state.player.player_name} {upgrade["message"]}',
            'player_damage': self.player.player_damage,
            'player_health': self.player.player_health,
            'player_blood': self.player.player_blood
        }

        return result


game_state = GameState()
