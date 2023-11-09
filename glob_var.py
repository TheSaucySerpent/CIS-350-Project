from character import Character
from weapons import Weapon
from weapons import Shotgun
from enemy import Enemy, Default, Tank, Runner
from object import Object
from room import Room
from item import Item

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
player = Character(name="Player", x=1100, y=100, width=50, height=50, speed=1, health=100, armor=50, gun=0, image_path="images/white_square.png")

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
player.gun = shotgun

# All Enemy List
enemy1 = Default()
enemy2 = Default()
enemy3 = Default()
enemy4 = Tank()
enemy5 = Runner()
enemy6 = Runner()
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
objs = [obj, obj2, obj3, obj4, obj5, obj6]

# Ignore
# player2 = Character(name="mc",x=1100, y=100, width=10, height=100, speed=1, health=100, armor=50, gun=0,image_path="images/door.png")

# Room Instances
r1 = Room(background_path="images/Tile Resized.jpg",screen_width=1200,screen_height=700)

# Adds all enemies to the room
for i in enemies:
    r1.add_enemy(i)

# Adds all objects to the room
for i in objs:
    r1.add_object(i)

# Items were a last minute addition, so it's not perfectly implemented currently. This is something we will clean up in the future version.
key = Item(50, 100, 75, 75, "images/golden key.png")
r1.add_item(key)
key.bounce()



