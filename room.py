import pygame

class Room:
    def __init__(self, background_path, screen_width, screen_height):
        self.background_path = background_path
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        self.characters = []  # List to hold Character objects
        self.enemies = []  # List to hold Enemy objects
        self.objects = []  # List to hold Object objects
        self.weapons = []

    def add_character(self, character):
        character.room = self
        self.characters.append(character)

    def add_enemy(self, enemy):
        enemy.room = self
        self.enemies.append(enemy)

    def add_object(self, obj):
        obj.room = self
        self.objects.append(obj)

    def add_weapon(self, weapon):
        weapon.room = self
        self.weapons.append(weapon)

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw characters
        for character in self.characters:
            character.draw(screen)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)

        # Draw objects
        for obj in self.objects:
            obj.draw(screen)

        # Draw weapons
        for weapon in self.weapons:
            weapon.draw(screen)  # Assuming weapons have a draw method
