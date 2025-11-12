from game.entities import Player
from game.enemies import basic_enemies, apostle_enemies, boss_enemies
from game.config import GameConfig


class GameState:
    def __init__(self):
        self.player = None
        self.current_wave = 0
        self.waves = []
        self.current_enemies = []
        self.reset_game()

    def setup_waves(self):
        self.waves = [
            {
                'name': 'basic_enemies',
                'enemies': basic_enemies,
                'required_kills': 2,
                'unlock_message': 'Basic_enemies are defeated!'
            },
            {
                'name': 'boss_enemies',
                'enemies': boss_enemies,
                'required_kills': 3,
                'unlock_message': 'boss_enemies are defeated!'
            },
            {
                'name': 'apostle_enemies',
                'enemies': apostle_enemies,
                'required_kills': 2,
                'unlock_message': 'apostle_enemies are defeated!'
            }
        ]

    def reset_game(self) -> None:
        self.player = Player(
            GameConfig.PLAYER_NAME,
            GameConfig.STARTING_PLAYER_BLOOD,
            GameConfig.STARTING_PLAYER_KILLS,
            GameConfig.STARTING_PLAYER_DAMAGE,
            GameConfig.STARTING_PLAYER_HEALTH,
            GameConfig.STARTING_PLAYER_MAX_HEALTH,
            True
        )
        self.current_wave = 0
        self.setup_waves()
        self.spawn_wave()
        return None

    def spawn_wave(self) -> None:
        if self.current_wave < len(self.waves):
            wave = self.waves[self.current_wave]
            self.current_enemies = wave['enemies'].copy()
            print(f"Wave {self.current_wave + 1}: {wave['name']} spawned!")
        return None

    def check_wave_progress(self) -> str | None:
        if self.current_wave >= len(self.waves):
            return None
        concurrent_wave_data = self.waves[self.current_wave]
        killed_in_wave = sum(1 for enemy in concurrent_wave_data['enemies'] if enemy.health <= 0)
        if killed_in_wave > concurrent_wave_data['required_kills']:
            self.current_wave += 1
            if self.current_wave < len(self.waves):
                self.spawn_wave()
                return concurrent_wave_data['unlock_message']
            else:
                return 'ALL WAVES ARE CLEARED!'
        return None

    def get_alive_enemies(self):
        return [enemy for enemy in self.current_enemies if enemy.health > 0]

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
        enemy_is_alive = enemy.health > 0

        # Враг не атакует, если игрок наносит добивающий удар
        # При смерти враг не даёт больше крови, чем у него оставалось ХП
        if enemy_is_alive:
            self.player.player_health -= enemy.damage
            self.player.player_blood += self.player.player_damage
        else:
            self.player.player_blood += self.player.player_damage + enemy.health

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

            wave_message = self.check_wave_progress()
            if wave_message:
                result['wave_message'] = wave_message
                result['new_wave'] = self.current_wave + 1

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
