import pygame
from character import Character
screen_width = 1200
screen_height = 700

#Now a child of Character, this way they can have guns. move_towards_character should be heavily adjusted to account for firearms

class Enemy(Character):
    def __init__(self, x, y, width, height, speed, health, armor, gun, character):
        super().__init__(x, y, width, height, speed, health, armor, gun)
        self.character = character

    def move_towards_character(self):
        # Calculate the direction towards the character
        dx = self.character.x - self.x
        dy = self.character.y - self.y

        # Normalize the direction vector
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        # Update the enemy's position based on the direction
        self.x += dx * self.speed
        self.y += dy * self.speed


