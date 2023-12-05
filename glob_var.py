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
This messy file is for all instances of all classes, located in one place for easy access universally. Although it streamlined the development process, it's been a nightmare to maintain
but was too difficult to remove so late in development. 
'''

# Path for player character
image_paths = {
    'up': ['images/Up standing.png', 'images/Up running.png'],
    'down': ['images/Down standing.png', 'images/Down running.png'],
    'left': ['images/Left standing.png', 'images/Left running .png'],
    'right': ['images/1.png', 'images/BackgroundEraser_image.png']
}

# Player Character
player = Character(name="Player", x=100, y=100, width=50, height=50, speed=1, health=100, armor=50, gun=0,
                   image_path="images/white_square.png")

# Weapon Instances
pistol = Weapon(name="Pistol", damage=10, proj_speed=1, attack_speed=3, mag_size=9, mag_count=5, reload_speed=10,
                owner=player, x=50, y=50, width=50, height=50, image_path=None)
ar = Weapon(name="Assault Rifle", damage=15, proj_speed=1.25, attack_speed=5, mag_size=30, mag_count=2, reload_speed=20,
            owner=player, x=600, y=350, width=100, height=50, image_path='images/ar.png')
dev_gun = Weapon("God's Draco", 10, 2, 100, 10000, 1, 10, player, x=200, y=300, width=100, height=50, image_path='images/minigun.png')
# Shotgun Instances
shotgun = Shotgun(name="Pump Shotgun", damage=10, proj_speed=1, attack_speed=2, mag_size=8, mag_count=2,
                  reload_speed=15, owner=player, spread=25, proj_number=8,  x=1050, y=600, width=100, height=50, image_path='images/shotgun.png')
dev_shotgun = Shotgun("God's Sawed-Off", 50, 5, 10, 1000, 1, 10, player, 20, 30,  x=50, y=50, width=50, height=50, image_path=None)

# List of all guns, used to draw all projectiles that could exist. This will be changed to a more efficient list in the final version
guns = [pistol, ar, dev_gun, shotgun, dev_shotgun]

# Debug change gun
player.gun = dev_gun

''' 
Start of room creation. Each room follows a similar creation pattern, and will be denoted as such:
Here is everything added to Room 1:
6 Enemies
6 Objects
Door
Assault Rifle
'''
enemy1 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
enemy2 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
enemy3 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
enemy4 = Tank(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
enemy5 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
enemy6 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
# List of all enemies for drawing and player tracking
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]
# Separate list including all enemies and main character, used for object collision
entities = [player]
for i in enemies:
    entities.append(i)


obj = Object(x=200, y=100, width=50, height=150, health=1000)
obj2 = Object(x=200, y=100, width=700, height=50, health=1000)
obj3 = Object(x=850, y=100, width=50, height=150, health=1000)
obj4 = Object(x=200, y=550, width=700, height=50, health=1000)
obj5 = Object(x=200, y=500, width=50, height=100, health=1000)
obj6 = Object(x=850, y=500, width=50, height=100, health=1000)
r1door1 = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')
# Object list, used for drawing and collision
r1objs = [obj, obj2, obj3, obj4, obj5, obj6, r1door1]
# Room Instance
r1 = Room(background_path="images/Tile Resized.jpg", screen_width=screen_width, screen_height=screen_height)

# Adds all enemies/entities to the room
for i in enemies:
    r1.add_enemy(i)
r1.entities = entities

# Adds all objects to the room
for i in r1objs:
    r1.add_object(i)

# Adds door to room
r1.door = r1door1

# Adds gun to room
r1.add_item(ar)

# Items are universal, meaning there's only one instance of them that is reused and reset when called.
key = Item("Key", 950, 100, 75, 75, "images/golden key.png")
medkit = Item("Medkit", 950, 100, 50, 50, "images/medkit.png")

'''
Here is everything added to Room 2:
6 enemies
5 objects
Door
'''
r2enemy1 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy2 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy3 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy4 = Tank(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy5 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r2enemy6 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r2enemies = [r2enemy1, r2enemy2, r2enemy3, r2enemy4, r2enemy5, r2enemy6]
r2entities = [player]
for i in r2enemies:
    r2entities.append(i)

r2obj = Object(x=150, y=100, width=50, height=500, health=1000)
r2obj2 = Object(x=150, y=600, width=700, height=50, health=1000)
r2obj3 = Object(x=350, y=50, width=600, height=50, health=1000)
r2obj4 = Object(x=950, y=50, width=50, height=500, health=1000)
r2obj5 = Object(x=500, y=300, width=100, height=100, health=1000)
r2objs = [r2obj, r2obj2, r2obj3, r2obj4, r2obj5]
r2door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')

r2 = Room(background_path="images/Tile Resized.jpg", screen_width=screen_width, screen_height=screen_height)
# Determines where the player spawns in the next level
r2.starting_x = 100
r2.starting_y = 100
r2.enemies = r2enemies
r2.entities = r2entities
r2.objects = r2objs
r2.door = r2door
# Make the previous room's door lead to this room
r1.next_room = r2

'''
Here is everything added to Room 3:
6 enemies
6 objects
Door
Shotgun
'''
r3enemy1 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r3enemy2 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r3enemy3 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r3enemy4 = Tank(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r3enemy5 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r3enemy6 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600))
r3enemies = [r3enemy1, r3enemy2, r3enemy3, r3enemy4, r3enemy5, r3enemy6]
r3entities = [player]
for i in r3enemies:
    r3entities.append(i)

r3obj = Object(x=1000, y=150, width=50, height=400, health=1000)
r3obj2 = Object(x=200, y=150, width=800, height=50, health=1000)
r3obj3 = Object(x=250, y=300, width=75, height=75, health=1000)
r3obj4 = Object(x=150, y=550, width=75, height=75, health=1000)
r3obj5 = Object(x=500, y=450, width=75, height=75, health=1000)
r3obj6 = Object(x=700, y=550, width=75, height=75, health=1000)
r3objs = [r3obj, r3obj2, r3obj3, r3obj4, r3obj5, r3obj6]
r3door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')

r3 = Room(background_path="images/Tile Resized.jpg", screen_width=screen_width, screen_height=screen_height)
r3.starting_x = 100
r3.starting_y = 100
r3.enemies = r3enemies
r3.entities = r3entities
r3.objects = r3objs
r3.add_item(shotgun)
r3.door = r3door
r2.next_room = r3

'''
Here is everything added to Room 4:
Boss Enemy
2 Minions
Door
'''
#r4enemy1 = Enemy(name='enemy', x=450, y=700, width=50, height=75, speed=.5, health=50, armor=0, gun=0, character=player, damage=20, image_path='images/waterEnemy1.png')
r4enemy2 = Enemy(name='enemy', x=450, y=400, width=50, height=75, speed=.5, health=50, armor=0, gun=0, character=player, damage=20, image_path='images/waterEnemy1.png')
r4enemy3 = Enemy(name='enemy', x=450, y=500, width=50, height=75, speed=.5, health=50, armor=0, gun=0, character=player, damage=20, image_path='images/waterEnemy1.png')
boss = Enemy(name='Boss', x=550, y=300, width=200, height=200, speed=.07, health=1000, armor=0, gun=0, character=player, damage=50, image_path='images/bossGolem.png')

r4 = Room(background_path="images/ocean.png", screen_width=screen_width, screen_height=screen_height)
r4.starting_x = 100
r4.starting_y = 300
r4enemies = [boss, r4enemy2, r4enemy3]
r4entities = [player]
for i in r4enemies:
    r4entities.append(i)
r4.entities = r4entities
r4.enemies = r4enemies

r4door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')
r4.door = r4door
r3.next_room = r4

'''
Here is everything added to Room 5:
A little guy. Self Explanatory
A minigun. Self Explanatory
Door
'''
r5 = Room(background_path="images/darkness.png", screen_width=screen_width, screen_height=screen_height)
little_guy = Enemy(name='enemy', x=800, y=500, width=50, height=50, speed=.001, health=10, armor=0, gun=0, character=player, damage=20, image_path='images/little_guy.png')
r5.starting_y = 300
r5.starting_x = 100
r5enemies = [little_guy]
r5entities = [player, little_guy]
r5.enemies = r5enemies
r5entities = r5entities
r5.add_item(dev_gun)
r5.door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')
r4.next_room = r5

'''
Here is everything added to Room 6:
24 enemies for minigun practice
'''
r6 = Room(background_path="images/darkness.png", screen_width=screen_width, screen_height=screen_height)
r6.starting_y = 50
r6.starting_x = 600

r6enemy1 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy2 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy3 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy4 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy5 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy6 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy7 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy8 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy9 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy10 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy11 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy12 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy13 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy14 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy15 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy16 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy17 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy18 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy19 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy20 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy21 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy22 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy23 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemy24 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600))
r6enemies = [r6enemy1, r6enemy2, r6enemy3, r6enemy4, r6enemy5, r6enemy6, r6enemy7, r6enemy8, r6enemy9, r6enemy10, r6enemy11, r6enemy12,
             r6enemy13, r6enemy14, r6enemy15, r6enemy16, r6enemy17, r6enemy24, r6enemy23, r6enemy18, r6enemy19, r6enemy20, r6enemy21, r6enemy22]
r6entities = [player]
for i in r6enemies:
    r6entities.append(i)
r6.enemies = r6enemies
r6.entities = r6entities
r5.next_room = r6

# Sets the starting room as room 1.
cur_room = r1
