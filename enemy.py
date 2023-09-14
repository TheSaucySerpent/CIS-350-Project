import pygame
from character import Character
screen_width = 1200
screen_height = 700

class Enemy():
    def __init__(self, x, y, width, height, speed, health, armor, character):
        self.x = x
        self. y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.armor = armor
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


    def take_damage(self, damage):
        extra_damage = 0
        if self.armor > 0:
            self.armor -= damage
            if self.armor < 0:
                extra_damage = self.armor * -1
                self.armor = 0
        if extra_damage > 0:
            self.health -= extra_damage
        else:
            self.health -= damage
