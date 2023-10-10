import pygame
from object import Object
from enemy import Enemy
from character import Character
from item import Item
from weapons import Weapon

class Room:
    def __init__(self, background_path, screen_width, screen_height):
        self.background_path = background_path
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.characters = []  # List to hold Character objects
        self.enemies = []  # List to hold Enemy objects
        self.objects = []  # List to hold Object objects
        self.weapons = []
        self.items = []

    def add_item(self, item):
        if isinstance(item, Item):
            item.room = self
            self.items.append(item)
        else:
            print("Error: Attempted to add an invalid item to the room.")

    def add_character(self, character):
        if isinstance(character, Character):
            character.room = self
            self.characters.append(character)
        else:
            print("Error: Attempted to add an invalid character to the room.")

    def add_enemy(self, enemy):
        if isinstance(enemy, Enemy):
            enemy.room = self
            self.enemies.append(enemy)
        else:
            print("Error: Attempted to add an invalid enemy to the room.")

    def add_object(self, obj):
        if isinstance(obj, Object):
            obj.room = self
            self.objects.append(obj)
        else:
            print("Error: Attempted to add an invalid object to the room.")

    def add_weapon(self, weapon):
        if isinstance(weapon, Weapon):
            weapon.room = self
            self.weapons.append(weapon)
        else:
            print("Error: Attempted to add an invalid weapon to the room.")

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        for item in self.items:
            item.draw(screen)

        for character in self.characters:
            character.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for obj in self.objects:
            obj.draw(screen)

        for weapon in self.weapons:
            weapon.draw(screen)
