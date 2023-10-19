from character import Character
from weapons import Weapon
from weapons import Shotgun
from enemy import Enemy
from object import Object
from room import Room
from item import Item

#If there's a better way to do this please share this file looks goofy
#If you want to add weapons, enemies and objects, add them to the corresponding list
image_paths = {
    'up': ['images/Up standing.png', 'images/Up running.png'],
    'down': ['images/Down standing.png', 'images/Down running.png'],
    'left': ['images/Left standing.png', 'images/Left running .png'],
    'right': ['images/1.png', 'images/BackgroundEraser_image.png']
}

#guns need an owner so this needs to be above it, but characters need a gun so it needs to be added after
player = Character(name="Player",x=1100, y=100, width=50, height=50, speed=1, health=100, armor=50, gun=0,image_path="images/white_square.png")

#(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner)
pistol = Weapon(name="Pistol", damage=10, proj_speed=.5, attack_speed=2, mag_size=9, mag_count=3, reload_speed=10, owner=player)
ar = Weapon(name="Assault Rifle", damage=15, proj_speed=1, attack_speed=5, mag_size=30, mag_count=2, reload_speed=20, owner=player)
dev_gun = Weapon("God's Draco", 100, 2, 100, 10000, 1, 10, player)
#shotgun adds spread and number of projectiles
shotgun = Shotgun(name="Pump Shotgun", damage=10, proj_speed=1, attack_speed=2, mag_size=8, mag_count=2, reload_speed=15, owner=player, spread=25, proj_number=8)
dev_shotgun = Shotgun("God's Sawed-Off", 50, 5, 10, 1000, 1, 10, player, 20, 30)



guns = [pistol, ar, dev_gun, shotgun, dev_shotgun]

#Debug change gun
player.gun = shotgun


enemy1 = Enemy(name='enemy', x=700, y=200, width=50, height=50, speed=.2, health=50, armor=10, gun=0, character=player, damage=10,image_path="images/green monster.png")
enemy2 = Enemy(name='enemy',x=500, y=500, width=50, height=50, speed=.25, health=50, armor=10, gun=0, character=player, damage=10, image_path="images/green monster.png")
enemy3 = Enemy(name='enemy',x=700, y=500, width=50, height=50, speed=.3, health=50, armor=10, gun=0, character=player, damage=10, image_path="images/green monster.png")
enemy4 = Enemy(name='enemy',x=600, y=500, width=70, height=70, speed=.1, health=80, armor=10, gun=0, character=player, damage=40, image_path="images/green monster.png")
enemy5 = Enemy(name='enemy',x=300, y=300, width=50, height=50, speed=.4, health=40, armor=0, gun=0, character=player, damage=70, image_path="images/green monster.png")
enemies = [enemy1, enemy2, enemy3, enemy4, enemy5]
#Separate list including all enemies and main character, used for object collision
entities = [player]
for i in enemies:
    entities.append(i)



obj = Object(x=200, y=150, width=50, height=200, health=1000)
obj2 = Object(x=200, y=150, width=700, height=50, health=1000)
obj3 = Object(x=850, y=150, width=50, height=200, health=1000)
obj4 = Object(x=200, y=150, width=300, height=200, health=1000)
objs = [obj, obj2, obj3]
player2 = Character(name="mc",x=1100, y=100, width=10, height=100, speed=1, health=100, armor=50, gun=0,image_path="images/door.png")


r1 = Room(background_path="images/sandpixel.jpg",screen_width=1200,screen_height=700)

for i in enemies:
    r1.add_enemy(i)

for i in objs:
    r1.add_object(i)


door = Item(100,100,100,150,5000,"images/door.png")
r1.add_item(door)
door.bounce()



