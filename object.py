import pygame


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
            health (int): The health of the object, ended up unused
            image_path (str): The path to the image for the object.
        """
        if not isinstance(x, (int)) or 0 > x > 1200:
            raise ValueError("X-coordinate must be a numeric value within bounds.")

        if not isinstance(y, (int)) or 0 > y > 700:
            raise ValueError("Y-coordinate must be a numeric value within bounds.")

        if not isinstance(width, (int)) or width <= 0:
            raise ValueError("Width must be a positive numeric value.")

        if not isinstance(height, (int)) or height <= 0:
            raise ValueError("Height must be a positive numeric value.")

        if not isinstance(health, int) or health < 0:
            raise ValueError("Health must be a non-negative integer.")

        # Additional checks
        if image_path is not None:
            if not isinstance(image_path, str):
                raise ValueError(f"Invalid image file path: {image_path}")

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

    def collision(self, player, entities):
        """
        Handle collision between objects and entities using pygame's built-in rectangle collision functions.
        Adds or subtracts from the entity's x and y values corresponding to the direction in which they collide.

        Args:
            player (Character):  The player character.
            entities (list): list of entities in the current room.
        """
        for entity in entities:
            entity_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
            if entity_rect.colliderect(self.obj_rect):
                initial_x, initial_y = entity.x, entity.y
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

                # Test to make sure it moved entity
                assert (initial_x, initial_y) != (entity.x, entity.y), "Entity position not updated after collision"

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
    """
    Door Class, used to have custom collision and image paths with an object
    """

    def __init__(self, x, y, width, height, health, image_path):
        """
        Initialize a door

        Args
        x (int): The x coordinate of the door
        y (int): The y coordinate of the door
        width (int): The width of the door
        height (int): The height of the door
        health (int): The health of the door, ended up unused
        image_path (str): The path to the image for the door.
        """
        super().__init__(x, y, width, height, health, image_path)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def collision(self, player, entities):
        """
        Handles the collision and use of the door Creates an instance of the player's hitbox, then checks if it
        collides with the door and if the player has a key in their inventory.

        Returns Boolean, updates room if True, ignores if False

        Args:
            player (Character):  The player character.
            entities (list): list of entities in the current room.

        Returns: Bool
        """
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        for item in player.inventory:
            if self.rect.colliderect(player_rect) and item.name == 'Key':
                return True
        return False
