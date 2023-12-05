import pygame
import glob_var


class Item:
    """ Class for items, anything that can be picked up is qualified as an item. """
    def __init__(self, name, x, y, width, height, image_path=None):
        """
        Initialize an Item

        Args:
        name (str): The name of the given Item.
        x (int): The x-coordinate of the object.
        y (int): The y-coordinate of the object.
        width (int): The width of the object.
        height (int): The height of the object.
        image_path (str, optional): Path to the image for the object (default is None).
        """
        # Validate input values
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")

        if not isinstance(x, (int, float) or 0 > x > glob_var.screen_width):
            raise ValueError("X-coordinate must be a numeric value.")

        if not isinstance(y, (int, float)) or 0 > y > glob_var.screen_height:
            raise ValueError("Y-coordinate must be a numeric value.")

        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive numeric value.")

        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive numeric value.")

        if image_path is not None:
            if not isinstance(image_path, str):
                raise ValueError(f"Invalid image file path: {image_path}")

        self.name = name
        self.x = x
        self.y = y
        self.original_y = y  # Store the original y position
        self.width = width
        self.height = height
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bounce_speed = 0.05  # Adjust the bounce speed for a slower bounce
        self.bounce_direction = 1

        self.image = None

        if image_path:
            self.image_path = image_path
            self.load_image()

    def load_image(self):
        """
        Load and scale the image for the object.

        This method loads an image specified by the image_path and scales it to the object's width and height.
        """
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def bounce(self):
        """
        Update the y position for bouncing and handle bounce limits.

        This method updates the y position of the object for bouncing and reverses the bounce direction when reaching
        the bounce limits.
        """
        self.y += self.bounce_speed * self.bounce_direction

        # Check if the object is within the bounce range
        if self.y >= self.original_y + 10 or self.y <= self.original_y - 10:
            # Reverse the bounce direction when reaching the limits
            self.bounce_direction *= -1

    def draw(self, screen):
        """
        Draw the object on the screen.

        Args:
            screen (pygame.Surface): The pygame screen surface on which to draw the object.
        """
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))
