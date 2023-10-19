import pygame
import glob_var

class Object:
    def __init__(self, x, y, width, height, health, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Initialize the image attribute with None
        self.image = None

        if image_path:
            self.image_path = image_path
            self.load_image()

    def collision(self, character):
        # Draw objects & handle object collision
        for obj in glob_var.objs:
            for entity in glob_var.entities:
                entity_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
                if entity_rect.colliderect(obj.obj_rect):
                    # Left Border
                    if entity.x + entity.width < obj.x + 2:
                        entity.x -= 1
                    # Right Border
                    elif entity.x > obj.x + obj.width - 2:
                        entity.x += 1
                    # Upper Border
                    elif entity.y < obj.y:
                        entity.y -= 1
                    # Lower Board
                    elif entity.y > obj.y:
                        entity.y += 1

    def load_image(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))
