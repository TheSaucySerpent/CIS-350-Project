from character import Character
from weapons import Weapon
from enemy import Enemy
from object import Object

#Make sure new weapons are in the guns list or they won't work
#name, damage, proj_speed, attack_speed, ammo, ammmo_cost, melee=False
pistol = Weapon("Pistol", 10, .5, 2, 1000, 2)
ar = Weapon("Assault Rifle", 15, 1, 5, 1000, 1)
dev_gun = Weapon("God's Draco", 100, 5, 50, 10000, 0)
guns = [pistol, ar, dev_gun]


mc = Character(x=100, y=100, width=50, height=50, speed=.5, health=100, armor=50, gun=dev_gun)


#               x,   y, width, height, speed, health, armor, gun, character
enemy =  Enemy(500, 500, 50, 50, .25, 50, 10, pistol, mc)
enemy2 = Enemy(700, 200, 50, 50, .25, 50, 10, pistol, mc)
enemies = [enemy, enemy2]

#x, y, width, height, health
obj = Object(200, 200, 50, 50, 1000)
objs = [obj]
