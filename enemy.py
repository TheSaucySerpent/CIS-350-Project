import random
import pygame
from character import Character


class Enemy(Character):
    """ Class for all Enemy Characters. Inherits from Character. """
    def __init__(self, name, x, y, width, height, speed, health, armor, gun, character, damage, image_path=None):
        """
        Args:
        name (str): The name of the enemy.
        x (int): The x-coordinate of the enemy's position.
        y (int): The y-coordinate of the enemy's position.
        width (int): The width of the enemy.
        height (int): The height of the enemy.
        speed (int): The movement speed of the enemy.
        health (int): The health of the enemy.
        armor (int): The armor rating of the enemy.
        gun (Weapon): The type of gun the enemy wields.
        character: The player character (or target) that the enemy is moving towards.
        damage (int): The damage dealt by the enemy.
        image_path (str, optional): Path to the image for the enemy (default is None).
        """
        super().__init__(name, x, y, width, height, speed, health, armor, gun)
        if character.name != 'Player':
            raise ValueError("self.character must always be glob_var.player")
        if damage < 0:
            raise ValueError("Damage must be a non-negative integer.")
        self.character = character
        self.damage = damage
        self.image_path = image_path

        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move_towards_character(self, player, screen_width, screen_height):
        """
        Moves the enemy towards the player. Will be edited when enemy weapons are added.
        Calculates the direction vector toward the target character, normalizes it, and updates the enemy's
        position based on speed and direction.
        Checks for collisions with the target character and deals damage
        to the target character if they collide.
        """
        # Calculate the direction towards the character
        dx = self.character.x - self.x
        dy = self.character.y - self.y

        # Normalize the direction vector, thanks internet
        magnitude = (dx ** 2 + dy ** 2) ** 0.5

        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Create a rectangle representing the new position
        entity_rect = pygame.Rect(new_x, new_y, self.width, self.height)

        # Check for collisions with the player
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)

        if entity_rect.colliderect(player_rect):
            initial_player_health = player.health
            # Characters are colliding, player takes damage
            player.take_damage(self.damage)
            # Add assertions for testing
            assert player.health <= initial_player_health, "Player health not reduced after collision"

        # Check if the new position is within the screen bounds
        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        """
        Draw the enemy character on the screen.
        If an image is available, it is drawn. Otherwise, a blue rectangle is drawn in its place.

        Args:
            screen (pygame.Surface): The pygame screen surface on which to draw the enemy.
        """
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))


class Default(Enemy):
    """
    A prebuilt instance of enemy, used for efficiently adding enemies to the first 3 levels
    """
    def __init__(self, name, x, y, player):
        super().__init__(name=name, x=x, y=y, width=50, height=50, speed=.3, health=50, armor=10, gun=0, character=player, damage=10, image_path="images/green monster.png")


class Tank(Enemy):
    """
    A prebuilt instance of enemy, used for efficiently adding enemies to the first 3 levels
    """
    def __init__(self, name, x, y, player):
        super().__init__(name=name, x=x, y=y, width=85, height=68, speed=.1, health=80, armor=10, gun=0, character=player, damage=60, image_path="images/SentryCrab.png")


class Runner(Enemy):
    """
    A prebuilt instance of enemy, used for efficiently adding enemies to the first 3 levels
    """
    def __init__(self, name, x, y, player):
        super().__init__(name=name, x=x, y=y, width=30, height=30, speed=.45, health=40, armor=0, gun=0, character=player, damage=40, image_path="images/slime.png")
