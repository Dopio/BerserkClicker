from game.entities import Mob


basic_enemies = [
    Mob("Weak Kaban", 3, 3, 0, 1, True),
    Mob("Kaban Warrior", 5, 5, 1, 2, True),
    Mob("Big Kaban", 8, 8, 2, 3, True),
    Mob("Kaban Chief", 12, 12, 3, 5, True),
    Mob("Kaban Berserker", 15, 15, 4, 7, True)
]

# ===== АПОСТОЛЫ И СИЛЬНЫЕ ВРАГИ =====
apostle_enemies = [
    Mob("Apostle Grunt", 10, 10, 3, 4, True),
    Mob("Snake Apostle", 15, 15, 5, 8, True),
    Mob("Zodd the Immortal", 25, 25, 8, 15, True),
    Mob("Wyald the Mad", 20, 20, 6, 12, True),
    Mob("Rosine the Butterfly", 18, 18, 7, 10, True)
]

# ===== БОССЫ =====
boss_enemies = [
    Mob("Nosferatu Zodd", 50, 50, 15, 30, True),
    Mob("Griffith", 40, 40, 12, 25, True),
    Mob("Femto", 100, 100, 25, 50, True),
    Mob("Skull Knight", 35, 35, 10, 20, True),
    Mob("Godo the Blacksmith", 30, 30, 8, 18, True)
]

# ===== СПЕЦИАЛЬНЫЕ ВРАГИ =====
special_enemies = [
    Mob("Ghost Soldier", 8, 8, 2, 3, True),
    Mob("Kushan Assassin", 12, 12, 6, 8, True),
    Mob("Troll", 25, 25, 10, 12, True),
    Mob("Kelpie", 15, 15, 5, 9, True),
    Mob("Pishacha Demon", 22, 22, 8, 15, True)
]

all_enemies = basic_enemies + apostle_enemies + boss_enemies + special_enemies
