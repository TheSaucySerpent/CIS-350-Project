import pygame
import glob_var


class Object:
    """
    The class used for all objects in the game. Specifically, any static with collision is classified as an object.
    """

    def __init__(self, x, y, width, height, health, image_path=None):
        """
        Initialize an Object.

        Args:
            x (int): The x-coordinate of the object.
            y (int): The y-coordinate of the object.
            width (int): The width of the object.
            height (int): The height of the object.
            health (int): The health of the object. This may be built upon to implement object destruction in a future update.
            image_path (str): The path to the image for the object.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = None

        if image_path:
            self.image_path = image_path
            self.load_image()

    def collision(self):
        """
        Handle collision between objects and entities using pygame's built-in rectangle collision functions.
        Adds or subtracts from the entity's x and y values corresponding to the direction in which they collide.
        """
        for entity in glob_var.cur_room.entities:
            entity_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
            if entity_rect.colliderect(self.obj_rect):
                # Left Border
                if entity.x + entity.width < self.x + 2:
                    entity.x -= 1
                # Right Border
                elif entity.x > self.x + self.width - 2:
                    entity.x += 1
                # Upper Border
                elif entity.y < self.y:
                    entity.y -= 1
                # Lower Board
                elif entity.y > self.y:
                    entity.y += 1

    def load_image(self):
        """
        Load and scale the image for the object.

        This method loads an image specified by the image_path and scales it to the object's width and height.
        """
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        """
        Draw the object on the screen.

        Args:
            screen: The screen to draw the object on.
        """
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (30, 30, 30), (self.x, self.y, self.width, self.height))


class Door(Object):
    def __init__(self, x, y, width, height, health, image_path):
        super().__init__(x, y, width, height, health, image_path)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def collision(self):
        player_rect = pygame.Rect(glob_var.player.x, glob_var.player.y, glob_var.player.width, glob_var.player.height)
        for item in glob_var.player.inventory:
            if self.rect.colliderect(player_rect) and item.name == 'Key':
                return True
        return False
