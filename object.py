import pygame
#Needed for game to run, in theory we could make character be a child of object

class Object:
    def __init__(self, x, y, width, height, health,image_path = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image_path = image_path

    def draw(self, screen):
        if self.image_path:
            # Load and blit the image if an image path is provided
            obj_image = pygame.image.load(self.image_path)
            screen.blit(obj_image, (self.x, self.y))
        else:
            # Draw a rectangle if no image path is provided
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))

