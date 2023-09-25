from character import Character
from weapons import Weapon
from weapons import Shotgun
from enemy import Enemy
from object import Object
from room import Room


image_paths = {
    'up': ['Up standing.png', 'Up running.png'],
    'down': ['Down standing.png', 'Down running.png'],
    'left': ['Left standing.png', 'Left running .png'],
    'right': ['1.png', 'BackgroundEraser_image.png']
}

mc = Character(x=1100, y=100, width=100, height=100, speed=1, health=100, armor=50, gun=0, image_path=image_paths)

# (self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner)
pistol = Weapon(name="Pistol", damage=10, proj_speed=.5, attack_speed=2, mag_size=9,
                mag_count=3, reload_speed=10, owner=mc)
ar = Weapon(name="Assault Rifle", damage=15, proj_speed=1, attack_speed=5, mag_size=30,
            mag_count=2, reload_speed=20, owner=mc)
dev_gun = Weapon("God's Draco", 100, 5, 50, 10000, 1, 10, mc)
#shotgun adds spread and number of projectiles
shotgun = Shotgun(name="Pump Shotgun", damage=20, proj_speed=1, attack_speed=2, mag_size=8,
                  mag_count=2, reload_speed=15, owner=mc, spread=25, proj_number=8)
dev_shotgun = Shotgun("God's Sawed-Off", 50, 5, 10, 1000, 1, 10, mc, 20, 30)

guns = [pistol, ar, dev_gun, shotgun, dev_shotgun]

#Debug change gun
mc.gun = dev_shotgun


enemy1 = Enemy(x=700, y=200, width=50, height=50, speed=.1, health=50, armor=10, gun=pistol, character=mc)

enemy12 = Enemy(20,34,34,34,0.5,99,88,7,mc,"green monster.png")
enemy2 = Enemy(x=500, y=500, width=50, height=50, speed=.01, health=50, armor=10, gun=pistol, character=mc)
enemy3 = Enemy(x=700, y=500, width=50, height=50, speed=.03, health=50, armor=10, gun=pistol, character=mc)

enemies = [enemy1, enemy2, enemy3]


table = Object(x=200, y=200, width=100, height=100, health=1000,image_path="table.png")
door = Object(x=1075, y=280, width=200, height=200, health=1000,image_path="door.png")
golden_key = Object(800,200,100,100,999,"golden key.png")

objs_1 = [table,door,golden_key]

room1 = Room("sandpixel.jpg",screen_width=1200,screen_height=700)

room1.add_enemy(enemy1)
room1.add_object(door)
room1.add_object(table)
room1.add_object(golden_key)
room1.add_enemy(enemy12)
room1.add_enemy(enemy3)

room2 = Room("columbus city.jpg",screen_width=1200,screen_height=700)
room2.add_character(mc)
room2.add_enemy(enemy2)