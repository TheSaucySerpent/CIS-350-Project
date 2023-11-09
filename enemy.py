from random import random

import pygame
import random
from character import Character
import glob_var
import game_functions as gf
# from main import screen_width, screen_height

screen_width = 1200
screen_height = 700


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
        self.character = character
        self.damage = damage
        self.image_path = image_path

        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move_towards_character(self):
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
        player_rect = pygame.Rect(glob_var.player.x, glob_var.player.y, glob_var.player.width, glob_var.player.height)

        if entity_rect.colliderect(player_rect):
            # Characters are colliding, player takes damage
            glob_var.player.take_damage(self.damage)

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
    def __init__(self):
        super().__init__(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600), width=50, height=50, speed=.25, health=50, armor=10, gun=0, character=glob_var.player, damage=10, image_path="images/green monster.png")


class Tank(Enemy):
    def __init__(self):
        super().__init__(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600), width=70, height=70, speed=.1, health=80, armor=10, gun=0, character=glob_var.player, damage=40, image_path="images/green monster.png")


class Runner(Enemy):
    def __init__(self):
        super().__init__(name='enemy',x=random.randint(400, 800), y=random.randint(200, 600), width=30, height=30, speed=.4, health=40, armor=0, gun=0, character=glob_var.player, damage=70, image_path="images/green monster.png")