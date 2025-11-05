from entities import Player, Mob
from enemies import basic_enemies
import random


def fight_with_enemy(player, enemy):
    if enemy.health <= 0:
        print(f'\n{enemy.name} already dead!\n')
    else:
        print('Fight is start! '
              f'Enemy: {enemy.name} (HP: {enemy.health})\n')
        while enemy.health > 0 and player.player_health > 0:
            player.player_attack(enemy)
            enemy.mob_attack(player)
        if enemy.health <= 0:
            player.player_kills += 1
            print(f'{enemy.name} is Dead!')
        else:
            print('YOU DIED\n')
            return False


def game_loop():
    player1 = Player('Guts', 0, 0, 1, 10)

    while player1.player_health > 0:
        print(f'1) Show all enemy\n'
              f'2) Attack random enemy\n'
              f'3) Update shop\n'
              f'4) Show stats\n'
              f'5) End game')
        player_choice = int(input('Your choice: '))
        print('\n')
        if player_choice == 1:
            while player1.player_health > 0:
                for i, enemy in enumerate(basic_enemies, 1):
                    if enemy.health <= 0:
                        print(f'{enemy.name} enemy already died')
                    else:
                        print(f'{i}) {enemy.name} (HP: {enemy.health})')
                print("Print 9 to exit to main menu")
                enemy_choice = int(input('Choice enemy to kill: \n')) - 1
                if 0 <= enemy_choice < len(basic_enemies):
                    fight_with_enemy(player1, basic_enemies[enemy_choice])
                elif enemy_choice == 8:
                    break
                else:
                    print('Wrong choice')

        if player_choice == 2:
            enemy = random.choice(basic_enemies)
            fight_with_enemy(player1, enemy)
        elif player_choice == 3:
            player1.buy_upgrade()
        elif player_choice == 4:
            print('\n')
            player1.show_player_stats()
            print('\n')
        elif player_choice == 5:
            print('Goodbye')
            break
        else:
            print('Unwrite choice')


if __name__ == "__main__":
    print('KILL THEM ALL')
    game_loop()
