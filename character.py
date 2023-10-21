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
        self.max_health = 100
        self.armor = armor
        self.gun = gun
        self.last_hurt = 0
        self.last_dodge = 0
        self.invulnerable = False
        self.image_index = 0
        self.image = None
        self.picked_up = False
        self.inventory = []

        self.image_path = {
            'up': ['images/Up standing.png', 'images/Up running.png'],
            'down': ['images/Down standing.png', 'images/Down running.png'],
            'left': ['images/Left standing.png', 'images/Left running .png'],
            'right': ['images/1.png', 'images/BackgroundEraser_image.png']
            }

        self.direction = 'down'
        self.image_change_delay = 100  # Delay between frame changes
        self.frame_count = 0

        if self.image_path:
            self.load_images()
            # Load the initial image
            self.image = self.images[self.direction][0]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def load_images(self):
        self.images = {}
        for direction, paths in self.image_path.items():
            self.images[direction] = [pygame.image.load(path) for path in paths]

    def set_image(self, direction):
        if direction in self.images:
            # Check the timer
            if self.frame_count >= self.image_change_delay:
                self.image_index = (self.image_index + 1) % len(self.images[direction])
                self.frame_count = 0  # Reset frame_count
                self.image = self.images[direction][self.image_index]
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            else:
                self.frame_count += 1

    def move(self, keys, extra_speed, is_invulnerable=False):
        new_x = self.x
        new_y = self.y

        if is_invulnerable:
            self.invulnerable = True

        direction = None  # Store the current movement direction

        if keys[pygame.K_w]:
            new_y -= self.speed + extra_speed
            direction = 'up'
        if keys[pygame.K_a]:
            new_x -= self.speed + extra_speed
            direction = 'left'
        if keys[pygame.K_s]:
            new_y += self.speed + extra_speed
            direction = 'down'
        if keys[pygame.K_d]:
            new_x += self.speed + extra_speed
            direction = 'right'

        if direction:
            self.set_image(direction)  # Set the character's image based on the current direction

        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            self.x = new_x
            self.y = new_y

        self.invulnerable = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

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
                self.y + self.height > item.y) and keys[pygame.K_e]:
                # Add the object to the character's inventory
                self.inventory.append(item)
                # Remove the object from the list of objects in the room
                current_room.items.remove(item)

    def update_position(self):
        # Update the object's position to the character inventory if it's picked up
        for item in self.inventory:
            item.x = self.x
            item.y = self.y + self.height
