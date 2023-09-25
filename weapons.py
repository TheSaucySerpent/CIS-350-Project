import pygame
import math
import random
import glob_var
from item import Item
screen_width = 1200
screen_height = 700


class Weapon(Item):
    def __init__(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner, room=None):
        super().__init__(name, owner)
        self.damage = damage
        self.attack_speed = attack_speed
        self.proj_speed = proj_speed
        self.mag_size = mag_size
        self.mag_ammo = mag_size
        self.mag_count = mag_count
        self.reload_speed = reload_speed
        self.last_attack = 0
        self.last_reload = 0
        self.projectiles = []
        self.room = room

    def draw(self, screen):
        if hasattr(self, 'image') and self.image:
            screen.blit(self.image, (self.owner.x, self.owner.y))
        else:
            # Draw a placeholder for the weapon if no image is set
            pygame.draw.rect(screen, (255, 0, 0), (self.owner.x, self.owner.y, 50, 50))

    def attack(self):
        # Check if enough time has passed since the last shot to fire again
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            # Obviously there is work to do here, need to implement melee and enemy attack setup
            if self.owner == glob_var.mc:
                if self.mag_ammo > 0:
                    direction = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y(), pygame.mouse.get_pos()[0] - self.owner.get_x()))
                    projectile = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, direction, self.damage)
                    self.projectiles.append(projectile)
                    self.mag_ammo -= 1
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

    def reload(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_reload > 10000 / self.reload_speed:
            if self.mag_count > 0:
                print("Reloading!")
                self.mag_ammo = self.mag_size
                self.mag_count -= 1
                self.last_reload = current_time
            else:
                print("Out of Mags")
                self.last_reload = current_time



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
                x = False
        return x

    def projectile_out_of_bounds(self):
        if 0 <= self.x <= screen_width - self.width and 0 <= self.y <= screen_height - self.height:
            return False
        else:
            return True




class Shotgun(Weapon):
    def __init__(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner, spread, proj_number):
        super().__init__(name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner)
        self.spread = spread
        self.proj_number = proj_number

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            if self.owner == glob_var.mc:
                if self.mag_ammo > 0:
                    direction = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y(), pygame.mouse.get_pos()[0] - self.owner.get_x()))
                    #I don't know how to explain this just look at it and think
                    dir_upper = direction + self.spread
                    dir_lower = direction - self.spread
                    for p in range(self.proj_number):
                        x = random.randint(0, 2)
                        if x == 0:
                            p = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, round((random.uniform(direction, dir_lower)),3), self.damage)
                        else:
                            p = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, round((random.uniform(direction, dir_upper)),3), self.damage)

                        self.projectiles.append(p)
                    self.mag_ammo -= 1
                    self.last_attack = current_time