class Player:
    def __init__(self, player_name, player_blood, player_kills, player_damage, player_health):
        self.player_name = player_name
        self.player_blood = player_blood
        self.player_kills = player_kills
        self.player_damage = player_damage
        self.player_health = player_health

    def show_player_stats(self):
        print(f'Player name: {self.player_name} \n'
              f'Blood count: {self.player_blood} \n'
              f'Kills: {self.player_kills} \n'
              f'Damage: {self.player_damage}\n'
              f'HP: {self.player_health}')

    def player_attack(self, mob):
        if mob.health > 0:
            print(f'Player {self.player_name} has attack {mob.name}')
            mob.take_damage(self.player_damage)
            self.player_blood += self.player_damage
            print(f'{mob.name} have {mob.health} HP left!\n')

    def take_damage(self, damage):
        self.player_health -= damage
        if self.player_health <= 0:
            return "Death"

    def buy_upgrade(self):
        print(f'Which upgrade you want? '
              f'You have {self.player_blood} for updates')
        print(f'1) Increase your damage: +1   (cost 2 blood)\n'
              f'2) Increase your damage: +2   (cost 5 blood)\n'
              f'3) Increase your damage: +3   (cost 8 blood)')
        player_choice = int(input())
        if player_choice == 1 and self.player_blood >= 2:
            self.player_damage += 1
            self.player_blood -= 2
            print(f'Your damage now is: {self.player_damage}')
        elif player_choice == 2 and self.player_blood >= 5:
            self.player_damage += 2
            self.player_blood -= 5
            print(f'Your damage now is: {self.player_damage}')
        elif player_choice == 3 and self.player_blood >= 8:
            self.player_damage += 3
            self.player_blood -= 8
            print(f'Your damage now is: {self.player_damage}')
        else:
            print('Not enough blood')


class Mob:
    def __init__(self, name, health, damage, gold_reward):
        self.name = name
        self.health = health
        self.damage = damage
        self.gold_reward = gold_reward

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return "Death"

    def mob_attack(self, player):
        if player.player_health > 0:
            print(f'{self.name} has attack {player.player_name} at {self.damage}')
            player.take_damage(self.damage)
            print(f'{player.player_name} have {player.player_health} HP left!\n')
