import pygame
import game_functions as gf
import tkinter as tk
from tkinter import Label, Frame, Toplevel, font , Button

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
root = tk.Tk()
root.withdraw()
class Character:
    def __init__(self, name, x, y, width, height, speed, health, armor, gun, image_path=None):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.max_health = 100  # VALUE WE WANT FOR MAX HEALTH
        self.armor = armor
        self.gun = gun
        self.last_hurt = 0
        self.last_dodge = 0
        self.invulnerable = False
        self.image_path = image_path
        self.picked_up = False
        self.inventory = []

        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def move(self, keys, extra_speed, is_invulnerable=False):
        new_x = self.x
        new_y = self.y

        if is_invulnerable:
            self.invulnerable = True

        if keys[pygame.K_w]:
            new_y -= self.speed + extra_speed
        if keys[pygame.K_a]:
            new_x -= self.speed + extra_speed
        if keys[pygame.K_s]:
            new_y += self.speed + extra_speed
        if keys[pygame.K_d]:
            new_x += self.speed + extra_speed

        # Check if the new position is wit
            # Update the position if there are no collisions
        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            # Check for collisions with objects

            # Update the position if there are no collisions
            self.x = new_x
            self.y = new_y

        self.invulnerable = False

    def take_damage(self, damage):
        if not self.invulnerable:
            current_time = pygame.time.get_ticks()
            if self.name == 'Player':
                #To change invulnerability time, change value of 300
                if current_time - self.last_hurt > 300:
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
                    if self.health < 0:
                        self.health = 0
                    self.last_hurt = current_time
            else:
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
                if self.health < 0:
                    self.health = 0

    def heal(self, amount):
        if self.health >= self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def pick_up(self, current_room):
        # Check if the character is on top of any objects and the 'P' key is pressed
        keys = pygame.key.get_pressed()
        items = current_room.items.copy()  # Make a copy of the items in the room to avoid modifying the original list while iterating
        for item in items:
            if (self.x < item.x + item.width and
                self.x + self.width > item.x and
                self.y < item.y + item.height and
                self.y + self.height > item.y) and keys[pygame.K_p]:
                # Add the object to the character's inventory
                self.inventory.append(item)
                # Remove the object from the list of objects in the room
                current_room.items.remove(item)

    def update_position(self):
        # Update the object's position to the character inventory if it's picked up
        for item in self.inventory:
            item.x = self.x
            item.y = self.y + self.height

