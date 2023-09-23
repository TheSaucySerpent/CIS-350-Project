import pygame
from character import Character
import glob_var
screen_width = 1200
screen_height = 700



class Enemy(Character):
    def __init__(self, name, x, y, width, height, speed, health, armor, gun, character, damage):
        super().__init__(name, x, y, width, height, speed, health, armor, gun)
        self.character = character
        self.damage = damage

    def move_towards_character(self):
        # Calculate the direction towards the character
        dx = self.character.x - self.x
        dy = self.character.y - self.y

        # Normalize the direction vector
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if self.gun == 0:
            if magnitude != 0:
                dx /= magnitude
                dy /= magnitude

            # Update the enemy's position based on the direction
            self.x += dx * self.speed
            self.y += dy * self.speed

            if glob_var.player.get_x() < self.x + self.width - 10 and glob_var.player.get_x() + glob_var.player.width > self.x \
                    and glob_var.player.get_y() < self.y + self.height - 10 and glob_var.player.get_y() + glob_var.player.height > self.y:
                # Characters are colliding, player takes damage
                glob_var.player.take_damage(self.damage)
        '''else:
            if magnitude > 400:
                dx /= magnitude
                dy /= magnitude

                # Update the enemy's position based on the direction
                self.x += dx * self.speed
                self.y += dy * self.speed
            else:
                self.gun.attack()'''


