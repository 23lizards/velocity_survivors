import math
import pygame
import pgzrun
import random


def reset():
    global game_paused, lvling_up, hero, hero_book, available_upgrades, enemies, \
        arena_width, arena_height

    game_paused = False
    lvling_up = False

    current_seed = 1
    random.seed(current_seed)

    arena_width = 800
    arena_height = 600

    hero = {
        'hp': 100,
        'radius': 20,
        'x': arena_width / 2,
        'y': arena_height / 2,
        'speed': 2,
        'lvl': 0,
        'xp': 0,
        'xp_in_lvl': 200
    }

    hero_book = {
        'dmg': 4,
        'radius': 9,
        'orbit_radius': 35,
        'angle': 0,
        'x': hero['x'] + 35 * math.cos(0),
        'y': hero['y'] + 35 * math.sin(0)
    }

    available_upgrades = [
        {
            'name': 'speed +5%',
            'subject': 'hero',
            'feature': 'speed',
            'coeff': 1.05
        },
        {
            'name': 'dmg +5%',
            'subject': 'hero_book',
            'feature': 'dmg',
            'coeff': 1.05
        }
    ]

    enemies = []
    enemy_type1 = {
        'hp': 25,
        'x': 0,
        'y': 0,
        'radius': 10,
        'speed': 0.6,
        'dmg': 3,
        'gives_xp': 100
    }
    enemy_type1_quantity = 4
    enemy_type2 = {
        'hp': 100,
        'x': 0,
        'y': 0,
        'radius': 30,
        'speed': 0.4,
        'dmg': 4,
        'gives_xp': 300
    }
    enemy_type2_quantity = 2
    enemies = []
    for x in range(enemy_type1_quantity):
        enemies.append(enemy_type1.copy())
    for x in range(enemy_type2_quantity):
        enemies.append(enemy_type2.copy())
    for enemy in enemies:
        enemy['x'] = random.randint(0, arena_width)
        enemy['y'] = random.randint(0, arena_height)


reset()


def move_towards_player(enemy, hero):
    # Find direction vector (dx, dy) between enemy and player.
    dir_vect = pygame.math.Vector2(hero['x'] - enemy['x'],
                                   hero['y'] - enemy['y'])
    dir_vect.normalize()
    # Move along this normalized vector towards the player at current speed.
    dir_vect.scale_to_length(enemy['speed'])
    # enemy.rect.move_ip(dir_vect)
    enemy['x'] += dir_vect.x
    enemy['y'] += dir_vect.y


def check_collision(obj1, obj2):
    if abs(obj1['x'] - obj2['x']) < max(obj1['radius'], obj2['radius']) and \
            abs(obj1['y'] - obj2['y']) < max(obj1['radius'], obj2['radius']):
        return True
    return False


def lvl_up():
    global game_paused, lvling_up
    game_paused = True
    lvling_up = True
    hero['lvl'] += 1
    hero['xp'] -= hero['xp_in_lvl']


def check_xp():
    if hero['xp'] >= hero['xp_in_lvl']:
        lvl_up()


def apply_upgrade(upgrade):
    global game_paused, lvling_up
    if upgrade['subject'] == 'hero':
        hero[upgrade['feature']] *= upgrade['coeff']
    elif upgrade['subject'] == 'hero_book':
        hero_book[upgrade['feature']] *= upgrade['coeff']
    lvling_up = False
    game_paused = False


def update():
    global game_paused, hero, hero_book, enemies

    if keyboard.r:
        reset()

    if keyboard.p:
        game_paused = not game_paused

    if not game_paused:
        if keyboard.left:
            hero['x'] -= hero['speed']

        if keyboard.right:
            hero['x'] += hero['speed']

        if keyboard.up:
            hero['y'] -= hero['speed']

        if keyboard.down:
            hero['y'] += hero['speed']

        for enemy in enemies:
            if check_collision(hero, enemy):
                hero['hp'] -= enemy['dmg']
            if check_collision(hero_book, enemy):
                enemy['hp'] -= hero_book['dmg']
            if enemy['hp'] <= 0:
                enemies.remove(enemy)
                hero['xp'] += enemy['gives_xp']
            move_towards_player(enemy, hero)

        check_xp()

        hero_book['angle'] += 0.1
        hero_book['x'] = hero['x'] + hero_book['orbit_radius'] * math.cos(hero_book['angle'])
        hero_book['y'] = hero['y'] + hero_book['orbit_radius'] * math.sin(hero_book['angle'])

    if lvling_up:
        if keyboard.k_1:
            apply_upgrade(available_upgrades[0])
        elif keyboard.k_2:
            apply_upgrade(available_upgrades[1])


def draw():
    global arena_height, lvling_up, available_upgrades

    screen.fill(color='black')

    for enemy in enemies:
        screen.draw.filled_circle(
            (enemy['x'], enemy['y']), enemy['radius'], color='red'
        )
        screen.draw.text(
            f'HP: {math.ceil(enemy["hp"])}',
            (enemy['x'] - 18, enemy['y'] - enemy['radius'] - 10),
            fontsize=16,
            color='salmon'
        )

    screen.draw.filled_circle(
        (hero['x'], hero['y']), hero['radius'], color='blue'
    )
    
    screen.draw.filled_circle(
        (hero_book['x'], hero_book['y']), hero_book['radius'], color='cyan'
    )

    screen.draw.text(
        f'HP: {hero["hp"]}',
        (hero['x'] - 18, hero['y'] - 30),
        fontsize=16,
        color='green'
    )

    screen.draw.text(
        f'LVL: {hero["lvl"]}\nXP: {hero["xp"]}\nDMG: {round(hero_book["dmg"], 2)}\nSPD: {round(hero["speed"], 2)}',
        (4, 4),
        fontsize=16,
        color='green'
    )

    if lvling_up:
        screen.fill(color='black')
        screen.draw.text(
            'LVL UP!\nChoose an upgrade',
            (arena_width / 2 - 32, arena_height / 2 - 16),
            fontsize=32,
            color='blue'
        )
        for i in range(2):
            screen.draw.text(
                f'{i + 1} = {available_upgrades[i]["name"]}',
                (arena_width / 2 - 32, arena_height / 2 - 16 + 64 + i * 32),
                fontsize=32,
                color='blue'
            )

    if hero['hp'] <= 0:
        screen.fill(color='black')
        screen.draw.text(
            'YOU DIED',
            (arena_width / 2 - 32, arena_height / 2 - 16),
            fontsize=32,
            color='salmon'
        )


pgzrun.go()
