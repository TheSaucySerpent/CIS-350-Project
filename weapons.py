import pygame
import math
import random
from item import Item


class Weapon(Item):
    """ Class for all weapons, Parent of Shotgun """

    def __init__(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner, x, y, width,
                 height, screen_width, screen_height, image_path=None):
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
        x (int): The x position of the item.
        y (int): The y position of the item.
        width (int): The width of the item.
        height (height): The height of the item.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        image_path (str, optional): Path to the image for the weapon (default is None). This will be used in the future to display a weapon design.
        """
        super().__init__(name, x, y, width, height, screen_width, screen_height, image_path)

        # Validate input values
        if not isinstance(damage, int) or damage < 0:
            raise ValueError("Damage must be a non-negative integer.")

        if not (isinstance(proj_speed, int) or isinstance(proj_speed, float)) or proj_speed <= 0:
            raise ValueError("Projectile speed must be a positive integer.")

        if not (isinstance(attack_speed, int) or isinstance(attack_speed, float)) or attack_speed <= 0:
            raise ValueError("Attack speed must be a positive integer.")

        if not isinstance(mag_size, int) or mag_size <= 0:
            raise ValueError("Magazine size must be a positive integer.")

        if not isinstance(mag_count, int) or mag_count < 0:
            raise ValueError("Magazine count must be a non-negative integer.")

        if not isinstance(reload_speed, (int, float)) or reload_speed <= 0:
            raise ValueError("Reload speed must be a positive integer.")

        # Continue with the initialization
        self.owner = owner
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

    def attack(self, player):
        """
        Attack with the weapon.

        This method checks if enough time has passed since the last shot to fire again. If the owner is the player, it also
        checks if there is enough ammunition in the magazine. It then calculates the direction and creates a new
        projectile. The method updates the last attack time and decreases the magazine ammo.

        Args:
            player (Character): The player character of the game.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            if self.owner == player:
                if self.mag_ammo > 0:
                    direction = math.degrees(
                        math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y() - (.5 * self.owner.height),
                                   pygame.mouse.get_pos()[0] - self.owner.get_x() - (.5 * self.owner.width)))
                    projectile = Projectile(self.owner.get_x() + (.5 * self.owner.width),
                                            self.owner.get_y() + (.5 * self.owner.height), 10, 10, self.proj_speed,
                                            direction, self.damage)
                    self.projectiles.append(projectile)
                    self.mag_ammo -= 1
                    self.last_attack = current_time

                    # Assertions for testing
                    # self.projectiles = []
                    # self.mag_ammo = -1
                    # self.last_attack = 21
                    assert len(self.projectiles) > 0, "No projectile created"
                    assert self.mag_ammo >= 0, "Negative ammo count after attack"
                    assert current_time == self.last_attack, "Last attack time not updated correctly"
            else:
                print("No weapon owner?")

            # This is work towards enemies that can shoot. It's not completed because I was too busy doing everything
            # else.
            '''else:
                direction = math.degrees(math.atan2(self.owner.character.get_x() - self.owner.get_y(), self.owner.character.get_x() - self.owner.get_x()))
                projectile = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed, direction, self.damage)
                self.projectiles.append(projectile)
                self.last_attack = current_time'''

    def update_projectiles(self, player, current_room, screen_width, screen_height):
        """
        Move and update all active projectiles.

        This method updates the position of all active projectiles,
        and removes any projectiles that collide with something.

        Args:
            player (Character): The player character of the game.
            current_room (Room): The current room the player is in.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            if self.owner == player:
                if Projectile.projectile_out_of_bounds(projectile, screen_width,
                                                       screen_height) or Projectile.projectile_hits_enemy(
                        projectile, current_room) or Projectile.projectile_hits_object(projectile, current_room):
                    projectiles_to_remove.append(projectile)
            else:
                if Projectile.projectile_out_of_bounds(projectile, screen_width, screen_height) or \
                        Projectile.projectile_hits_player(projectile, player) \
                        or Projectile.projectile_hits_object(projectile, current_room):
                    projectiles_to_remove.append(projectile)

            # Add assertions for testing
            assert projectile.x >= -5, "Projectile x-coordinate is negative"  # Given 5 pixel buffer for time it takes to update
            assert projectile.y >= -5, "Projectile y-coordinate is negative"  # Given 5 pixel buffer for time it takes to update
            assert projectile.x < screen_width, "Projectile x-coordinate exceeds screen width"
            assert projectile.y < screen_height, "Projectile y-coordinate exceeds screen height"
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

        # Test Assertions
        # Needed to give it a 1 bullet buffer for if you reload at just the right time while firing
        assert self.mag_ammo == self.mag_size or self.mag_ammo == self.mag_size - 1, "Magazine ammo not filled to capacity"
        assert self.mag_count >= 0, "Magazine count cannot be negative"


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
        initial_x, initial_y = self.x, self.y  # Store initial position for assertion

        self.x += self.speed * math.cos(math.radians(self.direction))
        self.y += self.speed * math.sin(math.radians(self.direction))

        # Test to make sure the projectile moves
        assert self.x != initial_x or self.y != initial_y, "Projectile position not updated"

    def projectile_hits_enemy(self, current_room):
        """
        Checks for any collision with enemies. If collision, does projectile damage to the enemy and returns True

        Args:
            current_room (Room): The current room the player is in.

        Returns: Bool
        """
        for enemy in current_room.enemies:
            initial_health = enemy.health  # Store initial health for assertions
            if enemy.health > 0:
                if self.x < enemy.x + enemy.width and self.x + self.width > enemy.x \
                        and self.y < enemy.y + enemy.height and self.y + self.height > enemy.y:
                    enemy.take_damage(self.damage)
                    assert enemy.health < initial_health, "Enemy health not reduced after projectile hit"
                    return True

    def projectile_hits_object(self, current_room):
        """
        Checks for collision with objects. If collision, returns True.

        Args:
            current_room (Room): The current room that the player is in.

        Returns: Bool
        """
        if len(current_room.objects) > 0:
            for ob in current_room.objects:
                if self.x < ob.x + ob.width and self.x + self.width > ob.x \
                        and self.y < ob.y + ob.height and self.y + self.height > ob.y:
                    return True
                else:
                    x = False
            return x
        else:
            return False

    def projectile_hits_player(self, player):
        """
        This method is only used on enemy projectiles. It currently doesn't work properly. Will return True when
        collision with player is detected.

        Args:
             player (Character): The player character of the game.

        Returns: Bool
        """
        if self.x < player.x + player.width and self.x + self.width > player.width \
                and self.y < player.y + player.height and self.y + self.height > player.y:
            player.take_damage(10)
            return True

    def projectile_out_of_bounds(self, screen_width, screen_height):
        """
        Removes any projectiles That go off-screen.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.

        Returns: Bool
        """
        if 0 <= self.x <= screen_width - self.width and 0 <= self.y <= screen_height - self.height:
            return False
        else:
            return True


class Shotgun(Weapon):
    """ Child of Weapon with a different attack method """

    def __init__(self, name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner, spread,
                 proj_number, x, y, width, height, screen_width, screen_height, image_path):
        """
        Shotgun init function, essentially the same as it's Parent Weapon

        name (str): The name of the weapon.
        damage (int): How much damage the weapon does each hit.
        proj_speed (int): How fast the projectile from the weapon travels.
        attack_speed (int): How fast the gun fires.
        mag_size (int): The size of the gun magazine.
        mag_count (int): How many magazines remaining the gun has.
        reload_speed (int): How long it takes to reload.
        owner (Character): Who is holding the weapon.
        spread (int): Determines the degrees of spread in the shotgun.
        proj_number (int): Determines the number of pellets shot out of the shotgun.
        x (int): The x position of the weapon.
        y (int): The y position of the weapon.
        width (int): The width of the weapon.
        height (int): The height of the weapon.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        image_path (str): The path to the image for the weapon.
        """
        super().__init__(name, damage, proj_speed, attack_speed, mag_size, mag_count, reload_speed, owner, x, y, width,
                         height, screen_width, screen_height, image_path)
        self.spread = spread
        self.proj_number = proj_number

    def attack(self, player):
        """
        Handles shooting a weapon.

        Args:
            player (Character): The player of the game who is shooting the weapon.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= 1000 / self.attack_speed:
            if self.owner == player:
                if self.mag_ammo > 0:
                    direction = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.owner.get_y(),
                                                        pygame.mouse.get_pos()[0] - self.owner.get_x()))
                    # Set an upper and lower bound for the shotgun spread
                    dir_upper = direction + self.spread
                    dir_lower = direction - self.spread
                    # Create a projectile for all in proj_number
                    for p in range(self.proj_number):
                        # Randomly decide if it's going to the upper or lower bound
                        x = random.randint(0, 2)
                        if x == 0:
                            p = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed,
                                           round((random.uniform(direction, dir_lower)), 3), self.damage)
                        else:
                            p = Projectile(self.owner.get_x(), self.owner.get_y(), 10, 10, self.proj_speed,
                                           round((random.uniform(direction, dir_upper)), 3), self.damage)

                        self.projectiles.append(p)
                    self.mag_ammo -= 1
                    self.last_attack = current_time
