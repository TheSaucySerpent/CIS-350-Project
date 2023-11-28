import random
from character import Character
from weapons import Weapon
from weapons import Shotgun
from enemy import Enemy, Default, Tank, Runner
from object import Object, Door
from room import Room
from item import Item

screen_width = 1200
screen_height = 700

'''
This messy file is for all instances of all classes, located in one place for easy access universally. Although it streamlined the development process up to this point,
we plan on removing/heavily altering this file in the future.
'''

# Path for player character
image_paths = {
    'up': ['images/Up standing.png', 'images/Up running.png'],
    'down': ['images/Down standing.png', 'images/Down running.png'],
    'left': ['images/Left standing.png', 'images/Left running .png'],
    'right': ['images/1.png', 'images/BackgroundEraser_image.png']
}


# Player Character
player = Character(name="Player",x=1100, y=100, width=50, height=50, speed=1, health=100, armor=50, gun=0,image_path="images/white_square.png")

# Weapon Instances
pistol = Weapon(name="Pistol", damage=10, proj_speed=.5, attack_speed=2, mag_size=9, mag_count=3, reload_speed=10, owner=player)
ar = Weapon(name="Assault Rifle", damage=15, proj_speed=1, attack_speed=5, mag_size=30, mag_count=2, reload_speed=20, owner=player)
dev_gun = Weapon("God's Draco", 100, 2, 100, 10000, 1, 10, player)
# Shotgun Instances
shotgun = Shotgun(name="Pump Shotgun", damage=10, proj_speed=1, attack_speed=2, mag_size=8, mag_count=2, reload_speed=15, owner=player, spread=25, proj_number=8)
dev_shotgun = Shotgun("God's Sawed-Off", 50, 5, 10, 1000, 1, 10, player, 20, 30)

# List of all guns, used to draw all projectiles that could exist. This will be changed to a more efficient list in the final version
guns = [pistol, ar, dev_gun, shotgun, dev_shotgun]


# Debug change gun
player.gun = dev_shotgun

# All Enemy List
enemy1 = Default(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
enemy2 = Default(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
enemy3 = Default(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
enemy4 = Tank(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
enemy5 = Runner(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
enemy6 = Runner(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
# List of all enemies for drawing and player tracking
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]
# Separate list including all enemies and main character, used for object collision
entities = [player]
for i in enemies:
    entities.append(i)


# All object instances
obj = Object(x=200, y=100, width=50, height=150, health=1000)
obj2 = Object(x=200, y=100, width=700, height=50, health=1000)
obj3 = Object(x=850, y=100, width=50, height=150, health=1000)
obj4 = Object(x=200, y=550, width=700, height=50, health=1000)
obj5 = Object(x=200, y=500, width=50, height=100, health=1000)
obj6 = Object(x=850, y=500, width=50, height=100, health=1000)
# Object list, used for drawing and collision
r1objs = [obj, obj2, obj3, obj4, obj5, obj6]
r1door1 = Door(x=800, y=300, width=50, height=50, health=1000, image_path='images/door.png')

# Ignore
# player2 = Character(name="mc",x=1100, y=100, width=10, height=100, speed=1, health=100, armor=50, gun=0,image_path="images/door.png")

# Room Instances
r1 = Room(background_path="images/Tile Resized.jpg", screen_width=screen_width, screen_height=screen_height)

# Adds all enemies to the room
for i in enemies:
    r1.add_enemy(i)

# Adds all objects to the room
for i in r1objs:
    r1.add_object(i)

r1.door = r1door1

# Items were a last minute addition, so it's not perfectly implemented currently. This is something we will clean up in the future version.
key = Item(50, 100, 75, 75, "images/golden key.png")
r1.add_item(key)

r1.entities = []

r2enemy1 = Default(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy2 = Default(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy3 = Default(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy4 = Tank(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy5 = Runner(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy6 = Runner(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600))
# List of all enemies for drawing and player tracking
r2enemies = [r2enemy1, r2enemy2, r2enemy3, r2enemy4, r2enemy5, r2enemy6]
# Separate list including all enemies and main character, used for object collision
r2entities = [player]
for i in r2enemies:
    r2entities.append(i)

r2obj = Object(x=200, y=100, width=50, height=150, health=1000)
r2obj2 = Object(x=200, y=100, width=700, height=50, health=1000)
r2obj3 = Object(x=850, y=100, width=50, height=150, health=1000)
r2obj4 = Object(x=200, y=550, width=700, height=50, health=1000)
r2obj5 = Object(x=200, y=500, width=50, height=100, health=1000)
r2obj6 = Object(x=850, y=500, width=50, height=100, health=1000)
# Object list, used for drawing and collision
r2objs = [r2obj, r2obj2, r2obj3, r2obj4, r2obj5, r2obj6]

r2 = Room(background_path="images/Tile Resized.jpg", screen_width=screen_width, screen_height=screen_height)
r2.enemies = r2enemies
r2.entities = r2entities
r2.objects = r2objs
r1.next_room = r2

cur_room = r1



