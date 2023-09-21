from character import Character
from weapons import Weapon
from weapons import Shotgun
from enemy import Enemy
from object import Object

#If there's a better way to do this please share this file looks goofy
#If you want to add weapons, enemies and objects, add them to the corresponding list


#guns need an owner so this needs to be above it, but characters need a gun so it needs to be added after
mc = Character(x=100, y=100, width=50, height=50, speed=.5, health=100, armor=50, gun=0)

#(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner)
pistol = Weapon(name="Pistol", damage=10, proj_speed=.5, attack_speed=2, mag_size=9, mag_count=3, reload_speed=10, owner=mc)
ar = Weapon(name="Assault Rifle", damage=15, proj_speed=1, attack_speed=5, mag_size=30, mag_count=2, reload_speed=20, owner=mc)
dev_gun = Weapon("God's Draco", 100, 5, 50, 10000, 1, 10, mc)
#shotgun adds spread and number of projectiles
shotgun = Shotgun(name="Pump Shotgun", damage=20, proj_speed=1, attack_speed=2, mag_size=8, mag_count=2, reload_speed=15, owner=mc, spread=25, proj_number=8)
dev_shotgun = Shotgun("God's Sawed-Off", 50, 5, 10, 1000, 1, 10, mc, 20, 30)

guns = [pistol, ar, dev_gun, shotgun, dev_shotgun]

#Debug change gun
mc.gun = dev_shotgun


enemy1 = Enemy(x=700, y=200, width=50, height=50, speed=.2, health=50, armor=10, gun=pistol, character=mc)
enemy2 = Enemy(x=500, y=500, width=50, height=50, speed=.25, health=50, armor=10, gun=pistol, character=mc)
enemy3 = Enemy(x=700, y=500, width=50, height=50, speed=.3, health=50, armor=10, gun=pistol, character=mc)
enemies = [enemy1, enemy2, enemy3]



obj = Object(x=200, y=200, width=50, height=50, health=1000)
obj2 = Object(x=500, y=200, width=100, height=50, health=1000)
objs = [obj, obj2]
