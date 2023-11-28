import pygame
from object import Object
from enemy import Enemy
from character import Character
from item import Item
from weapons import Weapon


class Room:
    """ Class for all Rooms, used to create, draw, and add to rooms. """
    def __init__(self, background_path, screen_width, screen_height):
        """
        Initialize a Room object.

        Args:
            background_path (str): Path to the background image for the room.
            screen_width (int): Width of the screen.
            screen_height (int): Height of the screen.
        """
        self.background_path = background_path
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.characters = []  # List to hold Character objects
        self.enemies = []  # List to hold Enemy objects
        self.objects = []  # List to hold Object objects
        self.weapons = []
        self.items = []
        self.entities = []
        self.door = None
        self.next_room = None
        self.starting_x = 0
        self.starting_y = 0

    def add_item(self, item):
        """
        Add an Item to the room.

        Args:
            item (Item): Item object to add to the room.
        """
        if isinstance(item, Item):
            item.room = self
            self.items.append(item)
        else:
            print("Error: Attempted to add an invalid item to the room.")

    def add_character(self, character):
        """
        Add a Character to the room.

        Args:
            character (Character): Character object to add to the room.
        """
        if isinstance(character, Character):
            character.room = self
            self.characters.append(character)
        else:
            print("Error: Attempted to add an invalid character to the room.")

    def add_enemy(self, enemy):
        """
        Add an Enemy to the room.

        Args:
            enemy (Enemy): Enemy object to add to the room.
        """
        if isinstance(enemy, Enemy):
            enemy.room = self
            self.enemies.append(enemy)
        else:
            print("Error: Attempted to add an invalid enemy to the room.")

    def add_object(self, obj):
        """
        Add an Object to the room.

        Args:
            obj (Object): Object to add to the room.
        """
        if isinstance(obj, Object):
            obj.room = self
            self.objects.append(obj)
        else:
            print("Error: Attempted to add an invalid object to the room.")

    def add_weapon(self, weapon):
        """
        Add a Weapon to the room.

        Args:
            weapon (Weapon): Weapon object to add to the room.
        """
        if isinstance(weapon, Weapon):
            weapon.room = self
            self.weapons.append(weapon)
        else:
            print("Error: Attempted to add an invalid weapon to the room.")

    def draw(self, screen):
        """
        Draw the room, along with its items, characters, enemies, objects, and weapons.

        Args:
            screen (pygame.Surface): The pygame screen surface on which to draw the room and objects.
        """
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

    def scale(self, prev_screen_width, prev_screen_height, new_screen_width, new_screen_height):
        self.background = pygame.transform.scale(self.background, (new_screen_width, new_screen_height))
        game_objects = self.items + self.characters + self.enemies + self.objects + self.weapons

        for element in game_objects:
            element.x = int(element.x * (new_screen_width / prev_screen_width))
            element.y = int(element.y * (new_screen_height / prev_screen_height))
