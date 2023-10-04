import pygame
from character import Character
import glob_var
import game_functions as gf

screen_width = 1200
screen_height = 700

class Enemy(Character):
    def __init__(self, name, x, y, width, height, speed, health, armor, gun, character, damage, image_path=None):
        super().__init__(name, x, y, width, height, speed, health, armor, gun)
        self.character = character
        self.damage = damage
        self.image_path = image_path

        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move_towards_character(self):
        # Calculate the direction towards the character
        dx = self.character.x - self.x
        dy = self.character.y - self.y

        # Normalize the direction vector
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
            # Check for collisions with objects
            for obj in gf.current_room.objects:
                if entity_rect.colliderect(obj.obj_rect):
                    # Handle collision with the object
                    # You can add collision handling logic here as needed.
                    # For now, we'll just skip the movement.
                    return

            # Update the position if there are no collisions
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))