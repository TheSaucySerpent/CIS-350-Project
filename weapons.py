import pygame
import math
import glob_var
from item import Item
screen_width = 1200
screen_height = 700


class Weapon(Item):
    def __init__(self, name, damage, proj_speed, attack_speed, ammo, ammo_cost, owner, melee=False):
        super().__init__(name, owner)
        self.damage = damage
        self.attack_speed = attack_speed
        self.proj_speed = proj_speed
        self.ammo = ammo
        # ammo_cost is how much ammo is subtracted with each shot, easier than having ammo types
        self.ammo_cost = ammo_cost
        self.melee = melee
        self.last_attack = 0
        self.projectiles = []

    def attack(self):
        # Check if enough time has passed since the last shot to fire again
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            # Obviously there is work to do here, need to implement melee and enemy attack setup
            if self.owner == glob_var.mc:
                if not self.melee:
                    if self.ammo > 0:
                        direction = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y(), pygame.mouse.get_pos()[0] - self.owner.get_x()))
                        projectile = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, direction, self.damage)
                        self.projectiles.append(projectile)
                        self.ammo -= self.ammo_cost
                        self.last_attack = current_time

    def update_projectiles(self):
        # Move and update all active projectiles
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            if Projectile.projectile_out_of_bounds(projectile) or Projectile.projectile_hits_enemy(projectile) or Projectile.projectile_hits_object(projectile):
                projectiles_to_remove.append(projectile)
        # Remove projectiles that are out of bounds or hit something
        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)


class Projectile:
    def __init__(self, x, y, width, height, speed, direction, damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.damage = damage

    def move(self):
        # Update the projectile's position based on its direction and speed
        self.x += self.speed * math.cos(math.radians(self.direction))
        self.y += self.speed * math.sin(math.radians(self.direction))

    def projectile_hits_enemy(self):
        for enemy in glob_var.enemies:
            if enemy.health > 0:
                if self.x < enemy.x + enemy.width and self.x + self.width > enemy.x \
                   and self.y < enemy.y + enemy.height and self.y + self.height > enemy.y:
                    enemy.take_damage(self.damage)
                    return True

    def projectile_hits_object(self):
        for ob in glob_var.objs:
            if self.x < ob.x + ob.width and self.x + self.width > ob.x \
                    and self.y < ob.y + ob.height and self.y + self.height > ob.y:
                return True
            else:
                return False

    def projectile_out_of_bounds(self):
        if 0 <= self.x <= screen_width - self.width and 0 <= self.y <= screen_height - self.height:
            return False
        else:
            return True
