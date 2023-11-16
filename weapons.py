import pygame
import math
import random
import glob_var


class Weapon:
    """ Class for all weapons, Parent of Shotgun """
    def __init__(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner,image_path = None):
        """
        Init for Weapon

        Args:
        name (str): The name of the weapon.
        damage (int): The damage dealt by the weapon.
        proj_speed (int): The projectile speed of the weapon.
        attack_speed (int): The rate of fire for the weapon (attacks per second).
        mag_size (int): The magazine size of the weapon.
        mag_count (int): The number of magazines the weapon has.
        reload_speed (int): The reload speed of the weapon.
        owner: The entity (e.g., player or enemy) that owns the weapon.
        image_path (str, optional): Path to the image for the weapon (default is None). This will be used in the future to display a weapon design.
        """
        self.owner = owner
        self.name = name
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
        self.image_path = image_path

    def attack(self):
        """
        Attack with the weapon.

        This method checks if enough time has passed since the last shot to fire again. If the owner is the player, it also
        checks if there is enough ammunition in the magazine. It then calculates the direction and creates a new
        projectile. The method updates the last attack time and decreases the magazine ammo.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            if self.owner == glob_var.player:
                if self.mag_ammo > 0:
                    direction = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y(), pygame.mouse.get_pos()[0] - self.owner.get_x()))
                    projectile = Projectile(self.owner.get_x() + (.5 * self.owner.width), self.owner.get_y() + (.5 * self.owner.height), 10, 10, self.proj_speed, direction, self.damage)
                    self.projectiles.append(projectile)
                    self.mag_ammo -= 1
                    self.last_attack = current_time
            # This is work towards enemies that can shoot. It's not completed for the presentation.
            '''else:
                direction = math.degrees(math.atan2(self.owner.character.get_x() - self.owner.get_y(), self.owner.character.get_x() - self.owner.get_x()))
                projectile = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, direction, self.damage)
                self.projectiles.append(projectile)
                self.last_attack = current_time'''

    def update_projectiles(self, screen_width, screen_height):
        """
        Move and update all active projectiles.

        This method updates the position of all active projectiles, and removes any projectiles that collide with something.
        """
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            if self.owner == glob_var.player:
                if Projectile.projectile_out_of_bounds(projectile, screen_width, screen_height) or Projectile.projectile_hits_enemy(projectile) or Projectile.projectile_hits_object(projectile):
                    projectiles_to_remove.append(projectile)
            else:
                if Projectile.projectile_out_of_bounds(projectile, screen_width, screen_height) or Projectile.projectile_hits_player(projectile) or Projectile.projectile_hits_object(projectile):
                    projectiles_to_remove.append(projectile)
        # Remove projectiles that are out of bounds or hit something
        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

    def reload(self):
        """
        Reload the weapon.

        This method checks if enough time has passed since the last reload to reload the weapon. If there are magazines
        remaining, it reloads the weapon by filling the magazine ammo and decreases the magazine count.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_reload > 10000 / self.reload_speed:
            if self.mag_count > 0:
                if self.mag_ammo != self.mag_size:
                    print("Reloading!")
                    self.mag_ammo = self.mag_size
                    self.mag_count -= 1
                    self.last_reload = current_time
            else:
                print("Out of Mags")
                self.last_reload = current_time

    def addAmmo(self):
        """ Debug for adding ammo, will be an item drop later"""

        self.mag_count += 1


class Projectile:
    """ Class used for all projectiles sent out from all weapons. """
    def __init__(self, x, y, width, height, speed, direction, damage):
        """
        Args:
        x (int): The x-coordinate of the projectile's position.
        y (int): The y-coordinate of the projectile's position.
        width (int): The width of the projectile.
        height (int): The height of the projectile.
        speed (int): The speed of the projectile.
        direction (float): The direction in degrees in which the projectile is traveling.
        damage (int): The damage dealt by the projectile.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.damage = damage

    def move(self):
        """ Update the projectile's position based on its direction and speed """
        self.x += self.speed * math.cos(math.radians(self.direction))
        self.y += self.speed * math.sin(math.radians(self.direction))

    def projectile_hits_enemy(self):
        """
        Checks for any collision with enemies. If collision, does projectile damage to the enemy and returns True
        :return: Bool
        """
        for enemy in glob_var.enemies:
            if enemy.health > 0:
                if self.x < enemy.x + enemy.width and self.x + self.width > enemy.x \
                   and self.y < enemy.y + enemy.height and self.y + self.height > enemy.y:
                    enemy.take_damage(self.damage)
                    return True

    def projectile_hits_object(self):
        """
        Checks for collision with objects. If collision, returns True.
        :return: Bool
        """
        for ob in glob_var.objs:
            if self.x < ob.x + ob.width and self.x + self.width > ob.x \
                    and self.y < ob.y + ob.height and self.y + self.height > ob.y:
                return True
            else:
                x = False
        return x

    def projectile_hits_player(self):
        """
        This method is only used on enemy projectiles. It currently doesn't work properly. Will return True when collision with player is detected.
        :return: Bool
        """
        if self.x < glob_var.player.x + glob_var.player.width and self.x + self.width > glob_var.player.width \
            and self.y < glob_var.player.y + glob_var.player.height and self.y + self.height > glob_var.player.y:
            glob_var.player.take_damage(10)
            return True

    def projectile_out_of_bounds(self, screen_width, screen_height):
        """
        Removes any projectiles That go off-screen.
        :return: Bool
        """
        if 0 <= self.x <= screen_width - self.width and 0 <= self.y <= screen_height - self.height:
            return False
        else:
            return True


class Shotgun(Weapon):
    """ Child of Weapon with a different attack method """
    def __init__(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner, spread, proj_number):
        """
        Shotgun init function, essentially the same as it's Parent Weapon

        spread (int): Determines the degrees of spread in the shotgun.
        proj_number (int): Determines the number of pellets shot out of the shotgun.
        """
        super().__init__(name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner)
        self.spread = spread
        self.proj_number = proj_number

    def attack(self):
        """
        See Weapon.attack for more details. Primary differences in comments:
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            if self.owner == glob_var.player:
                if self.mag_ammo > 0:
                    direction = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y(), pygame.mouse.get_pos()[0] - self.owner.get_x()))
                    # Set an upper and lower bound for the shotgun spread
                    dir_upper = direction + self.spread
                    dir_lower = direction - self.spread
                    # Create a projectile for all in proj_number
                    for p in range(self.proj_number):
                        # Randomly decide if it's going to the upper or lower bound
                        x = random.randint(0, 2)
                        if x == 0:
                            p = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, round((random.uniform(direction, dir_lower)),3), self.damage)
                        else:
                            p = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, round((random.uniform(direction, dir_upper)),3), self.damage)

                        self.projectiles.append(p)
                    self.mag_ammo -= 1
                    self.last_attack = current_time