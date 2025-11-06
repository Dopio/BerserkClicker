from game.entities import Mob


basic_enemies = [
    Mob("Weak Kaban", 3, 0, 1),
    Mob("Kaban Warrior", 5, 1, 2),
    Mob("Big Kaban", 8, 2, 3),
    Mob("Kaban Chief", 12, 3, 5),
    Mob("Kaban Berserker", 15, 4, 7)
]

# ===== АПОСТОЛЫ И СИЛЬНЫЕ ВРАГИ =====
apostle_enemies = [
    Mob("Apostle Grunt", 10, 3, 4),
    Mob("Snake Apostle", 15, 5, 8),
    Mob("Zodd the Immortal", 25, 8, 15),
    Mob("Wyald the Mad", 20, 6, 12),
    Mob("Rosine the Butterfly", 18, 7, 10)
]

# ===== БОССЫ =====
boss_enemies = [
    Mob("Nosferatu Zodd", 50, 15, 30),
    Mob("Griffith", 40, 12, 25),
    Mob("Femto", 100, 25, 50),
    Mob("Skull Knight", 35, 10, 20),
    Mob("Godo the Blacksmith", 30, 8, 18)
]

# ===== СПЕЦИАЛЬНЫЕ ВРАГИ =====
special_enemies = [
    Mob("Ghost Soldier", 8, 2, 3),
    Mob("Kushan Assassin", 12, 6, 8),
    Mob("Troll", 25, 10, 12),
    Mob("Kelpie", 15, 5, 9),
    Mob("Pishacha Demon", 22, 8, 15)
]

all_enemies = basic_enemies + apostle_enemies + boss_enemies + special_enemies
