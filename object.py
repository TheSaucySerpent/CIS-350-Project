import pygame


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

    def load_image(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))
