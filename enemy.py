import pygame
from character import Character

screen_width = 1200
screen_height = 700

class Enemy(Character):
    def __init__(self, x, y, width, height, speed, health, armor, gun, character, image_path=None):
        if not image_path:  # If no image path is provided, use a default one
            image_path = "green monster.png"
        super().__init__(x, y, width, height, speed, health, armor, gun, image_path)
        self.character = character

    def move_towards_character(self):
        dx = self.character.x - self.x
        dy = self.character.y - self.y
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude
        self.x += dx * self.speed
        self.y += dy * self.speed
